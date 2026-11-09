
from backend.prompts.prompt_manager import PromptManager

manager = PromptManager()

sample_code = """
def divide(a, b):
    return a / b

password = "admin123"
"""

strategies = ["zero_shot", "few_shot", "structured"]

for strategy in strategies:
    prompt = manager.get_prompt(strategy, sample_code)

    print("\n================================")
    print("PROMPT STRATEGY:", strategy.upper())
    print("================================")

    print(prompt[:300])
    print("\nPrompt generated successfully!")
