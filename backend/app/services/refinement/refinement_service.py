from app.models.response_models import ClassificationResponse, RefinementResponse
from app.services.refinement.deduplication import Deduplication
from app.services.refinement.compression import Compression
from app.services.refinement.prioritization import Prioritization
from app.services.refinement.structuring import Structuring

class RefinementService:
    
    def __init__(self):
        self.deduplication = Deduplication()
        self.compression = Compression()
        self.prioritization = Prioritization()
        self.structuring = Structuring()
    
    def refine(self, classification_response: ClassificationResponse) -> RefinementResponse:
        
        candidates = classification_response.classified_candidates

        candidates = self.deduplication.process(candidates)
        candidates = self.compression.process(candidates)
        candidates = self.prioritization.process(candidates)

        refined_candidates = self.structuring.process(candidates)

        return RefinementResponse(
            refined_candidates=refined_candidates,
            metadata={
                "candidate_count": len(refined_candidates),
                "roles": self.count_roles(refined_candidates)
            }
        )
    
    def count_roles(self, refined_candidates):
        counts = {}

        for candidate in refined_candidates:
            counts[candidate.role] = counts.get(candidate.role, 0) + 1

        return counts