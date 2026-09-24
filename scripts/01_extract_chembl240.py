#!/usr/bin/env python3
"""
01_extract_chembl240.py
=======================
Extract every activity record annotated against hERG (target CHEMBL240) from a
local ChEMBL SQLite dump, with full assay / document / compound context.

Design rules
------------
* NOTHING IS FILTERED. No standard_type filter, no relation filter, no
  validity filter, no deduplication. This is the raw pull; every filtering
  decision happens downstream in a script you can point at and defend.
* All context joins are LEFT JOINs, so an activity is never dropped because it
  lacks a cell line, a document, a structure or a variant annotation.
* The column list is checked against the live schema with PRAGMA table_info
  before the query is built, so a column renamed between ChEMBL releases
  produces a warning instead of a crash.

Outputs (in --outdir):
  chembl240_activities_raw.parquet   one row per activity_id (the main table)
  chembl240_assay_parameters.csv     assay-level parameters (1:many per assay)
  chembl240_activity_properties.csv  activity-level extra properties (1:many)
  chembl240_related_targets.csv      every ChEMBL target containing KCNH2
  extraction_provenance.json         ChEMBL version, query, row counts, hashes

Usage
-----
  python 01_extract_chembl240.py --db /path/to/chembl_37.db --outdir data/interim
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

TARGET = "CHEMBL240"
KCNH2_ACCESSION = "Q12809"  # UniProt accession for human KCNH2 / Kv11.1

# ---------------------------------------------------------------------------
# Column wish list: (alias, table, column, output_name)
# Anything missing from the live schema is reported and skipped.
# ---------------------------------------------------------------------------
COLUMNS: list[tuple[str, str, str, str]] = [
    # --- the measurement itself -------------------------------------------
    ("act", "activities", "activity_id", "activity_id"),
    ("act", "activities", "assay_id", "assay_id"),
    ("act", "activities", "doc_id", "doc_id"),
    ("act", "activities", "molregno", "molregno"),
    ("act", "activities", "standard_type", "standard_type"),
    ("act", "activities", "standard_relation", "standard_relation"),
    ("act", "activities", "standard_value", "standard_value"),
    ("act", "activities", "standard_units", "standard_units"),
    ("act", "activities", "standard_flag", "standard_flag"),
    ("act", "activities", "standard_upper_value", "standard_upper_value"),
    ("act", "activities", "pchembl_value", "pchembl_value"),
    ("act", "activities", "activity_comment", "activity_comment"),
    ("act", "activities", "data_validity_comment", "data_validity_comment"),
    ("act", "activities", "potential_duplicate", "potential_duplicate"),
    ("act", "activities", "bao_endpoint", "bao_endpoint"),
    ("act", "activities", "uo_units", "uo_units"),
    ("act", "activities", "action_type", "action_type"),
    ("act", "activities", "src_id", "activity_src_id"),
    # as-published values, before ChEMBL's own normalisation
    ("act", "activities", "type", "published_type"),
    ("act", "activities", "relation", "published_relation"),
    ("act", "activities", "value", "published_value"),
    ("act", "activities", "units", "published_units"),
    ("act", "activities", "upper_value", "published_upper_value"),
    # --- the assay ---------------------------------------------------------
    ("ass", "assays", "chembl_id", "assay_chembl_id"),
    ("ass", "assays", "description", "assay_description"),
    ("ass", "assays", "assay_type", "assay_type"),
    ("ass", "assays", "assay_test_type", "assay_test_type"),
    ("ass", "assays", "assay_category", "assay_category"),
    ("ass", "assays", "assay_organism", "assay_organism"),
    ("ass", "assays", "assay_tax_id", "assay_tax_id"),
    ("ass", "assays", "assay_strain", "assay_strain"),
    ("ass", "assays", "assay_tissue", "assay_tissue"),
    ("ass", "assays", "assay_cell_type", "assay_cell_type"),
    ("ass", "assays", "assay_subcellular_fraction", "assay_subcellular_fraction"),
    ("ass", "assays", "bao_format", "bao_format"),
    ("ass", "assays", "confidence_score", "confidence_score"),
    ("ass", "assays", "relationship_type", "relationship_type"),
    ("ass", "assays", "curated_by", "curated_by"),
    ("ass", "assays", "cell_id", "cell_id"),
    ("ass", "assays", "tissue_id", "tissue_id"),
    ("ass", "assays", "variant_id", "variant_id"),
    ("ass", "assays", "src_id", "assay_src_id"),
    ("ass", "assays", "src_assay_id", "src_assay_id"),
    # --- cell line ---------------------------------------------------------
    ("cd", "cell_dictionary", "cell_name", "cell_name"),
    ("cd", "cell_dictionary", "cell_description", "cell_description"),
    ("cd", "cell_dictionary", "cell_source_organism", "cell_source_organism"),
    ("cd", "cell_dictionary", "cell_source_tissue", "cell_source_tissue"),
    # --- protein variant (mutant hERG: Y652A, F656C, ...) ------------------
    ("vs", "variant_sequences", "mutation", "mutation"),
    ("vs", "variant_sequences", "accession", "variant_accession"),
    ("vs", "variant_sequences", "organism", "variant_organism"),
    # --- data source (literature vs deposited dataset) ---------------------
    ("src", "source", "src_short_name", "src_short_name"),
    ("src", "source", "src_description", "src_description"),
    # --- document ----------------------------------------------------------
    ("d", "docs", "chembl_id", "doc_chembl_id"),
    ("d", "docs", "year", "year"),
    ("d", "docs", "journal", "journal"),
    ("d", "docs", "volume", "volume"),
    ("d", "docs", "first_page", "first_page"),
    ("d", "docs", "pubmed_id", "pubmed_id"),
    ("d", "docs", "doi", "doi"),
    ("d", "docs", "title", "doc_title"),
    ("d", "docs", "doc_type", "doc_type"),
    # --- compound identity -------------------------------------------------
    ("md", "molecule_dictionary", "chembl_id", "molecule_chembl_id"),
    ("md", "molecule_dictionary", "pref_name", "pref_name"),
    ("md", "molecule_dictionary", "max_phase", "max_phase"),
    ("md", "molecule_dictionary", "first_approval", "first_approval"),
    ("md", "molecule_dictionary", "molecule_type", "molecule_type"),
    ("md", "molecule_dictionary", "structure_type", "structure_type"),
    ("md", "molecule_dictionary", "chirality", "chirality"),
    ("md", "molecule_dictionary", "prodrug", "prodrug"),
    ("md", "molecule_dictionary", "therapeutic_flag", "therapeutic_flag"),
    ("md", "molecule_dictionary", "black_box_warning", "black_box_warning"),
    ("mh", "molecule_hierarchy", "parent_molregno", "parent_molregno"),
    ("cs", "compound_structures", "canonical_smiles", "canonical_smiles"),
    ("cs", "compound_structures", "standard_inchi_key", "standard_inchi_key"),
    # --- precomputed physchem (useful later for chemotype analysis) --------
    ("cp", "compound_properties", "full_mwt", "full_mwt"),
    ("cp", "compound_properties", "mw_freebase", "mw_freebase"),
    ("cp", "compound_properties", "alogp", "alogp"),
    ("cp", "compound_properties", "cx_logp", "cx_logp"),
    ("cp", "compound_properties", "cx_logd", "cx_logd"),
    ("cp", "compound_properties", "cx_most_bpka", "cx_most_bpka"),
    ("cp", "compound_properties", "cx_most_apka", "cx_most_apka"),
    ("cp", "compound_properties", "molecular_species", "molecular_species"),
    ("cp", "compound_properties", "hba", "hba"),
    ("cp", "compound_properties", "hbd", "hbd"),
    ("cp", "compound_properties", "psa", "psa"),
    ("cp", "compound_properties", "rtb", "rtb"),
    ("cp", "compound_properties", "aromatic_rings", "aromatic_rings"),
    ("cp", "compound_properties", "heavy_atoms", "heavy_atoms"),
    ("cp", "compound_properties", "qed_weighted", "qed_weighted"),
]

FROM_CLAUSE = """
FROM target_dictionary td
JOIN assays               ass ON ass.tid          = td.tid
JOIN activities           act ON act.assay_id     = ass.assay_id
LEFT JOIN docs                d   ON d.doc_id         = act.doc_id
LEFT JOIN molecule_dictionary md  ON md.molregno      = act.molregno
LEFT JOIN molecule_hierarchy  mh  ON mh.molregno      = act.molregno
LEFT JOIN compound_structures cs  ON cs.molregno      = act.molregno
LEFT JOIN compound_properties cp  ON cp.molregno      = act.molregno
LEFT JOIN cell_dictionary     cd  ON cd.cell_id       = ass.cell_id
LEFT JOIN variant_sequences   vs  ON vs.variant_id    = ass.variant_id
LEFT JOIN source              src ON src.src_id       = ass.src_id
WHERE td.chembl_id = ?
"""


def live_columns(con: sqlite3.Connection, table: str) -> set[str]:
    try:
        rows = con.execute(f"PRAGMA table_info({table})").fetchall()
    except sqlite3.Error:
        return set()
    return {r[1] for r in rows}


def build_select(con: sqlite3.Connection) -> tuple[str, list[str]]:
    """Keep only wish-list columns that exist in this ChEMBL release."""
    schema: dict[str, set[str]] = {}
    kept, missing = [], []
    for alias, table, col, out in COLUMNS:
        schema.setdefault(table, live_columns(con, table))
        if not schema[table]:
            missing.append(f"{table} (table absent)")
            continue
        if col in schema[table]:
            kept.append(f"{alias}.{col} AS {out}")
        else:
            missing.append(f"{table}.{col}")
    if missing:
        print(f"[warn] {len(missing)} requested column(s) not in this schema:", file=sys.stderr)
        for m in sorted(set(missing)):
            print(f"       - {m}", file=sys.stderr)
    return "SELECT\n  " + ",\n  ".join(kept) + "\n" + FROM_CLAUSE, missing


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def write_table(df: pd.DataFrame, outdir: Path, stem: str) -> Path:
    """Parquet if pyarrow/fastparquet is available, gzipped CSV otherwise."""
    try:
        path = outdir / f"{stem}.parquet"
        df.to_parquet(path, index=False)
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] parquet unavailable ({exc}); writing CSV instead", file=sys.stderr)
        path = outdir / f"{stem}.csv.gz"
        df.to_csv(path, index=False, compression="gzip")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, type=Path, help="path to chembl_XX.db")
    ap.add_argument("--outdir", default=Path("data/interim"), type=Path)
    ap.add_argument("--target", default=TARGET)
    ap.add_argument("--hash-db", action="store_true",
                    help="SHA-256 the whole dump for provenance (slow: ~25 GB read)")
    args = ap.parse_args()

    if not args.db.exists():
        print(f"[error] no such file: {args.db}", file=sys.stderr)
        return 1
    args.outdir.mkdir(parents=True, exist_ok=True)

    con = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)

    # ChEMBL ships a one-row `version` table: name, creation_date, comments.
    try:
        version = pd.read_sql_query("SELECT * FROM version", con).to_dict("records")
    except Exception:  # noqa: BLE001
        version = [{"name": args.db.stem, "note": "no version table found"}]
    print(f"[info] database: {version}")

    # -- sanity: does the target exist, and what else contains KCNH2? -------
    tgt = pd.read_sql_query(
        "SELECT tid, chembl_id, pref_name, target_type, organism "
        "FROM target_dictionary WHERE chembl_id = ?", con, params=(args.target,))
    if tgt.empty:
        print(f"[error] target {args.target} not found", file=sys.stderr)
        return 1
    print(f"[info] target: {tgt.to_dict('records')[0]}")

    related = pd.read_sql_query(
        """
        SELECT td.chembl_id, td.pref_name, td.target_type, td.organism,
               COUNT(DISTINCT ass.assay_id)  AS n_assays,
               COUNT(act.activity_id)        AS n_activities
        FROM component_sequences cseq
        JOIN target_components tc ON tc.component_id = cseq.component_id
        JOIN target_dictionary td ON td.tid = tc.tid
        LEFT JOIN assays     ass ON ass.tid      = td.tid
        LEFT JOIN activities act ON act.assay_id = ass.assay_id
        WHERE cseq.accession = ?
        GROUP BY td.chembl_id, td.pref_name, td.target_type, td.organism
        ORDER BY n_activities DESC
        """, con, params=(KCNH2_ACCESSION,))
    related.to_csv(args.outdir / "chembl240_related_targets.csv", index=False)
    print(f"[info] {len(related)} ChEMBL target(s) contain {KCNH2_ACCESSION}; "
          f"see chembl240_related_targets.csv")

    # -- main pull ----------------------------------------------------------
    sql, missing = build_select(con)
    (args.outdir / "extraction_query.sql").write_text(sql.replace("?", f"'{args.target}'"))
    print("[info] running main query ...")
    df = pd.read_sql_query(sql, con, params=(args.target,))
    print(f"[info] {len(df):,} activity rows | "
          f"{df['assay_chembl_id'].nunique():,} assays | "
          f"{df['molregno'].nunique():,} compounds | "
          f"{df['doc_id'].nunique():,} documents")

    if df["activity_id"].duplicated().any():
        n = int(df["activity_id"].duplicated().sum())
        print(f"[warn] {n} duplicated activity_id rows — a LEFT JOIN fanned out. "
              f"Check variant_sequences / molecule_hierarchy.", file=sys.stderr)

    main_path = write_table(df, args.outdir, "chembl240_activities_raw")

    # -- one-to-many side tables -------------------------------------------
    assay_subq = ("SELECT ass.assay_id FROM assays ass "
                  "JOIN target_dictionary td ON td.tid = ass.tid WHERE td.chembl_id = ?")
    side = {}
    try:
        side["assay_parameters"] = pd.read_sql_query(
            f"SELECT * FROM assay_parameters WHERE assay_id IN ({assay_subq})",
            con, params=(args.target,))
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] assay_parameters: {exc}", file=sys.stderr)
    try:
        side["activity_properties"] = pd.read_sql_query(
            f"SELECT ap.* FROM activity_properties ap "
            f"JOIN activities act ON act.activity_id = ap.activity_id "
            f"WHERE act.assay_id IN ({assay_subq})", con, params=(args.target,))
    except Exception as exc:  # noqa: BLE001
        print(f"[warn] activity_properties: {exc}", file=sys.stderr)
    for name, sdf in side.items():
        sdf.to_csv(args.outdir / f"chembl240_{name}.csv", index=False)
        print(f"[info] {name}: {len(sdf):,} rows")

    # -- provenance ---------------------------------------------------------
    prov = {
        "extracted_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "db_path": str(args.db.resolve()),
        "db_size_bytes": args.db.stat().st_size,
        "db_sha256": sha256(args.db) if args.hash_db else None,
        "chembl_version_table": version,
        "target": args.target,
        "columns_requested": len(COLUMNS),
        "columns_missing": sorted(set(missing)),
        "n_activities": int(len(df)),
        "n_assays": int(df["assay_chembl_id"].nunique()),
        "n_compounds": int(df["molregno"].nunique()),
        "n_documents": int(df["doc_id"].nunique()),
        "side_tables": {k: int(len(v)) for k, v in side.items()},
        "outputs": [str(main_path.name)],
        "pandas_version": pd.__version__,
    }
    (args.outdir / "extraction_provenance.json").write_text(json.dumps(prov, indent=2))
    print(f"[done] wrote {main_path}")
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
