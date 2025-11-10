import re
from typing import TypedDict


class ActionItemExtract(TypedDict, total=False):
    """Structured action item with optional metadata."""

    description: str
    priority: str | None
    assignee: str | None
    category: str | None


def extract_action_items(text: str) -> list[str]:
    """
    Extract action items from text using sophisticated pattern recognition.

    Patterns recognized:
    - Action markers: TODO, FIXME, ACTION, HACK, NOTE, BUG, XXX, OPTIMIZE, REFACTOR
    - Imperative phrases: Need to, Must, Should, Remember to, Don't forget
    - Checkboxes: [ ], [x], - [ ], - [x]
    - Exclamations: Lines ending with !
    - Questions: Lines ending with ?
    - Imperative verbs: Add, Fix, Update, Remove, Create, Delete, etc.
    - Priority markers: [HIGH], [URGENT], [LOW], [P1], [P2], etc.
    - @mentions for assignees

    Args:
        text: Input text to extract action items from

    Returns:
        List of extracted action item descriptions
    """
    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[str] = []

    # Action markers pattern (case-insensitive)
    action_markers = [
        "todo:",
        "fixme:",
        "action:",
        "hack:",
        "note:",
        "bug:",
        "xxx:",
        "optimize:",
        "refactor:",
    ]

    # Imperative phrase patterns
    imperative_phrases = [
        r"^need to\s+",
        r"^must\s+",
        r"^should\s+",
        r"^remember to\s+",
        r"^don'?t forget\s+",
        r"^have to\s+",
        r"^got to\s+",
        r"^make sure\s+",
    ]

    # Checkbox patterns
    checkbox_pattern = r"^\[[ xX]?\]\s+"

    # Priority marker pattern (at start of line)
    priority_marker_pattern = r"^\[(?:HIGH|URGENT|LOW|P[1-5]|CRITICAL)\]\s+"

    # Imperative verb patterns (common action verbs)
    imperative_verbs = [
        r"^add\s+",
        r"^fix\s+",
        r"^update\s+",
        r"^remove\s+",
        r"^delete\s+",
        r"^create\s+",
        r"^implement\s+",
        r"^refactor\s+",
        r"^improve\s+",
        r"^enhance\s+",
        r"^optimize\s+",
        r"^test\s+",
        r"^verify\s+",
        r"^check\s+",
        r"^review\s+",
        r"^investigate\s+",
        r"^research\s+",
        r"^document\s+",
        r"^write\s+",
        r"^clean\s+",
        r"^merge\s+",
        r"^deploy\s+",
        r"^configure\s+",
    ]

    for line in lines:
        normalized = line.lower()
        is_action_item = False

        # Check action markers
        if any(normalized.startswith(marker) for marker in action_markers):
            is_action_item = True

        # Check imperative phrases
        elif any(re.match(pattern, normalized, re.IGNORECASE) for pattern in imperative_phrases):
            is_action_item = True

        # Check checkbox patterns
        elif re.match(checkbox_pattern, line):
            is_action_item = True

        # Check priority markers at start of line
        elif re.match(priority_marker_pattern, line, re.IGNORECASE):
            is_action_item = True

        # Check exclamation marks
        elif line.endswith("!"):
            is_action_item = True

        # Check question marks (potential action items needing resolution)
        elif line.endswith("?") and len(line) > 10:  # Avoid short questions
            is_action_item = True

        # Check imperative verbs (but require reasonable length)
        elif len(line) > 5 and any(
            re.match(pattern, normalized, re.IGNORECASE) for pattern in imperative_verbs
        ):
            is_action_item = True

        if is_action_item:
            # Strip checkbox patterns from the result
            cleaned_line = re.sub(checkbox_pattern, "", line).strip()
            results.append(cleaned_line)

    return results


def extract_action_items_detailed(text: str) -> list[ActionItemExtract]:
    """
    Extract action items with detailed metadata.

    Extracts the same patterns as extract_action_items() but returns structured
    data including priority, assignee, and category information.

    Args:
        text: Input text to extract action items from

    Returns:
        List of ActionItemExtract dictionaries with description and metadata
    """
    basic_items = extract_action_items(text)
    detailed_items: list[ActionItemExtract] = []

    # Priority pattern: [HIGH], [URGENT], [LOW], [P1], [P2], etc.
    priority_pattern = r"\[(?:HIGH|URGENT|LOW|P[1-5]|CRITICAL)\]"

    # Assignee pattern: @username
    assignee_pattern = r"@(\w+)"

    # Category pattern (action marker type)
    category_patterns = {
        "bug": r"^(?:bug|fixme):",
        "todo": r"^todo:",
        "optimization": r"^(?:optimize|refactor):",
        "documentation": r"^(?:note|doc):",
        "technical-debt": r"^(?:hack|xxx):",
    }

    for item in basic_items:
        extract: ActionItemExtract = {"description": item}

        # Extract priority
        priority_match = re.search(priority_pattern, item, re.IGNORECASE)
        if priority_match:
            extract["priority"] = priority_match.group(0).strip("[]").upper()

        # Extract assignee
        assignee_match = re.search(assignee_pattern, item)
        if assignee_match:
            extract["assignee"] = assignee_match.group(1)

        # Determine category
        item_lower = item.lower()
        for category, pattern in category_patterns.items():
            if re.match(pattern, item_lower):
                extract["category"] = category
                break

        detailed_items.append(extract)

    return detailed_items
