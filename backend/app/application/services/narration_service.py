from __future__ import annotations

from app.domain.entities.analysis import AnalysisResult


class NarrationService:
    def build(self, result: AnalysisResult) -> tuple[str, str]:
        steps = len(result.dry_run)
        complexity = f"Time {result.complexity.time}, Space {result.complexity.space}"

        english = (
            f"This program was analyzed in {steps} steps. "
            f"Detected patterns include: {', '.join(p.label for p in result.patterns) or 'none'}. "
            f"Complexity summary: {complexity}."
        )

        hindi = (
            f"Is program ka vishleshan {steps} steps me hua. "
            f"Pehchane gaye patterns: {', '.join(p.label for p in result.patterns) or 'koi nahi'}. "
            f"Complexity summary: {complexity}."
        )

        return english, hindi
