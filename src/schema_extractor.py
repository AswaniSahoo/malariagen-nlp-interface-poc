"""
API Schema Extractor for malariagen_data

Extracts method signatures, parameter types, docstrings, and Annotated
metadata from the malariagen_data library to build a machine-readable
schema that the NLP interface can use for:
  1. Intent classification (method lookup)
  2. Parameter validation
  3. Entity-to-parameter mapping

Usage:
    python schema_extractor.py > schema.json
"""

import inspect
import json
import typing
from typing import get_type_hints

# Target classes to introspect
TARGET_CLASSES = [
    "Ag3",
    "Af1",
]

# Method categories for NLP routing
METHOD_CATEGORIES = {
    "data_access": [
        "sample_metadata",
        "snp_calls",
        "haplotypes",
        "cnv_hmm",
        "cnv_discordant_read_calls",
    ],
    "frequency_analysis": [
        "plot_frequencies_heatmap",
        "plot_frequencies_time_series",
        "snp_allele_counts",
    ],
    "population_genetics": [
        "average_fst",
        "pairwise_average_fst",
        "plot_pairwise_average_fst",
    ],
    "haplotype_analysis": [
        "plot_haplotype_network",
        "plot_haplotype_clustering",
        "plot_haplotype_clustering_advanced",
    ],
    "selection_scans": [
        "plot_h12_gwss",
        "plot_g123_gwss",
        "ihs_gwss",
        "plot_ihs_gwss",
    ],
    "heterozygosity": [
        "plot_heterozygosity",
        "roh_hmm",
        "plot_roh",
    ],
    "pca": [
        "pca",
        "plot_pca_coords",
        "plot_pca_variance",
    ],
}


def extract_method_schema(cls, method_name: str) -> dict:
    """Extract schema for a single method."""
    method = getattr(cls, method_name, None)
    if method is None:
        return {"error": f"Method {method_name} not found on {cls.__name__}"}

    schema = {
        "name": method_name,
        "class": cls.__name__,
        "category": _get_category(method_name),
        "docstring": inspect.getdoc(method) or "",
        "parameters": {},
    }

    # Extract signature
    try:
        sig = inspect.signature(method)
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            param_info = {
                "kind": str(param.kind.name),
                "has_default": param.default is not inspect.Parameter.empty,
            }
            if param.default is not inspect.Parameter.empty:
                try:
                    # Attempt JSON serialization of default
                    json.dumps(param.default)
                    param_info["default"] = param.default
                except (TypeError, ValueError):
                    param_info["default"] = repr(param.default)

            if param.annotation is not inspect.Parameter.empty:
                param_info["annotation"] = _annotation_to_str(param.annotation)

            schema["parameters"][param_name] = param_info
    except (ValueError, TypeError) as e:
        schema["signature_error"] = str(e)

    return schema


def _get_category(method_name: str) -> str:
    """Look up which category a method belongs to."""
    for category, methods in METHOD_CATEGORIES.items():
        if method_name in methods:
            return category
    return "other"


def _annotation_to_str(annotation) -> str:
    """Convert a type annotation to a readable string."""
    if hasattr(annotation, "__metadata__"):
        # Annotated type — extract the description
        base = annotation.__args__[0] if hasattr(annotation, "__args__") else annotation
        metadata = annotation.__metadata__
        desc = next((m for m in metadata if isinstance(m, str)), None)
        return f"{getattr(base, '__name__', str(base))} — {desc}" if desc else str(base)
    elif hasattr(annotation, "__name__"):
        return annotation.__name__
    else:
        return str(annotation)


def extract_full_schema(class_name: str = "Ag3") -> dict:
    """Extract schema for all categorized methods from a target class."""
    try:
        import malariagen_data
        cls = getattr(malariagen_data, class_name)
    except (ImportError, AttributeError) as e:
        return {"error": str(e), "note": "malariagen_data must be installed"}

    schema = {
        "class": class_name,
        "total_methods": 0,
        "categories": {},
        "methods": {},
    }

    all_methods = set()
    for methods in METHOD_CATEGORIES.values():
        all_methods.update(methods)

    for method_name in sorted(all_methods):
        method_schema = extract_method_schema(cls, method_name)
        schema["methods"][method_name] = method_schema
        schema["total_methods"] += 1

    # Category summary
    for cat, methods in METHOD_CATEGORIES.items():
        available = [m for m in methods if hasattr(cls, m)]
        schema["categories"][cat] = {
            "total": len(methods),
            "available": len(available),
            "methods": available,
        }

    return schema


if __name__ == "__main__":
    schema = extract_full_schema("Ag3")
    print(json.dumps(schema, indent=2, default=str))
