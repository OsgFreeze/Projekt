from typing import List, Sequence
from spacy.tokens import Doc, Span, Token

from app.services.preprocessing.segmentation.utils import sort_tokens

# get noun chunks
def get_relevant_noun_chunks(doc: Doc) -> List[Span]:
    return [chunk for chunk in doc.noun_chunks if chunk.root.pos_ != "PRON"]

# expand noun chunks
def expand_chunk_roots_to_heads(chunks: Sequence[Span]) -> List[List[Token]]:
    results: List[List[Token]] = []

    for chunk in chunks:
        collected = [chunk.root]
        seen_ids = {chunk.root.i}
        current = chunk.root

        while True:
            head = current.head

            if head == current or head.i in seen_ids:
                break

            collected.append(head)
            seen_ids.add(head.i)

            if head.pos_ == "VERB" or head.pos_ == "AUX":
                break

            current = head

        results.append(sort_tokens(collected))

    return results

# merge noun chunks & expanded noun chunks
def merge_chunks_with_heads(
    chunks: Sequence[Span],
    head_paths: Sequence[Sequence[Token]],
) -> List[List[Token]]:
    merged: List[List[Token]] = []

    for chunk, stmt_tokens in zip(chunks, head_paths):
        all_tokens = set(chunk)
        all_tokens.update(stmt_tokens)

        _add_missing_articles(all_tokens)
        _remove_verbs_with_gaps(all_tokens)

        merged.append(sort_tokens(all_tokens))

    return merged

def _add_missing_articles(all_tokens: set[Token]) -> None:
    for token in list(all_tokens):
        if token.pos_ == "NOUN":
            j = token.i - 1
            while j >= 0:
                prev_token = token.doc[j]
                if prev_token.pos_ == "DET":
                    all_tokens.add(prev_token)
                    break
                if prev_token.pos_ in ("ADJ", "ADV"):
                    j -= 1
                    continue
                break


def _remove_verbs_with_gaps(all_tokens: set[Token]) -> None:
    verbs_to_remove: List[Token] = []

    for token in all_tokens:
        if token.pos_ != "VERB":
            continue

        token_ids = {t.i for t in all_tokens}
        min_i = min(token_ids)
        max_i = max(token_ids)

        if token.i == max_i:
            between_range = range(min_i, token.i)
        elif token.i == min_i:
            between_range = range(token.i + 1, max_i + 1)
        else:
            continue

        gap = False
        for i in between_range:
            doc_token = token.doc[i]
            if doc_token.pos_ == "PUNCT":
                continue
            if i not in token_ids:
                gap = True
                break

        if gap:
            verbs_to_remove.append(token)

    for verb in verbs_to_remove:
        all_tokens.discard(verb)



