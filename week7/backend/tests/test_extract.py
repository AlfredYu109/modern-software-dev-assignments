from backend.app.services.extract import (
    extract_action_items,
    extract_action_items_detailed,
)


class TestBasicExtraction:
    """Test basic action item extraction patterns."""

    def test_original_patterns(self):
        """Test the original TODO:, ACTION:, and ! patterns."""
        text = """
        This is a note
        - TODO: write tests
        - ACTION: review PR
        - Ship it!
        Not actionable
        """.strip()
        items = extract_action_items(text)
        assert "TODO: write tests" in items
        assert "ACTION: review PR" in items
        assert "Ship it!" in items
        assert "Not actionable" not in items

    def test_action_markers(self):
        """Test various action markers (FIXME, BUG, HACK, etc.)."""
        text = """
        FIXME: memory leak in parser
        BUG: off-by-one error
        HACK: temporary workaround
        NOTE: update documentation
        XXX: needs refactoring
        OPTIMIZE: slow query here
        REFACTOR: extract this method
        """.strip()
        items = extract_action_items(text)
        assert len(items) == 7
        assert "FIXME: memory leak in parser" in items
        assert "BUG: off-by-one error" in items
        assert "HACK: temporary workaround" in items

    def test_imperative_phrases(self):
        """Test imperative phrase patterns."""
        text = """
        Need to update dependencies
        Must fix the failing test
        Should refactor this code
        Remember to update changelog
        Don't forget to deploy
        Have to review the PR
        Make sure tests pass
        Regular sentence here
        """.strip()
        items = extract_action_items(text)
        assert "Need to update dependencies" in items
        assert "Must fix the failing test" in items
        assert "Should refactor this code" in items
        assert "Remember to update changelog" in items
        assert "Don't forget to deploy" in items
        assert "Have to review the PR" in items
        assert "Make sure tests pass" in items
        assert "Regular sentence here" not in items

    def test_checkbox_patterns(self):
        """Test checkbox patterns."""
        text = """
        [ ] Unchecked task
        [x] Completed task
        [X] Another completed task
        [] Empty checkbox
        Regular text
        """.strip()
        items = extract_action_items(text)
        assert "Unchecked task" in items
        assert "Completed task" in items
        assert "Another completed task" in items
        assert "Empty checkbox" in items
        assert "Regular text" not in items

    def test_exclamation_marks(self):
        """Test lines ending with exclamation marks."""
        text = """
        Deploy this now!
        Critical bug fix needed!
        Regular sentence.
        Another normal line
        """.strip()
        items = extract_action_items(text)
        assert "Deploy this now!" in items
        assert "Critical bug fix needed!" in items
        assert "Regular sentence." not in items

    def test_question_marks(self):
        """Test lines ending with question marks."""
        text = """
        Should we refactor this module?
        What about the edge cases?
        Why?
        Is this the right approach?
        """.strip()
        items = extract_action_items(text)
        # Long questions should be included
        assert "Should we refactor this module?" in items
        assert "What about the edge cases?" in items
        assert "Is this the right approach?" in items
        # Short questions (<=10 chars) should be excluded
        assert "Why?" not in items

    def test_imperative_verbs(self):
        """Test imperative verb patterns."""
        text = """
        Add error handling
        Fix the bug
        Update documentation
        Remove deprecated code
        Create new endpoint
        Implement feature X
        Test edge cases
        Review pull request
        Investigate performance issue
        This is not an action
        """.strip()
        items = extract_action_items(text)
        assert "Add error handling" in items
        assert "Fix the bug" in items
        assert "Update documentation" in items
        assert "Remove deprecated code" in items
        assert "Create new endpoint" in items
        # Patterns too short should be excluded
        assert "This is not an action" not in items


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_text(self):
        """Test extraction from empty text."""
        assert extract_action_items("") == []
        assert extract_action_items("   ") == []
        assert extract_action_items("\n\n\n") == []

    def test_no_action_items(self):
        """Test text with no recognizable action items."""
        text = """
        This is just a regular note.
        It contains some information.
        But no action items.
        """.strip()
        items = extract_action_items(text)
        assert len(items) == 0

    def test_mixed_patterns(self):
        """Test text with multiple different patterns."""
        text = """
        TODO: fix bug
        Need to refactor this
        [ ] Write tests
        Deploy immediately!
        Should we add logging?
        Update the README
        Regular text here
        """.strip()
        items = extract_action_items(text)
        assert len(items) == 6
        assert "TODO: fix bug" in items
        assert "Need to refactor this" in items
        assert "Write tests" in items
        assert "Deploy immediately!" in items
        assert "Should we add logging?" in items
        assert "Update the README" in items
        assert "Regular text here" not in items

    def test_case_insensitivity(self):
        """Test that patterns are case-insensitive."""
        text = """
        todo: lowercase marker
        TODO: uppercase marker
        ToDo: mixed case marker
        need to do something
        NEED TO DO SOMETHING
        add a feature
        ADD A FEATURE
        """.strip()
        items = extract_action_items(text)
        assert len(items) == 7

    def test_bullet_stripping(self):
        """Test that bullet points and dashes are stripped."""
        text = """
        - TODO: with dash
        - Need to do this
        - [ ] checkbox item
        """.strip()
        items = extract_action_items(text)
        # Dashes should be stripped
        assert "TODO: with dash" in items
        assert "Need to do this" in items


class TestDetailedExtraction:
    """Test detailed extraction with metadata."""

    def test_priority_extraction(self):
        """Test priority marker extraction."""
        text = """
        TODO: [HIGH] critical bug fix
        Need to [URGENT] deploy hotfix
        Should [LOW] refactor later
        Fix [P1] authentication issue
        Update [P2] documentation
        """.strip()
        items = extract_action_items_detailed(text)
        assert len(items) == 5

        high_item = next(i for i in items if "critical bug fix" in i["description"])
        assert high_item["priority"] == "HIGH"

        urgent_item = next(i for i in items if "deploy hotfix" in i["description"])
        assert urgent_item["priority"] == "URGENT"

        low_item = next(i for i in items if "refactor later" in i["description"])
        assert low_item["priority"] == "LOW"

        p1_item = next(i for i in items if "authentication issue" in i["description"])
        assert p1_item["priority"] == "P1"

    def test_assignee_extraction(self):
        """Test @mention assignee extraction."""
        text = """
        TODO: @alice fix the bug
        Need to @bob review this PR
        @charlie deploy to production!
        Fix issue without assignee
        """.strip()
        items = extract_action_items_detailed(text)

        alice_item = next(i for i in items if "@alice" in i["description"])
        assert alice_item["assignee"] == "alice"

        bob_item = next(i for i in items if "@bob" in i["description"])
        assert bob_item["assignee"] == "bob"

        charlie_item = next(i for i in items if "@charlie" in i["description"])
        assert charlie_item["assignee"] == "charlie"

        no_assignee = next(i for i in items if "without assignee" in i["description"])
        assert "assignee" not in no_assignee or no_assignee.get("assignee") is None

    def test_category_extraction(self):
        """Test category extraction based on markers."""
        text = """
        BUG: null pointer exception
        TODO: implement feature
        OPTIMIZE: slow database query
        HACK: temporary solution
        NOTE: update API docs
        FIXME: broken link
        """.strip()
        items = extract_action_items_detailed(text)

        bug_item = next(i for i in items if "null pointer" in i["description"])
        assert bug_item["category"] == "bug"

        todo_item = next(i for i in items if "implement feature" in i["description"])
        assert todo_item["category"] == "todo"

        opt_item = next(i for i in items if "database query" in i["description"])
        assert opt_item["category"] == "optimization"

        hack_item = next(i for i in items if "temporary solution" in i["description"])
        assert hack_item["category"] == "technical-debt"

        doc_item = next(i for i in items if "API docs" in i["description"])
        assert doc_item["category"] == "documentation"

    def test_combined_metadata(self):
        """Test extraction with multiple metadata fields."""
        text = """
        TODO: [HIGH] @alice fix critical bug
        BUG: [URGENT] @bob memory leak in parser
        Need to [P1] deploy hotfix
        """.strip()
        items = extract_action_items_detailed(text)

        alice_item = next(i for i in items if "@alice" in i["description"])
        assert alice_item["priority"] == "HIGH"
        assert alice_item["assignee"] == "alice"
        assert alice_item["category"] == "todo"

        bob_item = next(i for i in items if "@bob" in i["description"])
        assert bob_item["priority"] == "URGENT"
        assert bob_item["assignee"] == "bob"
        assert bob_item["category"] == "bug"

    def test_no_metadata(self):
        """Test items without any metadata."""
        text = """
        Deploy this now!
        Update the docs
        """.strip()
        items = extract_action_items_detailed(text)
        assert len(items) == 2

        for item in items:
            assert "description" in item
            # Metadata fields might not be present or might be None
            assert item.get("priority") is None or "priority" not in item
            assert item.get("assignee") is None or "assignee" not in item


class TestRealWorldScenarios:
    """Test realistic note content scenarios."""

    def test_meeting_notes(self):
        """Test extraction from meeting notes."""
        text = """
        Meeting Notes - 2025-01-15

        Attendees: Alice, Bob, Charlie

        Discussion points:
        - Reviewed Q4 metrics
        - Discussed new feature roadmap

        Action Items:
        - TODO: @alice finalize design document by Friday
        - Need to @bob set up staging environment
        - [ ] Schedule follow-up meeting
        - Review the analytics dashboard!

        Next meeting: Next Tuesday
        """.strip()
        items = extract_action_items(text)
        # Should extract the action items, not discussion points
        assert "TODO: @alice finalize design document by Friday" in items
        assert "Need to @bob set up staging environment" in items
        assert "Schedule follow-up meeting" in items
        assert "Review the analytics dashboard!" in items

    def test_code_review_comments(self):
        """Test extraction from code review comments."""
        text = """
        Code Review - PR #123

        Overall looks good, but a few issues:

        FIXME: memory leak in line 45
        BUG: off-by-one error in loop
        Should add error handling here
        Consider using a more efficient algorithm?
        Update the unit tests

        Approved with changes
        """.strip()
        items = extract_action_items(text)
        assert "FIXME: memory leak in line 45" in items
        assert "BUG: off-by-one error in loop" in items
        assert "Should add error handling here" in items
        assert "Consider using a more efficient algorithm?" in items
        assert "Update the unit tests" in items

    def test_project_planning(self):
        """Test extraction from project planning notes."""
        text = """
        Sprint Planning - Week 7

        Goals:
        - [HIGH] Complete authentication module
        - [P1] Fix critical bugs

        Tasks:
        [ ] Implement JWT authentication
        [ ] Add rate limiting
        [x] Set up CI/CD pipeline

        Remember to update the documentation!
        Don't forget to notify stakeholders
        """.strip()
        items = extract_action_items(text)
        # Should extract tasks and reminders
        assert any("[HIGH]" in item for item in items)
        assert "Implement JWT authentication" in items
        assert "Add rate limiting" in items
        assert "Remember to update the documentation!" in items
        assert "Don't forget to notify stakeholders" in items
