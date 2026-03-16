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