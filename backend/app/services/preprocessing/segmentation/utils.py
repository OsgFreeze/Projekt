from typing import List, Sequence
from spacy.tokens import Token


def sort_tokens(tokens: Sequence[Token]) -> List[Token]:
    return sorted(tokens, key=lambda token: token.i)


def tokens_to_strings(statements: Sequence[Sequence[Token]]) -> List[str]:
    return [" ".join(token.text for token in tokens) for tokens in statements]
