#!/usr/bin/env python3
"""
02_profile_chembl240.py
=======================
Describe the raw CHEMBL240 pull without changing it. Every table is written to
CSV and summarised in a single markdown report you can read, paste, or drop
straight into the repo.

Still no filtering. The point is to find out what is in there — including the
records most papers silently delete.

Usage
-----
  python 02_profile_chembl240.py --infile data/interim/chembl240_activities_raw.parquet \
                                 --outdir reports/profile
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

TOP = 25  # rows shown per category table


def load(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path, low_memory=False)


def counts(df: pd.DataFrame, col: str, dropna: bool = False) -> pd.DataFrame:
    if col not in df.columns:
        return pd.DataFrame({"note": [f"column {col} absent"]})
    s = df[col].value_counts(dropna=dropna)
    out = s.rename("n").to_frame()
    out["pct"] = (100 * out["n"] / len(df)).round(2)
    return out.rename_axis(col).reset_index()


def md_table(df: pd.DataFrame, limit: int | None = TOP) -> str:
    view = df.head(limit) if limit else df
    return view.to_markdown(index=False) + (
        f"\n\n*(showing {limit} of {len(df)} rows)*\n" if limit and len(df) > limit else "\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--infile", required=True, type=Path)
    ap.add_argument("--outdir", default=Path("reports/profile"), type=Path)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)

    df = load(args.infile)
    md: list[str] = []
    tables: dict[str, pd.DataFrame] = {}

    def section(title: str, table: pd.DataFrame, key: str, limit: int | None = TOP) -> None:
        tables[key] = table
        md.append(f"\n## {title}\n\n{md_table(table, limit)}")

    # ---------------------------------------------------------------- shape
    md.append("# CHEMBL240 (hERG) raw activity profile\n")
    shape = pd.DataFrame([
        ("activity records", len(df)),
        ("distinct assays", df["assay_chembl_id"].nunique()),
        ("distinct compounds (molregno)", df["molregno"].nunique()),
        ("distinct parent compounds", df.get("parent_molregno", pd.Series(dtype=float)).nunique()),
        ("distinct InChIKeys", df.get("standard_inchi_key", pd.Series(dtype=object)).nunique()),
        ("distinct documents", df["doc_id"].nunique()),
        ("rows with no SMILES", int(df.get("canonical_smiles", pd.Series(dtype=object)).isna().sum())),
        ("rows with no standard_value", int(df["standard_value"].isna().sum())),
        ("rows with no pchembl_value", int(df["pchembl_value"].isna().sum())),
    ], columns=["quantity", "n"])
    section("Overall shape", shape, "00_shape", limit=None)

    # -------------------------------------------------------- endpoint type
    section("standard_type", counts(df, "standard_type"), "01_standard_type")

    if {"standard_type", "standard_units"} <= set(df.columns):
        ct = (df.groupby(["standard_type", "standard_units"], dropna=False)
                .size().rename("n").reset_index().sort_values("n", ascending=False))
        section("standard_type x standard_units", ct, "02_type_x_units")

    # ------------------------------------------------------------- censoring
    section("standard_relation (censoring)", counts(df, "standard_relation"), "03_standard_relation")

    if "standard_type" in df.columns:
        rel = (df.assign(rel=df["standard_relation"].fillna("(null)"))
                 .pivot_table(index="standard_type", columns="rel",
                              values="activity_id", aggfunc="count", fill_value=0))
        rel["total"] = rel.sum(axis=1)
        non_eq = [c for c in rel.columns if c not in ("=", "total")]
        rel["pct_censored_or_null"] = (100 * rel[non_eq].sum(axis=1) / rel["total"]).round(1)
        rel = rel.sort_values("total", ascending=False).reset_index()
        section("Censoring by endpoint type", rel, "04_censoring_by_type")

    # ------------------------------------------------------------ assay side
    section("assay_type", counts(df, "assay_type"), "05_assay_type", limit=None)
    section("confidence_score", counts(df, "confidence_score").sort_values("confidence_score"),
            "06_confidence_score", limit=None)
    section("bao_format", counts(df, "bao_format"), "07_bao_format")
    section("cell_name", counts(df, "cell_name"), "08_cell_name")
    section("assay_organism", counts(df, "assay_organism"), "09_assay_organism")
    section("src_short_name (data source)", counts(df, "src_short_name"), "10_source", limit=None)
    section("mutation (protein variant)", counts(df, "mutation"), "11_mutation")

    # ----------------------------------------------------- quality flag side
    section("data_validity_comment", counts(df, "data_validity_comment"), "12_data_validity")
    section("potential_duplicate", counts(df, "potential_duplicate"), "13_potential_duplicate", limit=None)
    section("activity_comment", counts(df, "activity_comment"), "14_activity_comment")

    # ------------------------------------------------------------------ time
    if "year" in df.columns:
        yr = (df.groupby(df["year"].fillna(-1).astype(int), dropna=False)
                .agg(n_activities=("activity_id", "count"),
                     n_assays=("assay_chembl_id", "nunique"),
                     n_docs=("doc_id", "nunique"))
                .reset_index().rename(columns={"year": "year"}))
        section("Records per year", yr, "15_year", limit=None)

    section("doc_type", counts(df, "doc_type"), "16_doc_type", limit=None)
    if "journal" in df.columns:
        section("journal", counts(df, "journal"), "17_journal")

    # ------------------------------------------------------- per-assay shape
    per_assay = (df.groupby("assay_chembl_id")
                   .agg(n_records=("activity_id", "count"),
                        n_compounds=("molregno", "nunique"),
                        types=("standard_type", lambda s: "|".join(sorted(set(s.dropna())))),
                        year=("year", "first"),
                        confidence_score=("confidence_score", "first"),
                        cell_name=("cell_name", "first"),
                        description=("assay_description", "first"))
                   .sort_values("n_records", ascending=False).reset_index())
    tables["18_per_assay"] = per_assay
    md.append("\n## Records per assay\n\n" +
              md_table(per_assay["n_records"].describe().rename("value").rename_axis("stat").reset_index(), None))
    md.append("\nLargest assays:\n\n" + md_table(
        per_assay.drop(columns=["description"]).head(15), None))

    # ---------------------------------------------------- per-compound shape
    per_cmpd = (df.groupby("molregno")
                  .agg(n_records=("activity_id", "count"),
                       n_assays=("assay_chembl_id", "nunique"),
                       n_docs=("doc_id", "nunique"),
                       n_types=("standard_type", "nunique"),
                       pref_name=("pref_name", "first"),
                       inchikey=("standard_inchi_key", "first"))
                  .sort_values("n_records", ascending=False).reset_index())
    tables["19_per_compound"] = per_cmpd
    md.append("\n## Records per compound\n\n" +
              md_table(per_cmpd["n_records"].describe().rename("value").rename_axis("stat").reset_index(), None))
    rep = pd.DataFrame([
        ("compounds with 1 record", int((per_cmpd.n_records == 1).sum())),
        ("compounds with >= 2 records", int((per_cmpd.n_records >= 2).sum())),
        ("compounds with >= 3 records", int((per_cmpd.n_records >= 3).sum())),
        ("compounds with >= 2 distinct documents", int((per_cmpd.n_docs >= 2).sum())),
        ("compounds with >= 2 distinct standard_types", int((per_cmpd.n_types >= 2).sum())),
    ], columns=["quantity", "n"])
    section("Replicate structure (the raw material for the variance analysis)", rep, "20_replication", limit=None)
    md.append("\nMost-measured compounds:\n\n" + md_table(per_cmpd.head(15), None))

    # ----------------------------------------- IC50 value sanity, no filtering
    ic50 = df[(df["standard_type"] == "IC50") & df["standard_value"].notna()].copy()
    if len(ic50):
        nm = ic50[ic50["standard_units"] == "nM"]["standard_value"].astype(float)
        nm = nm[nm > 0]
        q = nm.quantile([0, .01, .05, .25, .5, .75, .95, .99, 1]).rename("nM").rename_axis("quantile").reset_index()
        q["pIC50"] = (9 - np.log10(q["nM"])).round(2)
        section("IC50 value distribution (nM, unfiltered)", q, "21_ic50_quantiles", limit=None)
        edge = pd.DataFrame([
            ("IC50 rows", len(ic50)),
            ("IC50 rows in nM", int((ic50["standard_units"] == "nM").sum())),
            ("IC50 rows in other/blank units", int((ic50["standard_units"] != "nM").sum())),
            ("IC50 < 0.1 nM (implausible, check units)", int((nm < 0.1).sum())),
            ("IC50 > 1 mM (implausible, check units)", int((nm > 1e6).sum())),
            ("IC50 rows censored (relation != '=')", int((ic50["standard_relation"].fillna("") != "=").sum())),
            ("IC50 rows with a validity comment", int(ic50["data_validity_comment"].notna().sum())),
            ("IC50 rows with no pchembl_value", int(ic50["pchembl_value"].isna().sum())),
        ], columns=["quantity", "n"])
        section("IC50 edge cases", edge, "22_ic50_edges", limit=None)

    # ------------------------------ free-text reconnaissance for step 5 rules
    if "assay_description" in df.columns:
        uniq = (df[["assay_chembl_id", "assay_description"]].drop_duplicates()
                  .dropna(subset=["assay_description"]))
        vocab = {
            "patch clamp": r"patch[- ]?clamp",
            "whole-cell": r"whole[- ]?cell",
            "manual": r"\bmanual\b",
            "automated": r"automat",
            "IonWorks": r"ionworks",
            "QPatch": r"qpatch",
            "PatchXpress": r"patchxpress",
            "SyncroPatch|Qube|Patchliner": r"syncropatch|qube|patchliner",
            "binding/radioligand": r"radioligand|\bbinding\b|dofetilide|astemizole|MK-?499",
            "flux/fluorescence": r"rubidium|\bRb\+|flux|fluorescen|thallium|FluxOR|DiBAC",
            "oocyte": r"oocyte|xenopus",
            "HEK": r"\bHEK",
            "CHO": r"\bCHO\b",
            "temperature stated": r"\d{2}\s?(?:°|deg)?\s?C\b|room temperature|physiological temperature",
            "holding/step voltage stated": r"-?\d{1,3}\s?mV",
        }
        hits = []
        for label, pat in vocab.items():
            m = uniq["assay_description"].str.contains(pat, case=False, regex=True, na=False)
            hits.append((label, int(m.sum()), round(100 * m.mean(), 1)))
        vocab_df = pd.DataFrame(hits, columns=["keyword_probe", "n_assays", "pct_of_assays"]) \
                     .sort_values("n_assays", ascending=False)
        section("Keyword reconnaissance over assay descriptions (assay level, probes overlap)",
                vocab_df, "23_description_keywords", limit=None)

        sample = uniq.sample(min(200, len(uniq)), random_state=0).sort_values("assay_chembl_id")
        sample.to_csv(args.outdir / "24_description_sample_200.csv", index=False)
        md.append(f"\n200 randomly sampled assay descriptions written to "
                  f"`24_description_sample_200.csv` — this is the file to read by hand "
                  f"before writing the method classifier.\n")

    # ------------------------------------------------------------ write out
    for key, tbl in tables.items():
        tbl.to_csv(args.outdir / f"{key}.csv", index=False)
    report = args.outdir / "profile_report.md"
    report.write_text("\n".join(md))
    print(f"[done] {len(tables)} tables + {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
