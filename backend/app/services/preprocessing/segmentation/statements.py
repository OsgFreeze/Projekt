from typing import List, Sequence, Tuple
from spacy.tokens import Token

from app.services.preprocessing.segmentation.utils import sort_tokens


def split_statements_at_adp_before_verb(statements: Sequence[Sequence[Token]]) -> List[List[Token]]:
    splitted: List[List[Token]] = []

    for tokens in statements:
        verb_index = next((i for i, token in enumerate(tokens) if token.pos_ == "VERB"), None)

        if verb_index is None:
            splitted.append(list(tokens))
            continue

        split_index = next(
            (i for i in range(verb_index - 1, -1, -1) if tokens[i].pos_ == "ADP"),
            None,
        )

        if split_index is None:
            splitted.append(list(tokens))
            continue

        left = list(tokens[:split_index])
        right = list(tokens[split_index:])

        if left:
            splitted.append(left)
        if right:
            splitted.append(right)

    return splitted


def remove_redundant_statements(statements: Sequence[Sequence[Token]]) -> List[List[Token]]:
    trimmed: List[List[Token]] = []

    for statement in statements:
        statement_ids = [t.i for t in statement]
        is_redundant = False

        for other in statements:
            other_ids = [t.i for t in other]

            if statement_ids == other_ids:
                continue

            if all(i in other_ids for i in statement_ids):
                is_redundant = True
                break

        if not is_redundant:
            trimmed.append(list(statement))

    return trimmed


def remove_duplicate_statements(statements: Sequence[Sequence[Token]]) -> List[List[Token]]:
    unique_statements: List[List[Token]] = []
    seen: set[Tuple[int, ...]] = set()

    for tokens in statements:
        key = tuple(t.i for t in tokens)
        if key not in seen:
            unique_statements.append(list(tokens))
            seen.add(key)

    return unique_statements


def cut_overlapping_prefixes(statements: Sequence[Sequence[Token]]) -> List[List[Token]]:
    final: List[List[Token]] = []
    used_token_ids: set[int] = set()

    for tokens in statements:
        cut_index = 0
        while cut_index < len(tokens) and tokens[cut_index].i in used_token_ids:
            token = tokens[cut_index]

            if token.tag_ == "VAFIN":
                has_subject = any(child.dep_ == "sb" for child in token.children)
                if has_subject:
                    break

            if token.pos_ == "NOUN":
                cut_index += 1
                continue

            cut_index += 1

        trimmed_tokens = list(tokens[cut_index:])

        if trimmed_tokens:
            final.append(trimmed_tokens)
            for token in trimmed_tokens:
                used_token_ids.add(token.i)

    return final


def _get_common_suffix_length(left: Sequence[Token], right: Sequence[Token]) -> int:
    max_len = min(len(left), len(right))
    count = 0

    for i in range(1, max_len + 1):
        if left[-i].text == right[-i].text:
            count += 1
        else:
            break

    return count


def _get_last_verb(tokens: Sequence[Token]) -> Token | None:
    for token in reversed(tokens):
        if token.pos_ in ("VERB", "AUX"):
            return token
    return None


def merge_coordinated_statement(statements: Sequence[Sequence[Token]]) -> List[List[Token]]:
    if not statements:
        return []

    merged: List[List[Token]] = [list(statements[0])]

    for current in statements[1:]:
        current_tokens = list(current)

        if not current_tokens:
            continue

        starts_with_cconj = current_tokens[0].pos_ == "CCONJ"

        if not starts_with_cconj:
            merged.append(current_tokens)
            continue

        previous_tokens = merged[-1]
        overlap_len = _get_common_suffix_length(previous_tokens, current_tokens[1:])

        if overlap_len > 0:
            new_tokens = previous_tokens[:-overlap_len] + current_tokens
            merged[-1] = sort_tokens(new_tokens)
        else:
            previous_last_verb = _get_last_verb(previous_tokens)
            current_last_verb = _get_last_verb(current_tokens)

            if (
                previous_last_verb is not None
                and current_last_verb is not None
                and previous_last_verb.lemma_ == current_last_verb.lemma_
            ):
                current_without_last_verb = current_tokens[:-1]
                new_tokens = previous_tokens[:-1] + current_without_last_verb + [previous_tokens[-1]]
                merged[-1] = sort_tokens(new_tokens)
            else:
                merged.append(current_tokens)

    return merged
