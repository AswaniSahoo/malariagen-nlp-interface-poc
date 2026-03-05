# MalariaGEN NLP Interface — Proof of Concept

Natural language → `malariagen_data` API translation for querying malaria vector genomic data without programming expertise.

## Demo

```
User:  "Show me allele frequencies for Vgsc in Kenya"
→ Intent:  plot_frequencies_heatmap (60% confidence)
→ Entities: gene=vgsc, transcript=AGAP004707-RD, country=kenya, area=KE

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
| Entities extracted | 29 total |
| API methods covered | 7 (data + analysis + plot) |

## Architecture

```
User Query → Intent Classifier → Entity Extractor → API Call Generator → Executable Code
```

**Current PoC:** Rule-based (keyword matching + regex entities + template generation)

**Proposed GSoC:** Fine-tuned LLM (LoRA) + RAG over API docstrings + runtime parameter validation

## Context

This PoC demonstrates the core concept for the GSoC 2026 project: *"Exploring natural-language interfaces to increase the understanding of malaria vector genomic data"* ([MalariaGEN](https://www.malariagen.net/vobs)).

Built on top of:
- [`describe_api()`](https://github.com/malariagen/malariagen-data-python/pull/904) — method-level API introspection (merged)
- [`malariagen-data-python`](https://github.com/malariagen/malariagen-data-python) — the target API

## Related Work

- [llama-task-agent](https://github.com/AswaniSahoo/llama-task-agent) — LLaMA-3.1-8B fine-tuned for NL → structured task execution
- [biodiversity-publication-analyzer](https://github.com/AswaniSahoo/biodiversity-publication-analyzer) — SciBERT genomics NLP pipeline (236 domain terms)

## Author

Aswani Sahoo ([@AswaniSahoo](https://github.com/AswaniSahoo))