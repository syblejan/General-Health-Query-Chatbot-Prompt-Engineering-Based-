# 🏥 General Health Query Chatbot (Prompt Engineering Based)

> A prompt-engineered AI health assistant powered by Mistral 7B that answers general medical queries with empathy, clarity, and built-in safety guardrails.

---

## 📌 Task Objective

The goal of this task was to build a general-purpose health query chatbot using **prompt engineering** — without any model training or fine-tuning. By carefully crafting a system prompt with explicit behavioral rules, the chatbot is guided to respond like a knowledgeable and empathetic medical assistant while strictly avoiding dangerous behaviors such as diagnosing conditions or prescribing treatments.

This project demonstrates how effective prompt design alone can shape an LLM's persona, tone, and safety boundaries.

---

## 🤖 Model Applied

**Model:** [`open-mistral-7b`](https://mistral.ai/news/announcing-mistral-7b/)  
**Provider:** Mistral AI API  
**Access:** Via the `mistralai` Python client library

Mistral 7B is a high-performance open-weight language model that delivers strong instruction-following capabilities at an efficient size, making it well-suited for real-time conversational applications.

### Inference Configuration

| Parameter     | Value |
|---------------|-------|
| Temperature   | 0.2   |
| Max Tokens    | 300   |
| Mode          | Chat Completion (`chat.complete`) |

A **low temperature (0.2)** was intentionally chosen to produce factual, consistent, and reliable health information rather than creative or unpredictable responses.

---

## 🧠 Prompt Engineering Approach

The chatbot's behavior is entirely defined through a structured **system prompt** — no fine-tuning required. The prompt establishes:

1. **Persona** — A friendly, empathetic, and knowledgeable medical assistant
2. **Objective** — Answer general health queries clearly and simply
3. **Safety Rules (Critical Guardrails):**
   - Never diagnose conditions or prescribe medications
   - Always remind the user to consult a licensed healthcare professional
   - Escalate to emergency services if severe symptoms are mentioned

```
You are a friendly, empathetic, and highly knowledgeable medical assistant.
Your objective is to answer general health queries clearly and simply.

CRITICAL SAFETY RULES:
1. You are an AI, not a licensed doctor. NEVER diagnose or prescribe.
2. Always include a disclaimer to consult a healthcare professional.
3. For emergencies (severe pain, breathing issues), direct to emergency care.
```

This pattern — combining a clear role definition with explicit behavioral constraints — is a core technique in responsible prompt engineering for healthcare applications.

---

## 💬 Sample Interactions

**Query 1: Informational**
> 🗣️ *"What causes a sore throat?"*  
> 🤖 The bot responded with a well-structured breakdown covering viral causes (cold, flu, COVID-19), bacterial causes (strep throat), environmental irritants, acid reflux, and overuse of the voice.

**Query 2: Treatment Advice**
> 🗣️ *"How do I treat a sore throat?"*  
> 🤖 The bot provided safe home remedies (warm liquids, honey, saltwater gargling, humidifier use) while clearly advising the user to seek medical care if symptoms persisted or worsened.

**Query 3: Medication Safety**
> 🗣️ *"Is paracetamol safe for children?"*  
> 🤖 The bot explained weight-based dosing guidelines, measurement tips, and precautions around combination products — all with a gentle disclaimer to consult a pediatrician.

---

## 🔑 Key Results & Findings

- **Prompt engineering alone** was sufficient to produce safe, structured, and helpful health responses — no model training was needed.
- The **low temperature setting** was critical for factual consistency; higher values produced less reliable medical information.
- The **system prompt guardrails** successfully prevented the model from making diagnostic claims or prescribing specific treatments across all tested queries.
- The chatbot correctly handled multi-turn conversation flow, including follow-up questions, within the interactive loop.
- **Emergency escalation behavior** was built in through prompt rules, demonstrating that safety-critical behaviors can be embedded via instructions rather than RLHF alone.

### Limitations
- Responses are capped at 300 tokens, which occasionally truncates longer explanations mid-sentence.
- The model has no memory between sessions — each call is stateless.
- As a general-purpose LLM, the model is not clinically validated and should not replace professional medical advice.

---

## 🛠️ Tech Stack

| Tool / Library  | Purpose                              |
|-----------------|--------------------------------------|
| `mistralai`     | Mistral API client for chat completions |
| `google.colab`  | Secure API key management via Secrets |
| Python          | Core scripting language              |
| Google Colab    | Development & execution environment  |


## ⚠️ Disclaimer

This chatbot is for **informational and educational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

---

*Built as part of an AI/ML Internship Program.*
