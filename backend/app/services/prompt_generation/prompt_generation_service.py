from app.services.prompt_generation.template_builder import TemplateBuilder
from app.services.prompt_generation.llm_builder import LLMBuilder
from app.models.response_models import RefinementResponse, PromptGenerationResponse

class PromptGenerationService:

    def __init__(self): 
        self.template_builder = TemplateBuilder()
        self.llm_builder = LLMBuilder()

    def generate(self, refinement_response: RefinementResponse, use_llm: bool = False) -> PromptGenerationResponse:

        refined_candidates = refinement_response.refined_candidates

        if use_llm:
            final_prompt = self.llm_builder.build(refined_candidates)
            strategy = "llm_builder"
        else:
            final_prompt = self.template_builder.build(refined_candidates)
            strategy = "template_builder"

        return PromptGenerationResponse(
            final_prompt=final_prompt,
            used_candidates=refined_candidates,
            metadata={
                "generation_strategy": strategy,
                "candidate_count": len(refined_candidates),
                "prompt_length_chars": len(final_prompt),
                "prompt_word_count": len(final_prompt.split())
            }
        )