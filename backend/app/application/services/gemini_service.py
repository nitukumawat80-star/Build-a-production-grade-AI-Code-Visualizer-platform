from __future__ import annotations

import json
from typing import Any

import httpx


class GeminiEnhancementService:
    def __init__(self, api_key: str, model: str, timeout_seconds: float = 25.0) -> None:
        self.api_key = api_key.strip()
        self.model = model.strip() or "gemini-2.5-flash"
        self.timeout_seconds = timeout_seconds

    @property
    def enabled(self) -> bool:
        return bool(self.api_key)

    async def enhance(
        self,
        language: str,
        source_code: str,
        complexity: dict[str, Any],
        patterns: list[dict[str, Any]],
        local_optimizations: list[str],
        local_code_smells: list[dict[str, Any]],
        local_bug_risks: list[dict[str, Any]],
        local_narration_en: str,
        local_narration_hi: str,
    ) -> dict[str, Any] | None:
        if not self.enabled:
            return None

        prompt = self._build_prompt(
            language=language,
            source_code=source_code,
            complexity=complexity,
            patterns=patterns,
            local_optimizations=local_optimizations,
            local_code_smells=local_code_smells,
            local_bug_risks=local_bug_risks,
            local_narration_en=local_narration_en,
            local_narration_hi=local_narration_hi,
        )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(
                    url,
                    headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                    json=payload,
                )
                response.raise_for_status()
                body = response.json()
        except Exception:
            return None

        text = self._extract_text(body)
        if not text:
            return None

        parsed = self._load_json(text)
        if not parsed:
            return None

        normalized = self._normalize_response(parsed)
        normalized["model"] = body.get("modelVersion", self.model)
        normalized["enhanced"] = True
        normalized["message"] = "Gemini enhancement applied."
        return normalized

    def _build_prompt(
        self,
        language: str,
        source_code: str,
        complexity: dict[str, Any],
        patterns: list[dict[str, Any]],
        local_optimizations: list[str],
        local_code_smells: list[dict[str, Any]],
        local_bug_risks: list[dict[str, Any]],
        local_narration_en: str,
        local_narration_hi: str,
    ) -> str:
        return (
            "You are an expert code reviewer and educator.\n"
            "Return ONLY valid JSON with this schema:\n"
            "{\n"
            '  "optimizations": string[],\n'
            '  "code_smells": [{"title": string, "severity": "low|medium|high", "details": string}],\n'
            '  "bug_risks": [{"title": string, "severity": "low|medium|high", "details": string}],\n'
            '  "narration_en": string,\n'
            '  "narration_hi": string\n'
            "}\n\n"
            f"Language: {language}\n"
            f"Complexity: {json.dumps(complexity)}\n"
            f"Detected patterns: {json.dumps(patterns)}\n"
            f"Local optimizations baseline: {json.dumps(local_optimizations)}\n"
            f"Local smells baseline: {json.dumps(local_code_smells)}\n"
            f"Local bug risks baseline: {json.dumps(local_bug_risks)}\n"
            f"Local narration EN baseline: {local_narration_en}\n"
            f"Local narration HI baseline: {local_narration_hi}\n\n"
            "Improve quality, avoid hallucinations, keep outputs concise and actionable.\n"
            "Source code:\n"
            "```"
            f"{source_code[:15000]}"
            "```"
        )

    def _extract_text(self, body: dict[str, Any]) -> str:
        candidates = body.get("candidates") or []
        if not candidates:
            return ""
        content = candidates[0].get("content") or {}
        parts = content.get("parts") or []
        if not parts:
            return ""
        return str(parts[0].get("text") or "").strip()

    def _load_json(self, text: str) -> dict[str, Any] | None:
        try:
            return json.loads(text)
        except Exception:
            pass

        if "```" in text:
            fragments = [frag.strip() for frag in text.split("```") if frag.strip()]
            for fragment in fragments:
                maybe_json = fragment.replace("json", "", 1).strip()
                try:
                    return json.loads(maybe_json)
                except Exception:
                    continue
        return None

    def _normalize_response(self, payload: dict[str, Any]) -> dict[str, Any]:
        optimizations = payload.get("optimizations")
        if not isinstance(optimizations, list):
            optimizations = []
        optimizations = [str(item) for item in optimizations if str(item).strip()]

        smells = self._normalize_insights(payload.get("code_smells"))
        bugs = self._normalize_insights(payload.get("bug_risks"))

        narration_en = str(payload.get("narration_en") or "").strip()
        narration_hi = str(payload.get("narration_hi") or "").strip()

        return {
            "optimizations": optimizations,
            "code_smells": smells,
            "bug_risks": bugs,
            "narration_en": narration_en,
            "narration_hi": narration_hi,
        }

    def _normalize_insights(self, raw: Any) -> list[dict[str, str]]:
        if not isinstance(raw, list):
            return []

        normalized: list[dict[str, str]] = []
        for item in raw[:10]:
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or "").strip()
            severity = str(item.get("severity") or "medium").strip().lower()
            details = str(item.get("details") or "").strip()
            if not title or not details:
                continue
            if severity not in {"low", "medium", "high"}:
                severity = "medium"
            normalized.append({"title": title, "severity": severity, "details": details})
        return normalized
