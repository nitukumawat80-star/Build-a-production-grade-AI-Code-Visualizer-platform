from __future__ import annotations

from app.domain.entities.analysis import PatternMatch


class PatternDetectionService:
    PATTERN_RULES = {
        "Arrays": ["[", "]", "append", "push", "pop"],
        "Strings": ["str", "substring", "split", "join", "charAt"],
        "Linked Lists": ["next", "node", "linked", "->next"],
        "Trees": ["left", "right", "root", "dfs", "inorder"],
        "Graphs": ["adj", "neighbors", "bfs", "visited", "edges"],
        "Dynamic Programming": ["dp", "memo", "tabulation", "cache"],
        "Greedy": ["sort", "largest", "smallest", "maximize", "minimize"],
        "Sliding Window": ["window", "left", "right", "while right", "while left"],
        "Two Pointer": ["low", "high", "i < j", "left < right", "two pointers"],
    }

    def detect(self, code: str) -> list[PatternMatch]:
        lowered = code.lower()
        found: list[PatternMatch] = []

        for label, keywords in self.PATTERN_RULES.items():
            hits = [kw for kw in keywords if kw.lower() in lowered]
            if not hits:
                continue
            confidence = min(0.99, 0.4 + 0.1 * len(hits))
            found.append(
                PatternMatch(
                    label=label,
                    confidence=round(confidence, 2),
                    evidence=", ".join(hits[:4]),
                )
            )

        return found
