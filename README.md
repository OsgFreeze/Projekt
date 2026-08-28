# Prompt Shortening Tool

A web application developed as part of my **Bachelor's thesis** for shortening and processing prompts.

## Prerequisites

Before starting the application, make sure the following are installed:

- Python
- Node.js / npm
- Ollama

## Setup

### 1. Install Python dependencies

Run the following command from the project root:

```bash
python -m pip install -r requirements.txt
```

### 2. Install required models

Install the required Ollama and spaCy models with:

```bash
python setup_models.py
```

## Startup

The backend and frontend can be started together using the existing VS Code configuration.

### Option 1: Run Task

1. Open the VS Code Command Palette with `Ctrl + Shift + P`.
2. Select **Tasks: Run Task**.
3. Select **Start Full Stack**.

### Option 2: Run and Debug

1. Open the **Run and Debug** tab with `Ctrl + Shift + D`.
2. Start debugging with `F5`.

The **Start Full Stack** task starts the required application components automatically.
