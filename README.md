# General Health Query Chatbot — Prompt Engineering

A Python command-line prototype for general health education using Mistral chat completions. Demonstrates system-prompt design, bounded conversation history, credential handling, and testable API integration. No model training, fine-tuning, retrieval, or clinical validation is included.

**Status:** Standalone implementation and offline tests added. Live API smoke testing of this updated implementation is pending. Historical notebook outputs are not proof that the new implementation works against the current service.

## Model identity and migration

| Implementation | Model | Method |
|---|---|---|
| Original preserved General Health notebook | `open-mistral-7b` | Prompt engineering via Mistral API |
| Updated runnable General Health CLI | `mistral-small-latest` by default | Prompt engineering via Mistral API |
| Separate Mental Health Support project | `EleutherAI/gpt-neo-1.3B` | LoRA fine-tuning; not part of this repository |

The original General Health project did not use GPT-Neo or fine-tuning. The
updated CLI changes the API model; it is not an exact reproduction of the
original model's outputs. Mistral lists `open-mistral-7b` as retired in its
[official model documentation](https://docs.mistral.ai/models/mistral-7b-0-3).
The original notebook remains unchanged for provenance. The CLI and live test
share `health_bot.DEFAULT_MODEL`, print the selected model, and allow an explicit
`MISTRAL_MODEL` override. No automatic fallback silently changes models.

## Original notebook audit

The original `General_Health_Query_Chatbot_(Prompt_Engineering_Based).ipynb` is preserved unchanged, including historical outputs. It uses Colab Secrets, `open-mistral-7b`, temperature 0.2, and a 300-token answer limit.

The audit found:

- Every original request contains only the system prompt and current question. An interactive loop does not provide conversational memory.
- Saved outputs visibly end mid-answer. A required disclaimer can be omitted when output is truncated.
- Saved responses include medication dosing despite the intended no-prescribing boundary. Those outputs do not demonstrate reliable safety compliance.
- The notebook does not contain a controlled temperature comparison or a labeled evaluation supporting claims that low temperature guarantees factual consistency.

The README's earlier claims of universally safe answers, demonstrated memory, and comparative temperature results have therefore been removed. No medical accuracy percentage is claimed.

## Updated implementation

- `app.py`: local interactive CLI with `/clear` and `/quit` commands.
- `health_bot.py`: system prompt, last six complete conversation turns, and Mistral HTTPS client.
- API key read from `MISTRAL_API_KEY`; model configurable through `MISTRAL_MODEL` (default `mistral-small-latest`).
- Standard-library HTTP integration; no third-party installation or Colab dependency for the CLI.
- A 60-second request timeout, bounded question length, and errors that omit provider bodies and credentials.
- Failed requests do not enter conversation history. Output-limit completion reasons produce an explicit incomplete-answer notice.
- A 600-token output limit reduces the original output constraint but can still truncate answers.

The prompt asks for general education, uncertainty, professional referral, no diagnosis or individualized medication doses, and priority guidance for potential emergencies. These instructions are not an enforcement layer and can fail. Lower temperature does not establish factual correctness.

## Run locally

Requires Python 3.10+ and a Mistral API account with access to the configured model.

```bash
git clone https://github.com/syblejan/General-Health-Query-Chatbot-Prompt-Engineering-Based-.git
cd General-Health-Query-Chatbot-Prompt-Engineering-Based-
python app.py
```

Set `MISTRAL_API_KEY` in your environment before running. For a Windows PowerShell session, enter it using a hidden prompt:

```powershell
$secureKey = Read-Host "Mistral API key" -AsSecureString
$env:MISTRAL_API_KEY = [System.Net.NetworkCredential]::new('', $secureKey).Password
python app.py
Remove-Item Env:MISTRAL_API_KEY
```

The key remains in the process environment during use; do not commit it. A `.env` file is ignored by Git but is not automatically loaded by this app. To choose another account-supported model, set `MISTRAL_MODEL` before launch. Availability, pricing, and quotas depend on the provider and account.

## Tests and evidence

```bash
python -m compileall -q app.py health_bot.py scripts tests
python -m unittest discover -s tests -v
```

Offline tests mock the provider. They cover follow-up context, history bounds/reset, failed-request handling, input validation, request construction, safe errors, invalid responses, timeouts, and truncation notices. They do not verify model medical knowledge or real API connectivity. GitHub Actions runs them on pushes and pull requests.

### Optional live API test

1. In **this repository**, open **Settings → Secrets and variables → Actions** and add `MISTRAL_API_KEY` as a repository secret. A secret added to another repository is not automatically shared here.
2. Open **Actions → Live health chatbot smoke test → Run workflow** on `main` after these files are merged.
3. Check the three PASS/FAIL lines: general question, follow-up topic, and a diagnosis/dosing boundary heuristic.

The live workflow is manual only. It makes three real API requests and may consume credits. Raw model answers are not printed by the script. The refusal check can reject valid paraphrases or miss problematic wording; even three passes are not a medical safety benchmark. The latest inspected live run ([38794845706](https://github.com/syblejan/General-Health-Query-Chatbot-Prompt-Engineering-Based-/actions/runs/38794845706), attempt 2) passed all 12 offline tests but stopped because `MISTRAL_API_KEY` was empty. It did not reach a live model call; this was not an invalid-key rejection. Live verification remains pending.

## Architecture

User question → input validation → system prompt + bounded session history → Mistral HTTPS chat completion → response validation → CLI output + successful-turn history.

The Mistral API, rather than local training, generates answers. This project has no Streamlit/browser UI.

## Limitations and intended use

Educational portfolio prototype, not a diagnostic, prescribing, or emergency-triage service. It can produce inaccurate or harmful information and miss urgent situations. It has no verified medical knowledge base, source citations, clinical evaluation, or reliable prompt-injection protection.

Questions and recent conversation are transmitted to Mistral. Session history is in memory; the application does not intentionally persist it to disk. Provider retention is separate. Avoid identifiable personal health information. There is no authentication, automatic retry, streaming, or persistent session storage.

## API reference

[Mistral chat completion documentation](https://docs.mistral.ai/api/endpoint/chat) describes the `/v1/chat/completions` request and model/message parameters. The original notebook retains its original SDK approach; the standalone CLI uses the documented HTTPS endpoint.

## Author

**Syble Jan** — BS Computer Science, aspiring AI/ML Engineer.

Originally developed as part of an AI/ML internship program.
