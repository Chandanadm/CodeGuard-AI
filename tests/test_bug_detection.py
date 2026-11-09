
from backend.analyzers.bug_detection_agent import BugDetectionAgent


def test_bug_detection():

    agent = BugDetectionAgent()

    result = agent.detect_bugs(
        "tests/sample_buggy_code.py"
    )

    assert "total_issues" in result
    assert "issues" in result

    print("Detected Issues:", result["total_issues"])
