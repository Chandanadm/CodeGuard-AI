
import ast
import subprocess
import sys
import tempfile
import os


class FixVerificationAgent:

    def verify_fix(self, source_code):

        results = {
            "syntax_valid": False,
            "pylint_check": False,
            "verification_status": "Failed",
            "errors": []
        }

        # Check Python syntax
        try:
            ast.parse(source_code)
            results["syntax_valid"] = True
        except SyntaxError as error:
            results["errors"].append(str(error))
            return results

        # Run Pylint on temporary code
        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".py",
                delete=False,
                encoding="utf-8"
            ) as temp_file:

                temp_file.write(source_code)
                temp_path = temp_file.name

            process = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pylint",
                    temp_path,
                    "--output-format=json"
                ],
                capture_output=True,
                text=True
            )

            if process.returncode == 0:
                results["pylint_check"] = True
            else:
                results["errors"].append(
                    "Pylint reported issues."
                )

        except Exception as error:
            results["errors"].append(str(error))

        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

        if results["syntax_valid"] and results["pylint_check"]:
            results["verification_status"] = "Passed"

        return results
