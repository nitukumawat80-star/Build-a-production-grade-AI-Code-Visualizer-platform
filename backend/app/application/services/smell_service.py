from __future__ import annotations

from app.domain.entities.analysis import Insight


class CodeSmellService:
    def detect(self, code: str) -> list[Insight]:
        findings: list[Insight] = []
        lines = code.splitlines()

        long_lines = [idx + 1 for idx, line in enumerate(lines) if len(line) > 120]
        if long_lines:
            findings.append(
                Insight(
                    title="Long Lines",
                    severity="low",
                    details=f"Lines >120 chars detected at: {long_lines[:8]}",
                )
            )

        nesting = self._max_indent(lines)
        if nesting > 5:
            findings.append(
                Insight(
                    title="Deep Nesting",
                    severity="medium",
                    details=f"Indentation depth appears high ({nesting}). Consider extracting functions.",
                )
            )

        mutable_globals = [line for line in lines if line.strip().startswith("global ")]
        if mutable_globals:
            findings.append(
                Insight(
                    title="Global State Usage",
                    severity="medium",
                    details="`global` usage can make debugging and testing difficult.",
                )
            )

        duplicate_condition = self._has_duplicate_conditions(lines)
        if duplicate_condition:
            findings.append(
                Insight(
                    title="Repeated Conditions",
                    severity="low",
                    details="Similar conditional blocks repeated; consider deduping logic.",
                )
            )

        return findings

    def _max_indent(self, lines: list[str]) -> int:
        max_depth = 0
        for line in lines:
            leading = len(line) - len(line.lstrip(" "))
            depth = leading // 2
            max_depth = max(max_depth, depth)
        return max_depth

    def _has_duplicate_conditions(self, lines: list[str]) -> bool:
        conditions = [
            line.strip()
            for line in lines
            if line.strip().startswith("if ") or line.strip().startswith("elif ")
        ]
        return len(conditions) != len(set(conditions))
