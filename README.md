# asd-precedent-engine

A validated database of every amorphous solid dispersion (ASD) drug product approved by the U.S. FDA between 2012 and 2023, with computed molecular descriptors, built to support polymer, process and dosage-form selection for new poorly water-soluble candidates by reasoning from approved precedent.

**Source dataset:** Moseson, D.E., Tran, T.B., Karunakaran, B., Ambardekar, R. & Hiew, T.N. *Trends in amorphous solid dispersion drug products approved by the U.S. Food and Drug Administration between 2012 and 2023.* **International Journal of Pharmaceutics: X** 7 (2024) 100259. [doi:10.1016/j.ijpx.2024.100259](https://doi.org/10.1016/j.ijpx.2024.100259) (CC BY-NC-ND).

---

## Why this exists

Most computational work on amorphous solid dispersions is structure-based: Hansen solubility parameters, Flory–Huggins interaction parameters, molecular dynamics. All of it requires a molecular structure.

In early development you often do not have a structure you can use. What you have is a **property envelope** — a molecular weight, a logP range, solubility in two or three solvents — and a target indication. The structure-based toolkit has nothing to say in that situation.

This project takes the other route. It treats the 48 approved products as a case base and asks a different question: *which approved molecules does this candidate resemble, and what did those programmes actually do?* Precedent of use is a documented driver of excipient selection in pharmaceutical development, so reasoning by analogy is not a consolation prize — it is close to how these decisions are really made.

The database is deliberately built from a **single citation source**. A smaller dataset where every value traces to one verifiable table is more defensible than a larger one assembled from many partially-remembered ones.

---

## What is in the database

| File | Contents |
|---|---|
| `data/asd_products.csv` | 48 approved drug products, 21 fields, transcribed from Table 1 of the source paper |
| `data/drug_identifiers.csv` | 36 unique amorphous drugs, with PubChem lookup terms |
| `data/drug_descriptors.csv` | Generated — structures and RDKit descriptors for those 36 drugs |
| `data/provenance.json` | Generated — library versions and date, so numbers can be reproduced |

**Product-level fields** include trade name, approval year, NDA holder, dosage form, dosage strengths, recommended dosage, manufacturing process, ASD polymer, therapeutic category, and flags for fixed-dose combinations, co-packaged products and US discontinuation. Two derived fields were added: `max_amorphous_mg_per_unit`, which required identifying which component of each combination product is actually the ASD, and `crystalline_drugs`, which records components present in crystalline form.

**Drug-level fields** are computed from PubChem structures with RDKit: molecular weight, cLogP (Crippen), TPSA, hydrogen bond donors and acceptors under two definitions, rotatable bonds, ring and aromatic ring counts, Fsp3, heavy atom count, stereocentre counts, and individually-flagged Rule-of-5 violations.

The dataset spans MW 383–1113 g/mol and cLogP 1.7–9.5. Tablets dominate the dosage forms (36 of 48), with capsules, pellets, granules and oral suspension powders making up the rest.

---

## Pipeline

```
data/drug_identifiers.csv
        │
        │  src/fetch_descriptors.py
        │  ├─ resolve each name to a PubChem CID
        │  ├─ batch-fetch structures in one POST request
        │  └─ compute RDKit descriptors and Ro5 flags
        ▼
data/drug_descriptors.csv ──┐
                            │  src/validate.py    → reproduce published statistics
data/asd_products.csv ──────┤
                            │  src/plot_landscape.py → figures/
                            ▼
```

### Running it

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python src/fetch_descriptors.py    # needs network access to PubChem
python src/validate.py
python src/plot_landscape.py
```

`fetch_descriptors.py` caches results, so an interrupted run resumes rather than refetching. It respects PubChem's usage policy (5 requests/second) and reads the `X-Throttling-Control` response header to back off when the service reports load.

---

## Validation

Every value in `asd_products.csv` was transcribed by hand from a published table, so it is checked against statistics the original authors computed from that same table. If the recomputed statistics match, the transcription is trustworthy and everything downstream inherits that.

```
$ python src/validate.py

Product-level checks
  [PASS] total approved drug products: got 48, expected 48
  [PASS] fixed-dose combinations: got 18, expected 18
  [PASS] unique amorphous drugs: got 36, expected 36

Drug-polymer combination checks
  [PASS] drug-polymer combinations: got 37, expected 37
  [PASS] PVPVA combinations: got 18, expected 18
  [PASS] HPMCAS combinations: got 11, expected 11

Process frequency checks
  [PASS] spray drying share (%): got 54.1, expected 54.1
  [PASS] HME share (%): got 35.1, expected 35.1
  [PASS] HPMCAS made by SD: got 10, expected 10

Dose checks
  [PASS] max amorphous dose per unit (mg): got 300, expected 300

Descriptor checks
  [PASS] MW violations: got 21, expected 21
  [PASS] HBD violations: got 0, expected 0
  [INFO] logP violations: got 15, paper 14
  [INFO] HBA violations by definition: CalcNumHBA 8, Lipinski N+O 17, paper 1
```

### A counting subtlety

The published polymer and process frequencies are computed over **drug–polymer combinations** (n = 37), not over products (n = 48). A combination is counted once however many products contain it, and tacrolimus counts twice because it appears with two different polymers by two different processes. Counting product rows instead gives 55.3% / 34.2% for spray drying and HME rather than the correct 54.1% / 35.1% — close enough to pass unnoticed, wrong enough to matter. `validate.py` rebuilds the combination set rather than counting rows.

### An error the validation caught

Lumacaftor was initially transcribed as an amorphous drug in Orkambi. This produced 37 unique drugs instead of 36 and inflated the HPMCAS count from 11 to 12. Footnote *c* of Table 1 marks lumacaftor as formulated in crystalline form — only ivacaftor is an ASD in that product. The failing check narrowed the candidates to two molecules within seconds. This is precisely what the checks exist to do.

---

## Findings

### 1. Polymer selection is strongly stratified by molecular weight

| Polymer | Combinations | MW range (g/mol) | Max cLogP |
|---|---|---|---|
| **PVPVA** | 18 | 434 – 1113 | 9.4 |
| HPMCAS | 11 | 383 – **701** | **5.7** |
| HPMC | 3 | 521 – 882 | 8.1 |
| HPMCP, PVP, PEG, HPC, methacrylic acid–EA | 1 each | 449 – 804 | — |

Above MW 850, seven of the eight approved amorphous drugs are formulated with PVPVA; the sole exception is elbasvir on HPMC. HPMCAS — the second most common polymer overall, accounting for 30% of all drug–polymer combinations — has never been approved above MW 701 (posaconazole) or cLogP 5.7.

This is a countable fact about approved products rather than an inference, and it is directly actionable: for a candidate above MW 850, PVPVA has extensive precedent and HPMCAS has none.

### 2. The Rule-of-5 analysis reproduces, except for HBA

MW violations (n = 21) and HBD violations (n = 0) reproduce exactly. logP violations come out at 15 against the published 14, which is expected — the source used Molinspiration and this pipeline uses RDKit's Crippen implementation, and the two atom-contribution schemes disagree by a few tenths near the threshold.

The HBA figure does not reproduce under any definition tested. The source reports n = 1. RDKit's `CalcNumHBA` gives 8, and a plain nitrogen-plus-oxygen count — which is what Lipinski (2000) actually specified — gives 17. Tacrolimus alone contains 13 nitrogen and oxygen atoms.

This is reported rather than resolved. Molinspiration's implementation is not open, so the discrepancy cannot be traced from outside. Both definitions are stored in the database as separate named columns rather than picking one and calling it "HBA", because that choice changes downstream violation counts and should not be hidden.

### 3. Descriptor definitions are version-dependent

The same SMILES produced different HBA counts under two RDKit releases, on 13 of 36 molecules, while molecular weight matched to two decimal places on all 36. RDKit ships several acceptor definitions, and what `CalcNumHBA` means has changed between versions.

`data/provenance.json` therefore records the RDKit and pandas versions used to generate each table. Without it, a descriptor value in this repository could not be reproduced.

---

## Figures

Generated by `src/plot_landscape.py`. The target molecule is defined by four constants at the top of that file; changing them repositions every figure for a different candidate.

### Polymer molecular-weight envelope

![Molecular weight range each polymer has been approved across](figures/polymer_envelope.png)

Each row is a polymer; each dot is one approved drug formulated with it, placed at that drug's molecular weight. The bar spans the range from the lightest to the heaviest drug that polymer has been used with. The dashed line marks an example candidate at MW 923.

The HPMCAS row ends at 701 g/mol, well short of the candidate line, while PVPVA extends past it to 1113. That gap is finding 1 above, rendered directly.

### Chemical space

![Approved ASD drugs in MW/logP space](figures/chemical_space.png)

All 36 approved amorphous drugs plotted by molecular weight and cLogP. Colour indicates polymer, marker shape indicates manufacturing process. Dotted lines mark the Rule-of-5 thresholds at MW 500 and logP 5; anything up and to the right of their intersection violates both.

The example candidate is the star, drawn with a vertical bar spanning its specified logP range of 5.5–7.5 rather than a single point, because that uncertainty is real and collapsing it would misrepresent the input. Only the two approved drugs heavier than the candidate are labelled.

The visible structure is the same finding from a second angle: HPMCAS (orange) occupies the lower-left, PVPVA (blue) extends across the entire upper-right.

### Rule-of-5 reproduction and a rigidity proxy

![Ro5 violations and Fsp3 against molecular weight](figures/ro5_and_rigidity.png)

**Left:** computed violation counts against the published figures. MW and HBD match exactly; logP differs by one; HBA differs by seven under RDKit's definition and by sixteen under Lipinski's original N+O count, marked separately.

**Right:** Fsp3 — the fraction of carbon atoms that are sp³-hybridised — against molecular weight. This is a **structural proxy** for the rigidity that influences glass transition temperature and crystallisation tendency, not a measurement of it. Rigid, planar, aromatic molecules tend toward higher Tg and pack more readily into crystal lattices. The panel is labelled as a proxy deliberately, because presenting it as a stand-in for Tg would be wrong.

---

## Known limitations

- **No glass transition or melting temperatures.** These are the properties that most directly constrain thermal process feasibility, and they are absent from the source table. Assembling them means hunting scattered primary literature across 36 drugs with inconsistent measurement conditions. This is the highest-value addition the database could receive.
- **No drug loading.** Not present in the source and not derivable from it; it would have to come from patents or prescribing information on a per-product basis.
- **Ionisation class and pKa are empty by design.** They matter for polymer selection — ionic polymers such as HPMCAS behave differently from neutral ones for weak bases under gastric conditions — so they should be populated from primary sources with the source recorded, not guessed.
- **`max_amorphous_mg_per_unit` is derived, not transcribed.** For combination products it required judging which component is the ASD.
- **cLogP is an estimate.** Values from different algorithms can differ by 1–2 log units for high-molecular-weight molecules. Treat them as approximate.
- **Nearest-neighbour similarity uses only MW and logP.** These are the two properties available for a candidate specified by envelope alone. They are not a complete description of formulation-relevant behaviour.

---

## Licence

Code: MIT. The underlying data are factual attributes of approved drug products; please cite Moseson et al. (2024) in any derived work.
