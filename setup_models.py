import subprocess
import sys

with open("ollama-models.txt", encoding="utf-8") as f:
    models = [
        line.strip()
        for line in f
        if line.strip() and not line.startswith("#")
    ]

for model in models:
    print(f"Lade: {model}...")
    subprocess.run(["ollama", "pull", model], check=True)

with open("spacy-models.txt", encoding="utf-8") as j:
    models = [
        line.strip()
        for line in j
        if line.strip() and not line.startswith("#")
    ]

for model in models:
    print(f"Lade: {model}...")
    subprocess.run([sys.executable, "-m", "spacy", "download", model], check=True)