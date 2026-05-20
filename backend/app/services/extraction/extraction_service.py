# Extract candidates
# -> combine semantic & technical candidates
# returns list of all candidates

from app.models.response_models import (
    PreprocessingResponse,  
    ExtractionResponse
)

from app.services.extraction.semantic_extraction import SemanticExtraction
from app.services.extraction.technical_extraction import TechnicalExtraction

class ExtractionService:
    
    def __init__(self):
        
        self.semantic_extraction = SemanticExtraction()
        self.technical_extraction = TechnicalExtraction()

    def extract(self, preprocessing_response: PreprocessingResponse) -> ExtractionResponse:
        
        if not preprocessing_response.sentences:
            return ExtractionResponse()

        semantic_candidates = self.semantic_extraction.extract(preprocessing_response)

        technical_candidates = self.technical_extraction.extract(preprocessing_response)

        all_candidates = semantic_candidates + technical_candidates       

        return ExtractionResponse(
            candidates=all_candidates,
            metadata={}
        )
