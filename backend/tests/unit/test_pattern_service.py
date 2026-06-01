from app.application.services.pattern_service import PatternDetectionService


def test_detect_dynamic_programming_pattern() -> None:
    code = """
def fib(n):
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
"""
    service = PatternDetectionService()
    patterns = service.detect(code)
    labels = {pattern.label for pattern in patterns}
    assert "Dynamic Programming" in labels
