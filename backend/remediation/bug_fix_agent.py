
import ast
import re
from pathlib import Path


class BugFixAgent:

    def suggest_fixes(self, bug_analysis):

        suggestions = []

        for issue in bug_analysis.get("issues", []):

            symbol = issue.get("symbol")
            line = issue.get("line")
            message = issue.get("message")

            if symbol == "unused-import":
                fix = "Remove the unused import statement."

            elif symbol == "missing-module-docstring":
                fix = "Add a descriptive module-level docstring."

            elif symbol == "missing-function-docstring":
                fix = "Add a descriptive docstring inside the function."

            else:
                fix = "Review this issue manually and update the code."

            suggestions.append({
                "issue": message,
                "line": line,
                "suggested_fix": fix
            })

        return {
            "total_suggestions": len(suggestions),
            "suggestions": suggestions
        }

    def apply_safe_fixes(self, source_code):

        fixed_code = source_code
        applied_fixes = []

        # Add module docstring if missing
        try:
            tree = ast.parse(fixed_code)

            if ast.get_docstring(tree) is None:
                fixed_code = (
                    '"""Module containing sample Python functions."""\n\n'
                    + fixed_code
                )
                applied_fixes.append("Added module docstring.")

            # Add missing function docstrings
            tree = ast.parse(fixed_code)

            lines = fixed_code.splitlines()

            for node in reversed(tree.body):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if ast.get_docstring(node) is None:
                        indent = " " * (node.col_offset + 4)
                        lines.insert(
                            node.body[0].lineno - 1,
                            indent + '"""Describe this function."""'
                        )
                        applied_fixes.append(
                            f"Added docstring to {node.name}."
                        )

            fixed_code = "\n".join(lines) + "\n"

        except SyntaxError as error:
            return {
                "success": False,
                "fixed_code": source_code,
                "applied_fixes": [],
                "error": str(error)
            }

        # Remove unused imports identified by Pylint
        # This handles simple, single-line imports only.
        unused_imports = re.findall(
            r"^\s*import\s+([A-Za-z_]\w*)\s*(?:#.*)?$",
            fixed_code,
            flags=re.MULTILINE
        )

        for module in unused_imports:
            if not re.search(
                rf"\b{re.escape(module)}\b",
                "\n".join(
                    line for line in fixed_code.splitlines()
                    if not re.match(
                        rf"^\s*import\s+{re.escape(module)}\b",
                        line
                    )
                )
            ):
                fixed_code = re.sub(
                    rf"^\s*import\s+{re.escape(module)}\s*(?:#.*)?\n?",
                    "",
                    fixed_code,
                    count=1,
                    flags=re.MULTILINE
                )
                applied_fixes.append(
                    f"Removed unused import: {module}."
                )

        # Final syntax check
        try:
            ast.parse(fixed_code)
        except SyntaxError as error:
            return {
                "success": False,
                "fixed_code": source_code,
                "applied_fixes": [],
                "error": str(error)
            }

        return {
            "success": True,
            "fixed_code": fixed_code,
            "applied_fixes": applied_fixes
        }

    def save_fixed_code(self, fixed_code, original_path):

        original = Path(original_path)

        output_path = original.with_name(
            original.stem + "_fixed" + original.suffix
        )

        output_path.write_text(
            fixed_code,
            encoding="utf-8"
        )

        return str(output_path)
