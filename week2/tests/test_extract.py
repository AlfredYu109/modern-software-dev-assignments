import json
import pytest

from ..app.services import extract as extract_module
from ..app.services.extract import extract_action_items, extract_action_items_llm

def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_extract_action_items_llm_structured_output(monkeypatch):
    captured = {}

    def fake_chat(model, messages, format):
        captured["model"] = model
        captured["messages"] = messages
        captured["format"] = format
        return {
            "message": {
                "role": "assistant",
                "content": json.dumps(
                    ["Set up database", "Implement API extract endpoint"]
                ),
            }
        }

    monkeypatch.setattr(extract_module, "chat", fake_chat)

    text = """
    Notes:
    - Set up database
    - Implement API extract endpoint
    """.strip()

    items = extract_action_items_llm(text, model="test-model")
    assert captured["model"] == "test-model"
    assert items == ["Set up database", "Implement API extract endpoint"]
    assert captured["format"]["type"] == "array"


def test_extract_action_items_llm_empty_input(monkeypatch):
    called = False

    def fake_chat(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("chat should not be called for empty input")

    monkeypatch.setattr(extract_module, "chat", fake_chat)
    assert extract_action_items_llm("   ") == []
    assert called is False


def test_extract_action_items_llm_fallback_to_heuristics(monkeypatch):
    def fake_chat(model, messages, format):
        return {"message": {"role": "assistant", "content": "not json"}}

    monkeypatch.setattr(extract_module, "chat", fake_chat)
    text = """
    todo: Refactor database layer
    Some other note.
    """.strip()

    items = extract_action_items_llm(text)
    assert "Refactor database layer" in items
