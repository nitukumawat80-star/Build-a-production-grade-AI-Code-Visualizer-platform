from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_analyses: int
    avg_time_complexity_score: float
    avg_space_complexity_score: float
    top_language: str
    monthly_growth_percent: float


class TrendPoint(BaseModel):
    bucket: str
    analyses: int
    avg_complexity_score: float
