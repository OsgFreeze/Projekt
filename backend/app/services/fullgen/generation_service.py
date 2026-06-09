import ollama
from app.services.config.generation_rules import SYSTEM_PROMPT
from app.models.response_models import GenerationResponse

class GenerationService:

    def __init__(self):
        self.model = "qwen2.5:7b"
        self.temperature = 0
        self.system_prompt = SYSTEM_PROMPT

    def generate(self, text: str) -> GenerationResponse:

        original_prompt = text

        user_prompt = self.build_user_prompt(original_prompt)

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
                "temperature": self.temperature
            }
        )

        generated_prompt = (response["message"]["content"].strip())

        return GenerationResponse(
            original_prompt=original_prompt,
            generated_prompt=generated_prompt
        )

    def build_user_prompt(self, original_prompt) -> str:

        lines = []

        lines.append("Komprimiere den folgenden Prompt gemäß den Systemregeln.")
        lines.append(f"Prompt: \n{original_prompt}")

        return "\n".join(lines)