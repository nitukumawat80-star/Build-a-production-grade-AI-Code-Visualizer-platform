from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AnalysisRunRequest(BaseModel):
    user_id: str = Field(..., description="UUID string")
    language: Literal["python", "javascript", "js", "java", "cpp", "c++"]
    code: str
    narration_language: Literal["en", "hi", "both"] = "both"
    optimization_level: Literal["standard", "aggressive"] = "standard"


class AnalysisResponse(BaseModel):
    analysis_id: str
    user_id: str
    language: str
    ast_summary: dict[str, Any]
    dry_run: list[dict[str, Any]]
    memory: list[dict[str, Any]]
    call_stack: list[dict[str, Any]]
    predicted_output: list[str]
    complexity: dict[str, Any]
    patterns: list[dict[str, Any]]
    optimizations: list[str]
    code_smells: list[dict[str, Any]]
    bug_risks: list[dict[str, Any]]
    narration: dict[str, str]


class AnalysisHistoryItem(BaseModel):
    id: str
    user_id: str
    language: str
    complexity_time: str | None = None
    complexity_space: str | None = None
    created_at: str | None = None
