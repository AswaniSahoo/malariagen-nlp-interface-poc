# Architecture: NLP Interface for malariagen-data-python

## Overview

This document describes the architecture of the natural-language interface for querying malaria vector genomic data through the `malariagen-data-python` API.

The system translates plain-language questions from researchers into executable `malariagen_data` API calls, removing the need to know specific method names, parameter types, or cohort query syntax.

---

## Pipeline Stages

```
┌──────────────┐     ┌──────────────────┐     ┌────────────────┐     ┌──────────────┐
│  User Query  │───▶│ Intent Classifier │───▶│ Entity         │───▶│ API Call     │
│  (string)    │     │                  │     │ Extractor      │     │ Generator    │
└──────────────┘     └──────────────────┘     └────────────────┘     └──────────────┘
                            │                       │                     │
                            ▼                       ▼                     ▼
                    Match query to          Extract structured     Generate valid
                    API method via          entities: gene,        Python code with
                    keyword scoring         country, contig,       correct parameter
                    + category boost        species, annotation    names and values
```

### Stage 1: Intent Classification

Maps the user's natural-language query to the most relevant `malariagen_data` API method.

**Current PoC approach:** Keyword scoring against a per-method keyword list, with contextual boosts for category hints ("show" → plot, "compute" → analysis, "get" → data) and phrase-level matching ("over time" → `plot_frequencies_time_series`).

**Proposed GSoC approach:** Replace keyword scoring with either:
- A fine-tuned LLM (LoRA on LLaMA-3.1-8B, leveraging [llama-task-agent](https://github.com/AswaniSahoo/llama-task-agent) architecture) that maps NL queries to method names
- A RAG pipeline that retrieves the most relevant method docstrings using embeddings, then uses few-shot prompting for selection

### Stage 2: Entity Extraction

Extracts structured entities from the query and maps them to valid API parameter values.

**Entity types supported:**

| Entity | Example Input | Mapped Value |
|--------|--------------|--------------|
| Gene name | "Vgsc", "kdr", "Ace1" | Transcript ID (e.g., `AGAP004707-RD`) |
| Country | "Kenya", "Burkina Faso" | ISO code or sample query |
| Contig | "chromosome 2L", "3R" | Normalised contig name |
| Species | "An. gambiae", "coluzzii" | Normalised taxon string |
| Cohort grouping | "by country", "by species" | Cohort column name |
| Annotation preference | "lower triangle", "with errors" | Annotation parameter value |

**Proposed GSoC approach:** Named Entity Recognition (NER) model fine-tuned on genomics vocabulary, grounded in the API's existing `Annotated` type aliases and `@doc()` docstrings. The 236 domain terms from [biodiversity-publication-analyzer](https://github.com/AswaniSahoo/biodiversity-publication-analyzer) provide a starting vocabulary.

### Stage 3: API Call Generation

Combines the resolved intent (method name) and extracted entities (parameter values) into executable Python code.

**Current PoC approach:** Template-based generation with per-method code templates that slot in entity values.

**Proposed GSoC approach:**
- Validate generated parameters against the method's type hints at runtime (using the same `@_check_types` / `typeguard` infrastructure the API already uses)
- Use `describe_api()` output (PR #904) for method-level discovery
- Use `inspect.signature()` + `typing.get_type_hints()` for parameter-level introspection
- Catch and explain validation errors in plain language

---

## API Schema Registry

The PoC maintains a manual registry of 7 API methods with their parameters, types, descriptions, and keyword lists. In the full implementation, this registry would be generated automatically from the API's introspection infrastructure:

| Source | What It Provides |
|--------|------------------|
| `describe_api()` (PR #904) | Method names, summaries, categories |
| `inspect.signature(method)` | Parameter names and defaults |
| `typing.get_type_hints(method)` | Parameter types including `Annotated` metadata |
| `Literal[...]` types in `*_params.py` | Valid value sets for constrained parameters |
| `@doc()` decorator content | Human-readable parameter descriptions |

---

## Entity Knowledge Base

The PoC includes domain-specific dictionaries that map natural-language terms to valid API values:

- **11 gene/transcript mappings** — insecticide resistance genes (Vgsc/kdr, Rdl, Ace1, CYP450s, GSTE2)
- **24 country/region mappings** — African countries + regional groupings (East Africa, West Africa)
- **15 contig aliases** — chromosome names in various formats
- **8 species mappings** — *Anopheles* species name normalization

In the full implementation, these would be populated from the API's sample metadata (`ag3.sample_metadata()`) and genome annotation data, ensuring they stay current as new data releases are added.

---

## Evaluation Strategy

The PoC demonstrates the concept with 10 test queries. The proposed GSoC evaluation suite would include:

1. **50+ natural-language queries** with expected API calls — covering all method categories
2. **Intent accuracy** — % of queries mapped to the correct method
3. **Entity extraction recall** — % of entities in the query that are correctly extracted
4. **Parameter validity** — % of generated calls that pass `@_check_types` validation
5. **End-to-end correctness** — % of generated calls that produce the expected output when executed against the Ag3 simulator

---

## Connection to Existing Infrastructure

This project builds on two pieces of existing infrastructure in `malariagen-data-python`:

1. **`describe_api()` (PR #904)** — provides method-level discovery. The NLP interface uses this as the first layer of its API schema registry.

2. **`Annotated` type aliases** — the parameter types in `fst_params.py`, `base_params.py`, etc. carry both type constraints and human-readable descriptions. These serve as machine-readable API metadata that the NLP system can introspect at runtime.

---

*Author: Aswani Sahoo ([@AswaniSahoo](https://github.com/AswaniSahoo))*