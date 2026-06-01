from __future__ import annotations

from typing import Any

from app.domain.interfaces.ast_parser import ASTParser

LANGUAGE_ALIASES = {
    "javascript": "javascript",
    "js": "javascript",
    "java": "java",
    "cpp": "cpp",
    "c++": "cpp",
}


class TreeSitterASTParser(ASTParser):
    def __init__(self, language: str) -> None:
        self.language = LANGUAGE_ALIASES.get(language.lower(), language.lower())

    def parse(self, code: str) -> dict[str, Any]:
        try:
            from tree_sitter_language_pack import get_parser
        except Exception as exc:
            return {
                "type": "ParseError",
                "message": "tree-sitter-language-pack unavailable",
                "error": str(exc),
                "language": self.language,
            }

        try:
            parser = get_parser(self.language)
            tree = parser.parse(bytes(code, "utf-8"))
            root = tree.root_node
            return self._node_to_dict(root, code)
        except Exception as exc:
            return {
                "type": "ParseError",
                "message": "tree-sitter parse failed",
                "error": str(exc),
                "language": self.language,
            }

    def _node_to_dict(self, node: Any, source: str) -> dict[str, Any]:
        start_point = getattr(node, "start_point", (0, 0))
        end_point = getattr(node, "end_point", (0, 0))
        start_row = start_point[0] if isinstance(start_point, tuple) else getattr(start_point, "row", 0)
        end_row = end_point[0] if isinstance(end_point, tuple) else getattr(end_point, "row", 0)

        entry = {
            "type": str(getattr(node, "type", "unknown")),
            "start_line": int(start_row) + 1,
            "end_line": int(end_row) + 1,
            "children": [],
        }
        if hasattr(node, "start_byte") and hasattr(node, "end_byte"):
            snippet = source[node.start_byte : node.end_byte].strip()
            if snippet:
                entry["text"] = snippet[:180]

        for child in getattr(node, "children", []):
            entry["children"].append(self._node_to_dict(child, source))

        return entry
