/**
 * Task interface matching the challenge specification
 * Each task represents a work item that needs to be prioritized
 */
export interface Task {
  /** Unique identifier for the task */
  id: string
  /** Human-readable name of the task */
  name: string
  /** Deadline date - can be a Date object or ISO string */
  deadline: Date | string
  /** Priority level from 1-5, where 5 is the highest priority */
  priority: number
  /** Array of task IDs that must be completed before this task */
  dependencies: string[]
  /** Estimated time to complete the task in hours */
  estimatedHours: number
}

/**
 * Normalized task with parsed deadline
 * Used internally for processing
 */
export interface NormalizedTask extends Omit<Task, "deadline"> {
  /** Parsed deadline as Date object */
  deadline: Date
}

/**
 * Priority range constants
 */
export const PRIORITY_MIN = 1
export const PRIORITY_MAX = 5

/**
 * Custom error for circular dependencies
 */
export class CircularDependencyError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "CircularDependencyError"
  }
}

/**
 * Custom error for invalid dependencies
 */
export class InvalidDependencyError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "InvalidDependencyError"
  }
}

/**
 * Custom error for invalid priority values
 */
export class InvalidPriorityError extends Error {
  constructor(message: string) {
    super(message)
    this.name = "InvalidPriorityError"
  }
}

