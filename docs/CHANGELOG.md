# Changelog

All notable changes to the NLP Interface PoC are documented here.

## [0.3.0] - 2026-04-17

### Added
- `src/schema_extractor.py` — API schema extraction module that introspects
  `malariagen_data` to build machine-readable method signatures (24 methods
  across 7 categories: data_access, frequency_analysis, population_genetics,
  haplotype_analysis, selection_scans, heterozygosity, pca)
- `docs/evaluation.md` — evaluation methodology covering metrics, query bank
  categories, and the transition plan from rule-based to LLM-based interface

## [0.2.0] - 2026-04-10

### Added
- 3 new haplotype/heterozygosity queries (10 → 13 total):
  - Query 11: `plot_haplotype_network` for Vgsc in Burkina Faso
  - Query 12: `plot_haplotype_clustering` for Ace1 gene region
  - Query 13: `plot_roh` for runs of homozygosity on chromosome 3R
- Haplotype clustering context boost in intent classifier
- Sample ID extraction via regex pattern (AN\d{4}-[A-Z])
- 3 new API method entries in the notebook registry

### Changed
- API methods covered: 7 → 10
- Total entities extracted: 29 → 37
- Average confidence: 84% → 85%
- Updated `README.md` and `examples/sample_queries.md` with verified results

## [0.1.0] - 2026-03-27

### Added
- Initial PoC notebook (`nlp_interface_poc.ipynb`) with full NLP pipeline:
  intent classification, entity extraction, API call generation
- 10 demo queries + 3 edge cases (84% avg confidence, 29 entities)
- Entity knowledge base: 11 genes, 24 countries, 15 contigs, 8 species
- `docs/architecture.md` — design rationale and pipeline documentation
- `examples/sample_queries.md` — full query outputs with analysis
- Multi-species Dxy support (gambiae + coluzzii → `plot_snps_dxy`)
- Region expansion (East Africa → individual country filters)
- Interactive demo interface

## [0.0.1] - 2026-03-27

### Added
- Repository initialized with README and project structure
