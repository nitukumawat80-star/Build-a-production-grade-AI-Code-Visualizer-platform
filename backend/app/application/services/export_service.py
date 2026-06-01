from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any


class ExportService:
    def create_job(self, analysis_id: str, export_type: str) -> dict[str, Any]:
        if export_type not in {"mp4", "gif", "pdf"}:
            raise ValueError("export_type must be one of: mp4, gif, pdf")

        job_id = str(uuid.uuid4())
        now = datetime.now(tz=timezone.utc).isoformat()

        return {
            "id": job_id,
            "analysis_id": analysis_id,
            "export_type": export_type,
            "status": "queued",
            "artifact_url": None,
            "created_at": now,
            "updated_at": now,
        }
