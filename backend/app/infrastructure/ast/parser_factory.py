from app.domain.interfaces.ast_parser import ASTParser
from app.infrastructure.ast.python_parser import PythonASTParser
from app.infrastructure.ast.tree_sitter_parser import TreeSitterASTParser


class ASTParserFactory:
    @staticmethod
    def create(language: str) -> ASTParser:
        normalized = language.lower()
        if normalized == "python":
            return PythonASTParser()
        if normalized in {"javascript", "js", "java", "cpp", "c++"}:
            return TreeSitterASTParser(normalized)
        raise ValueError(f"Unsupported language: {language}")
