from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.application.services.export_service import ExportService
from app.schemas.export import ExportCreateRequest, ExportJobResponse

router = APIRouter(prefix="/exports", tags=["exports"])
_service = ExportService()
_jobs: dict[str, dict] = {}


@router.post("", response_model=ExportJobResponse)
async def create_export(payload: ExportCreateRequest) -> dict:
    try:
        job = _service.create_job(payload.analysis_id, payload.export_type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    _jobs[job["id"]] = job
    return job


@router.get("/{job_id}", response_model=ExportJobResponse)
async def get_export(job_id: str) -> dict:
    job = _jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Export job not found")

    if job["status"] == "queued":
        job["status"] = "processing"
        job["updated_at"] = datetime.now(tz=timezone.utc).isoformat()
    elif job["status"] == "processing":
        job["status"] = "completed"
        job["artifact_url"] = f"https://cdn.example.com/exports/{job_id}.{job['export_type']}"
        job["updated_at"] = datetime.now(tz=timezone.utc).isoformat()

    return job
