from backend.app.services.extract import extract_action_items


def test_extracts_varied_action_patterns():
    text = """
    - TODO: update the onboarding docs
    * [ ] Ship the mobile build once QA signs off
    1. Schedule meeting with data team by Friday
    Alice: follow up with the vendor about the outage
    We should capture more metrics before launch.
    Action item: clean up the temp buckets!
    Nothing to do here, just a note.
    Implement caching for list endpoint.
    """

    items = extract_action_items(text)
    assert "TODO: update the onboarding docs" in items
    assert "Ship the mobile build once QA signs off" in items
    assert "Schedule meeting with data team by Friday" in items
    assert "Alice: follow up with the vendor about the outage" in items
    assert "We should capture more metrics before launch." in items
    assert "Action item: clean up the temp buckets!" in items
    assert "Implement caching for list endpoint." in items
    assert "Nothing to do here, just a note." not in items


def test_deduplicates_and_skips_noise():
    text = """
    Please fix the flaky tests.
    please fix the flaky tests.
    The app is stable now.
    """
    items = extract_action_items(text)
    assert items.count("Please fix the flaky tests.") == 1
    assert "The app is stable now." not in items
