# MalariaGEN NLP Interface - Proof of Concept

Natural language → [`malariagen_data`](https://github.com/malariagen/malariagen-data-python) API translation for querying malaria vector genomic data without programming expertise.

## Demo

```
User:  "Show me allele frequencies for Vgsc in Kenya"

→ Intent:     plot_frequencies_heatmap (60% confidence)
→ Entities:   gene=vgsc, transcript=AGAP004707-RD, country=kenya, area=KE
→ Explanation: Plots allele frequency heatmap for Vgsc gene in Kenya

Generated:
  ag3.plot_frequencies_heatmap(
      transcript="AGAP004707-RD",
      sample_query="country == 'Kenya'",
      min_cohort_size=10
  )
```

## Results

| Metric | Value |
|--------|-------|
| Queries resolved | 13/13 (100%) |
| Average confidence | 85% |
| Entities extracted | 37 total |
| API methods covered | 10 (data + analysis + plot) |
| Edge cases handled | 3/3 (graceful degradation) |

See [`examples/sample_queries.md`](examples/sample_queries.md) for all 13 test queries + 3 edge cases with full outputs.

## Architecture

```
User Query → Intent Classifier → Entity Extractor → API Call Generator → Executable Code
```

**Current PoC:** Rule-based (keyword matching + regex entity extraction + template code generation), with multi-species extraction, region expansion, and out-of-scope detection

**Proposed GSoC:** Fine-tuned LLM (LoRA) + RAG over API docstrings + runtime parameter validation via `@_check_types`

See [`docs/architecture.md`](docs/architecture.md) for the full design rationale, pipeline trace examples, and scaling plan.

## Key Capabilities

- **Multi-entity extraction** — gene + country + species in a single query
- **Multi-species handling** — "divergence between gambiae and coluzzii" → separate `cohort_query` parameters
- **Region expansion** — "East Africa" → individual country filters (`country in ['Kenya', 'Tanzania', ...]`)
- **Graceful degradation** — out-of-scope queries return `unknown` with clarification prompt
- **Pipeline traceability** — full keyword scores → entity matches → code generation trace

## Repository Structure

```
├── README.md                        This file
├── nlp_interface_poc.ipynb          Main notebook — full working pipeline
├── src/
│   └── schema_extractor.py         API schema extraction (24 methods, 7 categories)
├── docs/
│   ├── architecture.md             Design rationale, pipeline stages, evaluation plan
│   ├── evaluation.md               Evaluation methodology and transition roadmap
│   └── CHANGELOG.md                Project history and version tracking
└── examples/
    └── sample_queries.md           13 demo queries + 3 edge cases with expected outputs
```

## Context

This PoC demonstrates the core concept for the GSoC 2026 project: *"Exploring natural-language interfaces to increase the understanding of malaria vector genomic data"* ([MalariaGEN](https://www.malariagen.net/vobs)).

Built on top of:
- [`describe_api()`](https://github.com/malariagen/malariagen-data-python/pull/904) - method-level API introspection (merged by @mandeepsingh2007)
- [`malariagen-data-python`](https://github.com/malariagen/malariagen-data-python) - the target API
- [`Annotated` type aliases](https://github.com/malariagen/malariagen-data-python/blob/master/malariagen_data/anoph/fst_params.py) - machine-readable parameter metadata used for validation and documentation

## Related Work

- [llama-task-agent](https://github.com/AswaniSahoo/llama-task-agent) - LLaMA-3.1-8B fine-tuned with LoRA for NL → structured task execution (100% format compliance)
- [biodiversity-publication-analyzer](https://github.com/AswaniSahoo/biodiversity-publication-analyzer) - SciBERT genomics NLP pipeline (236 domain terms, 99.5% F1)
- [Contributions to malariagen-data-python](https://github.com/malariagen/malariagen-data-python/pulls?q=is%3Apr+author%3AAswaniSahoo+is%3Amerged) - 2 merged PRs (#895, #969)

## Author

Aswani Sahoo ([@AswaniSahoo](https://github.com/AswaniSahoo))
