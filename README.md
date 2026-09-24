# hERG data heterogeneity: assay-context-aware curation of public bioactivity data

**Status: work in progress (started September 2026).** Data extraction and profiling
are implemented; modelling and analysis are not. This repository is public so that the
design decisions and the curation logic can be inspected while the work is ongoing.

---

## Summary

Public hERG (Kv11.1, *KCNH2*) bioactivity data are routinely pooled across radioligand
binding, manual patch clamp, automated patch clamp and fluorescence assays, at different
temperatures and stimulation protocols, and then used to train cardiotoxicity models
benchmarked to three decimal places. Landrum and Riniker showed that simply combining
IC<sub>50</sub> values from different ChEMBL assays against the same target introduces
substantial noise, with 27% of paired measurements differing by more than one log unit
under minimal curation [1]. Independently, a HESI-coordinated study in which five
laboratories measured 28 drugs under a standardised ICH S7B protocol put the *irreducible*
variability of the manual patch clamp assay itself at roughly 5-fold in IC<sub>50</sub> [2].

This project asks what is left once those two numbers are taken seriously:

1. **Does the regulatory decision rule survive the data?** The Redfern 30-fold safety
   margin between hERG IC<sub>50</sub> and free therapeutic plasma concentration [3] is
   recomputed from naively pooled ChEMBL data and from assay-context-filtered subsets,
   and scored on how well each separates known torsadogenic risk classes.
2. **How much of the spread in public hERG data is recoverable signal?** A variance
   decomposition separating between-method variance, the within-method experimental floor
   taken from the HESI replication study [2], and residual variance.

The intended output is not another QSAR model. It is a defensible, documented account of
how much of the apparent disagreement in public hERG data is measurement noise, how much
is assay-context signal that metadata can recover, and what that implies for a safety
endpoint where the absolute number, not the rank order, drives the decision.

---

## Current status

| Stage | Status |
|---|---|
| Literature review and novelty assessment (~50 papers) | Done |
| Scope definition and research questions | Done |
| `01_extract_chembl240.py` — unfiltered pull of all CHEMBL240 activities with full assay/document/compound context | Implemented |
| `02_profile_chembl240.py` — profiling: endpoint types, censoring, confidence scores, replicate structure, unit-error edge cases | Implemented |
| Transcription of Redfern 2003 safety-margin tables | In progress |
| Transcription of HESI per-laboratory IC<sub>50</sub> values | In progress |
| Assay-method classifier over free-text assay descriptions | Not started |
| Variance decomposition | Not started |
| Safety-margin replication and risk-class separation | Not started |

---

## Why this is not a rerun of existing work

The literature was checked before the design was fixed. Three papers cover adjacent ground:

- **Sato et al. 2018** [4] built an integrated hERG database and already reported the
  divergence between binding and electrophysiology readouts. That finding is treated here
  as established, not as a result to rediscover.
- **Schoenmaker et al. 2025** [5] established assay-context-aware modelling using text
  embeddings of ChEMBL assay descriptions, but for protein–ligand interaction prediction
  generally, not for a safety endpoint.
- **Smit et al. 2026** [6] applied named-entity recognition to ChEMBL assay descriptions
  to enrich experimental-method annotations across the database.

What none of them combines: an assay-context treatment of a **safety** endpoint, anchored
to a **controlled-replication variance floor** from a multi-laboratory study, and evaluated
against a **regulatory decision rule** rather than an R² on a held-out split. That
combination is the gap this project targets.

---

## Data sources

| Source | Use | Access |
|---|---|---|
| ChEMBL 37, target CHEMBL240 | Primary bioactivity data | [EBI FTP](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/) (CC BY-SA 3.0) |
| Alvarez Baron et al. 2025 supplementary tables [2] | Within-method variance floor | Open access, *Sci Rep* |
| Redfern et al. 2003 tables [3] | Safety margins, TdP risk classes | *Cardiovasc Res* |
| Wang et al. 2016 benchmark set [7] | External comparison set (658 compounds; source of the TDC hERG split) | *Mol Pharm* supporting information |
| hERGCentral [8] | High-throughput screening cross-reference | Published database |
| ICH S7B, ICH E14, E14/S7B Q&As [9–11] | Decision-rule definitions | ICH, freely available |

**Not redistributed here.** No publisher PDFs, no ChEMBL dump, no derived parquet files are
committed. Scripts download and regenerate everything from the primary sources; `data/` and
`*.pdf` are git-ignored. Derived datasets, if released, will inherit ChEMBL's CC BY-SA 3.0.

---

## Repository structure

```
herg/
├── README.md
├── LICENSE
├── environment.yml
├── .gitignore
├── scripts/
│   ├── 01_extract_chembl240.py     # unfiltered ChEMBL pull, all context joins as LEFT JOIN
│   └── 02_profile_chembl240.py     # 24 profiling tables + profile_report.md
├── notebooks/                      # exploratory work
├── reports/
│   └── profile/                    # profiling output (committed: it is small and it is the design document)
└── data/
    ├── raw/                        # ChEMBL dump — git-ignored
    └── interim/                    # parquet — git-ignored
```

Design rule for the extraction step: **nothing is filtered**. No endpoint-type filter, no
relation filter, no validity filter, no deduplication. Every filtering decision is made in a
downstream script that can be pointed at and defended. The column list is checked against the
live schema with `PRAGMA table_info` before the query is built, so a column renamed between
ChEMBL releases produces a warning rather than a crash.

---

## Reproducing

```bash
git clone https://github.com/<user>/herg.git && cd herg
conda env create -f environment.yml && conda activate herg

# download ChEMBL 37 (~6 GB compressed, ~25 GB extracted)
cd data/raw
curl -O https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/chembl_37_sqlite.tar.gz
curl -O https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_37/checksums.txt
shasum -a 256 chembl_37_sqlite.tar.gz          # compare against checksums.txt
tar -xzf chembl_37_sqlite.tar.gz && cd ../..

python scripts/01_extract_chembl240.py \
  --db data/raw/chembl_37/chembl_37_sqlite/chembl_37.db --outdir data/interim
python scripts/02_profile_chembl240.py \
  --infile data/interim/chembl240_activities_raw.parquet --outdir reports/profile
```

`extraction_provenance.json` records the ChEMBL version table, row counts and any schema
columns that were absent, and is committed as the version pin.

---

## Background in one paragraph

hERG carries I<sub>Kr</sub>, the rapid delayed-rectifier potassium current that repolarises
the cardiac action potential. Blocking it prolongs the action potential, lengthens the QT
interval, and can trigger torsades de pointes — the mechanism behind the withdrawal of
terfenadine, astemizole and cisapride [12, 13]. The channel has an unusually large,
hydrophobic inner cavity and a promiscuous binding site, so a substantial fraction of
drug-like chemical space hits it; cryo-EM structures of the open channel and of
blocker-bound states have since localised the key pore-lining residues [14–16]. ICH S7B made
the in vitro hERG assay a standard non-clinical requirement [9], and the 2022 E14/S7B
Q&As allow negative non-clinical data to support clinical QTc risk assessment, provided the
data follow specified best-practice designs [11]. That change is what makes the absolute
IC<sub>50</sub>, and therefore its uncertainty, a regulatory quantity rather than a
screening convenience.

---

## References

1. Landrum GA, Riniker S. Combining IC50 or Ki values from different sources is a source of
   significant noise. *J Chem Inf Model*. 2024;64(5):1560–1567.
   [doi:10.1021/acs.jcim.4c00049](https://doi.org/10.1021/acs.jcim.4c00049)
2. Alvarez Baron C, Zhao J, Yu H, et al. Multi-laboratory comparisons of manual patch clamp
   hERG data generated using standardized protocols and following ICH S7B Q&A 2.1 best
   practices. *Sci Rep*. 2025;15:29995.
   [doi:10.1038/s41598-025-15761-8](https://doi.org/10.1038/s41598-025-15761-8)
3. Redfern WS, Carlsson L, Davis AS, et al. Relationships between preclinical cardiac
   electrophysiology, clinical QT interval prolongation and torsade de pointes for a broad
   range of drugs: evidence for a provisional safety margin in drug development.
   *Cardiovasc Res*. 2003;58(1):32–45.
   [doi:10.1016/S0008-6363(02)00846-5](https://doi.org/10.1016/S0008-6363(02)00846-5)
4. Sato T, Yuki H, Ogura K, Honma T. Construction of an integrated database for hERG
   blocking small molecules. *PLoS One*. 2018;13(7):e0199348.
   [doi:10.1371/journal.pone.0199348](https://doi.org/10.1371/journal.pone.0199348)
5. Schoenmaker L, Sastrokarijo EG, Heitman LH, Beltman JB, Jespers W, van Westen GJP.
   Toward assay-aware bioactivity model(er)s: getting a grip on biological context.
   *J Chem Inf Model*. 2025;65(13):7013–7023.
   [doi:10.1021/acs.jcim.5c00603](https://doi.org/10.1021/acs.jcim.5c00603)
6. Smit I, Adasme MF, Manners E, et al. Integrating artificial intelligence and manual
   curation to enhance bioassay annotations in ChEMBL. *J Cheminform*. 2026;18(1):24.
   [doi:10.1186/s13321-026-01165-x](https://doi.org/10.1186/s13321-026-01165-x)
7. Wang S, Sun H, Liu H, Li D, Li Y, Hou T. ADMET evaluation in drug discovery. 16.
   Predicting hERG blockers by combining multiple pharmacophores and machine learning
   approaches. *Mol Pharm*. 2016;13(8):2855–2866.
   [doi:10.1021/acs.molpharmaceut.6b00471](https://doi.org/10.1021/acs.molpharmaceut.6b00471)
8. Du F, Yu H, Zou B, Babcock J, Long S, Li M. hERGCentral: a large database to store,
   retrieve, and analyze compound–human ether-à-go-go related gene channel interactions to
   facilitate cardiotoxicity assessment in drug development.
   *Assay Drug Dev Technol*. 2011;9(6):580–588.
   [doi:10.1089/adt.2011.0425](https://doi.org/10.1089/adt.2011.0425)
9. ICH. S7B: The non-clinical evaluation of the potential for delayed ventricular
   repolarization (QT interval prolongation) by human pharmaceuticals. 2005.
10. ICH. E14: The clinical evaluation of QT/QTc interval prolongation and proarrhythmic
    potential for non-antiarrhythmic drugs. 2005.
11. ICH. E14/S7B implementation working group: clinical and nonclinical evaluation of QT/QTc
    interval prolongation and proarrhythmic potential — questions and answers. Step 4,
    February 2022.
12. Vandenberg JI, Perry MD, Perrin MJ, Mann SA, Ke Y, Hill AP. hERG K<sup>+</sup> channels:
    structure, function, and clinical significance. *Physiol Rev*. 2012;92(3):1393–1478.
    [doi:10.1152/physrev.00036.2011](https://doi.org/10.1152/physrev.00036.2011)
13. Sanguinetti MC, Mitcheson JS. Predicting drug–hERG channel interactions that cause
    acquired long QT syndrome. *Trends Pharmacol Sci*. 2005;26(3):119–124.
    [doi:10.1016/j.tips.2005.01.003](https://doi.org/10.1016/j.tips.2005.01.003)
14. Wang W, MacKinnon R. Cryo-EM structure of the open human ether-à-go-go-related
    K<sup>+</sup> channel hERG. *Cell*. 2017;169(3):422–430.
    [doi:10.1016/j.cell.2017.03.048](https://doi.org/10.1016/j.cell.2017.03.048)
15. Asai T, Adachi N, Moriya T, et al. Cryo-EM structure of K<sup>+</sup>-bound hERG channel
    complexed with the blocker astemizole. *Structure*. 2021;29(3):203–212.
    [doi:10.1016/j.str.2020.12.007](https://doi.org/10.1016/j.str.2020.12.007)
16. Miyashita Y, Moriya T, Kato T, et al. Improved higher resolution cryo-EM structures
    reveal the binding modes of hERG channel inhibitors. *Structure*. 2024;32(9):1332–1344.
    [doi:10.1016/j.str.2024.07.007](https://doi.org/10.1016/j.str.2024.07.007)
17. Zachariae U, Giordanetto F, Leach AG. Side chain flexibilities in the human
    ether-à-go-go related gene potassium channel (hERG) together with matched-pair binding
    studies suggest a new binding mode for channel blockers.
    *J Med Chem*. 2009;52(14):4266–4276.
    [doi:10.1021/jm900002x](https://doi.org/10.1021/jm900002x)
18. Elkins RC, Davies MR, Brough SJ, et al. Variability in high-throughput ion-channel
    screening data and consequences for cardiac safety assessment.
    *J Pharmacol Toxicol Methods*. 2013;68(1):112–122.
    [doi:10.1016/j.vascn.2013.04.007](https://doi.org/10.1016/j.vascn.2013.04.007)
19. Sanches IH, Braga RC, Alves VM, Andrade CH. Enhancing hERG risk assessment with
    interpretable classificatory and regression models.
    *Chem Res Toxicol*. 2024;37(6):910–922.
    [doi:10.1021/acs.chemrestox.3c00400](https://doi.org/10.1021/acs.chemrestox.3c00400)
20. El Harchi A, Hancox JC. hERG agonists pose challenges to web-based machine learning
    methods for prediction of drug–hERG channel interaction.
    *J Pharmacol Toxicol Methods*. 2023;123:107293.
    [doi:10.1016/j.vascn.2023.107293](https://doi.org/10.1016/j.vascn.2023.107293)
21. King TI, Indapurkar A, Tariq I, DePalma R, Mistry S, et al. Determination of five
    positive control drugs in hERG external solution (buffer) by LC-MS/MS to support
    in vitro hERG assay as recommended by ICH S7B.
    *J Pharmacol Toxicol Methods*. 2022;118:107229.
    [doi:10.1016/j.vascn.2022.107229](https://doi.org/10.1016/j.vascn.2022.107229)
22. Ruggiu F, Marcou G, Varnek A, Horvath D. ISIDA property-labelled fragment descriptors.
    *Mol Inform*. 2010;29(12):855–868.
    [doi:10.1002/minf.201000099](https://doi.org/10.1002/minf.201000099)

---

## Licence

Code: MIT. Derived data: CC BY-SA 3.0, inherited from ChEMBL.

## Author

Beatriz Ulate Caballero — MSc student, ChEMoinformaticsPlus Erasmus Mundus programme,
University of Strasbourg.
