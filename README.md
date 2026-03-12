# MalariaGEN NLP Interface — Proof of Concept

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
| Queries resolved | 10/10 (100%) |
| Average confidence | 62% |
| Entities extracted | 27 total |
| API methods covered | 7 (data + analysis + plot) |

See [`examples/sample_queries.md`](examples/sample_queries.md) for all 10 test queries with full outputs.

## Architecture

```
User Query ? Intent Classifier → Entity Extractor → API Call Generator → Executable Code
```

**Current PoC:** Rule-based (keyword matching + regex entity extraction + template code generation)

**Proposed GSoC:** Fine-tuned LLM (LoRA) + RAG over API docstrings + runtime parameter validation via `@_check_types`

See [`docs/architecture.md`](docs/architecture.md) for the full design rationale and scaling plan.

## Repository Structure

```
├── README.md                        This file
├── nlp_interface_poc.ipynb          Main notebook — full working pipeline
├── docs/
│   └── architecture.md             Design rationale, pipeline stages, evaluation plan
└── examples/
    └── sample_queries.md           10 demo queries with expected outputs
```

## Context

This PoC demonstrates the core concept for the GSoC 2026 project: *"Exploring natural-language interfaces to increase the understanding of malaria vector genomic data"* ([MalariaGEN](https://www.malariagen.net/vobs)).

Built on top of:
- [`describe_api()`](https://github.com/malariagen/malariagen-data-python/pull/904) — method-level API introspection (merged by @mandeepsingh2007)
- [`malariagen-data-python`](https://github.com/malariagen/malariagen-data-python) — the target API
- [`Annotated` type aliases](https://github.com/malariagen/malariagen-data-python/blob/master/malariagen_data/anoph/fst_params.py) — machine-readable parameter metadata used for validation and documentation

## Related Work

- [llama-task-agent](https://github.com/AswaniSahoo/llama-task-agent) — LLaMA-3.1-8B fine-tuned with LoRA for NL → structured task execution (100% format compliance)
- [biodiversity-publication-analyzer](https://github.com/AswaniSahoo/biodiversity-publication-analyzer) — SciBERT genomics NLP pipeline (236 domain terms, 99.5% F1)
- [Contributions to malariagen-data-python](https://github.com/malariagen/malariagen-data-python/pulls?q=is%3Apr+author%3AAswaniSahoo+is%3Amerged) — 2 merged PRs (#895, #969)

## Author

Aswani Sahoo ([@AswaniSahoo](https://github.com/AswaniSahoo))