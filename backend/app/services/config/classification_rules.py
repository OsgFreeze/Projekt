ROLE_RULES = {
    "TASK": {
        "verbs": {"erstellen", "implementieren", "entwickeln", "schreiben", "bauen", "programmieren"},
        "keywords": {"programmcode", "funktion", "klasse", "modul", "api", "algorithmus", "skript"},
        "markers": {"erstelle", "implementiere", "entwickle", "schreibe"},
        "weight": 1.0,
    },
    "FUNCTIONAL_REQUIREMENT": {
        "verbs": {"validieren", "berechnen", "traversieren", "durchsuchen", "parsen", "filtern", "sortieren"},
        "keywords": {"graph", "datei", "daten", "benutzer", "route", "request", "csv", "json"},
        "markers": {"soll", "muss", "verwende", "nutze"},
        "weight": 1.2,
    },
    "INPUT": {
        "verbs": {"übergeben", "einlesen", "laden", "bekommen", "erhalten"},
        "keywords": {"eingabe", "input", "parameter", "graph", "json", "csv", "datei"},
        "markers": {"gegeben", "übergeben", "als input", "als eingabe"},
        "weight": 1.1,
    },
    "OUTPUT": {
        "verbs": {"ausgeben", "zurückgeben", "anzeigen", "speichern", "liefern"},
        "keywords": {"ausgabe", "ergebnis", "pfad", "datei", "response", "rückgabewert"},
        "markers": {"anschließend", "danach", "am ende", "als ausgabe"},
        "weight": 1.2,
    },
    "EXISTING_CONTEXT": {
        "verbs": {"existieren", "vorhanden", "implementieren"},
        "keywords": {"projekt", "klasse", "methode", "struktur", "heuristik"},
        "markers": {"bereits", "schon", "vorhanden", "existiert", "implementiert"},
        "weight": 1.1,
    },
    "QUALITY_REQUIREMENT": {
        "verbs": {"berücksichtigen", "einhalten", "beachten"},
        "keywords": {"clean code", "solid", "wartbarkeit", "lesbarkeit", "qualität", "metriken"},
        "markers": {"achte darauf", "clean code", "robust", "wartbar", "lesbar"},
        "weight": 1.3,
    },
    "CONSTRAINT": {
        "verbs": {"dürfen", "müssen", "sollen"},
        "keywords": {"ohne", "maximal", "mindestens", "nur", "keine"},
        "markers": {"darf nicht", "ohne", "nur", "maximal", "mindestens", "keine"},
        "weight": 1.2,
    }
}

ROLE_PRIORITY = [
    "OUTPUT",
    "INPUT",
    "QUALITY_REQUIREMENT",
    "CONSTRAINT",
    "EXISTING_CONTEXT",
    "FUNCTIONAL_REQUIREMENT",
    "TASK",
    "MISC"
]

GENERIC_TARGETS = {
    "code",
    "programmcode",
    "programm",
    "funktion",
    "methode",
    "klasse",
    "skript"
}