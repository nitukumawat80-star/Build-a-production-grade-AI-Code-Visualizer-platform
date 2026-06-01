from __future__ import annotations

import hashlib
import json
import re
import sys
from typing import Any

from app.application.services.bug_service import BugDetectionService
from app.application.services.complexity_service import ComplexityService
from app.application.services.narration_service import NarrationService
from app.application.services.optimization_service import OptimizationSuggestionService
from app.application.services.pattern_service import PatternDetectionService
from app.application.services.smell_service import CodeSmellService
from app.domain.entities.analysis import AnalysisResult, CallFrame, MemoryCell
from app.domain.interfaces.repositories import AnalysisRepository
from app.infrastructure.ast.parser_factory import ASTParserFactory
from app.infrastructure.ast.runtime.python_dry_run import PythonDryRunEngine
from app.infrastructure.cache.redis_cache import RedisCache


class AnalysisService:
    def __init__(self, repository: AnalysisRepository, cache: RedisCache) -> None:
        self.repository = repository
        self.cache = cache
        self.complexity_service = ComplexityService()
        self.pattern_service = PatternDetectionService()
        self.optimization_service = OptimizationSuggestionService()
        self.smell_service = CodeSmellService()
        self.bug_service = BugDetectionService()
        self.narration_service = NarrationService()

    async def run(self, user_id: str, language: str, code: str) -> dict[str, Any]:
        cache_key = self._build_cache_key(language, code)
        cached = await self.cache.get(cache_key)
        if cached is not None:
            return cached

        parser = ASTParserFactory.create(language)
        ast_summary = parser.parse(code)

        if language.lower() == "python":
            dry_run, output, call_stack, scope = PythonDryRunEngine().run(code)
        else:
            dry_run, output, call_stack, scope = self._static_timeline_from_ast(ast_summary, code)

        memory = self._build_memory(scope)
        complexity = self.complexity_service.estimate(language, ast_summary, code)
        patterns = self.pattern_service.detect(code)
        optimizations = self.optimization_service.suggest(code)
        smells = self.smell_service.detect(code)
        bugs = self.bug_service.detect(code)

        result = AnalysisResult(
            language=language,
            ast_summary=ast_summary,
            dry_run=dry_run,
            memory=memory,
            call_stack=call_stack,
            predicted_output=output,
            complexity=complexity,
            patterns=patterns,
            optimizations=optimizations,
            code_smells=smells,
            bug_risks=bugs,
            narration_en="",
            narration_hi="",
        )
        narration_en, narration_hi = self.narration_service.build(result)
        result.narration_en = narration_en
        result.narration_hi = narration_hi

        analysis_id = await self.repository.save(user_id=user_id, code=code, result=result)
        payload = self._serialize_result(analysis_id, user_id, result)
        await self.cache.set(cache_key, payload, ttl_seconds=600)
        return payload

    async def get_by_id(self, analysis_id: str) -> dict[str, Any] | None:
        return await self.repository.get(analysis_id)

    async def get_history(self, user_id: str, limit: int = 20) -> list[dict[str, Any]]:
        return await self.repository.get_history(user_id=user_id, limit=limit)

    def _build_cache_key(self, language: str, code: str) -> str:
        digest = hashlib.sha256(f"{language}:{code}".encode("utf-8")).hexdigest()
        return f"analysis:{digest}"

    def _build_memory(self, scope: dict[str, Any]) -> list[MemoryCell]:
        memory: list[MemoryCell] = []
        for key, value in scope.items():
            if key.startswith("__"):
                continue
            memory.append(
                MemoryCell(
                    key=key,
                    value=self._sanitize_value(value),
                    value_type=type(value).__name__,
                    approx_bytes=sys.getsizeof(value),
                )
            )
        return memory

    def _static_timeline_from_ast(
        self, ast_summary: dict[str, Any], source_code: str
    ) -> tuple[list[Any], list[str], list[CallFrame], dict[str, Any]]:
        timeline: list[Any] = []
        output: list[str] = []
        call_stack: list[CallFrame] = []
        scope: dict[str, Any] = {}
        lines = source_code.splitlines()

        flat_nodes = self._flatten_ast(ast_summary)
        for idx, node in enumerate(flat_nodes):
            line_no = int(node.get("start_line", node.get("lineno", 0)) or 0)
            if 1 <= line_no <= len(lines):
                scope.update(self._extract_static_variables(lines[line_no - 1]))

            timeline.append(
                {
                    "index": idx,
                    "title": node.get("type", "Node"),
                    "line": line_no,
                    "action": "ast_visit",
                    "locals": scope.copy(),
                    "globals": {},
                    "output": None,
                }
            )

            node_type = str(node.get("type", "")).lower()
            node_text = str(node.get("text", "")).lower()
            if "call" in node_type or "method_invocation" in node_type:
                fn_name = node_text.split("(")[0][:40] if node_text else "function_call"
                call_stack.append(CallFrame(function=fn_name, line=node.get("start_line", 0), depth=1))
            if "print" in node_text or "cout" in node_text or "console.log" in node_text:
                output.append("Output predicted from print-like statement.")

        return timeline, output, call_stack, scope

    def _flatten_ast(self, node: dict[str, Any]) -> list[dict[str, Any]]:
        out = [node]
        for child in node.get("children", []):
            out.extend(self._flatten_ast(child))
        return out

    def _serialize_result(self, analysis_id: str, user_id: str, result: AnalysisResult) -> dict[str, Any]:
        def _default(obj: Any) -> Any:
            if hasattr(obj, "__dict__"):
                return obj.__dict__
            return str(obj)

        payload = {
            "analysis_id": analysis_id,
            "user_id": user_id,
            "language": result.language,
            "ast_summary": result.ast_summary,
            "dry_run": [step.__dict__ if hasattr(step, "__dict__") else step for step in result.dry_run],
            "memory": [cell.__dict__ for cell in result.memory],
            "call_stack": [frame.__dict__ for frame in result.call_stack],
            "predicted_output": result.predicted_output,
            "complexity": result.complexity.__dict__,
            "patterns": [pattern.__dict__ for pattern in result.patterns],
            "optimizations": result.optimizations,
            "code_smells": [smell.__dict__ for smell in result.code_smells],
            "bug_risks": [bug.__dict__ for bug in result.bug_risks],
            "narration": {"en": result.narration_en, "hi": result.narration_hi},
        }

        return json.loads(json.dumps(payload, default=_default))

    def _sanitize_value(self, value: Any) -> Any:
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, (list, tuple)):
            return [self._sanitize_value(item) for item in value]
        if isinstance(value, dict):
            return {str(k): self._sanitize_value(v) for k, v in value.items()}
        return str(value)

    def _extract_static_variables(self, line: str) -> dict[str, Any]:
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "//")):
            return {}

        typed_decl = re.match(
            r"^(?:int|long|float|double|char|bool|string|auto|let|const|var)\s+([A-Za-z_]\w*)\s*(?:=\s*(.+?))?[;]?$",
            stripped,
            flags=re.IGNORECASE,
        )
        if typed_decl:
            name = typed_decl.group(1)
            value = typed_decl.group(2) if typed_decl.group(2) else "<uninitialized>"
            return {name: value}

        generic_decl = re.match(
            r"^(?:[A-Za-z_][\w:<>\[\]]*\s+)+([A-Za-z_]\w*)\s*(?:=\s*(.+?))?[;]?$",
            stripped,
        )
        if generic_decl and "(" not in stripped:
            name = generic_decl.group(1)
            value = generic_decl.group(2) if generic_decl.group(2) else "<uninitialized>"
            return {name: value}

        assignment = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.+?)[;]?$", stripped)
        if assignment:
            return {assignment.group(1): assignment.group(2)}

        return {}
