from typing import List, Sequence
from spacy.tokens import Doc, Token

from app.services.preprocessing.segmentation.utils import sort_tokens


def extract_adverbs(doc: Doc) -> List[Token]:
    adverbs: List[Token] = []
    seen: set[int] = set()

    for token in doc:
        if token.pos_ == "ADV":
            if token.i not in seen:
                adverbs.append(token)
                seen.add(token.i)

    return adverbs


def ensure_all_adverbs_in_statements(
    doc: Doc,
    final_statements: Sequence[Sequence[Token]],
) -> List[List[Token]]:
    updated_statements: List[List[Token]] = [list(statement) for statement in final_statements]
    adverbs = extract_adverbs(doc)

    all_statement_ids = {t.i for statement in updated_statements for t in statement}

    for adv in adverbs:
        if adv.i in all_statement_ids:
            continue

        head = adv.head
        best_index = None

        for i, statement in enumerate(updated_statements):
            statement_ids = {t.i for t in statement}

            if head.i in statement_ids:
                best_index = i
                break

            if head.pos_ in ("VERB", "AUX"):
                if any(
                    t.pos_ in ("VERB", "AUX") and t.lemma_ == head.lemma_
                    for t in statement
                ):
                    best_index = i
                    break

        if best_index is None:
            continue

        statement = updated_statements[best_index]
        merged = set(statement)
        merged.add(adv)

        updated_statements[best_index] = sort_tokens(list(merged))

    return updated_statements
