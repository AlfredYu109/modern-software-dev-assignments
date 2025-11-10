import re
from typing import List, Set

TODO_PREFIXES = ("todo:", "action:", "follow up:", "fixme:", "task:")
MANDATORY_PHRASES = (
    "should ",
    "need to ",
    "remember to ",
    "make sure to ",
    "don't forget to ",
    "lets ",
    "let's ",
    "please ",
    "please, ",
)
CHECKBOX_RE = re.compile(r"^\s*\[[ xX]\]\s*")
BULLET_PREFIX_RE = re.compile(r"^\s*(?:[-*•]\s*|\d+\.\s*)")
ASSIGNMENT_RE = re.compile(r"^@?[a-z0-9_\-]+(?:\s+[a-z0-9_\-]+)*:\s+", re.IGNORECASE)
ACTION_VERBS = {
    "schedule",
    "fix",
    "update",
    "ship",
    "deploy",
    "implement",
    "investigate",
    "prepare",
    "draft",
    "send",
    "document",
    "review",
    "plan",
    "create",
    "write",
    "cleanup",
    "refactor",
    "monitor",
    "follow",
}


def _strip_structural_prefixes(line: str) -> str:
    stripped = BULLET_PREFIX_RE.sub("", line, count=1).strip()
    stripped = CHECKBOX_RE.sub("", stripped, count=1).strip()
    return stripped


def _starts_with_action_verb(text: str) -> bool:
    if not text:
        return False
    candidate = text.lower()
    for phrase in ("please ", "kindly ", "let's ", "lets ", "we need to ", "we should "):
        if candidate.startswith(phrase):
            candidate = candidate[len(phrase) :]
            break
    first_word = candidate.split(" ", 1)[0].strip("():")
    return first_word in ACTION_VERBS


def _contains_mandatory_phrase(text: str) -> bool:
    lower_text = text.lower()
    return any(phrase in lower_text for phrase in MANDATORY_PHRASES)


def extract_action_items(text: str) -> List[str]:
    """Extract likely action items from free-form meeting notes."""
    lines = [line.rstrip() for line in text.splitlines()]
    results: List[str] = []
    seen: Set[str] = set()
    for original in lines:
        candidate = original.strip()
        if not candidate:
            continue
        normalized = candidate.lower()
        de_bulleted = _strip_structural_prefixes(candidate)
        display_value = de_bulleted or candidate
        normalized_de_bulleted = de_bulleted.lower()

        def append_item(value: str) -> None:
            key = value.lower()
            if key not in seen:
                seen.add(key)
                results.append(value)

        if normalized.startswith(TODO_PREFIXES):
            append_item(display_value)
            continue
        if normalized.endswith("!"):
            append_item(display_value)
            continue

        checkbox_candidate = BULLET_PREFIX_RE.sub("", candidate, count=1).lstrip()
        if CHECKBOX_RE.match(checkbox_candidate):
            append_item(display_value)
            continue
        if ASSIGNMENT_RE.match(de_bulleted):
            append_item(display_value)
            continue
        if _contains_mandatory_phrase(de_bulleted):
            append_item(display_value)
            continue
        if _starts_with_action_verb(de_bulleted):
            append_item(display_value)
            continue
        if any(
            keyword in normalized_de_bulleted
            for keyword in (" due ", " by ", " asap", "action item")
        ):
            append_item(display_value)
            continue
    return results
