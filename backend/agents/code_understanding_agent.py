
import ast


class CodeUnderstandingAgent:

    def analyze_code(self, source_code):

        try:
            # Parse the Python source code
            tree = ast.parse(source_code)

            # Store code analysis information
            analysis = {
                "functions": [],
                "classes": [],
                "imports": [],
                "total_lines": len(source_code.splitlines())
            }

            # Examine the code structure
            for node in ast.walk(tree):

                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(node.name)

                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append(node.name)

                elif isinstance(node, ast.Import):
                    for item in node.names:
                        analysis["imports"].append(item.name)

                elif isinstance(node, ast.ImportFrom):
                    analysis["imports"].append(node.module)

            return analysis

        except SyntaxError as error:
            return {
                "error": "Syntax error detected",
                "message": str(error)
            }
