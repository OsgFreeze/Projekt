# Prompt Shortening Tool

A web application developed as part of my **Bachelor's thesis** for shortening, restructuring, and evaluating prompts with local language models via **Ollama**.

The backend provides three processing variants. All variants receive the **original prompt as a string**, but use different strategies to transform and shorten it. The thesis focuses on **Version 3 (`process_v3`)**; Versions 1 and 2 are retained as alternative approaches for comparison and experimentation.

---

## Prerequisites

Before starting the application, make sure the following are installed:

- Python
- Node.js / npm
- Ollama

---

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

---

## Startup

The backend, frontend, and Ollama initialization can be started together using the existing VS Code configuration.

### Option 1: Run Task

1. Open the VS Code Command Palette with `Ctrl + Shift + P`.
2. Select **Tasks: Run Task**.
3. Select **Start Full Stack**.

### Option 2: Run and Debug

1. Open the **Run and Debug** tab with `Ctrl + Shift + D`.
2. Start debugging with `F5`.

The **Start Full Stack** task starts the required application components automatically.

---

# Processing Variants

The `ProcessingOrchestrator` coordinates three different processing pipelines:

- `process()` — Version 1
- `process_v2()` — Version 2
- `process_v3()` — Version 3

Each variant starts with the same input — the original prompt — but differs in how strongly the processing is rule-based and where the language model is used.

## Version 3 — Direct LLM Compression

> **Main variant used in the Bachelor's thesis**

Version 3 is the central processing approach considered in the thesis. Instead of decomposing the prompt into individual candidates first, the original prompt is passed directly to the **GenerationService**.

```text
Original Prompt
      │
      ▼
GenerationService
      │
      ├── Build user prompt
      ├── Add system prompt
      ├── Send prompt to Ollama
      │
      ▼
Ollama / qwen2.5:7b
      │
      ▼
Compressed Prompt
      │
      ▼
Evaluation / Metrics
      │
      ▼
EvaluationResponse
```

The `GenerationService` instructs the local Ollama model to compress the original prompt according to the configured system rules. The generated prompt is then compared with the original prompt and returned together with evaluation metrics in an `EvaluationResponse`.

The following diagram shows the components involved in this thesis-focused processing flow:

![Backend component diagram](./backend-component-diagram.png)

### Main components

- **API Router / Endpoint** — receives the original prompt and forwards it to the orchestrator.
- **ProcessingOrchestrator** — selects and starts the Version 3 processing flow.
- **GenerationService** — constructs the LLM request, invokes Ollama, and processes the generated result.
- **Ollama / `qwen2.5:7b`** — locally generates the compressed prompt.
- **EvaluationService** — provides functionality used to calculate evaluation metrics such as token and word reduction.
- **EvaluationResponse** — contains the original prompt, compressed prompt, evaluation metrics, and metadata.

---

## Version 1 — Structured Prompt Processing

Version 1 follows a multi-stage, service-based processing pipeline. The prompt is first analyzed and decomposed before a final prompt is generated and evaluated.

```text
Original Prompt
      │
      ▼
PreprocessingService
      │
      ▼
ExtractionService
      │
      ▼
ClassificationService
      │
      ▼
RefinementService
      │
      ▼
PromptGenerationService
      │
      ▼
EvaluationService
      │
      ▼
EvaluationResponse
```

### Processing flow

1. **Preprocessing**  
   The input prompt is normalized and split into individual sentences. Relevant technical entities can be protected during this step.

2. **Extraction**  
   Semantic and technical information is extracted from the preprocessed sentences and represented as candidates.

3. **Classification**  
   The extracted candidates are classified and assigned to semantic roles such as tasks, inputs, outputs, constraints, or other prompt components.

4. **Refinement**  
   The classified candidates are deduplicated, compressed, prioritized, and structured into a cleaner representation.

5. **Prompt Generation**  
   The refined candidates are assembled into the final prompt.

6. **Evaluation**  
   The generated prompt is compared with the original prompt and several metrics are calculated before an `EvaluationResponse` is returned.

---

## Version 2 — LLM Transformation + Structured Processing

Version 2 builds on the same structured pipeline as Version 1, but adds an LLM-based transformation step before the rule-based processing begins.

```text
Original Prompt
      │
      ▼
TransformationService
      │
      ▼
PreprocessingService
      │
      ▼
ExtractionService
      │
      ▼
ClassificationService
      │
      ▼
RefinementService
      │
      ▼
PromptGenerationService
      │
      ▼
EvaluationService
      │
      ▼
EvaluationResponse
```

### Processing flow

1. **Transformation**  
   The original prompt is first sent to Ollama. The `TransformationService` rewrites the prompt into a simpler form that can subsequently be processed by the structured pipeline.

2. **Preprocessing, Extraction, Classification, and Refinement**  
   The transformed prompt then follows the same candidate-based processing stages as Version 1.

3. **Prompt Generation**  
   The refined candidates are assembled into the final prompt using the configured prompt-generation strategy.

4. **Evaluation**  
   The result is evaluated and returned as an `EvaluationResponse`.

---

## Comparison

| Variant | Initial LLM transformation | Candidate extraction & classification | Final prompt generation | Evaluation |
|---|---|---|---|---|
| **Version 1** | No | Yes | From refined candidates | Yes |
| **Version 2** | Yes | Yes | From refined candidates | Yes |
| **Version 3** | No separate preprocessing step | No | Directly by Ollama | Yes |

Version 1 and Version 2 explore a more explicit, modular decomposition of the prompt. Version 3 instead delegates the compression directly to the language model and therefore provides a substantially shorter processing pipeline. **Version 3 is the variant used as the main implementation in the Bachelor's thesis.**

---

## Implementation Note

In the current `ProcessingOrchestrator`, both Version 1 and Version 2 call the `PromptGenerationService` with `use_llm=False`. Consequently, the current implementation uses the **template-based builder** for the final candidate assembly in both variants. The `PromptGenerationService` also supports an LLM-based builder when `use_llm=True`.

---

## Project Scope

The project contains additional modules and implementation details beyond the overview above. This README focuses on the three main prompt-processing variants and the services involved in their high-level processing flow.
