# API Documentation

Base URL: `/api/v1`

## Health
- `GET /health`

## Analysis
- `POST /analysis/run`
  - Request: language, code, narration_language, optimization_level
  - Response: full visualization payload + complexity + insights
  - Example:
    ```json
    {
      "user_id": "de305d54-75b4-431b-adb2-eb6b9e546014",
      "language": "python",
      "code": "x = 1\nprint(x + 2)",
      "narration_language": "both",
      "optimization_level": "standard"
    }
    ```

- `GET /analysis/{analysis_id}`
  - Returns previously generated analysis

- `GET /analysis/history/{user_id}`
  - Paginated user history

## Dashboard
- `GET /dashboard/summary/{user_id}`
  - Premium usage analytics

- `GET /dashboard/trends/{user_id}`
  - Pattern and complexity trends over time

## Export Jobs
- `POST /exports`
  - Creates export job for `mp4|gif|pdf`
  - Example:
    ```json
    {
      "analysis_id": "6fd2905d-a37d-4ec2-a13f-bce7bce1f72e",
      "export_type": "mp4"
    }
    ```

- `GET /exports/{job_id}`
  - Export status and artifact URL

## Authentication (ready boundary)
- Add OAuth/JWT at API gateway or auth router.
- Existing models include `users` and `plans` scaffolding.
