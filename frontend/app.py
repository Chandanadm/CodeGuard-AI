
import streamlit as st
import requests
import pandas as pd
import difflib
import json
import plotly.graph_objects as go
from pathlib import Path

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CodeGuard AI | Advanced Code Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "review_result": None,
    "original_code": "",
    "review_history": [],
    "review_mode": "Paste Code"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# ADVANCED UI DESIGN AND ANIMATIONS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: linear-gradient(135deg, #080D1B, #101B32, #0B1428);
    color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080D1B, #14213D);
    border-right: 1px solid #263653;
}

[data-testid="stSidebar"] * {
    color: #E2E8F0;
}

.brand {
    font-size: 28px;
    font-weight: 800;
    color: #60A5FA;
    padding-top: 15px;
}

.brand-caption {
    font-size: 10px;
    color: #94A3B8;
    letter-spacing: 2px;
    margin-bottom: 20px;
}

.hero {
    padding: 35px;
    border-radius: 20px;
    background: linear-gradient(120deg, #172554, #1D4ED8, #312E81);
    background-size: 200% 200%;
    animation: gradientMove 8s ease infinite, fadeIn 0.8s ease;
    border: 1px solid rgba(147,197,253,0.3);
    box-shadow: 0 12px 40px rgba(37,99,235,0.18);
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #DBEAFE;
    font-size: 14px;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

@keyframes fadeIn {
    from {opacity: 0; transform: translateY(15px);}
    to {opacity: 1; transform: translateY(0);}
}

.metric-card {
    background: linear-gradient(145deg, #17243B, #111D32);
    border: 1px solid #2B4162;
    border-radius: 15px;
    padding: 21px;
    min-height: 115px;
    transition: all 0.3s ease;
    animation: fadeIn 0.7s ease;
}

.metric-card:hover {
    transform: translateY(-6px);
    border-color: #60A5FA;
    box-shadow: 0 10px 30px rgba(59,130,246,0.18);
}

.metric-label {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.metric-value {
    color: #60A5FA;
    font-size: 30px;
    font-weight: 800;
    margin-top: 9px;
}

.section-title {
    color: #93C5FD;
    font-size: 22px;
    font-weight: 800;
    margin: 25px 0 15px;
}

.panel {
    background: #14213A;
    border: 1px solid #293C5B;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 15px;
}

.stButton button {
    border-radius: 10px;
    font-weight: 700;
    border: 1px solid #3B82F6;
    transition: all 0.25s ease;
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 20px rgba(59,130,246,0.3);
}

.stDownloadButton button {
    border-radius: 10px;
    font-weight: 700;
}

.stTextArea textarea {
    background: #0B1220;
    color: #E2E8F0;
    border: 1px solid #334155;
    border-radius: 12px;
    font-family: Consolas, monospace;
}

div[data-testid="stFileUploader"] {
    background: #14213A;
    border: 1px dashed #3B82F6;
    border-radius: 12px;
    padding: 15px;
}

div[data-testid="stTabs"] button {
    color: #CBD5E1;
    font-weight: 700;
}

.footer {
    text-align: center;
    color: #64748B;
    padding: 30px;
    font-size: 11px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_fixed_code(result):
    fixed_path = result.get("fixed_file_path")

    if not fixed_path:
        return None

    try:
        path = Path(fixed_path)
        if path.is_file():
            return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    return None


def show_metric(label, value):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def show_issues(issues):
    if not issues:
        st.success("No code issues detected.")
        return

    rows = []

    for issue in issues:
        rows.append({
            "Issue": issue.get("message", "-"),
            "Severity": issue.get("severity", "-"),
            "Line": issue.get("line", "-"),
            "Rule": issue.get("symbol", "-")
        })

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )


def create_chart(issues, vulnerabilities, fixes):
    values = [
        len(issues),
        len(vulnerabilities),
        len(fixes)
    ]

    labels = [
        "Code Issues",
        "Security Findings",
        "Fixes Applied"
    ]

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=values,
            marker=dict(
                color=["#3B82F6", "#F97316", "#22C55E"],
                line=dict(width=0)
            ),
            text=values,
            textposition="outside"
        )
    ])

    fig.update_layout(
        title="Code Review Analytics",
        paper_bgcolor="#14213A",
        plot_bgcolor="#14213A",
        font=dict(color="#E2E8F0"),
        yaxis=dict(
            gridcolor="#293C5B",
            title="Count",
            rangemode="tozero"
        ),
        xaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=55, b=20),
        height=350
    )

    return fig


def run_review(code_bytes, filename, strategy):
    with st.spinner("CodeGuard AI is analyzing your code..."):
        response = requests.post(
            f"{API_URL}/review",
            files={
                "file": (
                    filename,
                    code_bytes,
                    "text/x-python"
                )
            },
            data={"prompt_strategy": strategy},
            timeout=180
        )

    if response.status_code != 200:
        st.error(f"API Error: {response.text}")
        return

    result = response.json()

    st.session_state.review_result = result
    st.session_state.original_code = code_bytes.decode(
        "utf-8-sig",
        errors="replace"
    )

    st.session_state.review_history.insert(0, {
        "filename": result.get("filename", filename),
        "issues": (result.get("bug_analysis") or {}).get(
            "total_issues", 0
        ),
        "fixes": len(result.get("applied_fixes", [])),
        "status": result.get("workflow_status", "Unknown")
    })

    st.success("Code review completed!")
    st.balloons()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        '<div class="brand">🛡️ CodeGuard AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-caption">ADVANCED CODE INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        [
            "Dashboard",
            "New Code Review",
            "Review Results",
            "Review History",
            "About System"
        ]
    )

    st.divider()

    st.markdown("### SYSTEM STATUS")

    try:
        health = requests.get(
            f"{API_URL}/health",
            timeout=3
        )

        if health.status_code == 200:
            st.success("API Connected")
        else:
            st.error("API Unavailable")

    except requests.RequestException:
        st.error("API Offline")

    st.caption("FastAPI • LangGraph • Streamlit")
    st.caption("CodeGuard AI | Advanced Edition")


# =========================================================
# COMMON DATA
# =========================================================

result = st.session_state.review_result

if result:
    bug_analysis = result.get("bug_analysis") or {}
    security_analysis = result.get("security_analysis") or {}
    verification = result.get("verification_result") or {}

    issues = bug_analysis.get("issues", [])
    vulnerabilities = security_analysis.get(
        "vulnerabilities", []
    )
    fixes = result.get("applied_fixes", [])

    fixed_code = get_fixed_code(result)

else:
    bug_analysis = {}
    security_analysis = {}
    verification = {}
    issues = []
    vulnerabilities = []
    fixes = []
    fixed_code = None


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">
    <h1>🛡️ CodeGuard AI</h1>
    <p>
        Advanced Code Intelligence Platform
        | Automated Code Review
        | Security Analysis
        | Intelligent Remediation
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">Workspace Overview</div>',
        unsafe_allow_html=True
    )

    if result:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            show_metric(
                "CODE ISSUES",
                bug_analysis.get("total_issues", 0)
            )

        with c2:
            show_metric(
                "SECURITY FINDINGS",
                security_analysis.get(
                    "total_vulnerabilities", 0
                )
            )

        with c3:
            show_metric("FIXES APPLIED", len(fixes))

        with c4:
            show_metric(
                "VERIFICATION",
                verification.get(
                    "verification_status", "N/A"
                )
            )

        st.markdown(
            '<div class="section-title">Analysis Overview</div>',
            unsafe_allow_html=True
        )

        st.plotly_chart(
            create_chart(issues, vulnerabilities, fixes),
            use_container_width=True
        )

        st.markdown("### Latest Review")

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        st.write("**File:**", result.get("filename"))
        st.write("**Prompt Strategy:**", result.get("prompt_strategy"))
        st.write("**Workflow Status:**", result.get("workflow_status"))

        if fixed_code:
            st.success("Corrected code is available in Review Results.")
        else:
            st.info("No corrected file was generated by the current fixer.")

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("Welcome! Start by reviewing your first Python program.")

        c1, c2, c3 = st.columns(3)

        with c1:
            show_metric("CODE REVIEWS", 0)

        with c2:
            show_metric("BUGS DETECTED", 0)

        with c3:
            show_metric("FIXES APPLIED", 0)

    st.markdown(
        '<div class="section-title">Agentic Review Workflow</div>',
        unsafe_allow_html=True
    )

    workflow = [
        ("01", "Code Input", "Submit Python code"),
        ("02", "Understanding", "Inspect program structure"),
        ("03", "Bug Detection", "Identify code issues"),
        ("04", "Security", "Analyze vulnerabilities"),
        ("05", "Remediation", "Apply supported fixes"),
        ("06", "Verification", "Validate corrected code")
    ]

    columns = st.columns(3)

    for index, (number, name, description) in enumerate(workflow):
        with columns[index % 3]:
            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:15px">
                <div class="metric-label">STAGE {number}</div>
                <div style="font-size:19px;font-weight:800;
                color:#60A5FA;margin-top:10px">{name}</div>
                <div style="font-size:12px;color:#94A3B8;
                margin-top:8px">{description}</div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# NEW CODE REVIEW
# =========================================================

elif page == "New Code Review":

    st.markdown(
        '<div class="section-title">New Code Review</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Submit your Python code and let CodeGuard AI analyze it."
    )

    mode = st.radio(
        "Choose input method",
        ["Paste Code", "Upload Python File"],
        horizontal=True
    )

    strategy = st.selectbox(
        "Prompt Engineering Strategy",
        ["zero_shot", "few_shot", "structured"]
    )

    code_bytes = None
    filename = "pasted_code.py"

    if mode == "Paste Code":

        pasted_code = st.text_area(
            "Paste your Python code here",
            height=350,
            placeholder=(
                "def calculate(a, b):\n"
                "    return a + b"
            )
        )

        if pasted_code.strip():
            code_bytes = pasted_code.encode("utf-8")

    else:

        uploaded_file = st.file_uploader(
            "Upload Python source file",
            type=["py"]
        )

        if uploaded_file:
            code_bytes = uploaded_file.getvalue()
            filename = uploaded_file.name

            st.success(
                f"Selected: {filename} "
                f"({uploaded_file.size} bytes)"
            )

    st.markdown("### Review Configuration")

    st.caption(
        "The original submitted code will remain unchanged."
    )

    run_review_button = st.button(
        "🚀 Analyze and Fix My Code",
        type="primary",
        use_container_width=True,
        disabled=not code_bytes
    )

    if run_review_button and code_bytes:

        try:
            run_review(code_bytes, filename, strategy)

        except requests.RequestException as error:
            st.error(f"Unable to connect to backend: {error}")

        except Exception as error:
            st.error(f"Review failed: {error}")


# =========================================================
# REVIEW RESULTS
# =========================================================

elif page == "Review Results":

    st.markdown(
        '<div class="section-title">Code Review Report</div>',
        unsafe_allow_html=True
    )

    if not result:

        st.info("Submit code first to view your review results.")

    else:

        st.write("**Reviewed File:**", result.get("filename"))

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Overview",
            "Code Analysis",
            "Security",
            "Corrected Code",
            "Verification"
        ])

        # OVERVIEW

        with tab1:

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                show_metric(
                    "CODE ISSUES",
                    bug_analysis.get("total_issues", 0)
                )

            with c2:
                show_metric(
                    "VULNERABILITIES",
                    security_analysis.get(
                        "total_vulnerabilities", 0
                    )
                )

            with c3:
                show_metric("FIXES APPLIED", len(fixes))

            with c4:
                show_metric(
                    "SYNTAX",
                    "Valid" if verification.get(
                        "syntax_valid"
                    ) else "Check"
                )

            st.markdown("### Review Information")

            st.write("**Prompt Strategy:**", result.get("prompt_strategy"))
            st.write("**Workflow Status:**", result.get("workflow_status"))
            st.write(
                "**Verification:**",
                verification.get("verification_status")
            )

            report = json.dumps(result, indent=4)

            st.download_button(
                "Download JSON Report",
                data=report,
                file_name="code_review_report.json",
                mime="application/json"
            )

        # CODE ANALYSIS

        with tab2:

            st.markdown("### Code Understanding")

            analysis = result.get("code_analysis") or {}

            a, b, c = st.columns(3)

            a.metric("Functions", len(analysis.get("functions", [])))
            b.metric("Classes", len(analysis.get("classes", [])))
            c.metric("Total Lines", analysis.get("total_lines", 0))

            with st.expander("View Functions, Classes and Imports"):
                st.write("**Functions:**", analysis.get("functions", []))
                st.write("**Classes:**", analysis.get("classes", []))
                st.write("**Imports:**", analysis.get("imports", []))

            st.markdown("### Bug Detection Findings")
            show_issues(issues)

        # SECURITY

        with tab3:

            st.markdown("### Security Assessment")

            if vulnerabilities:

                rows = []

                for item in vulnerabilities:
                    rows.append({
                        "Issue": item.get(
                            "issue_text",
                            item.get("message", "-")
                        ),
                        "Severity": item.get(
                            "issue_severity",
                            item.get("severity", "-")
                        ),
                        "Confidence": item.get(
                            "issue_confidence", "-"
                        ),
                        "Line": item.get(
                            "line_number",
                            item.get("line", "-")
                        )
                    })

                st.dataframe(
                    pd.DataFrame(rows),
                    use_container_width=True,
                    hide_index=True
                )

            else:
                st.success("No security vulnerabilities detected.")

        # CORRECTED CODE

        with tab4:

            st.markdown("### ✨ Corrected Python Code")

            if fixed_code:

                st.success("Corrected code is available!")

                view = st.radio(
                    "Code display",
                    [
                        "Corrected Code",
                        "Original Code",
                        "Side-by-Side Comparison",
                        "Unified Diff"
                    ],
                    horizontal=True
                )

                original = st.session_state.original_code

                if view == "Corrected Code":

                    st.code(
                        fixed_code,
                        language="python",
                        line_numbers=True
                    )

                    if st.button("📋 Copy Corrected Code"):
                        st.code(fixed_code, language="python")
                        st.info(
                            "Select and copy the code above. "
                            "Use the code block copy icon."
                        )

                elif view == "Original Code":

                    st.code(
                        original or "# Original code unavailable",
                        language="python",
                        line_numbers=True
                    )

                elif view == "Side-by-Side Comparison":

                    left, right = st.columns(2)

                    with left:
                        st.markdown("**Original Code**")
                        st.code(
                            original or "# Original unavailable",
                            language="python",
                            line_numbers=True
                        )

                    with right:
                        st.markdown("**Corrected Code**")
                        st.code(
                            fixed_code,
                            language="python",
                            line_numbers=True
                        )

                else:

                    difference = difflib.unified_diff(
                        original.splitlines(),
                        fixed_code.splitlines(),
                        fromfile="original.py",
                        tofile="corrected.py",
                        lineterm=""
                    )

                    st.code(
                        "\n".join(difference) or "No differences found.",
                        language="diff"
                    )

                st.download_button(
                    "⬇️ Download Corrected Python Code",
                    data=fixed_code.encode("utf-8"),
                    file_name="corrected_code.py",
                    mime="text/x-python",
                    type="primary",
                    use_container_width=True
                )

            elif result.get("fixed_file_path"):

                st.warning(
                    "A fixed file path was returned, "
                    "but the dashboard could not read it."
                )

            else:

                st.warning(
                    "The current remediation engine did not generate "
                    "a corrected file for this submission."
                )

            st.markdown("### Automatic Fixes Applied")

            if fixes:
                for fix in fixes:
                    st.success(fix)
            else:
                st.info("No automatic fixes were applied.")

            suggestions = (
                result.get("remediation_suggestions") or {}
            ).get("suggestions", [])

            st.markdown("### Suggested Improvements")

            for index, suggestion in enumerate(suggestions, 1):

                with st.expander(
                    f"Issue {index}: {suggestion.get('issue', 'Finding')}"
                ):
                    st.write("**Line:**", suggestion.get("line"))
                    st.write(
                        "**Recommendation:**",
                        suggestion.get("suggested_fix")
                    )

        # VERIFICATION

        with tab5:

            st.markdown("### Fix Verification")

            if verification.get("syntax_valid"):
                st.success("Python syntax validation passed.")
            else:
                st.error("Python syntax validation failed.")

            if verification.get("pylint_check"):
                st.success("Pylint verification passed.")
            else:
                st.warning("Pylint reported issues.")

            st.write(
                "**Verification Status:**",
                verification.get("verification_status")
            )

            for error in verification.get("errors", []):
                st.warning(error)

        with st.expander("View Complete API Response"):
            st.json(result)


# =========================================================
# REVIEW HISTORY
# =========================================================

elif page == "Review History":

    st.markdown(
        '<div class="section-title">Review History</div>',
        unsafe_allow_html=True
    )

    history = st.session_state.review_history

    if history:

        st.dataframe(
            pd.DataFrame(history),
            use_container_width=True,
            hide_index=True
        )

        if st.button("Clear Session History"):
            st.session_state.review_history = []
            st.rerun()

    else:
        st.info(
            "No reviews in this session yet. "
            "Your completed reviews will appear here."
        )


# =========================================================
# ABOUT SYSTEM
# =========================================================

elif page == "About System":

    st.markdown(
        '<div class="section-title">About CodeGuard AI</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="panel">
        <h2 style="color:#60A5FA">CodeGuard AI</h2>
        <p>
        An intelligent code review platform designed to analyze
        Python programs, identify code quality problems,
        assess security vulnerabilities and apply supported
        automatic code corrections.
        </p>
    </div>
    """, unsafe_allow_html=True)

    technologies = [
        ("Frontend", "Streamlit"),
        ("Backend", "FastAPI"),
        ("Agent Workflow", "LangGraph"),
        ("Code Understanding", "Python AST"),
        ("Bug Detection", "Pylint"),
        ("Security Analysis", "Bandit"),
        ("Remediation", "Python Safe Transformations"),
        ("Verification", "AST and Pylint")
    ]

    st.markdown("### Technology Stack")

    st.dataframe(
        pd.DataFrame(
            technologies,
            columns=["Component", "Technology"]
        ),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Core Capabilities")

    st.write("""
    - Python code submission and analysis
    - Code structure understanding
    - Bug and security detection
    - Prompt strategy selection
    - Supported automatic remediation
    - Corrected code comparison
    - Syntax and quality verification
    """)

    st.info(
        "The current implementation uses deterministic analysis "
        "and generated prompt templates. A live external LLM is "
        "not currently connected."
    )

    st.warning(
        "Automatic remediation currently supports selected safe "
        "fixes. It does not yet repair arbitrary logical bugs."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    CODEGUARD AI | ADVANCED CODE INTELLIGENCE PLATFORM
    <br>
    Automated Review • Security Analysis • Code Remediation
    <br><br>
    Version 2.0
</div>
""", unsafe_allow_html=True)
