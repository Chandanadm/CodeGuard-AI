
from backend.prompts.zero_shot_prompt import ZERO_SHOT_PROMPT
from backend.prompts.few_shot_prompt import FEW_SHOT_PROMPT
from backend.prompts.structured_prompt import STRUCTURED_PROMPT


class PromptManager:

    def get_prompt(self, strategy, code):

        prompts = {
            "zero_shot": ZERO_SHOT_PROMPT,
            "few_shot": FEW_SHOT_PROMPT,
            "structured": STRUCTURED_PROMPT
        }

        if strategy not in prompts:
            raise ValueError("Invalid prompt strategy")

        return prompts[strategy].format(code=code)
