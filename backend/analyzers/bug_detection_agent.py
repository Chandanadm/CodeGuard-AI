
import subprocess
import sys
import json


class BugDetectionAgent:

    def detect_bugs(self, file_path):

        try:
            # Run Pylint on the uploaded Python file
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    file_path,
                    "--output-format=json"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            # Convert Pylint output into JSON
            if result.stdout.strip():
                bugs = json.loads(result.stdout)
            else:
                bugs = []

            # Prepare detected issues
            findings = []

            for bug in bugs:

                findings.append({
                    "type": bug.get("type"),
                    "severity": bug.get("type"),
                    "message": bug.get("message"),
                    "line": bug.get("line"),
                    "symbol": bug.get("symbol")
                })

            return {
                "total_issues": len(findings),
                "issues": findings
            }

        except subprocess.TimeoutExpired:
            return {
                "error": "Code analysis timed out"
            }

        except Exception as error:
            return {
                "error": str(error)
            }
