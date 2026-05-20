from typing import List
from app.models.response_models import RefinedCandidate

class TemplateBuilder:

    def __init__(self):
        
        self.max_candidates = 15
        self.min_priority = 2.0
        self.role_order = [
            "LANGUAGE",
            "TECH_STACK",
            "TASK",
            "FUNCTIONAL_REQUIREMENT",
            "INPUT",
            "OUTPUT",
            "CONSTRAINT",
            "QUALITY_REQUIREMENT",
            "EXISTING_CONTEXT",
            "INTERFACE",
            "FILE_STRUCTURE",
            "MISC",
        ]

    def build(self, refined_candidates: List[RefinedCandidate]) -> str:

        filtered_candidates = self.filter_candidates(refined_candidates)
        sorted_candidates = self.sort_candidates(filtered_candidates)
        segments = []

        for candidate in sorted_candidates:
            text = self.normalize_segment(candidate.text)
            if text:
                segments.append(text)

        prompt = ", ".join(segments)

        return prompt.strip()

    def filter_candidates(self, candidates: List[RefinedCandidate]) -> List[RefinedCandidate]:

        filtered = []

        for candidate in candidates:

            # Zu niedrige Priorität ignorieren
            if candidate.priority < self.min_priority:
                continue

            # Leere Texte ignorieren
            if not candidate.text.strip():
                continue

            filtered.append(candidate)

        # Top-N Kandidaten
        filtered = sorted(
            filtered,
            key=lambda c: c.priority,
            reverse=True
        )

        return filtered[:self.max_candidates]
    
    def sort_candidates(self, candidates: List[RefinedCandidate]) -> List[RefinedCandidate]:

        return sorted(
            candidates,
            key=lambda c: (
                self.get_role_order(c.role),
                -c.priority
            )
        )

    def get_role_order(self, role: str) -> int:
        if role in self.role_order:
            return self.role_order.index(role)

        return len(self.role_order)
    
    def normalize_segment(self, text: str) -> str:

        text = text.strip()

        # trailing punctuation entfernen
        text = text.rstrip(".,;:")

        # doppelte spaces
        text = " ".join(text.split())

        return text