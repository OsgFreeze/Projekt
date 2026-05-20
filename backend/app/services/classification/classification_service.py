from collections import defaultdict
from typing import Dict, Optional
from app.models.response_models import (
    Candidate,
    ExtractionResponse,
    ClassificationResult,
    ClassifiedCandidate,
    ClassificationResponse
)
from app.services.config.classification_rules import (
    ROLE_RULES,
    ROLE_PRIORITY,
    GENERIC_TARGETS
)

class ClassificationService:

    def __init__(self):
        self.role_rules = ROLE_RULES
        self.role_priority = ROLE_PRIORITY
        self.generic_targets = GENERIC_TARGETS

    def classify(self, extraction_response: ExtractionResponse) -> ClassificationResponse:
        
        classified_candidates = []

        for candidate in extraction_response.candidates:

            classification = self.assign_role(candidate)

            classified_candidates.append(
                ClassifiedCandidate(
                    candidate=candidate, 
                    classification=classification
                )
            )

        return ClassificationResponse(
            classified_candidates=classified_candidates,
            metadata={}
        )
    
    # Assign Role
    def assign_role(self, candidate: Candidate) -> ClassificationResult:

        # Set Technical Candidates
        if candidate.metadata.get("technical"):
            role = candidate.metadata.get("role", "MISC")
            confidence = candidate.metadata.get("confidence", 1.0)

            return ClassificationResult(
                role=role,
                confidence=confidence,
                scores={
                    role: confidence
                }
            )

        # Semantic Scoring
        scores = self.score_candidate(candidate)

        if not scores:
            return ClassificationResult(
                role="MISC",
                confidence=0.0,
                scores={}
            )
        
        best_score = max(scores.values())
        best_roles = [role for role, score in scores.items() if score == best_score]
        best_role = sorted(best_roles, key=lambda r: self.role_priority.index(r))[0]

        return ClassificationResult(
            role=best_role,
            confidence=round(best_score, 2),
            scores=dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))
        )


    # Score Candidate
    def score_candidate(self, candidate: Candidate) -> Dict[str, float]:
        text = self.normalize(candidate.text)
        action = self.normalize(candidate.action)
        target = self.normalize(candidate.target)
        modifiers = " ".join(self.normalize(m) for m in candidate.modifiers)
        full_text = " ".join([text, action, target, modifiers])
        scores = defaultdict(float)

        for role, rules in self.role_rules.items():
            role_score = 0.0

            # 1. Verb/action signal
            if action in rules["verbs"]:
                role_score += 3.0

            # 2. Keyword signal
            for keyword in rules["keywords"]:
                if keyword in full_text:
                    role_score += 1.5

            # 3. Marker signal
            for marker in rules["markers"]:
                if marker in full_text:
                    role_score += 2.0

            # 4. Role-specific weighting
            role_score *= rules["weight"]

            if role_score > 0:
                scores[role] += role_score

        self.apply_bonus_rules(candidate, scores)
        self.apply_penalties(candidate, scores)

        return dict(scores) 


    # Bonus Rules
    def apply_bonus_rules(self, candidate: Candidate, scores):
        text = self.normalize(candidate.text)
        action = self.normalize(candidate.action)

        # Output-Bonus
        if action in {"ausgeben", "zurückgeben", "anzeigen", "liefern"}:
            scores["OUTPUT"] += 2.0

        # Input-Bonus
        if action in {"übergeben", "einlesen", "laden", "erhalten"}:
            scores["INPUT"] += 2.0

        # Existing-Context-Bonus
        if any(marker in text for marker in ["bereits", "vorhanden", "existiert", "implementiert"]):
            scores["EXISTING_CONTEXT"] += 2.0

        # Constraint-Bonus
        if any(marker in text for marker in ["darf nicht", "ohne", "keine", "maximal", "mindestens", "nur"]):
            scores["CONSTRAINT"] += 2.0

        # Quality-Bonus
        if any(marker in text for marker in ["clean code", "solid", "wartbar", "lesbar", "robust"]):
            scores["QUALITY_REQUIREMENT"] += 3.0

        # Functional Requirement: konkrete fachliche Aktion
        if action in {"validieren", "berechnen", "traversieren", "durchsuchen", "parsen", "sortieren", "filtern"}:
            scores["FUNCTIONAL_REQUIREMENT"] += 2.0


    # Penalties
    def apply_penalties(self, candidate: Candidate, scores):
        target = self.normalize(candidate.target)
        action = self.normalize(candidate.action)
        text = self.normalize(candidate.text)

        # Generic Tasks
        if "TASK" in scores:
            if any(word in target for word in self.generic_targets):
                scores["TASK"] -= 2.0

        # Output soll selten Task sein
        if action in {"ausgeben", "anzeigen", "zurückgeben", "liefern", "speichern"}:
            scores["TASK"] -= 2.0

        # Bereits vorhandene Dinge sind selten neue TASKs
        if any(marker in text for marker in ["bereits", "vorhanden", "existiert", "schon implementiert"]):
            scores["TASK"] -= 1.5

    # Helpers
    def normalize(self, text: Optional[str]) -> str:
        return (text or "").lower().strip()