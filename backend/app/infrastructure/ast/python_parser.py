import ast
from typing import Any

from app.domain.interfaces.ast_parser import ASTParser


class PythonASTParser(ASTParser):
    def parse(self, code: str) -> dict[str, Any]:
        tree = ast.parse(code)
        return self._node_to_dict(tree)

    def _node_to_dict(self, node: ast.AST) -> dict[str, Any]:
        result: dict[str, Any] = {
            "type": node.__class__.__name__,
            "lineno": getattr(node, "lineno", 0),
            "children": [],
        }

        simple_fields: dict[str, Any] = {}
        for field_name, field_value in ast.iter_fields(node):
            if isinstance(field_value, ast.AST):
                result["children"].append(self._node_to_dict(field_value))
            elif isinstance(field_value, list):
                for item in field_value:
                    if isinstance(item, ast.AST):
                        result["children"].append(self._node_to_dict(item))
                    else:
                        simple_fields[field_name] = field_value
            else:
                simple_fields[field_name] = field_value

        if simple_fields:
            result["fields"] = simple_fields

        return result
