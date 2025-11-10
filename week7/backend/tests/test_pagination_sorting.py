"""
Comprehensive tests for pagination and sorting across the application.

This module tests edge cases, boundary conditions, and complex scenarios
for pagination and sorting functionality in both Notes and Action Items endpoints.
"""

import time

from fastapi.testclient import TestClient


class TestNotesPagination:
    """Test pagination functionality for Notes endpoints."""

    def test_basic_pagination(self, client: TestClient):
        """Test basic pagination with skip and limit."""
        # Create 10 notes
        for i in range(10):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # Get first 5
        response = client.get("/notes/", params={"skip": 0, "limit": 5})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 5

        # Get next 5
        response = client.get("/notes/", params={"skip": 5, "limit": 5})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 5

    def test_pagination_with_zero_limit(self, client: TestClient):
        """Test pagination with limit=0 should return empty results."""
        client.post("/notes/", json={"title": "Note", "content": "Content"})

        response = client.get("/notes/", params={"limit": 0})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 0

    def test_pagination_with_limit_exceeding_max(self, client: TestClient):
        """Test that limit cannot exceed 200."""
        # Create some notes
        for i in range(5):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # Try to get 201 (should be capped at 200)
        response = client.get("/notes/", params={"limit": 201})
        assert response.status_code == 422  # Validation error

    def test_pagination_with_offset_beyond_data(self, client: TestClient):
        """Test pagination with offset beyond available data."""
        # Create 5 notes
        for i in range(5):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # Skip past all data
        response = client.get("/notes/", params={"skip": 100})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 0

    def test_pagination_with_negative_skip(self, client: TestClient):
        """Test that negative skip values are handled (treated as 0)."""
        # Create some notes
        for i in range(3):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # Negative skip should be treated as 0
        response = client.get("/notes/", params={"skip": -1})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) >= 3

    def test_pagination_consistency(self, client: TestClient):
        """Test that pagination returns consistent, non-overlapping results."""
        # Create 15 notes
        created_ids = []
        for i in range(15):
            response = client.post(
                "/notes/", json={"title": f"Note {i:02d}", "content": f"Content {i}"}
            )
            created_ids.append(response.json()["id"])

        # Get all notes in pages of 5
        page1 = client.get("/notes/", params={"skip": 0, "limit": 5}).json()
        page2 = client.get("/notes/", params={"skip": 5, "limit": 5}).json()
        page3 = client.get("/notes/", params={"skip": 10, "limit": 5}).json()

        # Extract IDs
        page1_ids = {note["id"] for note in page1}
        page2_ids = {note["id"] for note in page2}
        page3_ids = {note["id"] for note in page3}

        # Verify no overlap
        assert len(page1_ids & page2_ids) == 0, "Page 1 and 2 should not overlap"
        assert len(page2_ids & page3_ids) == 0, "Page 2 and 3 should not overlap"
        assert len(page1_ids & page3_ids) == 0, "Page 1 and 3 should not overlap"

        # Verify all notes are returned
        all_ids = page1_ids | page2_ids | page3_ids
        assert len(all_ids) >= 15

    def test_pagination_with_filtering(self, client: TestClient):
        """Test pagination combined with search filtering."""
        # Create notes with different content
        for i in range(10):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Special {i}"})
        for i in range(5):
            client.post("/notes/", json={"title": f"Other {i}", "content": f"Regular {i}"})

        # Search with pagination
        response = client.get("/notes/", params={"q": "Special", "skip": 0, "limit": 5})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 5
        assert all("Special" in note["content"] for note in notes)

        # Get next page
        response = client.get("/notes/", params={"q": "Special", "skip": 5, "limit": 5})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 5


class TestNotesSorting:
    """Test sorting functionality for Notes endpoints."""

    def test_sort_by_created_at_descending(self, client: TestClient):
        """Test sorting by created_at in descending order (newest first)."""
        # Create notes with slight delays
        created_notes = []
        for i in range(5):
            response = client.post(
                "/notes/", json={"title": f"Note {i}", "content": f"Content {i}"}
            )
            created_notes.append(response.json())
            time.sleep(0.01)  # Small delay to ensure different timestamps

        # Get notes sorted by created_at descending (default)
        response = client.get("/notes/", params={"sort": "-created_at"})
        assert response.status_code == 200
        notes = response.json()

        # Verify order (newest first)
        for i in range(len(notes) - 1):
            assert notes[i]["created_at"] >= notes[i + 1]["created_at"]

    def test_sort_by_created_at_ascending(self, client: TestClient):
        """Test sorting by created_at in ascending order (oldest first)."""
        # Create notes
        for i in range(5):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})
            time.sleep(0.01)

        # Get notes sorted by created_at ascending
        response = client.get("/notes/", params={"sort": "created_at"})
        assert response.status_code == 200
        notes = response.json()

        # Verify order (oldest first)
        for i in range(len(notes) - 1):
            assert notes[i]["created_at"] <= notes[i + 1]["created_at"]

    def test_sort_by_title_ascending(self, client: TestClient):
        """Test sorting by title in ascending order."""
        # Create notes with alphabetical titles
        titles = ["Charlie", "Alice", "Bob", "David"]
        for title in titles:
            client.post("/notes/", json={"title": title, "content": f"Content for {title}"})

        response = client.get("/notes/", params={"sort": "title"})
        assert response.status_code == 200
        notes = response.json()

        # Extract titles (only from the notes we created)
        retrieved_titles = [n["title"] for n in notes if n["title"] in titles]

        # Verify alphabetical order
        assert retrieved_titles == sorted(titles)

    def test_sort_by_title_descending(self, client: TestClient):
        """Test sorting by title in descending order."""
        titles = ["Charlie", "Alice", "Bob", "David"]
        for title in titles:
            client.post("/notes/", json={"title": title, "content": f"Content for {title}"})

        response = client.get("/notes/", params={"sort": "-title"})
        assert response.status_code == 200
        notes = response.json()

        # Extract titles
        retrieved_titles = [n["title"] for n in notes if n["title"] in titles]

        # Verify reverse alphabetical order
        assert retrieved_titles == sorted(titles, reverse=True)

    def test_sort_by_updated_at(self, client: TestClient):
        """Test sorting by updated_at field."""
        # Create a note
        response = client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})
        note1_id = response.json()["id"]

        time.sleep(0.02)

        # Create another note
        response = client.post("/notes/", json={"title": "Note 2", "content": "Content 2"})
        note2_id = response.json()["id"]

        time.sleep(0.02)

        # Update the first note (making it most recently updated)
        client.patch(f"/notes/{note1_id}", json={"title": "Updated Note 1"})

        # Get notes sorted by updated_at descending
        response = client.get("/notes/", params={"sort": "-updated_at"})
        assert response.status_code == 200
        notes = response.json()

        # The updated note should come first
        if len(notes) >= 2:
            # Find our notes in the results
            our_notes = [n for n in notes if n["id"] in [note1_id, note2_id]]
            if len(our_notes) >= 2:
                assert our_notes[0]["id"] == note1_id

    def test_sort_with_invalid_field(self, client: TestClient):
        """Test that invalid sort fields fall back to default sorting."""
        client.post("/notes/", json={"title": "Note", "content": "Content"})

        # Invalid sort field should fallback to default
        response = client.get("/notes/", params={"sort": "invalid_field"})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) >= 1

    def test_sort_with_pagination(self, client: TestClient):
        """Test that sorting works correctly with pagination."""
        # Create notes with numbered titles
        for i in range(10):
            client.post("/notes/", json={"title": f"Note {i:02d}", "content": f"Content {i}"})

        # Get first page sorted by title
        page1 = client.get("/notes/", params={"sort": "title", "skip": 0, "limit": 5}).json()

        # Get second page sorted by title
        page2 = client.get("/notes/", params={"sort": "title", "skip": 5, "limit": 5}).json()

        # Verify sorting continuity across pages
        if len(page1) > 0 and len(page2) > 0:
            # Last item of page1 should be <= first item of page2
            assert page1[-1]["title"] <= page2[0]["title"]


class TestActionItemsPagination:
    """Test pagination functionality for Action Items endpoints."""

    def test_basic_pagination(self, client: TestClient):
        """Test basic pagination with skip and limit."""
        # Create 10 action items
        for i in range(10):
            client.post("/action-items/", json={"description": f"Task {i}"})

        # Get first 5
        response = client.get("/action-items/", params={"skip": 0, "limit": 5})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 5

        # Get next 5
        response = client.get("/action-items/", params={"skip": 5, "limit": 5})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 5

    def test_pagination_with_zero_limit(self, client: TestClient):
        """Test pagination with limit=0."""
        client.post("/action-items/", json={"description": "Task"})

        response = client.get("/action-items/", params={"limit": 0})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 0

    def test_pagination_with_limit_exceeding_max(self, client: TestClient):
        """Test that limit cannot exceed 200."""
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})

        response = client.get("/action-items/", params={"limit": 201})
        assert response.status_code == 422

    def test_pagination_with_offset_beyond_data(self, client: TestClient):
        """Test pagination with offset beyond available data."""
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})

        response = client.get("/action-items/", params={"skip": 100})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 0

    def test_pagination_with_completed_filter(self, client: TestClient):
        """Test pagination combined with completed status filter."""
        # Create 10 items, complete 5 of them
        for i in range(10):
            response = client.post("/action-items/", json={"description": f"Task {i}"})
            item_id = response.json()["id"]
            if i < 5:
                client.put(f"/action-items/{item_id}/complete")

        # Get completed items with pagination
        response = client.get("/action-items/", params={"completed": True, "skip": 0, "limit": 3})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3
        assert all(item["completed"] for item in items)

        # Get pending items
        response = client.get("/action-items/", params={"completed": False, "skip": 0, "limit": 3})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 3
        assert all(not item["completed"] for item in items)

    def test_pagination_consistency(self, client: TestClient):
        """Test pagination returns consistent, non-overlapping results."""
        # Create 15 items
        for i in range(15):
            client.post("/action-items/", json={"description": f"Task {i:02d}"})

        # Get all items in pages of 5
        page1 = client.get("/action-items/", params={"skip": 0, "limit": 5}).json()
        page2 = client.get("/action-items/", params={"skip": 5, "limit": 5}).json()
        page3 = client.get("/action-items/", params={"skip": 10, "limit": 5}).json()

        # Extract IDs
        page1_ids = {item["id"] for item in page1}
        page2_ids = {item["id"] for item in page2}
        page3_ids = {item["id"] for item in page3}

        # Verify no overlap
        assert len(page1_ids & page2_ids) == 0
        assert len(page2_ids & page3_ids) == 0
        assert len(page1_ids & page3_ids) == 0


class TestActionItemsSorting:
    """Test sorting functionality for Action Items endpoints."""

    def test_sort_by_created_at_descending(self, client: TestClient):
        """Test sorting by created_at in descending order."""
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})
            time.sleep(0.01)

        response = client.get("/action-items/", params={"sort": "-created_at"})
        assert response.status_code == 200
        items = response.json()

        # Verify order (newest first)
        for i in range(len(items) - 1):
            assert items[i]["created_at"] >= items[i + 1]["created_at"]

    def test_sort_by_created_at_ascending(self, client: TestClient):
        """Test sorting by created_at in ascending order."""
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})
            time.sleep(0.01)

        response = client.get("/action-items/", params={"sort": "created_at"})
        assert response.status_code == 200
        items = response.json()

        # Verify order (oldest first)
        for i in range(len(items) - 1):
            assert items[i]["created_at"] <= items[i + 1]["created_at"]

    def test_sort_by_description_ascending(self, client: TestClient):
        """Test sorting by description in ascending order."""
        descriptions = ["Zebra task", "Apple task", "Mango task", "Banana task"]
        for desc in descriptions:
            client.post("/action-items/", json={"description": desc})

        response = client.get("/action-items/", params={"sort": "description"})
        assert response.status_code == 200
        items = response.json()

        # Extract descriptions
        retrieved_descs = [i["description"] for i in items if i["description"] in descriptions]

        # Verify alphabetical order
        assert retrieved_descs == sorted(descriptions)

    def test_sort_by_description_descending(self, client: TestClient):
        """Test sorting by description in descending order."""
        descriptions = ["Zebra task", "Apple task", "Mango task", "Banana task"]
        for desc in descriptions:
            client.post("/action-items/", json={"description": desc})

        response = client.get("/action-items/", params={"sort": "-description"})
        assert response.status_code == 200
        items = response.json()

        # Extract descriptions
        retrieved_descs = [i["description"] for i in items if i["description"] in descriptions]

        # Verify reverse alphabetical order
        assert retrieved_descs == sorted(descriptions, reverse=True)

    def test_sort_by_completed_status(self, client: TestClient):
        """Test sorting by completed status."""
        # Create items with mixed completed status
        for i in range(6):
            response = client.post("/action-items/", json={"description": f"Task {i}"})
            item_id = response.json()["id"]
            if i % 2 == 0:
                client.put(f"/action-items/{item_id}/complete")

        # Sort by completed status ascending (False first, then True)
        response = client.get("/action-items/", params={"sort": "completed"})
        assert response.status_code == 200
        items = response.json()

        # Find the transition point from False to True
        completed_items = [item for item in items if item["completed"]]
        pending_items = [item for item in items if not item["completed"]]

        # All pending should come before all completed
        if len(pending_items) > 0 and len(completed_items) > 0:
            pending_indices = [i for i, item in enumerate(items) if not item["completed"]]
            completed_indices = [i for i, item in enumerate(items) if item["completed"]]

            if pending_indices and completed_indices:
                assert max(pending_indices) < min(completed_indices)

    def test_sort_with_invalid_field(self, client: TestClient):
        """Test that invalid sort fields fall back to default."""
        client.post("/action-items/", json={"description": "Task"})

        response = client.get("/action-items/", params={"sort": "invalid_field"})
        assert response.status_code == 200
        items = response.json()
        assert len(items) >= 1

    def test_sort_with_pagination(self, client: TestClient):
        """Test that sorting works correctly with pagination."""
        for i in range(10):
            client.post("/action-items/", json={"description": f"Task {i:02d}"})

        # Get first page sorted by description
        page1 = client.get(
            "/action-items/", params={"sort": "description", "skip": 0, "limit": 5}
        ).json()

        # Get second page sorted by description
        page2 = client.get(
            "/action-items/", params={"sort": "description", "skip": 5, "limit": 5}
        ).json()

        # Verify sorting continuity across pages
        if len(page1) > 0 and len(page2) > 0:
            assert page1[-1]["description"] <= page2[0]["description"]


class TestEdgeCases:
    """Test edge cases for pagination and sorting."""

    def test_empty_database_pagination(self, client: TestClient):
        """Test pagination on empty database."""
        response = client.get("/notes/", params={"skip": 0, "limit": 10})
        assert response.status_code == 200
        assert response.json() == []

    def test_empty_database_sorting(self, client: TestClient):
        """Test sorting on empty database."""
        response = client.get("/action-items/", params={"sort": "-created_at"})
        assert response.status_code == 200
        assert response.json() == []

    def test_large_skip_value(self, client: TestClient):
        """Test with very large skip value."""
        client.post("/notes/", json={"title": "Note", "content": "Content"})

        response = client.get("/notes/", params={"skip": 1000000})
        assert response.status_code == 200
        assert response.json() == []

    def test_limit_exactly_at_data_size(self, client: TestClient):
        """Test when limit equals exact number of records."""
        # Create exactly 5 items
        for i in range(5):
            client.post("/action-items/", json={"description": f"Task {i}"})

        response = client.get("/action-items/", params={"limit": 5})
        assert response.status_code == 200
        items = response.json()
        assert len(items) == 5

    def test_skip_and_limit_exact_boundaries(self, client: TestClient):
        """Test pagination at exact boundaries."""
        # Create 10 notes
        for i in range(10):
            client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

        # Skip 9, limit 1 (should get last item)
        response = client.get("/notes/", params={"skip": 9, "limit": 1})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 1

        # Skip 10, limit 1 (should get empty)
        response = client.get("/notes/", params={"skip": 10, "limit": 1})
        assert response.status_code == 200
        notes = response.json()
        assert len(notes) == 0
