# Process Input Prompt
# -> Trim, normalize, detect language, segment
# returns: cleaned & segmented Input 

import re
from typing import List, Tuple
import spacy
from app.models.response_models import SentenceData, ProtectedEntity, PreprocessingResponse
from app.services.config.preprocessing_rules import (
    FILE_PATTERN,
    COMPLEXITY_PATTERN,
    ASTAR_PATTERN,
    CODE_BLOCK_PATTERN,
    BULLET_PATTERN
)

class PreprocessingService:

    def __init__(self):
        self.nlp = spacy.load("de_core_news_sm")

    def preprocess(self, text: str) -> PreprocessingResponse:
        original_text = text or ""
        
        # 1. Normalize whitespace
        cleaned_text = self.normalize_whitespace(original_text)

        # 2. Normalize list formatting
        cleaned_text = self.normalize_bullets(cleaned_text)

        # 3. Protect technical entities
        cleaned_text, protected_entities = self.protect_entities(cleaned_text)

        # 4. Detect language
        language = self.detect_language(cleaned_text)

        # 5. Sentence segmentation
        sentences = self.split_sentences(cleaned_text)

        # 6. Build response
        response = PreprocessingResponse(
            original_text=original_text,
            cleaned_text=cleaned_text,
            language=language,
            sentences=sentences,
            protected_entities=protected_entities,
            metadata={}
        )
        
        return response
    
    def normalize_whitespace(self, text: str) -> str:
        text = text.replace("\t", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def normalize_bullets(self, text: str) -> str:
        text = BULLET_PATTERN.sub(". ", text)
        return text

    def protect_entities(self, text: str) -> Tuple[str, List[ProtectedEntity]]:
        protected_entities = []
        counter = {
            "FILE": 0,
            "ALG": 0,
            "COMPLEXITY": 0,
            "CODE": 0
        }
        
        # mapping = {
        #   "FILE": "FILE_STRUCTURE",       done
        #   "ALG": "TECH_STACK",            open
        #   "COMPLEXITY": "CONSTRAINT",     open
        #   "CODE": None                    open
        # } 

        def replace_file(match):

            original = match.group()

            placeholder = f"FILE_{counter['FILE']}"

            counter["FILE"] += 1

            protected_entities.append(
                ProtectedEntity(
                    placeholder=placeholder,
                    original=original,
                    entity_type="FILE"
                )
            )

            return placeholder

        text = FILE_PATTERN.sub(replace_file, text)
    
        def replace_astar(match):

            original = match.group()

            placeholder = f"ALG_{counter['ALG']}"

            counter["ALG"] += 1

            protected_entities.append(
                ProtectedEntity(
                    placeholder=placeholder,
                    original=original,
                    entity_type="ALGORITHM"
                )
            )

            return placeholder

        text = ASTAR_PATTERN.sub(replace_astar, text)
    
        def replace_complexity(match):

            original = match.group()

            placeholder = f"COMPLEXITY_{counter['COMPLEXITY']}"

            counter["COMPLEXITY"] += 1

            protected_entities.append(
                ProtectedEntity(
                    placeholder=placeholder,
                    original=original,
                    entity_type="COMPLEXITY"
                )
            )

            return placeholder

        text = COMPLEXITY_PATTERN.sub(replace_complexity, text)
    
        def replace_code(match):

            original = match.group()

            placeholder = f"CODE_{counter['CODE']}"

            counter["CODE"] += 1

            protected_entities.append(
                ProtectedEntity(
                    placeholder=placeholder,
                    original=original,
                    entity_type="CODE_BLOCK"
                )
            )

            return placeholder

        text = CODE_BLOCK_PATTERN.sub(replace_code, text)

        return text, protected_entities
    
    def detect_language(self, text: str) -> str:
        # Placeholder
        # später optional langdetect/fasttext
        return "de"

    def split_sentences(
        self,
        text: str
    ) -> List[SentenceData]:

        doc = self.nlp(text)

        sentences = []

        for idx, sent in enumerate(doc.sents):

            sentence_text = sent.text.strip()

            if not sentence_text:
                continue

            sentences.append(
                SentenceData(
                    sentence_index=idx,
                    original_text=sentence_text,
                    cleaned_text=sentence_text
                )
            )

        return sentences
    
    def restore_placeholders(
        self,
        text: str,
        protected_entities: List[ProtectedEntity]
    ) -> str:

        restored = text

        for entity in protected_entities:
            restored = restored.replace(
                entity.placeholder,
                entity.original
            )

        return restored