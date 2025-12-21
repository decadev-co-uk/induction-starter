# Smart Task Prioritizer Challenge

## Overview

Welcome to the Smart Task Prioritizer challenge! This is a 20-minute technical challenge designed to evaluate your coding skills across multiple competencies including Git proficiency, JavaScript/TypeScript/Python knowledge, Data Structures & Algorithms, code quality, and testing.

## Challenge Objective

Build a task prioritization system that intelligently orders tasks based on multiple criteria including:
- **Deadline**: Tasks with earlier deadlines should be prioritized
- **Priority**: Tasks with higher priority (1-5, where 5 is highest) should be prioritized
- **Dependencies**: Tasks with dependencies must be ordered after their dependencies
- **Estimated Effort**: Consider estimated hours when priorities are equal

## Requirements

1. Implement a function that takes a list of tasks and returns them in priority order
2. Each task has the following properties:
   - `id`: Unique identifier (string)
   - `name`: Task name (string)
   - `deadline`: Deadline date (Date object or ISO string)
   - `priority`: Priority level from 1-5, where 5 is highest
   - `dependencies`: Array of task IDs that must be completed before this task
   - `estimatedHours`: Estimated time to complete (number)

3. **Dependency Rules**:
   - Tasks with dependencies must be ordered after their dependencies
   - Handle circular dependencies (should throw an error)
   - Handle missing task IDs in dependencies (should throw an error)

4. **Prioritization Rules**:
   - When dependencies are satisfied, prioritize by:
     1. Priority level (higher first)
     2. Deadline urgency (earlier first)
     3. Estimated effort (lower first, as a tiebreaker)

5. **Error Handling**:
   - Validate all inputs
   - Handle edge cases gracefully
   - Provide meaningful error messages

## Getting Started

This repository supports three language implementations:
- **TypeScript** (recommended)
- **JavaScript**
- **Python**

Choose the language you're most comfortable with. All implementations have the same requirements and test coverage.

### TypeScript Setup

```bash
cd typescript
npm install
npm test
```

### JavaScript Setup

```bash
cd javascript
npm install
npm test
```

### Python Setup

```bash
cd python
pip install -r requirements.txt
pytest
```

## Project Structure

Each language implementation follows a similar structure:

```
[language]/
├── src/
│   └── prioritizeTasks.[ts|js|py]  # Your implementation goes here
├── tests/
│   └── prioritizeTasks.test.[ts|js|py]  # Test suite
└── [config files]
```

## Implementation Guide

### What You Need to Implement

1. **Main Function**: `prioritizeTasks(tasks: Task[]): Task[]`
   - This is the core function you need to implement
   - The starter code provides the function signature and basic structure
   - You'll need to implement the prioritization algorithm

2. **Algorithm Hints**:
   - Use **topological sort** to handle dependencies
   - After resolving dependencies, sort by priority, deadline, and estimated hours
   - Consider using a priority queue or sorting algorithm

3. **Error Handling**:
   - Validate task IDs exist
   - Detect circular dependencies
   - Validate priority range (1-5)
   - Handle invalid date formats

### What's Provided

- Type definitions / interfaces
- Test suite with comprehensive test cases
- Project configuration files
- Basic function structure with validation skeleton
- Error classes/types

## Running Tests

### TypeScript/JavaScript

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

### Python

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## Test Coverage

The test suite includes:

1. **Basic Functionality**
   - Simple dependency ordering
   - Single task handling
   - Empty task list

2. **Priority Sorting**
   - Tasks with same dependencies, different priorities
   - Priority ordering when dependencies are satisfied

3. **Deadline Urgency**
   - Tasks with different deadlines
   - Deadline comparison with priority

4. **Complex Dependencies**
   - Multi-level dependencies
   - Branching dependency graphs
   - Tasks with multiple dependencies

5. **Edge Cases**
   - Circular dependencies (should throw error)
   - Missing task IDs (should throw error)
   - Invalid priority values (should throw error)
   - Invalid date formats (should handle gracefully)

6. **Integration Tests**
   - Real-world scenarios combining all factors
   - Complex task graphs with multiple sorting criteria

## Example Usage

### TypeScript/JavaScript

```typescript
import { prioritizeTasks } from './src/prioritizeTasks';
import type { Task } from '../types/task.types';

const tasks: Task[] = [
  {
    id: "1",
    name: "Setup project",
    deadline: "2024-01-15",
    priority: 5,
    dependencies: [],
    estimatedHours: 2
  },
  {
    id: "2",
    name: "Implement feature",
    deadline: "2024-01-20",
    priority: 4,
    dependencies: ["1"],
    estimatedHours: 8
  }
];

const prioritized = prioritizeTasks(tasks);
// Returns: [task1, task2] (task1 must come before task2 due to dependency)
```

### Python

```python
from src.prioritize_tasks import prioritize_tasks
from datetime import datetime

tasks = [
    {
        "id": "1",
        "name": "Setup project",
        "deadline": datetime(2024, 1, 15),
        "priority": 5,
        "dependencies": [],
        "estimated_hours": 2
    },
    {
        "id": "2",
        "name": "Implement feature",
        "deadline": datetime(2024, 1, 20),
        "priority": 4,
        "dependencies": ["1"],
        "estimated_hours": 8
    }
]

prioritized = prioritize_tasks(tasks)
# Returns: [task1, task2] (task1 must come before task2 due to dependency)
```

## Evaluation Criteria

Your submission will be evaluated on:

1. **Git Proficiency**: Commit history, commit messages, branch usage
2. **JavaScript/TypeScript Knowledge**: Language features, best practices
3. **Python Knowledge**: Language features, best practices (if using Python)
4. **Data Structures & Algorithms**: Efficient algorithm choice, correct implementation
5. **AI/LLM Concepts**: Code quality that demonstrates understanding
6. **Code Quality**: SOLID principles, clean code, maintainability
7. **Testing**: Test coverage, test quality
8. **Learning Speed**: How quickly you understand and implement the solution
9. **Overall Assessment**: Holistic evaluation

## Submission Guidelines

1. **Fork this repository** to your GitHub account
2. **Implement your solution** in your chosen language
3. **Ensure all tests pass** before submitting
4. **Create meaningful Git commits** with clear messages
5. **Create a Pull Request** to the original repository
6. **Submit the PR URL** using the submission form on the challenge platform

## Tips for Success

- **Read the tests first**: They show exactly what's expected
- **Start simple**: Get basic dependency ordering working first
- **Test incrementally**: Run tests frequently as you implement
- **Handle edge cases**: Don't forget circular dependencies and missing tasks
- **Write clean code**: Follow best practices for your chosen language
- **Document your approach**: Add comments explaining your algorithm

## Time Management

You have **20 minutes** to complete this challenge. Recommended breakdown:

- **2-3 minutes**: Read requirements and understand the problem
- **1-2 minutes**: Review test cases to understand expected behavior
- **10-12 minutes**: Implement the core algorithm
- **3-4 minutes**: Handle edge cases and ensure all tests pass
- **1-2 minutes**: Final review and cleanup

## Questions?

If you have questions about the challenge requirements, please refer to:
- The test cases (they are the source of truth)
- The type definitions (they show the expected data structures)
- The challenge platform instructions

Good luck! 🚀
