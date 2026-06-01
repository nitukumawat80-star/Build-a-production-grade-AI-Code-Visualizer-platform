from app.application.services.complexity_service import ComplexityService


def test_estimate_nested_loop_complexity() -> None:
    ast_like = {
        "type": "Module",
        "children": [
            {
                "type": "For",
                "children": [{"type": "For", "children": []}],
            }
        ],
    }
    code = "for i in range(n):\n  for j in range(n):\n    pass"
    report = ComplexityService().estimate("python", ast_like, code)
    assert report.time == "O(n^2)"
