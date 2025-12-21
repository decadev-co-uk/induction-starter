/**
 * Entry point for the TypeScript implementation
 * Re-exports the main function for easy importing
 */
export { prioritizeTasks } from "./prioritizeTasks"
export type { Task } from "../../types/task.types"
export {
  CircularDependencyError,
  InvalidDependencyError,
  InvalidPriorityError,
} from "../../types/task.types"

