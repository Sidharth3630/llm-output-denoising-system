"""Utilities for structured agent outputs.

The CrewAI agents in this project are instructed (via prompts) to return
structured JSON. This module provides helpers to extract/parse that JSON
robustly.
"""

from __future__ import annotations

import json
import re
from typing import Any


_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def extract_json(text: str) -> dict[str, Any]:
    """Extract a JSON object from model output.

    Accepts outputs that are either raw JSON or wrapped in a ```json``` block.

    Raises:
        ValueError: if no JSON object can be found/parsed.
    """
    if not text or not text.strip():
        raise ValueError("Empty model output; cannot extract JSON")

    # 1) Try fenced JSON
    m = _JSON_BLOCK_RE.search(text)
    if m:
        candidate = m.group(1)
        return json.loads(candidate)

    # 2) Try to find first {...} block
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start : end + 1]
        return json.loads(candidate)

    # 3) Last resort: direct parse
    return json.loads(text)

