
import subprocess
import sys
import json


class SecurityAnalysisAgent:

    def analyze_security(self, file_path):

        try:
            # Execute Bandit security scanner
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "bandit",
                    "-f",
                    "json",
                    file_path
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Read Bandit JSON output
            if result.stdout.strip():
                report = json.loads(result.stdout)
                issues = report.get("results", [])
            else:
                issues = []

            # Organize security findings
            findings = []

            for issue in issues:

                findings.append({
                    "issue": issue.get("issue_text"),
                    "severity": issue.get("issue_severity"),
                    "confidence": issue.get("issue_confidence"),
                    "line": issue.get("line_number"),
                    "test_id": issue.get("test_id")
                })

            return {
                "total_vulnerabilities": len(findings),
                "vulnerabilities": findings
            }

        except subprocess.TimeoutExpired:
            return {
                "error": "Security analysis timed out"
            }

        except Exception as error:
            return {
                "error": str(error)
            }
