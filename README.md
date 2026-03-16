# Ask My Dog 🐶

**Ask My Dog** is a playful AI app that answers questions from the perspective of your dog, combining creativity with technical experimentation in AI-driven UX.

Users can:

* Select a dog personality
* Adjust confidence levels
* Ask questions about training, food, or daily life

This project demonstrates skills in:

* **Prompt engineering** – designing AI prompts for engaging dog personas
* **Persona design** – crafting distinct AI personalities with unique behaviors
* **Lightweight AI UX** – building intuitive, interactive flows
* **Streamlit app development** – rapid prototyping of web-based AI applications

**Live demo:** [Insert Link]

---

## Architecture Overview

```mermaid
flowchart TD
    UI[User Interface (Browser/Web)] --> App[Streamlit App (Python)]
    App --> AI[AI Engine/API (OpenAI GPT)]
    
    UI -->|User Inputs: Question, Dog, Confidence| App
    App -->|Persona Config: Dog Personality, Confidence| AI
    AI -->|Response Generation: Text output| App
    App -->|Displayed Response| UI

    subgraph FutureEnhancements
        AI --> Memory[Conversation Memory]
        App --> MultiDog[Multiple Dog Personalities]
        AI --> Training[Personalized Training Recommendations]
    end
```

---

## Features

* **Dynamic AI personalities:** Users can pick dog types with different behaviors.
* **Confidence slider:** Adjust how “sure” the dog is in its responses.
* **Interactive Q&A:** Ask questions about training, food, or daily life.
* **Lightweight web interface:** Built in **Streamlit** for fast, accessible interaction.

---

## Future Improvements

* Personalized training recommendations based on user questions
* Multiple dog personalities with distinct behaviors
* Conversation memory for ongoing interactions
* Enhanced UX with richer feedback and interactive elements


Redeploy test.