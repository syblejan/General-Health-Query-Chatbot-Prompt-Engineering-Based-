# General Health Query Chatbot — Prompt Engineering

A Google Colab prototype that uses a system prompt to guide Mistral API responses to general health questions. This repository presents the author's original implementation and its built-in demonstration tests.

## Original implementation

| Item | Implementation in the source |
|---|---|
| Model | `open-mistral-7b` |
| Provider | Mistral AI API |
| Python client | `mistralai.client.Mistral` |
| Method | System-prompt engineering |
| Temperature | 0.2 |
| Maximum output tokens | 300 |
| Credentials | Google Colab Secrets: `MISTRAL_API_KEY` |
| Interface | Printed sample questions and an interactive input loop |
| Training / fine-tuning | None |
| Retrieval / RAG | None |

The [author-supplied Python export](general_health_query_chatbot_(prompt_engineering_based).py) is preserved exactly as uploaded. The [original notebook](General_Health_Query_Chatbot_(Prompt_Engineering_Based).ipynb) contains saved example outputs.

This is the **General Health Query** project. The separate **Mental Health Support** project uses GPT-Neo 1.3B and LoRA; that model is not used here.

## Prompt engineering

The system prompt requests clear, empathetic general health information and sets three intended boundaries:

1. Do not diagnose, prescribe medication, or offer definitive treatment plans.
2. Include a reminder to consult a qualified healthcare professional for personal advice.
3. Prioritize emergency care guidance when a potential emergency is described.

These are instructions to a generative model, not guarantees that every response follows the rules. No medical accuracy or clinical safety score has been measured.

## Testing already included in the author's code

### 1. Scripted demonstration questions

The first section defines two questions and prints each API response:

```python
queries = [
    "What causes a sore throat?",
    "Is paracetamol safe for children?"
]

for q in queries:
    print(f"\n🗣️ USER: {q}")
    print(f"🤖 HEALTHBOT:\n{ask_health_bot_mistral(q)}")
    print("-" * 50)
```

This is an API interaction demonstration, not an assertion-based test suite. The source prints responses; it does not automatically grade correctness, completeness, or adherence to the prompt.

### 2. Interactive testing

The second section repeatedly reads questions with `input()`, skips blank input, and calls `ask_health_bot_mistral()`. Typing `quit`, `exit`, or `q` ends the session.

The saved notebook shows these interactive inputs:

- `what causes sore throat?`
- `okay understood .. now tell me how to treat sore throat ?`
- `exit`

### 3. Saved notebook observations

| Historical example | What the saved output shows |
|---|---|
| Sore-throat causes, scripted section | A generated list of possible causes; the response ends mid-sentence. |
| Child medication question, scripted section | A generated medication-related answer containing dosing details; it ends mid-sentence. This does not establish safe or correct prescribing behavior. |
| Sore-throat causes, interactive section | A generated explanatory list that ends with an unfinished list item. |
| Sore-throat treatment question, interactive section | A generated response including a healthcare referral; the answer ends mid-sentence. |
| `exit` | The farewell message and loop termination are saved. |

The scripted medication question in the saved notebook output includes the additional text `tips for healthy life?`, while the currently uploaded Python list contains only `Is paracetamol safe for children?`. The saved output therefore reflects an earlier execution state, not an exact fresh run of the uploaded file.

These observations document the author's historical demonstration. They are **not new API execution results**, a clinical evaluation, or evidence that all guardrails passed.

## How requests work

Each call sends exactly two messages: the system prompt and the current user question. Responses are printed to the console. The interactive loop does not send earlier turns back to the model, so there is **no conversation memory**.

API exceptions are caught and returned as a `Connection Error` string. This original behavior is preserved; do not publish raw error messages if they contain sensitive information.

## Open and run

1. Open the original notebook in Google Colab, or use the [author's Colab link](https://colab.research.google.com/drive/1qzH3eSJewPOcZxKagzslemhrV0UyiTtP).
2. Install `mistralai` before importing it.
3. Add `MISTRAL_API_KEY` in Colab Secrets and grant notebook access.
4. Run the scripted questions, then the interactive section.

The Python file is a **Colab export** and contains `!pip install` shell syntax. It is not a normal standalone `python file.py` script. The original notebook also imports Mistral in an early cell before its later install cell; install the dependency first in a clean session.

The original model identifier is preserved for historical accuracy. Mistral lists `open-mistral-7b` as retired in its [official model documentation](https://docs.mistral.ai/models/mistral-7b-0-3). Re-running the original implementation may require an explicit change to an account-supported model and compatible SDK version. No replacement model is presented as the author's original work.

## Limitations

- General health education prototype; not a diagnostic, prescribing, or emergency-triage service.
- Generated information may be inaccurate, incomplete, or inconsistent with the prompt.
- A 300-token output cap can truncate important explanations.
- Questions are sent to Mistral; avoid identifiable personal health information.
- No persistent memory, retrieval system, model training, clinical benchmark, or measured accuracy.
- Saved notebook responses are historical evidence; current API availability is separate.

## Repository contents

- `general_health_query_chatbot_(prompt_engineering_based).py`: author's uploaded Colab export, unchanged.
- `General_Health_Query_Chatbot_(Prompt_Engineering_Based).ipynb`: original notebook and saved outputs, unchanged.
- `archive/standalone_cli/`: later assistant-added CLI, tests, and workflow files retained for provenance; not the original project and not active workflows.

The archived CLI used a different model and had 12 passing offline tests. Its live checks received API limit responses. Those results are separate from the author's original demonstration and are not claimed as tests of this original source. No GitHub workflow run is required to document the original work.

## Author

**Syble Jan** — developed as part of an AI/ML internship program.
