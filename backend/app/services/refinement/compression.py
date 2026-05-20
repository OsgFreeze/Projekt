import re
import spacy
from typing import List

from app.models.response_models import ClassifiedCandidate
from app.services.config.refinement_rules import KEEP_WORDS, TECHNICAL_ROLES

class Compression:

    def __init__(self):
        self.nlp = spacy.load("de_core_news_sm")
        self.protected_tokens_pattern = re.compile(r"\b(FILE_\d+|ALG_\d+|COMPLEXITY_\d+|CODE_\d+)\b")
        self.keep_words = KEEP_WORDS
        self.technical_roles = TECHNICAL_ROLES

    def process(self, candidates: List[ClassifiedCandidate]) -> List[ClassifiedCandidate]:

        for candidate in candidates:
            role = candidate.classification.role
            original = candidate.candidate.text
            compressed = self.compress_text(text=original, role=role)
            candidate.candidate.metadata["text_before_compression"] = original
            candidate.candidate.text = compressed

        return candidates

    def compress_text(self, text: str, role: str) -> str:

        if role in self.technical_roles:
            return text.strip()

        doc = self.nlp(text)

        tokens = []

        for token in doc:
            if self.should_keep_token(token):
                tokens.append(token.text)

        compressed = " ".join(tokens)
        compressed = self.normalize_spacing(compressed)

        if not compressed:
            return text.strip()

        return compressed

    def should_keep_token(self, token) -> bool:
        lower = token.text.lower()

        # Platzhalter und technische Tokens behalten
        if self.protected_tokens_pattern.fullmatch(token.text):
            return True

        # Negationen / Constraints behalten
        if lower in self.keep_words:
            return True

        # Satzzeichen entfernen
        if token.is_punct or token.is_space:
            return False

        # Artikel, Pronomen, Hilfsverben vorsichtig entfernen
        if token.pos_ in {"DET", "PRON", "AUX"}:
            return False

        # Partikeln meist entfernen, aber nicht Negationen
        if token.pos_ == "PART":
            return False

        return True

    def normalize_spacing(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s+([,.;:])", r"\1", text)
        return text.strip()