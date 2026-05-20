from app.models.response_models import (
    RefinementResponse,
    PromptGenerationResponse,
    EvaluationResponse,
    PreprocessingResponse
)
from app.services.evaluation.token_counter import TokenCounter


class EvaluationService:

    def __init__(self):
        self.token_counter = TokenCounter()

    def evaluate(
            self, 
            preprocessing_response: PreprocessingResponse, 
            refinement_response: RefinementResponse, 
            prompt_generation_response: PromptGenerationResponse
        ) -> EvaluationResponse:

        original_prompt = preprocessing_response.original_text
        final_prompt = prompt_generation_response.final_prompt

        original_words = len(original_prompt.split())
        final_words = len(final_prompt.split())

        original_tokens = self.token_counter.count(original_prompt)
        final_tokens = self.token_counter.count(final_prompt)

        token_reduction = original_tokens - final_tokens
        word_reduction = original_words - final_words

        role_coverage = self.count_roles(refinement_response.refined_candidates)
        semantic_retention = self.calculate_semantic_retention(refinement_response)

        return EvaluationResponse(
            original_prompt=original_prompt,
            final_prompt=final_prompt,

            original_word_count=original_words,
            final_word_count=final_words,
            word_reduction=word_reduction,
            word_reduction_percent=self.percent(word_reduction, original_words),

            original_token_count=original_tokens,
            final_token_count=final_tokens,
            token_reduction=token_reduction,
            token_reduction_percent=self.percent(token_reduction, original_tokens),

            compression_ratio=self.safe_div(final_tokens, original_tokens),

            original_candidate_count=refinement_response.metadata.get("input_candidate_count", 0),
            final_candidate_count=len(refinement_response.refined_candidates),

            role_coverage=role_coverage,
            role_coverage_percent={},

            semantic_retention=semantic_retention,

            prompt_length_chars_original=len(original_prompt),
            prompt_length_chars_final=len(final_prompt),
            prompt_length_reduction_percent=self.percent(len(original_prompt) - len(final_prompt), len(original_prompt)),

            metadata={}
        )

    def count_roles(self, candidates):
        counts = {}
        for candidate in candidates:
            counts[candidate.role] = counts.get(candidate.role, 0) + 1
        return counts

    def calculate_semantic_retention(self, refinement_response):
        total_priority = refinement_response.metadata.get("total_priority_before_filtering")
        final_priority = sum(c.priority for c in refinement_response.refined_candidates)

        if total_priority:
            return round(final_priority / total_priority, 4)

        return 1.0

    def percent(self, value, base):
        if base == 0:
            return 0.0
        return round((value / base) * 100, 2)

    def safe_div(self, a, b):
        if b == 0:
            return 0.0
        return round(a / b, 4)