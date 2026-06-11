import ollama
from app.services.config.generation_rules import SYSTEM_PROMPT
from app.models.response_models import EvaluationResponse
from app.services.evaluation.evaluation_service import EvaluationService

class GenerationService:

    def __init__(self):
        self.model = "qwen2.5:7b"
        self.temperature = 0
        self.system_prompt = SYSTEM_PROMPT
        self.es = EvaluationService()

    def generate(self, text: str) -> EvaluationResponse:

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

        # Prepare EvaluationResult
        original_words = len(original_prompt.split())
        final_words = len(generated_prompt.split())

        original_tokens = self.es.token_counter.count(original_prompt)
        final_tokens = self.es.token_counter.count(generated_prompt)

        token_reduction = original_tokens - final_tokens
        word_reduction = original_words - final_words


        return EvaluationResponse(
            original_prompt=original_prompt,
            final_prompt=generated_prompt,

            original_word_count=original_words,
            final_word_count=final_words,
            word_reduction=word_reduction,
            word_reduction_percent=self.es.percent(word_reduction, original_words),

            original_token_count=original_tokens,
            final_token_count=final_tokens,
            token_reduction=token_reduction,
            token_reduction_percent=self.es.percent(token_reduction, original_tokens),

            compression_ratio=self.es.safe_div(final_tokens, original_tokens),

            original_candidate_count=-1,
            final_candidate_count=-1,

            role_coverage={},
            role_coverage_percent={},

            semantic_retention=-1,

            prompt_length_chars_original=len(original_prompt),
            prompt_length_chars_final=len(generated_prompt),
            prompt_length_reduction_percent=self.es.percent(len(original_prompt) - len(generated_prompt), len(original_prompt)),

            metadata={}
        )

    def build_user_prompt(self, original_prompt) -> str:

        lines = []

        lines.append("Komprimiere den folgenden Prompt gemäß den Systemregeln.")
        lines.append(f"Prompt: \n{original_prompt}")

        return "\n".join(lines)