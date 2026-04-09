# Sample Queries - NLP Interface PoC

Thirteen natural-language queries demonstrating the translation pipeline from plain English to executable `malariagen_data` API calls, plus three edge-case queries showing graceful out-of-scope handling.

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
| Intent | `sample_metadata` (100% confidence) |
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

## Query 8 - Genetic Divergence Between Species (Multi-Species Extraction)

**Input:** "What is the genetic divergence between gambiae and coluzzii populations?"

| Field | Value |
|-------|-------|
| Intent | `plot_snps_dxy` (100% confidence) |
| Entities | species_1=coluzzii, species_2=gambiae, multi_species=True |
| Explanation | Plots Dxy across chromosome 2L between coluzzii and gambiae |

```python
ag3.plot_snps_dxy(
    contig="2L",
    cohort1_query="taxon == 'coluzzii'",
    cohort2_query="taxon == 'gambiae'",
    window_size=20000
)
```

This query demonstrates multi-species entity extraction: both species names are identified and mapped to separate `cohort_query` parameters, and the intent is correctly routed to `plot_snps_dxy` (not `pairwise_average_fst`).

---

## Query 9 - Species-Specific Metadata with Region Expansion

**Input:** "List all samples of An. arabiensis from East Africa"

| Field | Value |
|-------|-------|
| Intent | `sample_metadata` (80% confidence) |
| Entities | country=east africa, area=[KE, TZ, UG, ET, MZ, MW], species=arabiensis |
| Explanation | Retrieves sample metadata for arabiensis in East Africa |

```python
ag3.sample_metadata(
    sample_query="taxon == 'arabiensis' and country in ['Kenya', 'Tanzania', 'Uganda', 'Ethiopia', 'Mozambique', 'Malawi']"
)
```

This query demonstrates region expansion: "East Africa" is expanded into individual country names rather than passed as an invalid string literal, producing a valid `sample_query` that the API can execute.

---

## Query 10 - Resistance Mutations

**Input:** "Visualize insecticide resistance mutations in Mozambique"

| Field | Value |
|-------|-------|
| Intent | `plot_frequencies_heatmap` (60% confidence) |
| Entities | country=mozambique, area=MZ |
| Explanation | Plots allele frequency heatmap for Vgsc gene in Mozambique |

```python
ag3.plot_frequencies_heatmap(
    transcript="AGAP004707-RD",
    sample_query="country == 'Mozambique'",
    min_cohort_size=10
)
```

---

## Query 11 — Haplotype Network Visualization

**Input:** "Show me the haplotype network for Vgsc in Burkina Faso"

| Field | Value |
|-------|-------|
| Intent | `plot_haplotype_network` (80% confidence) |
| Entities | gene=vgsc, transcript=AGAP004707-RD, country=burkina faso, area=BF |
| Explanation | Plots median-joining haplotype network for Vgsc gene in Burkina Faso |

```python
ag3.plot_haplotype_network(
    region="AGAP004707-RD",
    color="country",
    sample_query="country == 'Burkina Faso'"
)
```

This query targets the `plot_haplotype_network` method which visualises genetic distances between haplotypes using Cytoscape. The `color` parameter partitions haplotype nodes by country, and `region` accepts a transcript ID to define the genomic region.

---

## Query 12 — Haplotype Clustering

**Input:** "Cluster haplotypes in the Ace1 gene region"

| Field | Value |
|-------|-------|
| Intent | `plot_haplotype_clustering` (80% confidence) |
| Entities | gene=ace1, transcript=AGAP001356-RA |
| Explanation | Hierarchically clusters haplotypes in the Ace1 gene region |

```python
ag3.plot_haplotype_clustering(
    region="AGAP001356-RA",
    color="country",
    title="Ace1 haplotype clustering"
)
```

This query exercises `plot_haplotype_clustering` which produces an interactive dendrogram of haplotype distances. The method computes pairwise Hamming distances between phased haplotypes and uses hierarchical clustering.

---

## Query 13 — Runs of Homozygosity

**Input:** "Show heterozygosity and runs of homozygosity for sample AN0131-C on chromosome 3R"

| Field | Value |
|-------|-------|
| Intent | `plot_roh` (80% confidence) |
| Entities | sample=AN0131-C, contig=3R |
| Explanation | Plots windowed heterozygosity with inferred ROH for a single sample |

```python
ag3.plot_roh(
    sample="AN0131-C",
    region="3R"
)
```

This query targets `plot_roh` which combines windowed heterozygosity, HMM-inferred runs of homozygosity, and a gene track into a single stacked figure. The `sample` parameter takes a specific sample ID and `region` takes a contig name.

---

## Query 11 — Haplotype Network Visualization

**Input:** "Show me the haplotype network for Vgsc in Burkina Faso"

| Field | Value |
|-------|-------|
| Intent | `plot_haplotype_network` (100% confidence) |
| Entities | gene=vgsc, transcript=AGAP004707-RD, country=burkina faso, area=BF |
| Explanation | Plots median-joining haplotype network for vgsc in Burkina Faso |

```python
ag3.plot_haplotype_network(
    region="AGAP004707-RD",
    color="country",
    sample_query="country == 'Burkina Faso'"
)
```

This query targets the `plot_haplotype_network` method which visualises genetic distances between haplotypes using Cytoscape. The `color` parameter partitions haplotype nodes by country, and `region` accepts a transcript ID to define the genomic region.

---

## Query 12 — Haplotype Clustering

**Input:** "Cluster haplotypes in the Ace1 gene region"

| Field | Value |
|-------|-------|
| Intent | `plot_haplotype_clustering` (60% confidence) |
| Entities | gene=ace1, transcript=AGAP001356-RA |
| Explanation | Hierarchically clusters haplotypes in the ace1 gene region |

```python
ag3.plot_haplotype_clustering(
    region="AGAP001356-RA",
    color="country",
    title="ace1 haplotype clustering"
)
```

This query exercises `plot_haplotype_clustering` which produces an interactive dendrogram of haplotype distances. The method computes pairwise Hamming distances between phased haplotypes and uses hierarchical clustering.

---

## Query 13 — Runs of Homozygosity

**Input:** "Show heterozygosity and runs of homozygosity for sample AN0131-C on chromosome 3R"

| Field | Value |
|-------|-------|
| Intent | `plot_roh` (100% confidence) |
| Entities | sample=AN0131-C, contig=3R |
| Explanation | Plots windowed heterozygosity with inferred ROH for sample AN0131-C on 3R |

```python
ag3.plot_roh(
    sample="AN0131-C",
    region="3R"
)
```

This query targets `plot_roh` which combines windowed heterozygosity, HMM-inferred runs of homozygosity, and a gene track into a single stacked figure. The `sample` parameter takes a specific sample ID and `region` takes a contig name.

---

## Edge Cases — Out-of-Scope Queries

Three queries that fall outside the system's scope, demonstrating graceful degradation.

### Edge Case 1: "What is the weather like in Nairobi?"

| Field | Value |
|-------|-------|
| Intent | `unknown` (0% confidence) |
| Entities | (none) |
| ⚠ | LOW CONFIDENCE — system would ask for clarification |

### Edge Case 2: "Tell me about malaria treatment drugs"

| Field | Value |
|-------|-------|
| Intent | `unknown` (0% confidence) |
| Entities | (none) |
| ⚠ | LOW CONFIDENCE — system would ask for clarification |

### Edge Case 3: "Run a GWAS analysis on chromosome 2L with PCA"

| Field | Value |
|-------|-------|
| Intent | `unknown` (0% confidence) |
| Entities | contig=2L |
| ⚠ | LOW CONFIDENCE — system would ask for clarification |

The edge cases show that the system extracts valid entities where possible (contig=2L) but correctly refuses to generate an API call when it cannot identify a valid intent, preventing false-positive method matches.

---

## Summary

| # | Query | Intent | Confidence | Entities |
|---|-------|--------|-----------|----------|
| 1 | Allele frequencies for Vgsc in Kenya | `plot_frequencies_heatmap` | 60% | 4 |
| 2 | kdr trends over time in Ghana | `plot_frequencies_time_series` | 100% | 4 |
| 3 | Fst by country on chr 3L | `pairwise_average_fst` | 60% | 2 |
| 4 | Fst heatmap lower triangle | `plot_pairwise_average_fst` | 100% | 1 |
| 5 | Samples from Tanzania | `sample_metadata` | 100% | 2 |
| 6 | SNP data for Ace1 in Uganda | `snp_calls` | 80% | 4 |
| 7 | cyp6p3 trends in Burkina Faso | `plot_frequencies_time_series` | 100% | 4 |
| 8 | Divergence gambiae vs coluzzii | `plot_snps_dxy` | 100% | 3 |
| 9 | An. arabiensis in East Africa | `sample_metadata` | 80% | 3 |
| 10 | Resistance mutations in Mozambique | `plot_frequencies_heatmap` | 60% | 2 |
| 11 | Haplotype network for Vgsc in Burkina Faso | `plot_haplotype_network` | 100% | 4 |
| 12 | Cluster haplotypes in Ace1 region | `plot_haplotype_clustering` | 60% | 2 |
| 13 | Heterozygosity + ROH for sample on 3R | `plot_roh` | 100% | 2 |

**Overall:** 13/13 resolved, 85% average confidence, 37 total entities extracted, 3/3 edge cases handled gracefully.

---

*Generated from `nlp_interface_poc.ipynb`*