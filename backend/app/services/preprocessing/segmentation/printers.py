from typing import Sequence
from spacy.tokens import Doc, Span, Token

from app.services.preprocessing.segmentation.utils import tokens_to_strings


def print_tokens(doc: Doc) -> None:
    print("\n=== Tokens ===")
    for token in doc:
        print(
            f"{token.text:<15} | POS: {token.pos_:<6} | Lemma: {token.lemma_:<15} | "
            f"Dep: {token.dep_:<10} | Head: {token.head.text:<15} | TAG: {token.tag_}"
        )


def print_noun_chunks(chunks: Sequence[Span]) -> None:
    print("\n=== Noun Chunks ===")
    for chunk in chunks:
        print(f"- {chunk.text} , ROOT: {chunk.root.text}")


def print_token_lists(title: str, statements: Sequence[Sequence[Token]]) -> None:
    print(f"\n=== {title} ===")
    for tokens in statements:
        text = " ".join(t.text for t in tokens)
        print("-", text)


def print_statements(statements: Sequence[Sequence[Token]]) -> None:
    print("\n=== Statements ===")
    for statement in tokens_to_strings(statements):
        print(f"- {statement}")


def print_verbs(verb_groups: Sequence[Sequence[Token]]) -> None:
    print("\n=== VERBS ===")
    for group in verb_groups:
        print("-", " ".join(token.text for token in group))


def print_adverbs(adverbs: Sequence[Token]) -> None:
    print("\n=== ADVERBS ===")
    for adv in adverbs:
        print(f"- {adv.text}")
