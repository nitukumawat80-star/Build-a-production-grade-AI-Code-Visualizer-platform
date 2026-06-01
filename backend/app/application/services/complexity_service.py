from __future__ import annotations

from typing import Any

from app.domain.entities.analysis import ComplexityReport


class ComplexityService:
    def estimate(self, language: str, ast_summary: dict[str, Any], source_code: str) -> ComplexityReport:
        source = source_code.lower()
        loop_count = self._count_nodes(ast_summary, {"For", "While", "for_statement", "while_statement"})
        nested_loop_depth = self._max_loop_depth(ast_summary)
        recursion_hint = self._has_recursion(source)

        if nested_loop_depth >= 2:
            time = "O(n^2)"
        elif loop_count >= 1:
            time = "O(n)"
        else:
            time = "O(1)"

        if recursion_hint:
            time = "O(2^n)" if "dp" not in source else "O(n)"

        if any(tok in source for tok in ["matrix", "graph", "adj", "memo", "dp"]):
            space = "O(n)"
        elif "sort(" in source or "sorted(" in source:
            space = "O(log n)"
        else:
            space = "O(1)"

        notes = [
            f"Detected {loop_count} loop-like AST nodes.",
            f"Estimated max loop nesting: {nested_loop_depth}.",
        ]
        if recursion_hint:
            notes.append("Recursive call pattern detected.")

        return ComplexityReport(time=time, space=space, notes=notes)

    def _count_nodes(self, node: dict[str, Any], targets: set[str]) -> int:
        count = 1 if node.get("type") in targets else 0
        for child in node.get("children", []):
            count += self._count_nodes(child, targets)
        return count

    def _max_loop_depth(self, node: dict[str, Any], current: int = 0) -> int:
        node_type = str(node.get("type", ""))
        is_loop = node_type in {"For", "While", "for_statement", "while_statement"}
        depth = current + 1 if is_loop else current
        best = depth
        for child in node.get("children", []):
            best = max(best, self._max_loop_depth(child, depth))
        return best

    def _has_recursion(self, source: str) -> bool:
        lines = [line.strip() for line in source.splitlines() if line.strip()]
        declared = set()
        calls: list[str] = []
        for line in lines:
            if line.startswith("def ") and "(" in line:
                declared.add(line.split("def ", 1)[1].split("(", 1)[0].strip())
                continue
            if line.startswith("function ") and "(" in line:
                declared.add(line.split("function ", 1)[1].split("(", 1)[0].strip())
                continue
            calls.append(line)
        call_text = "\n".join(calls)
        return any(f"{fn}(" in call_text for fn in declared)
