"""Single source of truth for EmpiricalWiki entity schemas.

Centralizes the constants that lint.py and research_wiki.py both need:
entity directories, valid edge types, required frontmatter fields per
entity, valid enum values, and safe defaults for `lint --fix`.

If you change anything here, also update the matching template comments
in `i18n/en/CLAUDE.md` and `i18n/zh/CLAUDE.md` (and re-run setup.sh).
The Cross-Reference table in those files is the human-facing spec; this
file is the machine-facing copy that the tools actually consume.
"""

from __future__ import annotations

from pathlib import Path

# Entity directories. Summary lives at the wiki root, not under entities, but
# lint treats it as an entity directory because it has frontmatter pages.
ENTITY_DIRS = [
    "papers",
    "variables", "datasets", "models", "mechanisms", "hypotheses",
    "identification", "robustness", "heterogeneity", "tables",
    "assumptions", "propositions",
    "concepts", "topics", "people",
    "ideas", "experiments", "claims", "Summary",
    "foundations",
]

# Obsidian-facing group folders that nest entity directories for cleaner UX.
# Entity dirs live inside these; tools resolve paths through this mapping.
GROUP_FOLDERS: dict[str, str] = {
    "papers": "01_论文库",
    "variables": "02_研究设计",
    "datasets": "02_研究设计",
    "models": "02_研究设计",
    "mechanisms": "02_研究设计",
    "hypotheses": "02_研究设计",
    "identification": "02_研究设计",
    "robustness": "02_研究设计",
    "heterogeneity": "02_研究设计",
    "tables": "02_研究设计",
    "assumptions": "02_研究设计",
    "propositions": "02_研究设计",
    "concepts": "03_知识体系",
    "topics": "03_知识体系",
    "foundations": "03_知识体系",
    "Summary": "03_知识体系",
    "people": "04_研究者与想法",
    "ideas": "04_研究者与想法",
    "experiments": "04_研究者与想法",
    "claims": "04_研究者与想法",
    "outputs": "05_产出",
    "graph": "_系统",
}

_GROUP_SET: frozenset[str] = frozenset(GROUP_FOLDERS.values())


def resolve_entity_dir(root: Path, name: str) -> Path:
    """Resolve an entity directory path, searching group folders if needed."""
    direct = root / name
    if direct.exists():
        return direct
    if name in GROUP_FOLDERS:
        nested = root / GROUP_FOLDERS[name] / name
        if nested.exists():
            return nested
    return direct


def resolve_node_kind(node_id: str) -> str:
    """Extract entity kind from node_id, accounting for group folder nesting."""
    if "/" not in node_id:
        return ""
    parts = node_id.split("/")
    if parts[0] in _GROUP_SET:
        return parts[1] if len(parts) > 1 else ""
    return parts[0]


def find_page(root: Path, node_id: str) -> Path | None:
    """Find a wiki page by node_id (e.g., 'papers/some-slug').

    Searches recursively within entity directories, so papers can be
    organized into domain subfolders without breaking node references.
    """
    if "/" not in node_id:
        return None
    kind, slug = node_id.split("/", 1)
    entity_dir = resolve_entity_dir(root, kind)
    if not entity_dir.exists():
        return None
    # Try direct path first
    direct = entity_dir / f"{slug}.md"
    if direct.exists():
        return direct
    # Recursive search
    results = list(entity_dir.rglob(f"{slug}.md"))
    return results[0] if results else None

EDGE_CONFIDENCE_VALUES = {"high", "medium", "low"}

CITATION_EDGE_TYPES = {"cites"}
CITATION_SOURCES = {"semantic_scholar", "parsed_bib", "manual"}

ANY_ENDPOINT = "*"
DIRECTION_DIRECTED = "directed"
DIRECTION_SYMMETRIC = "symmetric"
CONFIDENCE_REQUIRED = "required"
CONFIDENCE_NONE = "none"

# Single registry for typed semantic graph edges (graph/edges.jsonl).
# Attributes here are the source of truth; compatibility constants below are
# derived views for older tool code and CLI help.
EDGE_TYPE_SPECS: dict[str, dict[str, str]] = {
    # /ingest paper-paper semantic judgments.
    "same_problem_as": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_SYMMETRIC,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "similar_method_to": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_SYMMETRIC,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "complementary_to": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_SYMMETRIC,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "builds_on": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "compares_against": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "improves_on": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "challenges": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "surveys": {
        "from_kind": "papers",
        "to_kind": "papers",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },

    # /ingest paper-concept semantic judgments.
    "introduces_concept": {
        "from_kind": "papers",
        "to_kind": "concepts",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "uses_concept": {
        "from_kind": "papers",
        "to_kind": "concepts",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "extends_concept": {
        "from_kind": "papers",
        "to_kind": "concepts",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },
    "critiques_concept": {
        "from_kind": "papers",
        "to_kind": "concepts",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "ingest",
    },

    # Empirical-research extraction edges.
    "operationalizes": {
        "from_kind": "papers",
        "to_kind": "variables",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "uses_dataset": {
        "from_kind": "papers",
        "to_kind": "datasets",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "estimates_model": {
        "from_kind": "papers",
        "to_kind": "models",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "tests_mechanism": {
        "from_kind": "papers",
        "to_kind": "mechanisms",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "tests_hypothesis": {
        "from_kind": "papers",
        "to_kind": "hypotheses",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "addresses_endogeneity_with": {
        "from_kind": "papers",
        "to_kind": "identification",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "uses_robustness_check": {
        "from_kind": "papers",
        "to_kind": "robustness",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "uses_heterogeneity_split": {
        "from_kind": "papers",
        "to_kind": "heterogeneity",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "empirical_ingest",
    },
    "reports_table": {
        "from_kind": "papers",
        "to_kind": "tables",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "empirical_ingest",
    },

    # /theory-ingest extraction edges. `assumes` and `proves` are definite
    # structural facts (the paper literally states the assumption / proves the
    # result), so no confidence is required. `formalizes_mechanism` and
    # `predicts` are judgment calls (does this model really formalize that
    # mechanism / does this result really map to that testable hypothesis?),
    # so they require confidence, mirroring the empirical semantic edges.
    "assumes": {
        "from_kind": "papers",
        "to_kind": "assumptions",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "theory_ingest",
    },
    "proves": {
        "from_kind": "papers",
        "to_kind": "propositions",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "theory_ingest",
    },
    "formalizes_mechanism": {
        "from_kind": "papers",
        "to_kind": "mechanisms",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "theory_ingest",
    },
    "predicts": {
        "from_kind": "propositions",
        "to_kind": "hypotheses",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_REQUIRED,
        "workflow": "theory_ingest",
    },

    # Other semantic/provenance workflows. Endpoint constraints stay broad here
    # because older skills use these across claims, ideas, experiments, papers,
    # concepts, outputs, and foundations.
    "supports": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "claim_evidence",
    },
    "contradicts": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "claim_evidence",
    },
    "tested_by": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "experiment",
    },
    "invalidates": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "experiment",
    },
    "addresses_gap": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "idea",
    },
    "derived_from": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "provenance",
    },
    "inspired_by": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "idea",
    },
    # wiki cross-reference derived edges.
    "related_to": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": ANY_ENDPOINT,
        "direction": DIRECTION_SYMMETRIC,
        "confidence": CONFIDENCE_NONE,
        "workflow": "graph",
    },
    "has_contributor": {
        "from_kind": ANY_ENDPOINT,
        "to_kind": "people",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "graph",
    },
    "authored_by": {
        "from_kind": "papers",
        "to_kind": "people",
        "direction": DIRECTION_DIRECTED,
        "confidence": CONFIDENCE_NONE,
        "workflow": "graph",
    },
}

# Accepted only for backwards compatibility; lint reports endpoint-specific
# migration warnings when these appear on old /ingest-shaped endpoints.
LEGACY_EDGE_TYPES = {"extends", "supersedes"}
LEGACY_PAPER_PAPER_EDGE_TYPES = LEGACY_EDGE_TYPES | {"inspired_by", "contradicts", "supports"}
LEGACY_PAPER_CONCEPT_EDGE_TYPES = {"supports", "extends"}


def _spec_matches(spec: dict[str, str], key: str, value: str | None) -> bool:
    return value is None or spec.get(key) == value


def edge_types_matching(*, from_kind: str | None = None,
                        to_kind: str | None = None,
                        direction: str | None = None,
                        confidence: str | None = None,
                        workflow: str | None = None) -> set[str]:
    """Return edge types whose registry metadata matches all provided filters."""
    matches: set[str] = set()
    for edge_type, spec in EDGE_TYPE_SPECS.items():
        if not _spec_matches(spec, "from_kind", from_kind):
            continue
        if not _spec_matches(spec, "to_kind", to_kind):
            continue
        if not _spec_matches(spec, "direction", direction):
            continue
        if not _spec_matches(spec, "confidence", confidence):
            continue
        if not _spec_matches(spec, "workflow", workflow):
            continue
        matches.add(edge_type)
    return matches


def edge_type_spec(edge_type: str) -> dict[str, str] | None:
    """Return registry metadata for a semantic edge type, or None if unknown."""
    return EDGE_TYPE_SPECS.get(edge_type)


def edge_is_symmetric(edge_type: str) -> bool:
    spec = edge_type_spec(edge_type)
    return bool(spec and spec.get("direction") == DIRECTION_SYMMETRIC)


def edge_requires_confidence(edge_type: str) -> bool:
    spec = edge_type_spec(edge_type)
    return bool(spec and spec.get("confidence") == CONFIDENCE_REQUIRED)


def edge_expected_endpoint(edge_type: str, endpoint: str) -> str:
    spec = edge_type_spec(edge_type)
    if not spec:
        return ANY_ENDPOINT
    return spec.get(f"{endpoint}_kind", ANY_ENDPOINT)


def edge_endpoint_matches(edge_type: str, from_kind: str, to_kind: str) -> bool:
    spec = edge_type_spec(edge_type)
    if not spec:
        return True
    expected_from = spec.get("from_kind", ANY_ENDPOINT)
    expected_to = spec.get("to_kind", ANY_ENDPOINT)
    from_ok = expected_from == ANY_ENDPOINT or expected_from == from_kind
    to_ok = expected_to == ANY_ENDPOINT or expected_to == to_kind
    return from_ok and to_ok


def edge_is_legacy_for_endpoint(edge_type: str, from_kind: str,
                                to_kind: str) -> bool:
    """Return True for legacy edge types on endpoint pairs /ingest no longer writes."""
    if from_kind == "papers" and to_kind == "papers":
        return edge_type in LEGACY_PAPER_PAPER_EDGE_TYPES
    if from_kind == "papers" and to_kind == "concepts":
        return edge_type in LEGACY_PAPER_CONCEPT_EDGE_TYPES
    return False


def edge_legacy_replacement_message(edge_type: str, from_kind: str,
                                    to_kind: str) -> str:
    """Human-facing migration hint for legacy edge endpoint pairs."""
    if from_kind == "papers" and to_kind == "papers":
        return f"Legacy paper-paper edge {edge_type!r}; use the new paper relation types"
    if from_kind == "papers" and to_kind == "concepts":
        return (
            f"Legacy paper-concept edge {edge_type!r}; use introduces_concept, "
            "uses_concept, extends_concept, or critiques_concept"
        )
    return f"Legacy edge {edge_type!r}"


# Derived views for existing tool call sites. These are not independent
# categories; each is computed from EDGE_TYPE_SPECS above.
PAPER_PAPER_EDGE_TYPES = edge_types_matching(
    from_kind="papers", to_kind="papers", workflow="ingest"
)
PAPER_CONCEPT_EDGE_TYPES = edge_types_matching(
    from_kind="papers", to_kind="concepts", workflow="ingest"
)
SYMMETRIC_EDGE_TYPES = edge_types_matching(direction=DIRECTION_SYMMETRIC)
CONFIDENCE_REQUIRED_EDGE_TYPES = edge_types_matching(confidence=CONFIDENCE_REQUIRED)
VALID_EDGE_TYPES = set(EDGE_TYPE_SPECS) | LEGACY_EDGE_TYPES

# Required frontmatter fields per entity type (lint.py reports a 🔴 if missing).
# Aligned with docs/runtime-page-templates.zh.md and actual wiki page conventions.
REQUIRED_FIELDS = {
    "papers": ["title", "slug", "tags", "importance", "domain", "year"],
    "variables": ["title", "slug", "type", "domain", "provenance", "measurement", "source_papers"],
    "datasets": ["title", "slug", "provider", "coverage", "unit", "fields"],
    "models": ["title", "slug", "source_papers"],
    "mechanisms": ["title", "slug", "type", "domain", "provenance", "source_papers", "evidence_strength", "empirical_status"],
    "hypotheses": ["title", "slug", "status", "source_papers", "mechanism"],
    "identification": ["title", "slug", "source_paper", "type"],
    "robustness": ["title", "slug", "source_paper", "type"],
    "heterogeneity": ["title", "slug", "source_paper", "type"],
    "tables": ["title", "slug", "table_type", "source_paper", "variables", "interpretation"],
    "assumptions": ["title", "slug", "assumption_type", "source_papers", "formal_statement"],
    "propositions": ["title", "slug", "proposition_type", "source_papers", "formal_statement"],
    "concepts": ["title", "tags", "maturity", "key_papers"],
    "topics": ["title", "tags"],
    "people": ["title", "slug", "research_areas", "key_papers"],
    "Summary": ["title", "scope", "key_topics"],
    "ideas": ["title", "slug", "status", "origin", "tags", "priority"],
    "experiments": ["title", "slug", "status", "target_claim", "hypothesis", "tags"],
    "claims": ["title", "slug", "status", "confidence", "tags", "source_papers", "evidence"],
    "foundations": ["title", "slug", "domain", "status"],
}

# Valid enum values per entity-qualified field. Format: "{entity}.{field}".
VALID_VALUES = {
    "papers.importance": {"1", "2", "3", "4", "5"},
    "papers.paper_kind": {"empirical", "theory", "both"},
    "assumptions.assumption_type": {
        "information", "timing", "payoff", "agent_behavior",
        "technology", "constraint", "other",
    },
    "propositions.proposition_type": {
        "existence", "characterization", "comparative_statics",
        "welfare", "uniqueness", "efficiency", "other",
    },
    "variables.role": {
        "dependent", "core_explanatory", "mediator", "moderator",
        "control", "instrument", "fixed_effect", "sample_filter", "other",
    },
    "hypotheses.status": {"proposed", "literature_supported", "tested", "rejected"},
    "identification.strategy_type": {
        "ols", "fixed_effects", "did", "iv", "psm", "rd", "heckman",
        "event_study", "system_gmm", "text_analysis", "machine_learning", "other",
    },
    "robustness.check_type": {
        "alternative_variable", "alternative_sample", "alternative_model",
        "winsorization", "lagged_variable", "placebo", "psm", "iv",
        "fixed_effects", "cluster_se", "other",
    },
    "concepts.maturity": {"stable", "active", "emerging", "deprecated"},
    "ideas.status": {"proposed", "in_progress", "tested", "validated", "failed"},
    "ideas.priority": {"1", "2", "3", "4", "5"},
    "experiments.status": {"planned", "running", "completed", "abandoned"},
    "experiments.outcome": {"succeeded", "failed", "inconclusive", ""},
    "claims.status": {"proposed", "weakly_supported", "supported", "challenged", "deprecated"},
    "foundations.status": {"mainstream", "historical"},
}

# Safe defaults for `lint --fix`. Only fields where a neutral default is
# reasonable. Note: `importance: "3"` and `confidence: "0.5"` are biased
# defaults for bulk-ingested wikis (3=field-standard, 0.5=coin-flip), but
# fixing that is a separate concern from centralizing the schema — see
# devlog for the discussion. Preserved as-is here.
FIELD_DEFAULTS = {
    "papers": {"tags": "[]", "importance": "3", "domain": "", "year": ""},
    "variables": {"source_papers": "[]", "domain": "", "provenance": "published", "type": "variable", "measurement": ""},
    "datasets": {"fields": "[]"},
    "models": {"source_papers": "[]"},
    "mechanisms": {"source_papers": "[]", "type": "mechanism", "domain": "", "provenance": "published", "evidence_strength": "medium", "empirical_status": "theoretical"},
    "hypotheses": {"status": "proposed", "source_papers": "[]"},
    "identification": {"source_paper": "", "type": "identification"},
    "robustness": {"source_paper": "", "type": "robustness"},
    "heterogeneity": {"source_paper": "", "type": "heterogeneity"},
    "tables": {"variables": "[]"},
    "assumptions": {"assumption_type": "other", "source_papers": "[]"},
    "propositions": {"proposition_type": "other", "source_papers": "[]"},
    "concepts": {"tags": "[]", "maturity": "active", "key_papers": "[]"},
    "topics": {"tags": "[]"},
    "people": {"research_areas": "[]", "key_papers": "[]"},
    "Summary": {"key_topics": "[]"},
    "ideas": {"tags": "[]", "priority": "3"},
    "experiments": {"tags": "[]"},
    "claims": {"tags": "[]", "confidence": "0.5"},
    "foundations": {"status": "mainstream"},
}
