from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Annotated

from pydantic import Field

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
EXERCISE_FILES = REPOSITORY_ROOT / "exercises/02-build-service-operations-agent/files"
HANDBOOK_PATH = EXERCISE_FILES / "service-handbook.md"
METRICS_PATH = EXERCISE_FILES / "service-metrics.csv"
WORD_PATTERN = re.compile(r"[A-Za-z0-9ก-๙]+")
STOP_WORDS = {
    "about",
    "and",
    "for",
    "from",
    "how",
    "the",
    "what",
    "when",
    "where",
    "with",
    "การ",
    "คือ",
    "ที่",
    "หรือ",
}


def _terms(text: str) -> set[str]:
    return {
        token.lower()
        for token in WORD_PATTERN.findall(text)
        if len(token) > 2 and token.lower() not in STOP_WORDS
    }


def _handbook_sections(path: Path = HANDBOOK_PATH) -> list[str]:
    text = path.read_text(encoding="utf-8")
    sections = re.split(r"(?=^## )", text, flags=re.MULTILINE)
    return [section.strip() for section in sections if section.strip()]


def search_service_handbook(
    query: Annotated[
        str,
        Field(description="Question or keywords to find in the service handbook"),
    ],
) -> str:
    """Return the most relevant synthetic Fabrikam service-handbook section."""
    query_terms = _terms(query)
    sections = _handbook_sections()
    ranked = sorted(
        (
            (len(query_terms & _terms(section)), index, section)
            for index, section in enumerate(sections)
        ),
        key=lambda item: (-item[0], item[1]),
    )
    if not ranked or ranked[0][0] == 0:
        return "No matching handbook section was found. Ask for a policy topic or priority level."
    return ranked[0][2]


def list_service_metrics() -> str:
    """Return all synthetic service metrics and their targets as JSON."""
    with METRICS_PATH.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    return json.dumps(rows, ensure_ascii=False, indent=2)
