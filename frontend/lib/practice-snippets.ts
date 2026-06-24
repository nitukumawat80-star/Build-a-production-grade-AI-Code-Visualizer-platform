export type PracticeSnippet = {
  id: string;
  title: string;
  language: "python";
  concept: string;
  description: string;
  dryRunFocus: string;
  expectedOutput: string;
  code: string;
};

export const practiceSnippets: PracticeSnippet[] = [
  {
    id: "two-sum",
    title: "Two Sum",
    language: "python",
    concept: "Hash Map",
    description: "Track seen numbers and find the complement in O(n).",
    dryRunFocus: "Dictionary updates, loop iterations, and early return.",
    expectedOutput: "[0, 1]",
    code: `def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))`
  },
  {
    id: "factorial",
    title: "Factorial",
    language: "python",
    concept: "Recursion",
    description: "Classic recursive function with a base case.",
    dryRunFocus: "Call stack growth, return values, and nested function calls.",
    expectedOutput: "120",
    code: `def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(5))`
  },
  {
    id: "binary-search",
    title: "Binary Search",
    language: "python",
    concept: "Divide and Conquer",
    description: "Reduce the search space by half on every iteration.",
    dryRunFocus: "Loop conditions, pointer movement, and mid calculation.",
    expectedOutput: "3",
    code: `def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

print(binary_search([1, 3, 5, 7, 9, 11], 7))`
  },
  {
    id: "sliding-window",
    title: "Sliding Window",
    language: "python",
    concept: "Window Technique",
    description: "Maintain a rolling sum and update it as the window moves.",
    dryRunFocus: "Variable updates inside the loop and moving window boundaries.",
    expectedOutput: "9",
    code: `def max_sum_k(arr, k):
    window_sum = sum(arr[:k])
    best = window_sum
    for right in range(k, len(arr)):
        window_sum += arr[right] - arr[right - k]
        best = max(best, window_sum)
    return best

print(max_sum_k([2, 1, 5, 1, 3, 2], 3))`
  }
];
