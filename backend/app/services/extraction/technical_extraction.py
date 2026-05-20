import re
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Set

from app.models.response_models import (
    PreprocessingResponse,
    Candidate
)

from app.services.config.technical_extraction_rules import (
    LANGUAGES,
    TECH_STACK,
    FILE_PATTERN,
    PATH_PATTERN,
    FUNCTION_CALL_PATTERN,
    PYTHON_DEF_PATTERN,
    JAVA_LIKE_METHOD_PATTERN,
    ENDPOINT_PATTERN
)

class TechnicalExtraction:

    def __init__(self):
        self.languages = LANGUAGES
        self.tech_stack = TECH_STACK
        self.file_pattern = FILE_PATTERN
        self.path_pattern = PATH_PATTERN
        self.function_call_pattern = FUNCTION_CALL_PATTERN
        self.python_def_pattern = PYTHON_DEF_PATTERN
        self.java_like_method_pattern = JAVA_LIKE_METHOD_PATTERN
        self.endpoint_pattern = ENDPOINT_PATTERN

    def extract(self, preprocessing_response: PreprocessingResponse) -> List[Candidate]:

        candidates: List[Candidate] = []
        seen: Set[str] = set()

        candidates.extend(
            self.extract_protected_entity_candidates(
                preprocessing_response=preprocessing_response,
                seen=seen
            )
        )

        for sentence in preprocessing_response.sentences:
            text = sentence.cleaned_text

            candidates.extend(
                self.extract_dictionary_candidates(
                    text=text,
                    source_sentence=sentence.original_text,
                    sentence_index=sentence.sentence_index,
                    seen=seen
                )
            )

            candidates.extend(
                self.extract_regex_candidates(
                    text=text,
                    source_sentence=sentence.original_text,
                    sentence_index=sentence.sentence_index,
                    seen=seen
                )
            )

        return candidates

    # Handle Protected Entities
    def extract_protected_entity_candidates(
        self,
        preprocessing_response: PreprocessingResponse,
        seen: Set[str]
    ) -> List[Candidate]:

        candidates = []

        for entity in preprocessing_response.protected_entities:

            role = self.map_protected_entity_to_role(
                entity.entity_type
            )

            if not role:
                continue

            source_sentence = self.find_source_sentence_for_placeholder(
                placeholder=entity.placeholder,
                preprocessing_response=preprocessing_response
            )

            sentence_index = (
                source_sentence.sentence_index
                if source_sentence
                else -1
            )

            source_text = (
                source_sentence.original_text
                if source_sentence
                else preprocessing_response.cleaned_text
            )

            candidate = self.create_candidate(
                text=entity.original,
                role=role,
                source_sentence=source_text,
                sentence_index=sentence_index,
                extraction_type="protected_entity",
                confidence=1.0,
                seen=seen
            )

            if candidate:
                candidate.metadata["placeholder"] = entity.placeholder
                candidate.metadata["entity_type"] = entity.entity_type
                candidates.append(candidate)

        return candidates

    def map_protected_entity_to_role(
        self,
        entity_type: str
    ) -> Optional[str]:

        mapping = {
            "FILE": "FILE_STRUCTURE",
            "CODE_BLOCK": "INTERFACE",
            "FUNCTION": "INTERFACE",
            "METHOD": "INTERFACE",
            "ENDPOINT": "INTERFACE",
        }

        return mapping.get(entity_type)
    
    def find_source_sentence_for_placeholder(
        self,
        placeholder: str,
        preprocessing_response: PreprocessingResponse
    ):

        for sentence in preprocessing_response.sentences:
            if placeholder in sentence.cleaned_text:
                return sentence

        return None

    # Dictionary
    def extract_dictionary_candidates(
        self,
        text: str,
        source_sentence: str,
        sentence_index: int,
        seen: Set[str]
    ) -> List[Candidate]:

        candidates = []

        candidates.extend(
            self.find_terms(
                text=text,
                dictionary=self.languages,
                role="LANGUAGE",
                source_sentence=source_sentence,
                sentence_index=sentence_index,
                seen=seen
            )
        )

        candidates.extend(
            self.find_terms(
                text=text,
                dictionary=self.tech_stack,
                role="TECH_STACK",
                source_sentence=source_sentence,
                sentence_index=sentence_index,
                seen=seen
            )
        )

        return candidates

    def find_terms(
        self,
        text: str,
        dictionary: Dict[str, str],
        role: str,
        source_sentence: str,
        sentence_index: int,
        seen: Set[str]
    ) -> List[Candidate]:

        candidates = []
        normalized_text = self.normalize_text(text)

        for key, canonical in dictionary.items():
            normalized_key = self.normalize_text(key)

            if self.contains_term(normalized_text, normalized_key):
                candidate = self.create_candidate(
                    text=canonical,
                    role=role,
                    source_sentence=source_sentence,
                    sentence_index=sentence_index,
                    extraction_type="dictionary",
                    confidence=1.0,
                    seen=seen
                )

                if candidate:
                    candidates.append(candidate)

        candidates.extend(
            self.find_fuzzy_terms(
                text=text,
                dictionary=dictionary,
                role=role,
                source_sentence=source_sentence,
                sentence_index=sentence_index,
                seen=seen
            )
        )

        return candidates

    def find_fuzzy_terms(
        self,
        text: str,
        dictionary: Dict[str, str],
        role: str,
        source_sentence: str,
        sentence_index: int,
        seen: Set[str]
    ) -> List[Candidate]:

        candidates = []

        words = re.findall(r"[a-zA-Z+#.\-]{2,}", text)

        for word in words:
            normalized_word = self.normalize_text(word)

            for key, canonical in dictionary.items():
                normalized_key = self.normalize_text(key)

                if abs(len(normalized_word) - len(normalized_key)) > 3:
                    continue

                similarity = self.similarity(
                    normalized_word,
                    normalized_key
                )

                if similarity >= 0.88:
                    candidate = self.create_candidate(
                        text=canonical,
                        role=role,
                        source_sentence=source_sentence,
                        sentence_index=sentence_index,
                        extraction_type="fuzzy_dictionary",
                        confidence=round(similarity, 2),
                        seen=seen
                    )

                    if candidate:
                        candidates.append(candidate)

        return candidates

    # Regex
    def extract_regex_candidates(
        self,
        text: str,
        source_sentence: str,
        sentence_index: int,
        seen: Set[str]
    ) -> List[Candidate]:

        candidates = []

        for match in self.file_pattern.finditer(text):
            candidate = self.create_candidate(
                text=match.group().strip(),
                role="FILE_STRUCTURE",
                source_sentence=source_sentence,
                sentence_index=sentence_index,
                extraction_type="regex_file",
                confidence=1.0,
                seen=seen
            )

            if candidate:
                candidates.append(candidate)

        for match in self.path_pattern.finditer(text):
            candidate = self.create_candidate(
                text=match.group().strip(),
                role="FILE_STRUCTURE",
                source_sentence=source_sentence,
                sentence_index=sentence_index,
                extraction_type="regex_path",
                confidence=0.95,
                seen=seen
            )

            if candidate:
                candidates.append(candidate)

        for pattern, extraction_type in [
            (self.python_def_pattern, "regex_python_def"),
            (self.java_like_method_pattern, "regex_method_signature"),
            (self.endpoint_pattern, "regex_endpoint"),
            (self.function_call_pattern, "regex_function_call"),
        ]:
            for match in pattern.finditer(text):
                candidate = self.create_candidate(
                    text=match.group().strip(),
                    role="INTERFACE",
                    source_sentence=source_sentence,
                    sentence_index=sentence_index,
                    extraction_type=extraction_type,
                    confidence=1.0,
                    seen=seen
                )

                if candidate:
                    candidates.append(candidate)

        return candidates

    # Helpers
    def create_candidate(
        self,
        text: str,
        role: str,
        source_sentence: str,
        sentence_index: int,
        extraction_type: str,
        confidence: float,
        seen: Set[str]
    ) -> Optional[Candidate]:

        normalized = self.normalize_text(text)

        key = f"{role}:{normalized}:{sentence_index}"

        if key in seen:
            return None

        seen.add(key)

        return Candidate(
            text=text,
            action=None,
            target=text,
            modifiers=[],
            source_sentence=source_sentence,
            metadata={
                "sentence_index": sentence_index,
                "role": role,
                "confidence": confidence,
                "extraction_type": extraction_type,
                "technical": True
            }
        )

    def normalize_text(self, text: str) -> str:
        return (
            text
            .lower()
            .replace("_", " ")
            .replace("-", " ")
            .strip()
        )

    def contains_term(
        self,
        text: str,
        term: str
    ) -> bool:

        pattern = r"(?<!\w)" + re.escape(term) + r"(?!\w)"

        return re.search(pattern, text, re.IGNORECASE) is not None

    def similarity(
        self,
        first: str,
        second: str
    ) -> float:

        return SequenceMatcher(
            None,
            first,
            second
        ).ratio()