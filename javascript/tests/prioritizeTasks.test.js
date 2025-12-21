import { describe, it, expect } from "@jest/globals"
import {
  prioritizeTasks,
  CircularDependencyError,
  InvalidDependencyError,
  InvalidPriorityError,
} from "../src/prioritizeTasks.js"

describe("prioritizeTasks", () => {
  describe("Basic Functionality", () => {
    it("should return empty array for empty input", () => {
      const result = prioritizeTasks([])
      expect(result).toEqual([])
    })

    it("should return single task as-is", () => {
      const task = {
        id: "1",
        name: "Single task",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task])
      expect(result).toEqual([task])
    })

    it("should order tasks with simple dependencies", () => {
      const task1 = {
        id: "1",
        name: "Setup project",
        deadline: "2024-01-20",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Implement feature",
        deadline: "2024-01-15",
        priority: 5,
        dependencies: ["1"],
        estimatedHours: 8,
      }
      const result = prioritizeTasks([task2, task1])
      expect(result).toEqual([task1, task2])
      expect(result[0].id).toBe("1")
      expect(result[1].id).toBe("2")
    })

    it("should handle tasks with no dependencies", () => {
      const task1 = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Task 2",
        deadline: "2024-01-20",
        priority: 4,
        dependencies: [],
        estimatedHours: 4,
      }
      const result = prioritizeTasks([task1, task2])
      // Both have no dependencies, so should be sorted by priority
      expect(result[0].id).toBe("2") // Higher priority first
      expect(result[1].id).toBe("1")
    })
  })

  describe("Priority Sorting", () => {
    it("should prioritize tasks by priority when dependencies are satisfied", () => {
      const task1 = {
        id: "1",
        name: "Low priority",
        deadline: "2024-01-15",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "High priority",
        deadline: "2024-01-15",
        priority: 5,
        dependencies: [],
        estimatedHours: 2,
      }
      const task3 = {
        id: "3",
        name: "Medium priority",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task1, task2, task3])
      expect(result.map((t) => t.id)).toEqual(["2", "3", "1"])
    })

    it("should prioritize by priority after dependencies are resolved", () => {
      const task1 = {
        id: "1",
        name: "Dependency",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "High priority dependent",
        deadline: "2024-01-20",
        priority: 5,
        dependencies: ["1"],
        estimatedHours: 4,
      }
      const task3 = {
        id: "3",
        name: "Low priority dependent",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: ["1"],
        estimatedHours: 4,
      }
      const result = prioritizeTasks([task3, task2, task1])
      expect(result.map((t) => t.id)).toEqual(["1", "2", "3"])
    })
  })

  describe("Deadline Urgency", () => {
    it("should prioritize earlier deadlines when priorities are equal", () => {
      const task1 = {
        id: "1",
        name: "Later deadline",
        deadline: "2024-01-20",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Earlier deadline",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task1, task2])
      expect(result[0].id).toBe("2")
      expect(result[1].id).toBe("1")
    })

    it("should use deadline as tiebreaker after priority", () => {
      const task1 = {
        id: "1",
        name: "High priority, later deadline",
        deadline: "2024-01-20",
        priority: 5,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "High priority, earlier deadline",
        deadline: "2024-01-15",
        priority: 5,
        dependencies: [],
        estimatedHours: 2,
      }
      const task3 = {
        id: "3",
        name: "Low priority",
        deadline: "2024-01-10",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task1, task2, task3])
      // Priority 5 tasks first, then sorted by deadline
      expect(result[0].id).toBe("2") // Priority 5, earlier deadline
      expect(result[1].id).toBe("1") // Priority 5, later deadline
      expect(result[2].id).toBe("3") // Priority 2
    })

    it("should handle Date objects as deadlines", () => {
      const task1 = {
        id: "1",
        name: "Later deadline",
        deadline: new Date("2024-01-20"),
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Earlier deadline",
        deadline: new Date("2024-01-15"),
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task1, task2])
      expect(result[0].id).toBe("2")
      expect(result[1].id).toBe("1")
    })
  })

  describe("Complex Dependencies", () => {
    it("should handle multi-level dependencies", () => {
      const task1 = {
        id: "1",
        name: "Level 1",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Level 2",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: ["1"],
        estimatedHours: 2,
      }
      const task3 = {
        id: "3",
        name: "Level 3",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: ["2"],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task3, task1, task2])
      expect(result.map((t) => t.id)).toEqual(["1", "2", "3"])
    })

    it("should handle branching dependencies", () => {
      const task1 = {
        id: "1",
        name: "Root",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Branch A",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: ["1"],
        estimatedHours: 2,
      }
      const task3 = {
        id: "3",
        name: "Branch B",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: ["1"],
        estimatedHours: 2,
      }
      const task4 = {
        id: "4",
        name: "Merge",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: ["2", "3"],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task4, task3, task1, task2])
      expect(result[0].id).toBe("1") // Root first
      // Tasks 2 and 3 can be in any order (both depend on 1)
      expect(result.slice(1, 3).map((t) => t.id).sort()).toEqual(["2", "3"])
      expect(result[3].id).toBe("4") // Merge last
    })

    it("should handle tasks with multiple dependencies", () => {
      const task1 = {
        id: "1",
        name: "Dependency 1",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Dependency 2",
        deadline: "2024-01-20",
        priority: 2,
        dependencies: [],
        estimatedHours: 2,
      }
      const task3 = {
        id: "3",
        name: "Requires both",
        deadline: "2024-01-20",
        priority: 5,
        dependencies: ["1", "2"],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task3, task1, task2])
      expect(result[0].id).toBe("1") // Or 2, order doesn't matter
      expect(result[1].id).toBe("2") // Or 1, order doesn't matter
      expect(result[2].id).toBe("3") // Must be last
    })
  })

  describe("Estimated Hours (Tiebreaker)", () => {
    it("should use estimated hours as final tiebreaker", () => {
      const task1 = {
        id: "1",
        name: "Long task",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: [],
        estimatedHours: 8,
      }
      const task2 = {
        id: "2",
        name: "Short task",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task1, task2])
      // Same priority and deadline, so shorter task first
      expect(result[0].id).toBe("2")
      expect(result[1].id).toBe("1")
    })
  })

  describe("Integration Tests", () => {
    it("should handle complex real-world scenario", () => {
      const tasks = [
        {
          id: "1",
          name: "Setup project",
          deadline: "2024-01-25",
          priority: 5,
          dependencies: [],
          estimatedHours: 2,
        },
        {
          id: "2",
          name: "Write tests",
          deadline: "2024-01-20",
          priority: 4,
          dependencies: ["1"],
          estimatedHours: 4,
        },
        {
          id: "3",
          name: "Implement feature",
          deadline: "2024-01-22",
          priority: 5,
          dependencies: ["1"],
          estimatedHours: 8,
        },
        {
          id: "4",
          name: "Code review",
          deadline: "2024-01-18",
          priority: 3,
          dependencies: ["2", "3"],
          estimatedHours: 2,
        },
        {
          id: "5",
          name: "Documentation",
          deadline: "2024-01-30",
          priority: 2,
          dependencies: ["4"],
          estimatedHours: 3,
        },
      ]
      const result = prioritizeTasks(tasks)

      // Task 1 must be first (no dependencies, highest priority)
      expect(result[0].id).toBe("1")

      // Tasks 2 and 3 depend on 1
      // Task 3 has higher priority (5 vs 4), so should come before 2
      expect(result[1].id).toBe("3")
      expect(result[2].id).toBe("2")

      // Task 4 depends on both 2 and 3
      expect(result[3].id).toBe("4")

      // Task 5 depends on 4
      expect(result[4].id).toBe("5")
    })
  })

  describe("Edge Cases - Errors", () => {
    it("should throw CircularDependencyError for circular dependencies", () => {
      const task1 = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: ["2"],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Task 2",
        deadline: "2024-01-20",
        priority: 3,
        dependencies: ["1"],
        estimatedHours: 2,
      }
      expect(() => prioritizeTasks([task1, task2])).toThrow(CircularDependencyError)
    })

    it("should throw CircularDependencyError for self-referencing task", () => {
      const task = {
        id: "1",
        name: "Self-referencing",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: ["1"],
        estimatedHours: 2,
      }
      expect(() => prioritizeTasks([task])).toThrow(CircularDependencyError)
    })

    it("should throw CircularDependencyError for longer circular chain", () => {
      const task1 = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: ["3"],
        estimatedHours: 2,
      }
      const task2 = {
        id: "2",
        name: "Task 2",
        deadline: "2024-01-20",
        priority: 3,
        dependencies: ["1"],
        estimatedHours: 2,
      }
      const task3 = {
        id: "3",
        name: "Task 3",
        deadline: "2024-01-25",
        priority: 3,
        dependencies: ["2"],
        estimatedHours: 2,
      }
      expect(() => prioritizeTasks([task1, task2, task3])).toThrow(CircularDependencyError)
    })

    it("should throw InvalidDependencyError for missing task ID", () => {
      const task = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15",
        priority: 3,
        dependencies: ["999"],
        estimatedHours: 2,
      }
      expect(() => prioritizeTasks([task])).toThrow(InvalidDependencyError)
      expect(() => prioritizeTasks([task])).toThrow(/non-existent task/)
    })

    it("should throw InvalidPriorityError for priority below minimum", () => {
      const task = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15",
        priority: 0,
        dependencies: [],
        estimatedHours: 2,
      }
      expect(() => prioritizeTasks([task])).toThrow(InvalidPriorityError)
    })

    it("should throw InvalidPriorityError for priority above maximum", () => {
      const task = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15",
        priority: 6,
        dependencies: [],
        estimatedHours: 2,
      }
      expect(() => prioritizeTasks([task])).toThrow(InvalidPriorityError)
    })
  })

  describe("Edge Cases - Date Handling", () => {
    it("should handle ISO string dates", () => {
      const task = {
        id: "1",
        name: "Task 1",
        deadline: "2024-01-15T00:00:00Z",
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task])
      expect(result).toHaveLength(1)
      expect(result[0].id).toBe("1")
    })

    it("should handle Date objects", () => {
      const task = {
        id: "1",
        name: "Task 1",
        deadline: new Date("2024-01-15"),
        priority: 3,
        dependencies: [],
        estimatedHours: 2,
      }
      const result = prioritizeTasks([task])
      expect(result).toHaveLength(1)
      expect(result[0].id).toBe("1")
    })
  })
})

