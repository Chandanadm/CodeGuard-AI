
ZERO_SHOT_PROMPT = """
You are an expert Python code reviewer.

Review the following Python code carefully.

Identify:
1. Programming errors
2. Logical mistakes
3. Code quality issues
4. Security risks
5. Performance problems

For every issue, explain:
- Issue description
- Severity (High, Medium, Low)
- Line number (if identifiable)
- Suggested correction

If no issue is found, clearly mention that.

Python Code:
{code}
"""
