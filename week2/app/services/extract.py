from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
try:
    from ollama import chat
except ImportError:  # pragma: no cover - handles environments without Ollama
    chat = None  # type: ignore[assignment]
try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv(*args: Any, **kwargs: Any) -> bool:
        return False

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _remove_prefix(value: str, prefix: str) -> str:
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def _trim_keyword_prefix(value: str) -> str:
    lowered = value.lower()
    for prefix in KEYWORD_PREFIXES:
        if lowered.startswith(prefix):
            return value[len(prefix) :].lstrip()
    return value


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = _remove_prefix(cleaned, "[ ]").strip()
            cleaned = _remove_prefix(cleaned, "[todo]").strip()
            cleaned = _trim_keyword_prefix(cleaned)
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str, *, model: str | None = None) -> List[str]:
    """Use an Ollama-backed LLM to extract action items from free-form text."""
    if not text or not text.strip():
        return []

    model_name = (
        model
        or os.getenv("OLLAMA_ACTION_MODEL")
        or os.getenv("OLLAMA_MODEL")
        or "llama3.1"
    )
    schema: dict[str, Any] = {
        "type": "array",
        "items": {"type": "string"},
    }
    messages = [
        {
            "role": "system",
            "content": (
                "Extract actionable tasks from the user's notes. "
                "Respond strictly as a JSON array of strings with each string "
                "representing one action item."
            ),
        },
        {
            "role": "user",
            "content": text.strip(),
        },
    ]

    if chat is None:
        return extract_action_items(text)

    try:
        response = chat(model=model_name, messages=messages, format=schema)
    except Exception:
        return extract_action_items(text)

    content = response.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return extract_action_items(text)

    if not isinstance(parsed, list):
        return extract_action_items(text)

    cleaned: List[str] = []
    for item in parsed:
        if not isinstance(item, str):
            continue
        stripped_item = item.strip()
        if stripped_item:
            cleaned.append(stripped_item)

    if not cleaned:
        return extract_action_items(text)

    seen: set[str] = set()
    unique: List[str] = []
    for entry in cleaned:
        lowered = entry.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(entry)
    return unique


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
