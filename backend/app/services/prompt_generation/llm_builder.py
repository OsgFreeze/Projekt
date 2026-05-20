from typing import List
import ollama
from app.models.response_models import RefinedCandidate
from app.services.config.llm_builder_rules import SYSTEM_PROMPT

class LLMBuilder:

    def __init__(self):
        self.model = "qwen2.5:3b"
        self.temperature = 0
        self.system_prompt = SYSTEM_PROMPT

    def build(self, refined_candidates: List[RefinedCandidate]) -> str:

        user_prompt = self.build_user_prompt(refined_candidates)

        response = ollama.chat(
            model=self.model,
            keep_alive="10m", 
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            options={
                "temperature": self.temperature,
                "num_predict": 80
            }
        )

        final_prompt = (response["message"]["content"].strip())

        return final_prompt


    def build_user_prompt(self, refined_candidates: List[RefinedCandidate]) -> str:

        lines = []

        lines.append("Kandidaten:\n")

        for candidate in refined_candidates:
            role = candidate.role
            text = candidate.text

            lines.append(f"[{role}]: {text}")

        lines.append("\n Erzeuge daraus einen kurzen kompakten Coding-Prompt.")

        return "\n".join(lines)