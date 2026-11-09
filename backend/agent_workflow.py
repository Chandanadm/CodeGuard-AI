
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from backend.agents.code_understanding_agent import CodeUnderstandingAgent
from backend.analyzers.bug_detection_agent import BugDetectionAgent
from backend.analyzers.security_analysis_agent import SecurityAnalysisAgent
from backend.prompts.prompt_manager import PromptManager
from backend.remediation.bug_fix_agent import BugFixAgent
from backend.testing.fix_verification_agent import FixVerificationAgent


class CodeReviewState(TypedDict, total=False):
    file_path: str
    source_code: str
    prompt_strategy: str
    generated_prompt: str
    code_analysis: dict
    bug_analysis: dict
    security_analysis: dict
    remediation_result: dict
    fixed_code: str
    applied_fixes: list
    fixed_file_path: str
    verification_result: dict
    workflow_status: str


code_agent = CodeUnderstandingAgent()
bug_agent = BugDetectionAgent()
security_agent = SecurityAnalysisAgent()
prompt_manager = PromptManager()
fix_agent = BugFixAgent()
verification_agent = FixVerificationAgent()


def prompt_generation_node(state):
    strategy = state.get("prompt_strategy", "zero_shot")
    prompt = prompt_manager.get_prompt(strategy, state["source_code"])
    return {"generated_prompt": prompt}


def code_understanding_node(state):
    return {
        "code_analysis": code_agent.analyze_code(state["source_code"])
    }


def bug_detection_node(state):
    return {
        "bug_analysis": bug_agent.detect_bugs(state["file_path"])
    }


def security_analysis_node(state):
    return {
        "security_analysis": security_agent.analyze_security(state["file_path"])
    }


def route_after_analysis(state):
    bug_count = state["bug_analysis"].get("total_issues", 0)
    security_count = state["security_analysis"].get(
        "total_vulnerabilities", 0
    )

    if bug_count > 0 or security_count > 0:
        return "bug_remediation"

    return "finish_review"


def bug_remediation_node(state):
    suggestions = fix_agent.suggest_fixes(state["bug_analysis"])
    fix_result = fix_agent.apply_safe_fixes(state["source_code"])

    return {
        "remediation_result": suggestions,
        "fixed_code": fix_result["fixed_code"],
        "applied_fixes": fix_result["applied_fixes"]
    }


def fix_verification_node(state):
    result = verification_agent.verify_fix(state["fixed_code"])

    fixed_path = None

    if result["syntax_valid"]:
        fixed_path = fix_agent.save_fixed_code(
            state["fixed_code"],
            state["file_path"]
        )

    return {
        "verification_result": result,
        "fixed_file_path": fixed_path,
        "workflow_status": result["verification_status"]
    }


def finish_review_node(state):
    return {
        "workflow_status": "Completed - No issues detected"
    }


def create_code_review_workflow():
    workflow = StateGraph(CodeReviewState)

    workflow.add_node("prompt_generation", prompt_generation_node)
    workflow.add_node("code_understanding", code_understanding_node)
    workflow.add_node("bug_detection", bug_detection_node)
    workflow.add_node("security_analysis", security_analysis_node)
    workflow.add_node("bug_remediation", bug_remediation_node)
    workflow.add_node("fix_verification", fix_verification_node)
    workflow.add_node("finish_review", finish_review_node)

    workflow.add_edge(START, "prompt_generation")
    workflow.add_edge("prompt_generation", "code_understanding")
    workflow.add_edge("code_understanding", "bug_detection")
    workflow.add_edge("bug_detection", "security_analysis")

    workflow.add_conditional_edges(
        "security_analysis",
        route_after_analysis,
        {
            "bug_remediation": "bug_remediation",
            "finish_review": "finish_review"
        }
    )

    workflow.add_edge("bug_remediation", "fix_verification")
    workflow.add_edge("fix_verification", END)
    workflow.add_edge("finish_review", END)

    return workflow.compile()
