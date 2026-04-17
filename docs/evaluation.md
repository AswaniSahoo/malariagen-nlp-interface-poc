# Evaluation Methodology

## Current PoC Metrics (Rule-Based Baseline)

| Metric | Value | Target (Midterm) | Target (Final) |
|--------|-------|-------------------|-----------------|
| Query resolution rate | 13/13 (100%) | 75% on 30 queries | 85% on 50 queries |
| Average confidence | 85% | 70% | 80% |
| API methods covered | 10 | 15 | 20+ |
| Entity types | 5 (gene, country, species, contig, sample) | 8 | 10+ |
| Edge case handling | 3/3 | 5/5 | 10/10 |

## Evaluation Dimensions

### 1. Intent Classification Accuracy
- **Metric**: % of queries correctly mapped to the right API method
- **Evaluation set**: Curated query bank (13 → 30 → 50 queries across milestones)
- **Method**: Confusion matrix across all supported methods
- **Baseline**: Current rule-based system achieves 100% on 13 direct queries

### 2. Entity Extraction Completeness
- **Metric**: F1 score for entity extraction
- **Entity types**: gene, country, species, contig, sample, sample_set, cohort, analysis_type
- **Edge cases**: Synonyms (kdr → Vgsc), regions (East Africa → country list), multi-entity queries

### 3. Code Generation Correctness
- **Metric**: % of generated code that executes without error on the API
- **Validation**: Runtime parameter validation via `@_check_types` decorators
- **Method**: Execute generated code against simulated data fixtures

### 4. User Experience
- **Metric**: Time-to-result compared to manual API usage
- **Method**: Timed comparison study with 5 representative queries
- **Target**: 3x faster than reading docs + writing code manually

## Query Bank Categories

| Category | Example | Methods Tested |
|----------|---------|----------------|
| Simple lookup | "What samples from Kenya?" | `sample_metadata` |
| Gene-specific | "Allele frequencies for Vgsc" | `plot_frequencies_heatmap` |
| Temporal | "kdr trends over time in Ghana" | `plot_frequencies_time_series` |
| Comparative | "Fst between populations by country" | `pairwise_average_fst` |
| Multi-entity | "Divergence between gambiae and coluzzii" | `plot_snps_dxy` |
| Haplotype | "Haplotype network for Vgsc in Burkina Faso" | `plot_haplotype_network` |
| Clustering | "Cluster haplotypes in Ace1 region" | `plot_haplotype_clustering` |
| Heterozygosity | "ROH for sample AN0131-C on 3R" | `plot_roh` |
| Region expansion | "arabiensis in East Africa" | `sample_metadata` (multi-country) |
| Edge case | "What is the weather in Nairobi?" | graceful degradation |

## Transition: Rule-Based → LLM-Based

### Phase 1: Schema Registry (Current)
- `src/schema_extractor.py` introspects 24 methods across 7 categories
- Provides machine-readable parameter types and docstrings
- Serves as grounding data for LLM-based generation

### Phase 2: RAG Pipeline (GSoC Weeks 3-6)
- Index API docstrings + training course notebooks in vector store
- Retrieve relevant method signatures at query time
- Ground LLM generation in actual API documentation

### Phase 3: Fine-Tuned LLM (GSoC Weeks 7-10)
- LoRA fine-tuning on curated (query, API call) pairs
- Validate outputs against `@_check_types` at runtime
- Target: 85% accuracy on 50-query evaluation set

## Automated Evaluation Pipeline

```
Query → NLP System → Generated Code → Validator → Score
                                          ↓
                                  Expected Output
                                  (from query bank)
```

Each query in the bank has:
1. **Input**: Natural language query
2. **Expected intent**: Correct API method name
3. **Expected entities**: Required extracted entities
4. **Expected code**: Valid Python API call
5. **Validation**: Whether the call would execute successfully

---

*This evaluation methodology will be expanded as the GSoC project progresses.*
