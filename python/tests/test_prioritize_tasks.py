"""
Comprehensive test suite for prioritize_tasks function.
"""

import pytest
from datetime import datetime
from src.prioritize_tasks import (
    prioritize_tasks,
    CircularDependencyError,
    InvalidDependencyError,
    InvalidPriorityError,
)


class TestBasicFunctionality:
    """Tests for basic functionality."""

    def test_empty_input(self):
        """Should return empty list for empty input."""
        result = prioritize_tasks([])
        assert result == []

    def test_single_task(self):
        """Should return single task as-is."""
        task = {
            "id": "1",
            "name": "Single task",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task])
        assert result == [task]

    def test_simple_dependencies(self):
        """Should order tasks with simple dependencies."""
        task1 = {
            "id": "1",
            "name": "Setup project",
            "deadline": "2024-01-20",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Implement feature",
            "deadline": "2024-01-15",
            "priority": 5,
            "dependencies": ["1"],
            "estimated_hours": 8,
        }
        result = prioritize_tasks([task2, task1])
        assert result == [task1, task2]
        assert result[0]["id"] == "1"
        assert result[1]["id"] == "2"

    def test_no_dependencies(self):
        """Should handle tasks with no dependencies."""
        task1 = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Task 2",
            "deadline": "2024-01-20",
            "priority": 4,
            "dependencies": [],
            "estimated_hours": 4,
        }
        result = prioritize_tasks([task1, task2])
        # Both have no dependencies, so should be sorted by priority
        assert result[0]["id"] == "2"  # Higher priority first
        assert result[1]["id"] == "1"


class TestPrioritySorting:
    """Tests for priority-based sorting."""

    def test_priority_when_dependencies_satisfied(self):
        """Should prioritize tasks by priority when dependencies are satisfied."""
        task1 = {
            "id": "1",
            "name": "Low priority",
            "deadline": "2024-01-15",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "High priority",
            "deadline": "2024-01-15",
            "priority": 5,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task3 = {
            "id": "3",
            "name": "Medium priority",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task1, task2, task3])
        assert [t["id"] for t in result] == ["2", "3", "1"]

    def test_priority_after_dependencies_resolved(self):
        """Should prioritize by priority after dependencies are resolved."""
        task1 = {
            "id": "1",
            "name": "Dependency",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "High priority dependent",
            "deadline": "2024-01-20",
            "priority": 5,
            "dependencies": ["1"],
            "estimated_hours": 4,
        }
        task3 = {
            "id": "3",
            "name": "Low priority dependent",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": ["1"],
            "estimated_hours": 4,
        }
        result = prioritize_tasks([task3, task2, task1])
        assert [t["id"] for t in result] == ["1", "2", "3"]


class TestDeadlineUrgency:
    """Tests for deadline-based sorting."""

    def test_earlier_deadline_when_priorities_equal(self):
        """Should prioritize earlier deadlines when priorities are equal."""
        task1 = {
            "id": "1",
            "name": "Later deadline",
            "deadline": "2024-01-20",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Earlier deadline",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task1, task2])
        assert result[0]["id"] == "2"
        assert result[1]["id"] == "1"

    def test_deadline_as_tiebreaker_after_priority(self):
        """Should use deadline as tiebreaker after priority."""
        task1 = {
            "id": "1",
            "name": "High priority, later deadline",
            "deadline": "2024-01-20",
            "priority": 5,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "High priority, earlier deadline",
            "deadline": "2024-01-15",
            "priority": 5,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task3 = {
            "id": "3",
            "name": "Low priority",
            "deadline": "2024-01-10",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task1, task2, task3])
        # Priority 5 tasks first, then sorted by deadline
        assert result[0]["id"] == "2"  # Priority 5, earlier deadline
        assert result[1]["id"] == "1"  # Priority 5, later deadline
        assert result[2]["id"] == "3"  # Priority 2

    def test_datetime_objects_as_deadlines(self):
        """Should handle datetime objects as deadlines."""
        task1 = {
            "id": "1",
            "name": "Later deadline",
            "deadline": datetime(2024, 1, 20),
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Earlier deadline",
            "deadline": datetime(2024, 1, 15),
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task1, task2])
        assert result[0]["id"] == "2"
        assert result[1]["id"] == "1"


class TestComplexDependencies:
    """Tests for complex dependency scenarios."""

    def test_multi_level_dependencies(self):
        """Should handle multi-level dependencies."""
        task1 = {
            "id": "1",
            "name": "Level 1",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Level 2",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": ["1"],
            "estimated_hours": 2,
        }
        task3 = {
            "id": "3",
            "name": "Level 3",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": ["2"],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task3, task1, task2])
        assert [t["id"] for t in result] == ["1", "2", "3"]

    def test_branching_dependencies(self):
        """Should handle branching dependencies."""
        task1 = {
            "id": "1",
            "name": "Root",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Branch A",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": ["1"],
            "estimated_hours": 2,
        }
        task3 = {
            "id": "3",
            "name": "Branch B",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": ["1"],
            "estimated_hours": 2,
        }
        task4 = {
            "id": "4",
            "name": "Merge",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": ["2", "3"],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task4, task3, task1, task2])
        assert result[0]["id"] == "1"  # Root first
        # Tasks 2 and 3 can be in any order (both depend on 1)
        assert sorted([t["id"] for t in result[1:3]]) == ["2", "3"]
        assert result[3]["id"] == "4"  # Merge last

    def test_multiple_dependencies(self):
        """Should handle tasks with multiple dependencies."""
        task1 = {
            "id": "1",
            "name": "Dependency 1",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Dependency 2",
            "deadline": "2024-01-20",
            "priority": 2,
            "dependencies": [],
            "estimated_hours": 2,
        }
        task3 = {
            "id": "3",
            "name": "Requires both",
            "deadline": "2024-01-20",
            "priority": 5,
            "dependencies": ["1", "2"],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task3, task1, task2])
        assert result[0]["id"] == "1"  # Or 2, order doesn't matter
        assert result[1]["id"] == "2"  # Or 1, order doesn't matter
        assert result[2]["id"] == "3"  # Must be last


class TestEstimatedHours:
    """Tests for estimated hours as tiebreaker."""

    def test_estimated_hours_as_tiebreaker(self):
        """Should use estimated hours as final tiebreaker."""
        task1 = {
            "id": "1",
            "name": "Long task",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 8,
        }
        task2 = {
            "id": "2",
            "name": "Short task",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task1, task2])
        # Same priority and deadline, so shorter task first
        assert result[0]["id"] == "2"
        assert result[1]["id"] == "1"


class TestIntegration:
    """Integration tests for complex scenarios."""

    def test_complex_real_world_scenario(self):
        """Should handle complex real-world scenario."""
        tasks = [
            {
                "id": "1",
                "name": "Setup project",
                "deadline": "2024-01-25",
                "priority": 5,
                "dependencies": [],
                "estimated_hours": 2,
            },
            {
                "id": "2",
                "name": "Write tests",
                "deadline": "2024-01-20",
                "priority": 4,
                "dependencies": ["1"],
                "estimated_hours": 4,
            },
            {
                "id": "3",
                "name": "Implement feature",
                "deadline": "2024-01-22",
                "priority": 5,
                "dependencies": ["1"],
                "estimated_hours": 8,
            },
            {
                "id": "4",
                "name": "Code review",
                "deadline": "2024-01-18",
                "priority": 3,
                "dependencies": ["2", "3"],
                "estimated_hours": 2,
            },
            {
                "id": "5",
                "name": "Documentation",
                "deadline": "2024-01-30",
                "priority": 2,
                "dependencies": ["4"],
                "estimated_hours": 3,
            },
        ]
        result = prioritize_tasks(tasks)

        # Task 1 must be first (no dependencies, highest priority)
        assert result[0]["id"] == "1"

        # Tasks 2 and 3 depend on 1
        # Task 3 has higher priority (5 vs 4), so should come before 2
        assert result[1]["id"] == "3"
        assert result[2]["id"] == "2"

        # Task 4 depends on both 2 and 3
        assert result[3]["id"] == "4"

        # Task 5 depends on 4
        assert result[4]["id"] == "5"


class TestEdgeCasesErrors:
    """Tests for error handling and edge cases."""

    def test_circular_dependency(self):
        """Should raise CircularDependencyError for circular dependencies."""
        task1 = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": ["2"],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Task 2",
            "deadline": "2024-01-20",
            "priority": 3,
            "dependencies": ["1"],
            "estimated_hours": 2,
        }
        with pytest.raises(CircularDependencyError):
            prioritize_tasks([task1, task2])

    def test_self_referencing_task(self):
        """Should raise CircularDependencyError for self-referencing task."""
        task = {
            "id": "1",
            "name": "Self-referencing",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": ["1"],
            "estimated_hours": 2,
        }
        with pytest.raises(CircularDependencyError):
            prioritize_tasks([task])

    def test_longer_circular_chain(self):
        """Should raise CircularDependencyError for longer circular chain."""
        task1 = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": ["3"],
            "estimated_hours": 2,
        }
        task2 = {
            "id": "2",
            "name": "Task 2",
            "deadline": "2024-01-20",
            "priority": 3,
            "dependencies": ["1"],
            "estimated_hours": 2,
        }
        task3 = {
            "id": "3",
            "name": "Task 3",
            "deadline": "2024-01-25",
            "priority": 3,
            "dependencies": ["2"],
            "estimated_hours": 2,
        }
        with pytest.raises(CircularDependencyError):
            prioritize_tasks([task1, task2, task3])

    def test_missing_task_id(self):
        """Should raise InvalidDependencyError for missing task ID."""
        task = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15",
            "priority": 3,
            "dependencies": ["999"],
            "estimated_hours": 2,
        }
        with pytest.raises(InvalidDependencyError) as exc_info:
            prioritize_tasks([task])
        assert "non-existent task" in str(exc_info.value)

    def test_priority_below_minimum(self):
        """Should raise InvalidPriorityError for priority below minimum."""
        task = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15",
            "priority": 0,
            "dependencies": [],
            "estimated_hours": 2,
        }
        with pytest.raises(InvalidPriorityError):
            prioritize_tasks([task])

    def test_priority_above_maximum(self):
        """Should raise InvalidPriorityError for priority above maximum."""
        task = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15",
            "priority": 6,
            "dependencies": [],
            "estimated_hours": 2,
        }
        with pytest.raises(InvalidPriorityError):
            prioritize_tasks([task])


class TestDateHandling:
    """Tests for date handling."""

    def test_iso_string_dates(self):
        """Should handle ISO string dates."""
        task = {
            "id": "1",
            "name": "Task 1",
            "deadline": "2024-01-15T00:00:00",
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task])
        assert len(result) == 1
        assert result[0]["id"] == "1"

    def test_datetime_objects(self):
        """Should handle datetime objects."""
        task = {
            "id": "1",
            "name": "Task 1",
            "deadline": datetime(2024, 1, 15),
            "priority": 3,
            "dependencies": [],
            "estimated_hours": 2,
        }
        result = prioritize_tasks([task])
        assert len(result) == 1
        assert result[0]["id"] == "1"

