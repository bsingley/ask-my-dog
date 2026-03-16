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

    st.markdown(f"### 🐶 {dog['name']}")
    st.caption(f"Self-Story: {dog['self_story']}")

    st.divider()

    # NEW: Drama Level → strength of self-story belief
    drama_level = st.selectbox(
        "🎭 Drama Level",
        [
            "🐾 Low – Mostly normal dog reactions",
            "🐕 Moderate – Story influences some thoughts/actions",
            "👑 High – Story guides most thoughts/actions",
            "🦸 Extreme – Story defines everything the dog thinks and does"
        ],
        help="Controls how strongly the dog believes its own story."
    )

    if "Low" in drama_level:
        drama_strength = "The dog mostly reacts normally; its self-story has little effect."
    elif "Moderate" in drama_level:
        drama_strength = "The dog sometimes filters its thoughts and behavior through its self-story."
    elif "High" in drama_level:
        drama_strength = "The dog mostly acts and thinks according to its self-story."
    else:
        drama_strength = "The dog fully believes in its self-story; all thoughts and reactions are filtered through it."

    st.caption(f"Current Drama Level: {drama_level}")

    st.divider()

    # Former “Drama Level” → Storytelling Style
    story_style = st.selectbox(
        "🎨 Storytelling Style",
        [
            "🐾 Doggish Dog",
            "🎬 Sitcom Dog",
            "📖 Shakespearean Dog",
            "🎮 RPG Hero Dog",
            "🎵 Snoop Dogg Dog"
        ],
        help="Controls the tone and style of the dog's responses."
    )

    if story_style == "Realistic Dog":
        story_style_prompt = "Speak like a normal dog thinking in simple playful thoughts."
    elif story_style == "Sitcom Dog":
        story_style_prompt = "Respond like a sarcastic sitcom character observing ridiculous human behavior."        
    elif story_style == "Shakespearean Dog":
        story_style_prompt = "Speak in overly dramatic Shakespearean-style language."
    elif story_style == "RPG Hero Dog":
        story_style_prompt = "Speak like a heroic RPG character on a noble quest to protect the household."
    else:  # Snoop Dogg Dog
        story_style_prompt = (
            "Speak in a laid-back, cool, rhyming style reminiscent of Snoop Dogg. "
            "Use playful slang, humor, and rhythm while describing dog thoughts."
    )
    
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

Background personality info (use only if relevant):
{dog['age']}, {dog['breed']}, {', '.join(dog['personality_traits'])}, etc.

Self-Story:
{dog['self_story']}

Drama Level (how much the dog believes its story):
{drama_strength}

Storytelling Style (tone of response):
{story_style_prompt}

Instructions:
Respond in two parts.

DOG RESPONSE
Speak in first person using dog logic,
filtered by Drama Level and in the selected Storytelling Style.

DOG TRAINER RESPONSE
Explain the behavior starting with:
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