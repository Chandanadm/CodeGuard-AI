
from pathlib import Path
from backend.agent_workflow import create_code_review_workflow

file_path = Path("tests/sample_buggy_code.py")
source_code = file_path.read_text(encoding="utf-8")

app = create_code_review_workflow()

initial_state = {
    "file_path": str(file_path),
    "source_code": source_code,
    "prompt_strategy": "few_shot"
}

result = app.invoke(initial_state)

print("\n========== AGENTIC CODE REVIEW REPORT ==========")

print("\n1. SELECTED PROMPT STRATEGY")
print(initial_state["prompt_strategy"])

print("\n2. CODE UNDERSTANDING")
print(result["code_analysis"])

print("\n3. BUG DETECTION")
print(result["bug_analysis"])

print("\n4. SECURITY ANALYSIS")
print(result["security_analysis"])

print("\n5. BUG REMEDIATION SUGGESTIONS")
print(result["remediation_result"])

print("\n6. FIX VERIFICATION")
print(result["verification_result"])

print("\n7. AUTOMATIC FIXES APPLIED")
print(result["applied_fixes"])

print("\n8. FIXED FILE LOCATION")
print(result["fixed_file_path"])

print("\n========== REVIEW COMPLETED ==========")
