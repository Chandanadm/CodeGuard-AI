
from backend.analyzers.security_analysis_agent import SecurityAnalysisAgent


def test_security_analysis():

    agent = SecurityAnalysisAgent()

    result = agent.analyze_security(
        "tests/sample_insecure_code.py"
    )

    assert "total_vulnerabilities" in result
    assert "vulnerabilities" in result

    assert result["total_vulnerabilities"] > 0

    print(
        "Security Issues:",
        result["total_vulnerabilities"]
    )
