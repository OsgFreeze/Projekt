from difflib import SequenceMatcher
from typing import List

from app.models.response_models import ClassifiedCandidate


class Deduplication:

    def __init__(self):
        self.similarity_threshold = 0.88

    def process(self, candidates: List[ClassifiedCandidate]) -> List[ClassifiedCandidate]:

        unique_candidates: List[ClassifiedCandidate] = []

        for candidate in candidates:
            if self.is_duplicate(candidate, unique_candidates):
                continue

            unique_candidates.append(candidate)

        return unique_candidates

    def is_duplicate(self, candidate: ClassifiedCandidate, unique_candidates: List[ClassifiedCandidate]) -> bool:

        for existing in unique_candidates:
            if self.are_duplicates(candidate, existing):
                return True

        return False

    def are_duplicates(self, first: ClassifiedCandidate, second: ClassifiedCandidate) -> bool:

        first_text = self.normalize(first.candidate.text)
        second_text = self.normalize(second.candidate.text)

        first_role = first.classification.role
        second_role = second.classification.role

        # Unterschiedliche Rollen nicht deduplizieren
        if first_role != second_role:
            return False

        # Exakt gleich
        if first_text == second_text:
            return True

        # Ein Text enthält den anderen
        if self.is_contained(first_text, second_text):
            return True

        # Ähnliche Texte
        if self.similarity(first_text, second_text) >= self.similarity_threshold:
            return True

        return False

    def is_contained(self, first_text: str, second_text: str) -> bool:

        if not first_text or not second_text:
            return False

        shorter = min(first_text, second_text, key=len)
        longer = max(first_text, second_text, key=len)

        # Sehr kurze Texte nicht per contains entfernen
        if len(shorter.split()) < 2:
            return False

        return shorter in longer

    def normalize(self, text: str) -> str:

        return (
            text
            .lower()
            .strip()
            .replace(",", "")
            .replace(".", "")
            .replace(":", "")
            .replace(";", "")
        )

    def similarity(self, first: str, second: str) -> float:
        return SequenceMatcher(None, first, second).ratio()