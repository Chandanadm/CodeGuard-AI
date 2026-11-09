# 🛡️ CodeGuard AI
### Prompt-Engineered Code Review and Intelligent Bug Remediation System

**An agent-based Python code analysis platform for automated code review, security vulnerability detection, safe bug remediation, and fix verification.**

---

## 📌 Project Overview

CodeGuard AI is an automated code review system designed to help developers identify code quality issues, detect potential security vulnerabilities, and apply selected safe corrections to Python source code.

The system uses a multi-agent workflow orchestrated with **LangGraph**, combining static code analysis, security scanning, rule-based remediation, and automated verification.

It also supports three prompt-engineering strategies—Zero-Shot, Few-Shot, and Structured Prompting—as part of its architecture for future generative AI integration.

## ✨ Key Features

- **Automated Code Review:** Analyzes uploaded or pasted Python code.
- **Code Understanding:** Extracts functions, classes, imports, and structural information using Python AST.
- **Bug Detection:** Identifies coding issues using Pylint.
- **Security Analysis:** Detects potential vulnerabilities using Bandit.
- **Intelligent Remediation:** Suggests corrections and automatically applies selected safe transformations.
- **Fix Verification:** Validates corrected code using syntax analysis and Pylint.
- **Prompt Engineering:** Supports Zero-Shot, Few-Shot, and Structured prompt generation.
- **Interactive Dashboard:** Provides a Streamlit interface with review metrics, findings, and code comparison.
- **Corrected Code:** Displays original and corrected code with comparison and download options.

## 🏗️ System Architecture

```text
                 User
                   |
                   v
          Streamlit Frontend
                   |
                   v
             FastAPI Backend
                   |
                   v
           LangGraph Workflow
                   |
        +----------+-----------+
        |                      |
        v                      v
  Prompt Generation      Code Understanding
                               |
                               v
                         Bug Detection
                               |
                               v
                       Security Analysis
                               |
                      Issues Detected?
                         /          \
                       Yes           No
                        |             |
                        v             v
                 Bug Remediation   Complete Review
                        |
                        v
                  Fix Verification
                        |
                        v
                   Review Results
```

## 🤖 Agent Components

| Component | Responsibility |
|---|---|
| Code Understanding Agent | Analyzes Python code structure using AST |
| Bug Detection Agent | Detects code quality issues using Pylint |
| Security Analysis Agent | Identifies potential security vulnerabilities using Bandit |
| Prompt Manager | Generates Zero-Shot, Few-Shot, and Structured prompts |
| Bug Remediation Agent | Suggests and applies supported safe fixes |
| Fix Verification Agent | Checks syntax validity and Pylint results |
| LangGraph Workflow | Coordinates analysis, remediation, and verification |

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| Agent Orchestration | LangGraph |
| Static Code Analysis | Python AST, Pylint |
| Security Analysis | Bandit |
| Data Visualization | Plotly |
| API Communication | Requests |
| Testing | Pytest |
| Version Control | Git and GitHub |

## 📂 Project Structure

```text
Agentic_Code_Review/
│
├── backend/
│   ├── agents/
│   ├── analyzers/
│   ├── prompts/
│   ├── remediation/
│   ├── testing/
│   ├── agent_workflow.py
│   └── api.py
│
├── frontend/
│   └── app.py
│
├── tests/
├── requirements.txt
├── run_agentic_review.py
├── .gitignore
└── README.md
```

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Chandanadm/CodeGuard-AI.git
cd CodeGuard-AI
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Start the Backend

```powershell
python -m uvicorn backend.api:app --reload
```

Backend URL:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

### 5. Start the Frontend

Open a second terminal in the project directory, activate the virtual environment, and run:

```powershell
streamlit run frontend/app.py
```

Open the application:

`http://localhost:8501`

## 💻 How to Use

1. Open the CodeGuard AI dashboard.
2. Navigate to **New Code Review**.
3. Upload a Python file or paste Python source code.
4. Select a prompt strategy.
5. Start the automated code review.
6. Examine code analysis findings and security results.
7. View remediation suggestions and applied fixes.
8. Compare original and corrected code.
9. Review the verification status and download corrected code when available.

## 🧪 Example

**Original Code**

```python
import os

def calculate_total(price, quantity):
    return price * quantity

print(calculate_total(100, 5))
```

**Possible Findings**

- Unused import (`os`)
- Missing module docstring
- Missing function docstring

**Corrected Code**

```python
"""Calculate and display a total."""


def calculate_total(price, quantity):
    """Calculate the total from price and quantity."""
    return price * quantity


print(calculate_total(100, 5))
```

This example illustrates the supported safe-remediation functionality.

## 🔐 Security Analysis

CodeGuard AI uses Bandit to identify potentially insecure Python coding patterns.

Security findings are reported for developer review. Detection of a security issue does not necessarily mean the system can automatically repair it.

## 🧠 Prompt Engineering Strategies

**Zero-Shot Prompting:** Generates review instructions without examples.

**Few-Shot Prompting:** Includes examples to guide the expected review format.

**Structured Prompting:** Defines a structured response format for review output.

**Current implementation note:** The system generates prompt templates but does not currently execute them through a live large language model. Automated corrections use supported rule-based transformations. LLM-powered code review and remediation are planned enhancements.

## 🧪 Testing

Run the test suite from the project directory:

```powershell
python -m pytest tests -v
```

The tests cover selected code analysis, security analysis, and workflow functionality.

## 🔮 Future Enhancements

- Integrate a live LLM for contextual code review and suggested corrections.
- Expand remediation to cover more bug categories.
- Add multi-language code review support.
- Support GitHub repository and pull-request analysis.
- Add persistent review history and analytics.
- Introduce automated security re-scanning after remediation.
- Add Docker deployment and CI/CD integration.

## 🎯 Project Objective

To develop an automated, extensible code review platform that improves developer productivity by combining agent-based orchestration, static analysis, security assessment, and verified safe code transformations.

---

**Developed as an academic project exploring agent-based software analysis, prompt engineering, and automated code quality improvement.**