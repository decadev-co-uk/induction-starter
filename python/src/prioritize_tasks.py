"""
Smart Task Prioritizer - Python Implementation

This module provides functionality to prioritize tasks based on dependencies,
priority, deadline, and estimated effort.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Union
from typing_extensions import TypedDict

# Priority range constants
PRIORITY_MIN = 1
PRIORITY_MAX = 5


class TaskDict(TypedDict):
    """Type definition for task dictionary."""
    id: str
    name: str
    deadline: Union[datetime, str]
    priority: int
    dependencies: List[str]
    estimated_hours: float


@dataclass
class Task:
    """Represents a task with all its properties."""

    id: str
    name: str
    deadline: datetime
    priority: int
    dependencies: List[str]
    estimated_hours: float


class CircularDependencyError(Exception):
    """Raised when circular dependencies are detected."""

    pass


class InvalidDependencyError(Exception):
    """Raised when dependencies reference non-existent tasks."""

    pass


class InvalidPriorityError(Exception):
    """Raised when priority is out of valid range."""

    pass


def parse_deadline(deadline: Union[datetime, str]) -> datetime:
    """
    Parses a deadline from datetime object or ISO string to datetime object.

    Args:
        deadline: Deadline as datetime object or ISO string

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If date cannot be parsed
    """
    if isinstance(deadline, datetime):
        return deadline
    try:
        # Try parsing ISO format
        if "T" in deadline:
            return datetime.fromisoformat(deadline.replace("Z", "+00:00"))
        else:
            return datetime.fromisoformat(deadline)
    except (ValueError, AttributeError) as e:
        raise ValueError(f"Invalid date format: {deadline}") from e


def validate_task(task: Task, all_task_ids: set) -> None:
    """
    Validates a single task.

    Args:
        task: Task to validate
        all_task_ids: Set of all valid task IDs

    Raises:
        InvalidPriorityError: If priority is out of range
        InvalidDependencyError: If dependencies reference non-existent tasks
        ValueError: If estimated hours is negative
    """
    # Validate priority range
    if task.priority < PRIORITY_MIN or task.priority > PRIORITY_MAX:
        raise InvalidPriorityError(
            f'Task "{task.id}" has invalid priority {task.priority}. '
            f"Priority must be between {PRIORITY_MIN} and {PRIORITY_MAX}."
        )

    # Validate dependencies exist
    for dep_id in task.dependencies:
        if dep_id not in all_task_ids:
            raise InvalidDependencyError(
                f'Task "{task.id}" has dependency on non-existent task "{dep_id}".'
            )

    # Validate estimated hours is non-negative
    if task.estimated_hours < 0:
        raise ValueError(f'Task "{task.id}" has negative estimated hours.')


def detect_circular_dependencies(tasks: dict) -> None:
    """
    Detects circular dependencies using DFS.

    Args:
        tasks: Dictionary mapping task ID to Task object

    Raises:
        CircularDependencyError: If circular dependency is detected
    """
    visited = set()
    recursion_stack = set()

    def has_cycle(task_id: str) -> bool:
        if task_id in recursion_stack:
            return True  # Circular dependency detected
        if task_id in visited:
            return False  # Already processed, no cycle

        visited.add(task_id)
        recursion_stack.add(task_id)

        task = tasks.get(task_id)
        if task:
            for dep_id in task.dependencies:
                if has_cycle(dep_id):
                    return True

        recursion_stack.remove(task_id)
        return False

    for task_id in tasks.keys():
        if task_id not in visited and has_cycle(task_id):
            raise CircularDependencyError(
                f'Circular dependency detected involving task "{task_id}".'
            )


def normalize_tasks(tasks: List[TaskDict]) -> dict:
    """
    Normalizes tasks by parsing deadlines and creating a dictionary.

    Args:
        tasks: List of task dictionaries

    Returns:
        Dictionary mapping task ID to normalized Task object
    """
    normalized = {}
    for task_dict in tasks:
        normalized[task_dict["id"]] = Task(
            id=task_dict["id"],
            name=task_dict["name"],
            deadline=parse_deadline(task_dict["deadline"]),
            priority=task_dict["priority"],
            dependencies=task_dict["dependencies"],
            estimated_hours=task_dict["estimated_hours"],
        )
    return normalized


def prioritize_tasks(tasks: List[TaskDict]) -> List[TaskDict]:
    """
    Prioritizes tasks based on dependencies, priority, deadline, and estimated effort.

    Algorithm:
    1. Validate all tasks (priority range, dependencies exist)
    2. Detect circular dependencies
    3. Use topological sort to order tasks respecting dependencies
    4. Within each dependency level, sort by:
       - Priority (higher first)
       - Deadline (earlier first)
       - Estimated hours (lower first, as tiebreaker)

    Args:
        tasks: List of task dictionaries to prioritize

    Returns:
        List of task dictionaries in priority order

    Raises:
        CircularDependencyError: If circular dependencies are detected
        InvalidDependencyError: If dependencies reference non-existent tasks
        InvalidPriorityError: If priority is out of range
        ValueError: If date format is invalid or estimated hours is negative
    """
    # Handle empty input
    if not tasks:
        return []

    # Create set of all task IDs for validation
    all_task_ids = {task["id"] for task in tasks}

    # Normalize tasks (parse deadlines)
    normalized_tasks = normalize_tasks(tasks)

    # Validate all tasks
    for task in normalized_tasks.values():
        validate_task(task, all_task_ids)

    # Detect circular dependencies
    detect_circular_dependencies(normalized_tasks)

    # TODO: Implement the prioritization algorithm
    #
    # Steps to implement:
    # 1. Perform topological sort to handle dependencies
    #    - Tasks with no dependencies come first
    #    - Then tasks whose dependencies are already in the result
    # 2. Within each dependency level, sort by:
    #    - Priority (descending: 5 is highest)
    #    - Deadline (ascending: earlier deadlines first)
    #    - Estimated hours (ascending: lower effort first)
    #
    # Hint: You can use a queue-based approach or recursive DFS for topological sort
    # Hint: After topological sort, you may need to do a stable sort by priority/deadline/effort
    # Hint: Consider using Python's sorted() function with a key function

    # Placeholder: Return tasks as-is (this will fail tests)
    # Replace this with your implementation
    return tasks

