
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from backend.agent_workflow import create_code_review_workflow


app = FastAPI(
    title="Agentic AI Code Review System",
    description="Automated code review and bug remediation API",
    version="1.0"
)


# Create upload folder
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Create LangGraph workflow
review_workflow = create_code_review_workflow()


@app.get("/")
def home():
    return {
        "message": "Agentic AI Code Review API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/review")
async def review_code(
    file: UploadFile = File(...),
    prompt_strategy: str = Form("zero_shot")
):
    # Validate file extension
    if not file.filename or Path(file.filename).suffix.lower() != ".py":
        raise HTTPException(
            status_code=400,
            detail="Please upload a Python (.py) file."
        )

    # Validate prompt strategy
    if prompt_strategy not in ["zero_shot", "few_shot", "structured"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid prompt strategy."
        )

    # Read uploaded file
    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    try:
        # Decode and normalize line endings
        source_code = content.decode("utf-8")
        source_code = source_code.replace("\r\n", "\n").replace("\r", "\n")

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="File must contain valid UTF-8 Python code."
        )

    # Save uploaded file
    saved_path = UPLOAD_DIR / f"{uuid4().hex}_{Path(file.filename).name}"
    saved_path.write_text(source_code, encoding="utf-8", newline="\n")

    try:
        # Execute code review workflow
        result = review_workflow.invoke({
            "file_path": str(saved_path),
            "source_code": source_code,
            "prompt_strategy": prompt_strategy
        })

        return {
            "filename": file.filename,
            "prompt_strategy": prompt_strategy,
            "code_analysis": result.get("code_analysis"),
            "bug_analysis": result.get("bug_analysis"),
            "security_analysis": result.get("security_analysis"),
            "remediation_suggestions": result.get("remediation_result"),
            "applied_fixes": result.get("applied_fixes", []),
            "verification_result": result.get("verification_result"),
            "fixed_file_path": result.get("fixed_file_path"),
            "workflow_status": result.get("workflow_status")
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Code review failed: {str(error)}"
        )
