from typing import List
from app.models.response_models import ClassifiedCandidate
from app.services.config.refinement_rules import ROLE_WEIGHTS

class Prioritization:

    def __init__(self):
        self.role_weights = ROLE_WEIGHTS
        self.max_sentence_bonus = 2.0
        self.max_confidence_bonus = 2.0
        self.max_length_bonus = 1.5
        self.optimal_length_range = (3, 8)

    def process(self, candidates: List[ClassifiedCandidate]) -> List[ClassifiedCandidate]:

        for candidate in candidates:
            priority = self.calculate_priority(candidate)
            candidate.candidate.metadata["priority"] = (round(priority, 2))

        candidates.sort(
            key=lambda c: (
                c.candidate.metadata.get(
                    "priority",
                    0.0
                )
            ),
            reverse=True
        )

        return candidates


    def calculate_priority(self, candidate: ClassifiedCandidate) -> float:

        role = candidate.classification.role
        confidence = (candidate.classification.confidence)
        sentence_index = (
            candidate.candidate.metadata.get(
                "sentence_index",
                999
            )
        )

        # Role Weight
        text = candidate.candidate.text
        priority = self.role_weights.get(role, 1.0)

        # Confidence Bonus
        confidence_bonus = (confidence * self.max_confidence_bonus)
        priority += confidence_bonus

        # Sentence Bonus
        sentence_bonus = (self.max_sentence_bonus / (1 + sentence_index))
        priority += sentence_bonus

        # Length Bonus
        token_count = len(text.split())
        min_len, max_len = (self.optimal_length_range)
        length_bonus = 0.0

        if min_len <= token_count <= max_len:
            length_bonus = self.max_length_bonus
        elif token_count < min_len:
            length_bonus = (token_count / min_len) * self.max_length_bonus
        else:
            overflow = (token_count - max_len)
            penalty_factor = min(overflow * 0.15, 1.0)
            length_bonus = (self.max_length_bonus * (1.0 - penalty_factor))

        priority += length_bonus

        # Special Boosts
        priority += self.apply_special_boosts(candidate)

        # Special Penalties
        priority -= self.apply_special_penalties(candidate)

        return max(priority, 0.0)


    def apply_special_boosts(self, candidate: ClassifiedCandidate) -> float:

        text = candidate.candidate.text.lower()
        role = candidate.classification.role
        boost = 0.0

        if role == "CONSTRAINT":

            important_constraint_words = {
                "nicht",
                "ohne",
                "maximal",
                "mindestens",
                "muss",
                "darf"
            }

            if any(word in text for word in important_constraint_words):
                boost += 1.5

        if "alg_" in text.lower():
            boost += 1.0

        if "file_" in text.lower():
            boost += 0.5

        if ("clean code" in text or "solid" in text):
            boost += 1.0

        return boost


    def apply_special_penalties(self, candidate: ClassifiedCandidate) -> float:

        text = candidate.candidate.text.lower()
        penalty = 0.0

        generic_phrases = {
            "code erstellen",
            "funktion erstellen",
            "methode erstellen",
            "programmcode erstellen"
        }

        if text in generic_phrases:
            penalty += 2.0

        if len(text.split()) <= 1:
            penalty += 2.0

        return penalty