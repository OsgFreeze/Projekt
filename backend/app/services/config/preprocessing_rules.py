import re

FILE_PATTERN = re.compile(
    r"\b[\w\-\/]+\.(py|java|js|ts|tsx|jsx|cpp|cs|go|rs|php|html|css|json|yaml|yml|sql)\b",
    re.IGNORECASE
)

COMPLEXITY_PATTERN = re.compile(
    r"O\([^)]+\)"
)

ASTAR_PATTERN = re.compile(
    r"\bA\*\b"
)

CODE_BLOCK_PATTERN = re.compile(
    r"```.*?```",
    re.DOTALL
)

BULLET_PATTERN = re.compile(
    r"(\n\s*[-•*]\s+)"
)