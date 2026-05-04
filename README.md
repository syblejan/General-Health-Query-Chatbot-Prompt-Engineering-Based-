# General Health Query Chatbot (Prompt Engineering Based) 🏥🤖

Welcome to my AI/ML internship repository! This project features an interactive, AI-powered health assistant designed to answer general medical queries clearly and empathetically. 

## Task Objective
* The primary objective is to develop a highly knowledgeable medical assistant chatbot.
* It aims to answer general health queries simply while strictly adhering to critical safety rules.
* The bot is engineered to never diagnose conditions or prescribe medications, and to always remind users to consult a licensed healthcare professional.

## Dataset Used
* No traditional static dataset (like CSVs) was used for training.
* The project operates dynamically based on real-time user inputs through an interactive chat loop.
* Responses are generated using advanced prompt engineering techniques to guide the LLM's behavior.

## Models Applied
* **Model:** `open-mistral-7b`.
* **Framework/API:** Mistralai Python Client API.
* **Technique:** System Prompt Engineering (configuring temperature to 0.2 and max_tokens to 300 for focused, concise responses).

## Key Results and Findings
* Successfully built an interactive chat loop that can handle back-and-forth user questions until the user types 'quit', 'exit', or 'q'.
* The bot accurately answered test queries such as "What causes a sore throat?" and "Is paracetamol safe for children?" with detailed, structured, and helpful information.
* **Safety Compliance:** The prompt engineering successfully restricted the AI from acting as a doctor; it consistently included gentle disclaimers advising users to seek professional medical care for severe symptoms.
