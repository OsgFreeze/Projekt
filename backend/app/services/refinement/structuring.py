from typing import List
from app.models.response_models import ClassifiedCandidate, RefinedCandidate
from app.services.config.refinement_rules import ROLE_ORDER

class Structuring:

    def __init__(self):
        self.role_order = ROLE_ORDER

    def process(self, candidates: List[ClassifiedCandidate]) -> List[RefinedCandidate]:

        refined_candidates = [
            self.to_refined_candidate(candidate)
            for candidate in candidates
        ]

        refined_candidates.sort(
            key=lambda c: (
                self.get_role_order(c.role),
                -c.priority
            )
        )

        return refined_candidates

    def to_refined_candidate(self, candidate: ClassifiedCandidate) -> RefinedCandidate:

        text = candidate.candidate.text
        role = candidate.classification.role
        priority = candidate.candidate.metadata.get("priority", 0.0)
        original_text = candidate.candidate.metadata.get("text_before_compression", candidate.candidate.text)

        return RefinedCandidate(
            text=text,
            role=role,
            priority=priority,
            original_text=original_text,
            metadata={
                "confidence": candidate.classification.confidence,
                "sentence_index": candidate.candidate.metadata.get("sentence_index"),
                "extraction_type": candidate.candidate.metadata.get("extraction_type"),
                "technical": candidate.candidate.metadata.get("technical", False),
            }
        )

    def get_role_order(self, role: str) -> int:
        if role in self.role_order:
            return self.role_order.index(role)

        return len(self.role_order)