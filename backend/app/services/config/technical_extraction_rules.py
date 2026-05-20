import re

LANGUAGES = {
    "python": "Python",
    "java": "Java",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "c++": "C++",
    "cpp": "C++",
    "c#": "C#",
    "csharp": "C#",
    "go": "Go",
    "golang": "Go",
    "rust": "Rust",
    "php": "PHP",
    "ruby": "Ruby",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "scala": "Scala",
    "r": "R",
    "sql": "SQL",
    "html": "HTML",
    "css": "CSS",
}

TECH_STACK = {
    "fastapi": "FastAPI",
    "flask": "Flask",
    "django": "Django",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "react": "React",
    "vue": "Vue",
    "angular": "Angular",
    "node": "Node.js",
    "node.js": "Node.js",
    "express": "Express",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "nestjs": "NestJS",
    "sqlite": "SQLite",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "pandas": "pandas",
    "numpy": "NumPy",
    "scikit-learn": "scikit-learn",
    "sklearn": "scikit-learn",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "pytest": "pytest",
    "junit": "JUnit",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
}

FILE_PATTERN = re.compile(
    r"""
    (?<!\w)
    [\w\-./\\]+
    \.
    (py|java|js|jsx|ts|tsx|cpp|c|h|hpp|cs|go|rs|php|rb|kt|swift|
        scala|html|css|scss|json|yaml|yml|xml|sql|md|txt|csv|env|
        dockerfile|toml|ini|cfg)
    \b
    """,
    re.IGNORECASE | re.VERBOSE
)

PATH_PATTERN = re.compile(
    r"""
    (?:
        (?:\.{1,2}/|/|src/|app/|lib/|test/|tests/)
        [\w\-./\\]+
    )
    """,
    re.IGNORECASE | re.VERBOSE
)

FUNCTION_CALL_PATTERN = re.compile(
    r"\b[a-zA-Z_][a-zA-Z0-9_]*\s*\([^()\n]*\)"
)

PYTHON_DEF_PATTERN = re.compile(
    r"\bdef\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)"
)

JAVA_LIKE_METHOD_PATTERN = re.compile(
    r"""
    \b
    (public|private|protected|static|async)?
    \s*
    [A-Za-z_<>\[\]]+
    \s+
    [a-zA-Z_][a-zA-Z0-9_]*
    \s*
    \([^)]*\)
    """,
    re.VERBOSE
)

ENDPOINT_PATTERN = re.compile(
    r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/[a-zA-Z0-9_\-/{}/:.]*)",
    re.IGNORECASE
)