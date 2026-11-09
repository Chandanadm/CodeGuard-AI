
from backend.agents.code_understanding_agent import CodeUnderstandingAgent

agent = CodeUnderstandingAgent()


def test_code_analysis():

    code = """
import math

class Calculator:

    def add(self, a, b):
        return a + b

def multiply(a, b):
    return a * b
"""

    result = agent.analyze_code(code)

    assert "Calculator" in result["classes"]
    assert "add" in result["functions"]
    assert "multiply" in result["functions"]
    assert "math" in result["imports"]


def test_syntax_error():

    code = "def add(:"

    result = agent.analyze_code(code)

    assert "error" in result
