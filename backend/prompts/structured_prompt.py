
STRUCTURED_PROMPT = """
You are an expert Python code reviewer.

Analyze the following Python code and identify:
1. Programming errors
2. Logical mistakes
3. Security vulnerabilities
4. Code quality issues
5. Performance problems

Return your response ONLY in valid JSON format.

Use this exact structure:

{{
    "summary": "Short review summary",
    "total_issues": 0,
    "findings": [
        {{
            "issue_type": "Bug or Security or Code Quality",
            "severity": "High or Medium or Low",
            "line_number": 1,
            "description": "Explain the issue",
            "suggested_fix": "Explain how to fix it"
        }}
    ],
    "overall_status": "Pass or Needs Improvement"
}}

If no issues are found, return an empty findings list.

Do not include Markdown code fences or extra text.

Python Code:
{code}
"""
