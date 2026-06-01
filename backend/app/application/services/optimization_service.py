from __future__ import annotations


class OptimizationSuggestionService:
    def suggest(self, code: str) -> list[str]:
        lowered = code.lower()
        suggestions: list[str] = []

        if "for" in lowered and "for" in lowered.split("for", 1)[1]:
            suggestions.append(
                "Nested loops detected: evaluate hash-map or prefix-sum strategies to reduce time complexity."
            )

        if "sort(" in lowered and "for" in lowered:
            suggestions.append(
                "If sort is inside repeated logic, move it outside loops or cache sorted results."
            )

        if "dp" not in lowered and ("fib" in lowered or "rec" in lowered):
            suggestions.append(
                "Recursive pattern detected: memoization or bottom-up DP may improve performance."
            )

        if "string" in lowered or "str" in lowered:
            suggestions.append(
                "For repeated concatenation, use list-buffer/join strategy to avoid quadratic behavior."
            )

        if not suggestions:
            suggestions.append("Code looks reasonably optimized for baseline readability and performance.")

        return suggestions
