from typing import List, Sequence
from spacy.tokens import Doc, Token

from app.services.preprocessing.segmentation.utils import sort_tokens


def _build_verb_group(verb: Token) -> List[Token]:
    group = [verb]

    if verb.head.pos_ == "AUX":
        group.append(verb.head)

    return sort_tokens(group)


def _add_verb_group(
    verbs: List[List[Token]],
    seen: set[tuple[int, ...]],
    group: Sequence[Token],
) -> None:
    key = tuple(token.i for token in group)

    if key not in seen:
        verbs.append(list(group))
        seen.add(key)


def _add_coordinated_verb_group(
    doc: Doc,
    verb: Token,
    verbs: List[List[Token]],
    seen: set[tuple[int, ...]],
) -> None:
    cconj_index = None

    for i in range(verb.i + 1, len(doc)):
        next_token = doc[i]

        if next_token.pos_ == "PUNCT":
            continue

        if next_token.pos_ == "CCONJ":
            cconj_index = i
            break

        if next_token.pos_ in ("VERB", "AUX", "NOUN", "PROPN", "PRON"):
            break

    if cconj_index is None:
        return

    aux_token = None
    verb_token = None

    for i in range(cconj_index + 1, len(doc)):
        next_token = doc[i]

        if next_token.pos_ == "PUNCT":
            continue

        if next_token.pos_ == "AUX" and aux_token is None:
            aux_token = next_token
            continue

        if next_token.pos_ == "VERB":
            verb_token = next_token
            break

        if next_token.pos_ in ("NOUN", "PROPN", "PRON"):
            break

    if verb_token is not None:
        group = [verb_token]
        if aux_token is not None:
            group.append(aux_token)
        _add_verb_group(verbs, seen, sort_tokens(group))


def extract_verbs(doc: Doc) -> List[List[Token]]:
    verbs: List[List[Token]] = []
    seen: set[tuple[int, ...]] = set()

    for token in doc:
        if token.pos_ == "VERB":
            _add_verb_group(verbs, seen, _build_verb_group(token))
            _add_coordinated_verb_group(doc, token, verbs, seen)

        if token.i == 0 and token.head.pos_ in ("NOUN", "PROPN") and token.pos_ != "DET":
            key = (token.i,)
            if key not in seen:
                verbs.append([token])
                seen.add(key)

    return verbs


def get_missing_verb_groups(
    verb_groups: Sequence[Sequence[Token]],
    final_statements: Sequence[Sequence[Token]],
) -> List[List[Token]]:
    missing: List[List[Token]] = []

    for verb_group in verb_groups:
        verb_ids = {t.i for t in verb_group}

        found = False
        for statement in final_statements:
            statement_ids = {t.i for t in statement}
            if verb_ids.issubset(statement_ids):
                found = True
                break

        if not found:
            missing.append(list(verb_group))

    return missing


def integrate_missing_verbs_via_aux(
    final_statements: Sequence[Sequence[Token]],
    missing_verb_groups: Sequence[Sequence[Token]],
) -> List[List[Token]]:
    updated_statements: List[List[Token]] = [list(statement) for statement in final_statements]

    for i, statement in enumerate(updated_statements):
        statement_ids = {t.i for t in statement}
        tokens_to_add: List[Token] = []

        for verb_group in missing_verb_groups:
            aux_tokens = [t for t in verb_group if t.pos_ == "AUX"]
            verb_tokens = [t for t in verb_group if t.pos_ == "VERB"]

            if not aux_tokens or not verb_tokens:
                continue

            aux_token = aux_tokens[0]
            verb_token = verb_tokens[0]

            has_aux = aux_token.i in statement_ids
            has_verb = verb_token.i in statement_ids

            if has_aux != has_verb:
                if not has_aux:
                    tokens_to_add.append(aux_token)
                if not has_verb:
                    tokens_to_add.append(verb_token)

        if tokens_to_add:
            merged = set(statement)
            merged.update(tokens_to_add)
            updated_statements[i] = sort_tokens(list(merged))

    return updated_statements

def merge_statements_sharing_wrapped_verb_group(
    final_statements: Sequence[Sequence[Token]],
    verb_groups: Sequence[Sequence[Token]],
) -> List[List[Token]]:
    statements = [list(statement) for statement in final_statements]
    consumed_indices: set[int] = set()
    merged_results: List[List[Token]] = []

    for verb_group in verb_groups:
        aux_tokens = [t for t in verb_group if t.pos_ == "AUX"]
        verb_tokens = [t for t in verb_group if t.pos_ == "VERB"]

        if len(aux_tokens) != 1 or len(verb_tokens) != 1:
            continue

        aux_token = aux_tokens[0]
        verb_token = verb_tokens[0]

        matching_indices = []

        for i, statement in enumerate(statements):
            statement_ids = {t.i for t in statement}
            if aux_token.i in statement_ids and verb_token.i in statement_ids:
                matching_indices.append(i)

        if len(matching_indices) != 2:
            continue

        i1, i2 = matching_indices
        s1 = statements[i1]
        s2 = statements[i2]

        if i1 in consumed_indices or i2 in consumed_indices:
            continue

        if _has_adjacent_aux_verb(s1, aux_token, verb_token) and _is_wrapped_by_aux_verb(s2, aux_token, verb_token):
            merged_results.append(_merge_two_statements(s1, s2))
            consumed_indices.update({i1, i2})
        elif _has_adjacent_aux_verb(s2, aux_token, verb_token) and _is_wrapped_by_aux_verb(s1, aux_token, verb_token):
            merged_results.append(_merge_two_statements(s1, s2))
            consumed_indices.update({i1, i2})

    for i, statement in enumerate(statements):
        if i not in consumed_indices:
            merged_results.append(statement)

    return [sort_tokens(statement) for statement in merged_results]


def _has_adjacent_aux_verb(
    statement: Sequence[Token],
    aux_token: Token,
    verb_token: Token,
) -> bool:
    for i in range(len(statement) - 1):
        if statement[i].i == aux_token.i and statement[i + 1].i == verb_token.i:
            return True
    return False


def _is_wrapped_by_aux_verb(
    statement: Sequence[Token],
    aux_token: Token,
    verb_token: Token,
) -> bool:
    if not statement:
        return False
    return statement[0].i == aux_token.i and statement[-1].i == verb_token.i


def _merge_two_statements(
    left: Sequence[Token],
    right: Sequence[Token],
) -> List[Token]:
    merged = set(left)
    merged.update(right)
    return sort_tokens(list(merged))

def ensure_all_verbs_in_statements(
    doc: Doc,
    final_statements: Sequence[Sequence[Token]],
) -> List[List[Token]]:
    updated_statements = [list(statement) for statement in final_statements]
    verb_groups = extract_verbs(doc)
    missing_verb_groups = get_missing_verb_groups(verb_groups, final_statements)

    if missing_verb_groups:
        updated_statements = integrate_missing_verbs_via_aux(updated_statements, missing_verb_groups)

    updated_statements = merge_statements_sharing_wrapped_verb_group(updated_statements, verb_groups)

    return updated_statements
