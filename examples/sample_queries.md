# Sample Queries - NLP Interface PoC

Ten natural-language queries demonstrating the translation pipeline from plain English to executable `malariagen_data` API calls.

---

## Query 1 - Allele Frequencies by Gene and Country

**Input:** "Show me allele frequencies for Vgsc in Kenya"

| Field | Value |
|-------|-------|
| Intent | `plot_frequencies_heatmap` (60% confidence) |
| Entities | gene=vgsc, transcript=AGAP004707-RD, country=kenya, area=KE |
| Explanation | Plots allele frequency heatmap for vgsc gene in Kenya |

```python
ag3.plot_frequencies_heatmap(
    transcript="AGAP004707-RD",
    sample_query="country == 'Kenya'",
    min_cohort_size=10
)
```

---

## Query 2 - Temporal Trends

**Input:** "How have kdr mutation frequencies changed over time in Ghana?"

| Field | Value |
|-------|-------|
| Intent | `plot_frequencies_time_series` (100% confidence) |
| Entities | gene=kdr, transcript=AGAP004707-RD, country=ghana, area=GH |
| Explanation | Plots temporal trends of kdr mutation frequencies in Ghana |

```python
ag3.plot_frequencies_time_series(
    transcript="AGAP004707-RD",
    area=Region("GH"),
    period_by="year",
    min_cohort_size=10
)
```

---

## Query 3 - Population Differentiation

**Input:** "Compare genetic differentiation between populations by country on chromosome 3L"

| Field | Value |
|-------|-------|
| Intent | `pairwise_average_fst` (60% confidence) |
| Entities | contig=3L, cohort_by=country |
| Explanation | Computes pairwise Fst on chromosome 3L grouped by country |

```python
fst_df = ag3.pairwise_average_fst(
    contig="3L",
    cohorts="country",
    min_cohort_size=10
)
```

---

## Query 4 - Fst Heatmap with Display Preference

**Input:** "Plot the Fst heatmap with lower triangle only"

| Field | Value |
|-------|-------|
| Intent | `plot_pairwise_average_fst` (100% confidence) |
| Entities | annotation=lower triangle |
| Explanation | Plots Fst heatmap with lower triangle display |

```python
ag3.plot_pairwise_average_fst(
    fst_df,
    annotation="lower triangle"
)
```

---

## Query 5 - Sample Metadata Lookup

**Input:** "What samples do we have from Tanzania?"

| Field | Value |
|-------|-------|
| Intent | `sample_metadata` (20% confidence) |
| Entities | country=tanzania, area=TZ |
| Explanation | Retrieves sample metadata in Tanzania |

```python
ag3.sample_metadata(
    sample_query="country == 'Tanzania'"
)
```

---

## Query 6 - SNP Data for a Specific Gene

**Input:** "Get SNP genotype data for Ace1 in Uganda"

| Field | Value |
|-------|-------|
| Intent | `snp_calls` (80% confidence) |
| Entities | gene=ace1, transcript=AGAP001356-RA, country=uganda, area=UG |
| Explanation | Retrieves SNP genotype data for ace1 |

```python
ag3.snp_calls(
    region="AGAP001356-RA",
    sample_query="country == 'Uganda'"
)
```

---

## Query 7 - Frequency Trends for CYP450 Gene

**Input:** "Show me the frequency trends for cyp6p3 in Burkina Faso"

| Field | Value |
|-------|-------|
| Intent | `plot_frequencies_time_series` (100% confidence) |
| Entities | gene=cyp6p3, transcript=AGAP002865-RB, country=burkina faso, area=BF |
| Explanation | Plots temporal trends of cyp6p3 mutation frequencies in Burkina Faso |

```python
ag3.plot_frequencies_time_series(
    transcript="AGAP002865-RB",
    area=Region("BF"),
    period_by="year",
    min_cohort_size=10
)
```

---

## Query 8 - Genetic Divergence Between Species

**Input:** "What is the genetic divergence between gambiae and coluzzii populations?"

| Field | Value |
|-------|-------|
| Intent | `pairwise_average_fst` (20% confidence) |
| Entities | species=gambiae |
| Explanation | Computes pairwise Fst on chromosome 3L grouped by country |

```python
fst_df = ag3.pairwise_average_fst(
    contig="3L",
    cohorts="country",
    min_cohort_size=10
)
```

*Note: Low confidence — the query mentions two species but the current PoC extracts only the first. A production system would generate separate cohort queries for each species and use `plot_snps_dxy` or species-aware Fst cohorts.*

---

## Query 9 - Species-Specific Metadata

**Input:** "List all samples of An. arabiensis from East Africa"

| Field | Value |
|-------|-------|
| Intent | `sample_metadata` (40% confidence) |
| Entities | country=east africa, area=[KE, TZ, UG, ET, MZ, MW], species=arabiensis |
| Explanation | Retrieves sample metadata for arabiensis in East Africa |

```python
ag3.sample_metadata(
    sample_query="taxon == 'arabiensis' and country == 'East Africa'"
)
```

*Note: "East Africa" is a region grouping, not a single country value. A production system would expand this into individual country filters or use the area code list directly.*

---

## Query 10 - Resistance Mutations

**Input:** "Visualize insecticide resistance mutations in Mozambique"

| Field | Value |
|-------|-------|
| Intent | `plot_frequencies_heatmap` (40% confidence) |
| Entities | country=mozambique, area=MZ |
| Explanation | Plots allele frequency heatmap for Vgsc gene in Mozambique |

```python
ag3.plot_frequencies_heatmap(
    transcript="AGAP004707-RD",
    sample_query="country == 'Mozambique'",
    min_cohort_size=10
)
```

*Note: "Insecticide resistance" is mapped to Vgsc by default. A production system would query multiple resistance-associated genes (Vgsc, Rdl, Ace1, CYP450s) and present combined results.*

---

## Summary

| # | Query | Intent | Confidence | Entities |
|---|-------|--------|-----------|----------|
| 1 | Allele frequencies for Vgsc in Kenya | `plot_frequencies_heatmap` | 60% | 4 |
| 2 | kdr trends over time in Ghana | `plot_frequencies_time_series` | 100% | 4 |
| 3 | Fst by country on chr 3L | `pairwise_average_fst` | 60% | 2 |
| 4 | Fst heatmap lower triangle | `plot_pairwise_average_fst` | 100% | 1 |
| 5 | Samples from Tanzania | `sample_metadata` | 20% | 2 |
| 6 | SNP data for Ace1 in Uganda | `snp_calls` | 80% | 4 |
| 7 | cyp6p3 trends in Burkina Faso | `plot_frequencies_time_series` | 100% | 4 |
| 8 | Divergence gambiae vs coluzzii | `pairwise_average_fst` | 20% | 1 |
| 9 | An. arabiensis in East Africa | `sample_metadata` | 40% | 3 |
| 10 | Resistance mutations in Mozambique | `plot_frequencies_heatmap` | 40% | 2 |

**Overall:** 10/10 resolved, 62% average confidence, 27 total entities extracted.

---

*Generated from `nlp_interface_poc.ipynb`*