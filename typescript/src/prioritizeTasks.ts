import type { Task, NormalizedTask } from "../../types/task.types"
import {
  CircularDependencyError,
  InvalidDependencyError,
  InvalidPriorityError,
  PRIORITY_MIN,
  PRIORITY_MAX,
} from "../../types/task.types"

/**
 * Parses a deadline from Date object or ISO string to Date object
 * @param deadline - Deadline as Date object or ISO string
 * @returns Parsed Date object
 * @throws Error if date cannot be parsed
 */
function parseDeadline(deadline: Date | string): Date {
  if (deadline instanceof Date) {
    return deadline
  }
  const parsed = new Date(deadline)
  if (isNaN(parsed.getTime())) {
    throw new Error(`Invalid date format: ${deadline}`)
  }
  return parsed
}

/**
 * Validates a single task
 * @param task - Task to validate
 * @param allTaskIds - Set of all valid task IDs
 * @throws InvalidPriorityError if priority is out of range
 * @throws InvalidDependencyError if dependencies reference non-existent tasks
 */
function validateTask(task: Task, allTaskIds: Set<string>): void {
  // Validate priority range
  if (task.priority < PRIORITY_MIN || task.priority > PRIORITY_MAX) {
    throw new InvalidPriorityError(
      `Task "${task.id}" has invalid priority ${task.priority}. Priority must be between ${PRIORITY_MIN} and ${PRIORITY_MAX}.`
    )
  }

  // Validate dependencies exist
  for (const depId of task.dependencies) {
    if (!allTaskIds.has(depId)) {
      throw new InvalidDependencyError(
        `Task "${task.id}" has dependency on non-existent task "${depId}".`
      )
    }
  }

  // Validate estimated hours is non-negative
  if (task.estimatedHours < 0) {
    throw new Error(`Task "${task.id}" has negative estimated hours.`)
  }
}

/**
 * Detects circular dependencies using DFS
 * @param tasks - Map of task ID to normalized task
 * @throws CircularDependencyError if circular dependency is detected
 */
function detectCircularDependencies(tasks: Map<string, NormalizedTask>): void {
  const visited = new Set<string>()
  const recursionStack = new Set<string>()

  function hasCycle(taskId: string): boolean {
    if (recursionStack.has(taskId)) {
      return true // Circular dependency detected
    }
    if (visited.has(taskId)) {
      return false // Already processed, no cycle
    }

    visited.add(taskId)
    recursionStack.add(taskId)

    const task = tasks.get(taskId)
    if (task) {
      for (const depId of task.dependencies) {
        if (hasCycle(depId)) {
          return true
        }
      }
    }

    recursionStack.delete(taskId)
    return false
  }

  for (const taskId of tasks.keys()) {
    if (!visited.has(taskId) && hasCycle(taskId)) {
      throw new CircularDependencyError(
        `Circular dependency detected involving task "${taskId}".`
      )
    }
  }
}

/**
 * Normalizes tasks by parsing deadlines and creating a map
 * @param tasks - Array of tasks to normalize
 * @returns Map of task ID to normalized task
 */
function normalizeTasks(tasks: Task[]): Map<string, NormalizedTask> {
  const normalized = new Map<string, NormalizedTask>()

  for (const task of tasks) {
    normalized.set(task.id, {
      ...task,
      deadline: parseDeadline(task.deadline),
    })
  }

  return normalized
}

/**
 * Prioritizes tasks based on dependencies, priority, deadline, and estimated effort.
 *
 * Algorithm:
 * 1. Validate all tasks (priority range, dependencies exist)
 * 2. Detect circular dependencies
 * 3. Use topological sort to order tasks respecting dependencies
 * 4. Within each dependency level, sort by:
 *    - Priority (higher first)
 *    - Deadline (earlier first)
 *    - Estimated hours (lower first, as tiebreaker)
 *
 * @param tasks - Array of tasks to prioritize
 * @returns Array of tasks in priority order
 * @throws CircularDependencyError if circular dependencies are detected
 * @throws InvalidDependencyError if dependencies reference non-existent tasks
 * @throws InvalidPriorityError if priority is out of range
 */
export function prioritizeTasks(tasks: Task[]): Task[] {
  // Handle empty input
  if (tasks.length === 0) {
    return []
  }

  // Create set of all task IDs for validation
  const allTaskIds = new Set(tasks.map((t) => t.id))

  // Validate all tasks
  for (const task of tasks) {
    validateTask(task, allTaskIds)
  }

  // Normalize tasks (parse deadlines)
  const normalizedTasks = normalizeTasks(tasks)

  // Detect circular dependencies
  detectCircularDependencies(normalizedTasks)

  // TODO: Implement the prioritization algorithm
  // 
  // Steps to implement:
  // 1. Perform topological sort to handle dependencies
  //    - Tasks with no dependencies come first
  //    - Then tasks whose dependencies are already in the result
  // 2. Within each dependency level, sort by:
  //    - Priority (descending: 5 is highest)
  //    - Deadline (ascending: earlier deadlines first)
  //    - Estimated hours (ascending: lower effort first)
  //
  // Hint: You can use a queue-based approach or recursive DFS for topological sort
  // Hint: After topological sort, you may need to do a stable sort by priority/deadline/effort

  // Placeholder: Return tasks as-is (this will fail tests)
  // Replace this with your implementation
  return tasks
}

