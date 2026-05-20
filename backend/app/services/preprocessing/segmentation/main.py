import spacy
from typing import List

from .adverbs import ensure_all_adverbs_in_statements
from .chunks import expand_chunk_roots_to_heads, get_relevant_noun_chunks, merge_chunks_with_heads
from .statements import (
    cut_overlapping_prefixes,
    merge_coordinated_statement,
    remove_duplicate_statements,
    remove_redundant_statements,
    split_statements_at_adp_before_verb,
)
from .verbs import ensure_all_verbs_in_statements
from .utils import tokens_to_strings


class SimpleSpacySegmenter:
    def __init__(self, model_name: str = "de_core_news_sm"):
        self.nlp = spacy.load(model_name)

    def get_segments(self, sentences: List[str]) -> List[str]:
        segments: List[str] = []
        
        if sentences == []:
            return sentences
        
        for sent in sentences:
            segments.extend(self.segment(sent))

        return segments

    def segment(self, text: str) -> List[str]:
        doc = self.nlp(text)
        
        chunks = get_relevant_noun_chunks(doc)
        chunk_heads = expand_chunk_roots_to_heads(chunks)
        merged_statements = merge_chunks_with_heads(chunks, chunk_heads)
        split_statements = split_statements_at_adp_before_verb(merged_statements)
        trimmed_statements = remove_redundant_statements(split_statements)
        unique_statements = remove_duplicate_statements(trimmed_statements)
        cleaned_statements = cut_overlapping_prefixes(unique_statements)
        coordinated_statements = merge_coordinated_statement(cleaned_statements)
        final_statements = ensure_all_verbs_in_statements(doc, coordinated_statements)
        final_statements = ensure_all_adverbs_in_statements(doc, final_statements)
        final_statements = tokens_to_strings(final_statements)

        return final_statements
    
