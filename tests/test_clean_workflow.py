from backend.agent_workflow import create_code_review_workflow

file_path = "tests/sample_clean_code.py"

with open(file_path, "r", encoding="utf-8") as file:
    source_code = file.read()

app = create_code_review_workflow()

result = app.invoke({
    "file_path": file_path,
    "source_code": source_code,
    "prompt_strategy": "zero_shot"
})

print("\n========== CLEAN CODE REVIEW ==========")
print("Bug Analysis:", result["bug_analysis"])
print("Security Analysis:", result["security_analysis"])
print("Workflow Status:", result["workflow_status"])

print("\nRemediation executed:",
      "remediation_result" in result)

print("\n========== TEST COMPLETED ==========")