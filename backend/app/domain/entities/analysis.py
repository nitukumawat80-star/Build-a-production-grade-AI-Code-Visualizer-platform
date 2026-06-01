from dataclasses import dataclass, field
from typing import Any


@dataclass
class TimelineStep:
    index: int
    title: str
    line: int
    action: str
    locals: dict[str, Any]
    globals: dict[str, Any]
    output: str | None = None


@dataclass
class MemoryCell:
    key: str
    value: Any
    value_type: str
    approx_bytes: int


@dataclass
class CallFrame:
    function: str
    line: int
    depth: int
    locals: dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplexityReport:
    time: str
    space: str
    notes: list[str] = field(default_factory=list)


@dataclass
class PatternMatch:
    label: str
    confidence: float
    evidence: str


@dataclass
class Insight:
    title: str
    severity: str
    details: str


@dataclass
class AnalysisResult:
    language: str
    ast_summary: dict[str, Any]
    dry_run: list[TimelineStep]
    memory: list[MemoryCell]
    call_stack: list[CallFrame]
    predicted_output: list[str]
    complexity: ComplexityReport
    patterns: list[PatternMatch]
    optimizations: list[str]
    code_smells: list[Insight]
    bug_risks: list[Insight]
    narration_en: str
    narration_hi: str
