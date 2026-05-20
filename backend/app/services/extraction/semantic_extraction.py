import spacy
from spacy.tokens import Token
from typing import List, Optional

from app.models.response_models import (
    PreprocessingResponse, 
    SentenceData, 
    Candidate
)

from app.services.config.semantic_extraction_rules import (
    GENERIC_VERBS,
    LOCATION_FOCUSED_VERBS
)

class SemanticExtraction:

    def __init__(self):
        self.nlp = spacy.load("de_core_news_sm")
        self.generic_verbs = GENERIC_VERBS
        self.location_focused_verbs = LOCATION_FOCUSED_VERBS

    def extract(self, preprocessing_response: PreprocessingResponse):

        candidates = []

        for sentence_data in preprocessing_response.sentences:
            sentence_candidates = self.extract_candidates(sentence_data)
            candidates.extend(sentence_candidates)        

        return candidates

    def extract_candidates(self, sentence_data: SentenceData) -> List[Candidate]:
        sentence = sentence_data.cleaned_text
        doc = self.nlp(sentence)
        candidates = []

        for token in doc:
            if not self.is_candidate_verb(token):
                continue
            candidate = self.build_candidate(
                token=token,
                sentence_data=sentence_data
            )

            if candidate:
                candidates.append(candidate)

        return candidates


    def is_candidate_verb(self, token: Token) -> bool:

        # Nur Verben
        if token.pos_ not in {"VERB", "AUX"}:
            return False

        # Nur Vollverben
        if not token.tag_.startswith("VV"):
            return False

        # Hilfs-/Kopulaverben ignorieren
        if token.dep_ in {"aux", "cop"}:
            return False

        lemma = token.lemma_.lower()

        # Sehr generische Verben ignorieren
        if lemma in self.generic_verbs:
            return False

        # Klammern ignorieren
        if token.dep_ == "par":
            return False

        return True

    # Build Candidate
    def build_candidate(self, token: Token, sentence_data: SentenceData) -> Candidate | None:

        action = token.lemma_.lower()

        modifiers = self.extract_modifiers(token)

        if action in self.location_focused_verbs:
            location_phrase = self.extract_location_phrase(token)

            if location_phrase:
                target = location_phrase
                modifiers = [m for m in modifiers if m != target]
            elif modifiers:
                target = modifiers[0]
                modifiers = [m for m in modifiers if m != target]
            else:
                target = self.extract_target(token)
        else:
            target = self.extract_target(token)

            if not target and modifiers:
                target = modifiers[0]

        if not self.is_valid_candidate(target, modifiers):
            return None

        candidate_text = self.build_candidate_text(
            target=target,
            modifiers=modifiers,
            action=action
        )

        if not candidate_text:
            return None

        return Candidate(
            text=candidate_text,
            action=action,
            target=target,
            modifiers=modifiers,
            source_sentence=sentence_data.original_text,
            metadata={
                "sentence_index": sentence_data.sentence_index,
                "token_index": token.i,
                "dependency": token.dep_,
                "pos": token.pos_,
                "tag": token.tag_
            }
        )
        
    # Extract Target
    def extract_target(self, verb_token: Token) -> Optional[str]:
        # Direktes Objekt suchen
        for child in verb_token.children:
            if child.dep_ in {"oa", "obj"}:
                return self.get_subtree_text(child)

        # Partizipien / Passiv
        if verb_token.tag_ == "VVPP":
            coordinated_np = self.extract_coordinated_left_noun_phrase(verb_token)
            if coordinated_np:
                return coordinated_np

            closest_np = self.extract_closest_left_noun_phrase(verb_token)
            if closest_np:
                return closest_np

            largest_np = self.extract_largest_left_noun_phrase(verb_token)
            if largest_np:
                return largest_np

        # Subjektartige Konstruktionen
        for child in verb_token.children:
            if child.dep_ in {"sb"}:
                return self.get_subtree_text(child)

        
        # Größte linke NP
        largest_np = (self.extract_largest_left_noun_phrase(verb_token))
        if largest_np:
            return largest_np

        # Noun Chunks Fallback
        sentence = verb_token.sent
        for chunk in sentence.noun_chunks:
            if chunk.root.pos_ in {"NOUN", "PROPN"}:
                return chunk.text


        return None
        
    # Extract largest Noun Phrase
    def extract_largest_left_noun_phrase(self, verb_token: Token):
        candidates = []
        for chunk in verb_token.sent.noun_chunks:
            if chunk.end <= verb_token.i:
                candidates.append(chunk)
        
        if not candidates:
            return None
        
        largest = max(candidates, key=lambda c: (len(c.text), -abs(verb_token.i - c.end)))

        return largest.text

    # Extract closest Noun Phrase
    def extract_closest_left_noun_phrase(self, verb_token: Token):
        candidates = []

        for chunk in verb_token.sent.noun_chunks:
            if chunk.end <= verb_token.i:
                if chunk.root.pos_ not in {"NOUN", "PROPN", "PRON"}:
                    continue
                distance = verb_token.i - chunk.end
                candidates.append((distance, chunk))

        if not candidates:
            return None

        closest = min(candidates, key=lambda x: x[0])

        return closest[1].text

    # Extract location Phrase
    def extract_location_phrase(self, verb_token: Token) -> Optional[str]:

        location_markers = {"in", "im", "unter", "bei", "auf", "innerhalb"}

        tokens = list(verb_token.sent)

        for i, token in enumerate(tokens):
            if token.i >= verb_token.i:
                break

            if token.text.lower() in location_markers:
                phrase_tokens = []

                for next_token in tokens[i:]:
                    if next_token.i >= verb_token.i:
                        break

                    phrase_tokens.append(next_token.text)

                phrase = " ".join(phrase_tokens).strip()

                if phrase:
                    return phrase

        return None

    # Extract coordinated Noun Phrase
    def extract_coordinated_left_noun_phrase(self, verb_token: Token) -> Optional[str]:

        tokens = [
            token for token in verb_token.sent
            if token.i < verb_token.i
        ]

        if not tokens:
            return None

        text_before_verb = " ".join(token.text for token in tokens).strip()

        # Nur verwenden, wenn es wirklich wie eine koordinierte NP aussieht
        if " und " not in text_before_verb:
            return None

        if len(text_before_verb.split()) < 3:
            return None

        return text_before_verb

    # Extract Modifiers
    def extract_modifiers(self, verb_token: Token) -> List[str]:
        modifiers = []
        for child in verb_token.children:

            # Modifier / Präpositionalphrasen
            if child.dep_ in {"mo", "mnr", "nk", "pg", "op"}:

                phrase = self.get_subtree_text(child)

                if self.is_valid_modifier(phrase):
                    modifiers.append(phrase)

        return modifiers

    # Modifier Validation
    def is_valid_modifier(self, text: str) -> bool:
        text = text.strip()
        if not text:
            return False

        # zu kurze Modifier ignorieren
        if len(text.split()) < 2:
            return False

        return True
        
    # Candidate Validation
    def is_valid_candidate(self, target, modifiers):
        if not target and not modifiers:
            return False
        return True

    # Build Candidate Text
    def build_candidate_text(self, target: Optional[str], modifiers: List[str], action: str) -> str:

        parts = []

        if target:
            parts.append(target)

        if modifiers:
            for modifier in modifiers:
                if modifier != target:
                    parts.append(modifier)

        parts.append(action)

        return " ".join(parts).strip()

    # Helper
    def get_subtree_text(self, token: Token) -> str:
        return " ".join([t.text for t in token.subtree])