from __future__ import annotations

from app.domain.entities.analysis import Insight


class BugDetectionService:
    def detect(self, code: str) -> list[Insight]:
        results: list[Insight] = []
        lowered = code.lower()

        if "while true" in lowered or "while(1)" in lowered:
            results.append(
                Insight(
                    title="Potential Infinite Loop",
                    severity="high",
                    details="Detected unbounded while loop. Ensure a terminating condition exists.",
                )
            )

        if "except:" in lowered:
            results.append(
                Insight(
                    title="Broad Exception Handling",
                    severity="medium",
                    details="Bare `except:` can hide real failures. Catch specific exceptions.",
                )
            )

        if "== none" in lowered or "!= none" in lowered:
            results.append(
                Insight(
                    title="None Comparison Style",
                    severity="low",
                    details="Use `is None` / `is not None` for clarity and correctness.",
                )
            )

        if "/ 0" in lowered:
            results.append(
                Insight(
                    title="Division by Zero Risk",
                    severity="high",
                    details="Expression suggests a possible division by zero path.",
                )
            )

        return results
