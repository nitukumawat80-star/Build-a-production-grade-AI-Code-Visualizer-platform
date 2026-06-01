from pydantic import BaseModel


class ExportCreateRequest(BaseModel):
    analysis_id: str
    export_type: str


class ExportJobResponse(BaseModel):
    id: str
    analysis_id: str
    export_type: str
    status: str
    artifact_url: str | None
    created_at: str
    updated_at: str
