
FEW_SHOT_PROMPT = """
You are an expert Python code reviewer.

Learn from the following examples before reviewing the new code.

EXAMPLE 1:

Buggy Code:
def divide(a, b):
    return a / b

Issue:
The function may crash when b is zero.

Suggested Fix:
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

EXAMPLE 2:

Buggy Code:
password = "admin123"

Issue:
Hardcoded password creates a security risk.

Suggested Fix:
Read the password from a secure environment variable.

Now review the following Python code.

Identify:
1. Programming errors
2. Logical mistakes
3. Security vulnerabilities
4. Code quality issues

For each issue provide:
- Issue description
- Severity (High, Medium, Low)
- Line number
- Suggested correction

Python Code:
{code}
"""
