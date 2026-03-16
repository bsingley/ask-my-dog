import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os

# -----------------------------
# Setup
# -----------------------------

st.set_page_config(page_title="Ask My Dog", page_icon="🐾")

st.title("🐾 Ask My Dog")

client = OpenAI()

dog_file = "dog_profile.json"

# -----------------------------
# Default Dog Profile
# -----------------------------

default_dog = {
    "name": "Luna",
    "age": "10 months",
    "breed": "lab mix",
    "energy_level": "very high",
    "training_level": "basic obedience",
    "fear_triggers": ["new objects", "loud sounds"],
    "personality_traits": ["extremely intelligent", "curious", "cautious"],
    "self_identity": "fearless guardian",
    "self_confidence": "extreme",
    "self_story": "protector of the household",
    "superhero_identity": "None"
}

if os.path.exists(dog_file):
    with open(dog_file) as f:
        dog = json.load(f)
else:
    dog = default_dog.copy()

# -----------------------------
# Chat History
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar Persona
# -----------------------------

with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=120)

    st.markdown(f"""
    ### 🐶 {dog['name']}
    **{dog['breed']} • {dog['age']}**
    """)

    st.divider()

    confidence_choice = st.selectbox(
        "How does this dog view themselves?",
        [
            "🐶 Nervous Puppy",
            "🐕 Normal Dog",
            "👑 Very Important Dog",
            "🦸 Legendary Household Guardian"
        ]
    )

    if "Nervous Puppy" in confidence_choice:
        confidence_style = "The dog is slightly unsure and cautious."
    elif "Normal Dog" in confidence_choice:
        confidence_style = "The dog has normal playful dog confidence."
    elif "Very Important Dog" in confidence_choice:
        confidence_style = "The dog believes they are responsible for important household decisions."
    else:
        confidence_style = "The dog believes they are the heroic protector of the household."

    st.divider()


    drama_level = st.selectbox(
        "🎭 Drama Level",
        [
            "🐾 Realistic Dog",
            "🎬 Sitcom Dog",
            "📖 Shakespearean Dog",
            "🎮 RPG Hero Dog"
        ],
        help="Controls how dramatic your dog's internal monologue will be."
    )

    if "Realistic Dog" in drama_level:
        drama_style = "Speak like a normal dog thinking in simple playful thoughts."

    elif "Sitcom Dog" in drama_level:
        drama_style = "Respond like a sarcastic sitcom character observing ridiculous human behavior."

    elif "Shakespearean Dog" in drama_level:
        drama_style = "Speak in overly dramatic Shakespearean-style language as if narrating an epic tragedy."

    else:
        drama_style = "Speak like a heroic RPG character on a noble quest to protect the household."

    st.divider()


    with st.expander("⚙️ Edit Dog Persona"):

        dog["name"] = st.text_input("Dog name", dog["name"])
        dog["breed"] = st.text_input("Breed", dog["breed"])
        dog["age"] = st.text_input("Age", dog["age"])
        dog["energy_level"] = st.text_input("Energy level", dog["energy_level"])
        dog["training_level"] = st.text_input("Training level", dog["training_level"])
        dog["self_identity"] = st.text_input("Self identity", dog["self_identity"])
        dog["self_story"] = st.text_input("Self story", dog["self_story"])
        dog["superhero_identity"] = st.text_input("Superhero identity", dog["superhero_identity"])

        if st.button("Save Persona"):
            with open(dog_file, "w") as f:
                json.dump(dog, f, indent=2)
            st.success("Saved!")

        if st.button("Reset to Luna"):
            dog = default_dog.copy()
            st.success("Reset to default")

# -----------------------------
# Example Prompts
# -----------------------------

st.caption("Try asking:")
st.caption("• Why do you bark at the vacuum?")
st.caption("• Why do you steal socks?")
st.caption("• What happens during Zoom meetings?")
st.caption("• Why do you stare at me while I eat?")

st.divider()

# -----------------------------
# Display Chat History
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------

user_question = st.chat_input(f"Ask {dog['name']} something...")

# -----------------------------
# AI Response
# -----------------------------

if user_question:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_question)

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    prompt = f"""
You are a dog named {dog['name']}.

Background personality information (use only if relevant):
Age: {dog['age']}
Breed: {dog['breed']}
Energy level: {dog['energy_level']}
Training level: {dog['training_level']}
Fear triggers: {', '.join(dog['fear_triggers'])}
Personality traits: {', '.join(dog['personality_traits'])}
Self identity: {dog['self_identity']}
Self story: {dog['self_story']}
Superhero identity: {dog['superhero_identity']}

Confidence style:
{confidence_style}

Drama style:
{drama_style}

Instructions:

Respond in two parts.

DOG RESPONSE
Speak in first person using dog logic.

Examples of dog logic:
- vacuums are hostile mechanical beasts
- mail carriers are suspicious invaders
- meetings exist so humans eventually throw balls
- cooking means food might fall
- laptops steal human attention

The dog believes their own heroic narrative.

Do not number sections.
Do not repeat the dog's name.
Do not list personality traits.

DOG TRAINER RESPONSE

Then explain the behavior starting with:

As a dog trainer:

User question:
{user_question}
"""

    try:

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = response.output_text.strip()

        if "As a dog trainer:" in text:
            dog_part, trainer_part = text.split("As a dog trainer:", 1)
        else:
            dog_part = text
            trainer_part = ""

        # Display response
        with st.chat_message("assistant"):

            st.markdown(f"### 🐶 {dog['name']} thinks...")
            st.markdown(dog_part)

            if trainer_part:
                with st.expander("🧑‍🏫 Dog trainer explains"):
                    st.markdown(trainer_part)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"### 🐶 {dog['name']} thinks...\n{dog_part}\n\n**Dog Trainer:**\n{trainer_part}"
        })

    except OpenAIError:

        st.error("The AI dog is taking a nap. Check your API key or connection.")