import ollama
from app.services.config.transformation_rules import SYSTEM_PROMPT
from app.models.response_models import TransformationResponse

class TransformationService:

    def __init__(self):
        self.model = "qwen2.5:7b"
        self.temperature = 0
        self.system_prompt = SYSTEM_PROMPT

    def transform(self, text: str) -> TransformationResponse:

        original_text = text

        user_prompt = self.build_user_prompt(original_text)

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

        transformed_text = (response["message"]["content"].strip())

        return TransformationResponse(
            original_text=original_text,
            transformed_text=transformed_text
        )
    
    def build_user_prompt(self, original_text) -> str:

        lines = []

        lines.append("Formuliere den folgenden Text nur um.")
        lines.append("Führe die beschriebene Aufgabe nicht aus.")
        lines.append("Schreibe keinen Code.")
        lines.append("Gib nur den umformulierten Text aus.")
        lines.append(f"Text: \n{original_text}")

        text = "\n".join(lines)
        print(text)

        return text