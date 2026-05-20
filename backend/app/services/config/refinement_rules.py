KEEP_WORDS = {
    "nicht",
    "keine",
    "kein",
    "ohne",
    "nur",
    "mindestens",
    "maximal",
}

TECHNICAL_ROLES = {
    "LANGUAGE",
    "TECH_STACK",
    "FILE_STRUCTURE",
    "INTERFACE",
}

ROLE_WEIGHTS = {
    "TASK": 10.0,
    "FUNCTIONAL_REQUIREMENT": 9.0,
    "INPUT": 8.5,
    "OUTPUT": 8.5,
    "CONSTRAINT": 8.0,
    "QUALITY_REQUIREMENT": 6.5,
    "EXISTING_CONTEXT": 5.0,
    "TECH_STACK": 4.0,
    "LANGUAGE": 3.5,
    "INTERFACE": 3.0,
    "FILE_STRUCTURE": 2.5,
    "MISC": 1.0,
}

ROLE_ORDER = [
    "LANGUAGE",
    "TECH_STACK",
    "TASK",
    "FUNCTIONAL_REQUIREMENT",
    "INPUT",
    "OUTPUT",
    "CONSTRAINT",
    "QUALITY_REQUIREMENT",
    "EXISTING_CONTEXT",
    "INTERFACE",
    "FILE_STRUCTURE",
    "MISC",
]