
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from backend.agents.code_understanding_agent import CodeUnderstandingAgent
from backend.analyzers.bug_detection_agent import BugDetectionAgent
from backend.analyzers.security_analysis_agent import SecurityAnalysisAgent


class CodeReviewState(TypedDict, total=False):
    file_path: str
    source_code: str
    code_analysis: dict
    bug_analysis: dict
    security_analysis: dict
    status: str


code_agent = CodeUnderstandingAgent()
bug_agent = BugDetectionAgent()
security_agent = SecurityAnalysisAgent()


def code_understanding_node(state):
    result = code_agent.analyze_code(state["source_code"])
    return {"code_analysis": result}


def bug_detection_node(state):
    result = bug_agent.detect_bugs(state["file_path"])
    return {"bug_analysis": result}


def security_analysis_node(state):
    result = security_agent.analyze_security(state["file_path"])
    return {"security_analysis": result}


def create_code_review_workflow():
    workflow = StateGraph(CodeReviewState)

    workflow.add_node("code_understanding", code_understanding_node)
    workflow.add_node("bug_detection", bug_detection_node)
    workflow.add_node("security_analysis", security_analysis_node)

    workflow.add_edge(START, "code_understanding")
    workflow.add_edge("code_understanding", "bug_detection")
    workflow.add_edge("bug_detection", "security_analysis")
    workflow.add_edge("security_analysis", END)

    return workflow.compile()
