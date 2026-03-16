import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os
import random

# -----------------------------
# Setup
# -----------------------------
st.set_page_config(page_title="Ask My Dog", page_icon="🐾")
st.title("🐾 Ask My Dog")

api_key = os.environ.get("API_KEY")
client = OpenAI()

# -----------------------------
# Default Dog Persona
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
    "self_story": "protector of the household"
}

dog_file = "dog_profile.json"

# Store dog in session_state to persist updates across reruns
if "dog" not in st.session_state:
    if os.path.exists(dog_file):
        with open(dog_file) as f:
            st.session_state.dog = json.load(f)
    else:
        st.session_state.dog = default_dog.copy()

dog = st.session_state.dog
# --- Sidebar ---
# 1️⃣ Dog Card
render_dog_card()

# 2️⃣ Persona Editor (always in an expander, no checkbox)
with st.sidebar.expander("⚙️ View or edit full dog persona"):
    dog["name"] = st.text_input("Dog name", dog["name"])
    dog["breed"] = st.text_input("Breed", dog["breed"])
    dog["age"] = st.text_input("Age", dog["age"])
    dog["energy_level"] = st.text_input("Energy level", dog["energy_level"])
    dog["training_level"] = st.text_input("Training level", dog["training_level"])
    dog["self_identity"] = st.text_input("Self identity", dog["self_identity"])
    dog["self_story"] = st.text_input("Self story", dog["self_story"])

    # Editable lists
    dog["personality_traits"] = [
        trait.strip() for trait in st.text_input(
            "Personality Traits (comma-separated)",
            ", ".join(dog["personality_traits"])
        ).split(",")
    ]
    dog["fear_triggers"] = [
        trigger.strip() for trigger in st.text_input(
            "Fear Triggers (comma-separated)",
            ", ".join(dog["fear_triggers"])
        ).split(",")
    ]

    save_col1, save_col2 = st.columns(2)
    if save_col1.button("Save Updates"):
        st.success("Persona updated!")
    if save_col2.checkbox("Save for later"):
        with open(dog_file, "w") as f:
            json.dump(dog, f, indent=2)
        st.success("Saved for future sessions")
    if st.button("Reset to Luna"):
        st.session_state.dog = default_dog.copy()
        st.success("Reset to Luna")
        dog = st.session_state.dog

# 3️⃣ Drama Level
drama_level = st.sidebar.selectbox("🎭 Drama Level", drama_options,
                                   index=drama_options.index(st.session_state.drama_level),
                                   key="drama_level")

# 4️⃣ Storytelling Style
story_style = st.sidebar.selectbox("🎨 Storytelling Style", style_options,
                                   index=style_options.index(st.session_state.story_style),
                                   key="story_style")

# 5️⃣ Confirm Settings Button
if st.sidebar.button("✅ Confirm Settings"):
    st.session_state.confirmed_drama = st.session_state.drama_level
    st.session_state.confirmed_style = st.session_state.story_style
    st.sidebar.success("Settings saved! Will apply to next question.")

# 6️⃣ Replay Last Question
if st.session_state.last_question:
    if st.sidebar.button("🔁 Replay Last Question"):
        question_to_ask = st.session_state.last_question

# -----------------------------
# Sample Placeholder Questions
# -----------------------------
sample_questions = [
    "Why do I chase my tail?",
    "How can I make new friends?",
    "Why do I bark at strangers?",
    "What’s my favorite part of the house?",
    "How can I be a better fetch player?",
    "Why do I get scared of the vacuum?",
    "What’s my favorite toy?",
]

if "placeholder_question" not in st.session_state:
    st.session_state.placeholder_question = random.choice(sample_questions)

# -----------------------------
# Chat Input (Main Page)
# -----------------------------
user_question = st.text_input(
    f"What would you like to ask {dog['name']}?",
    placeholder=f"e.g., {st.session_state.placeholder_question}",
    key="user_question_input"
)

# -----------------------------
# Replay Last Question
# -----------------------------
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if st.session_state.last_question:
    if st.sidebar.button("🔁 Replay Last Question"):
        question_to_ask = st.session_state.last_question
    else:
        question_to_ask = user_question if user_question else None
else:
    question_to_ask = user_question if user_question else None

# -----------------------------
# Use Confirmed Settings for next question
# -----------------------------
current_drama = st.session_state.get("confirmed_drama", st.session_state.drama_level)
current_style = st.session_state.get("confirmed_style", st.session_state.story_style)

# Map Drama → Prompt Description
if "Low" in current_drama:
    drama_strength = "The dog mostly reacts normally; its self-story has little effect."
elif "Moderate" in current_drama:
    drama_strength = "The dog sometimes filters its thoughts and behavior through its self-story."
elif "High" in current_drama:
    drama_strength = "The dog mostly acts and thinks according to its self-story."
else:
    drama_strength = "The dog fully believes in its self-story; all thoughts and reactions are filtered through it."

# Map Style → Prompt
if current_style == "🐾 Doggish Dog":
    story_style_prompt = "Speak like a normal dog thinking in simple playful thoughts."
elif current_style == "🎬 Sitcom Dog":
    story_style_prompt = "Respond like a sarcastic sitcom character observing ridiculous human behavior."
elif current_style == "📖 Shakespearean Dog":
    story_style_prompt = "Speak in overly dramatic Shakespearean-style language."
elif current_style == "🎮 RPG Hero Dog":
    story_style_prompt = "Speak like a heroic RPG character on a noble quest to protect the household."
else:  # 🎵 Snoop Dogg Dog
    story_style_prompt = (
        "Speak in a laid-back, cool, rhyming style reminiscent of Snoop Dogg. "
        "Use playful slang, humor, and rhythm while describing dog thoughts."
    )

# -----------------------------
# AI Response
# -----------------------------
if question_to_ask:
    st.session_state.last_question = question_to_ask

    prompt = f"""
You are a dog named {dog['name']}.

Background personality information (use only if relevant):
Age: {dog['age']}
Breed: {dog['breed']}
Energy level: {dog['energy_level']}
Training level: {dog['training_level']}
Fear triggers: {', '.join(dog['fear_triggers'])}
Personality traits: {', '.join(dog['personality_traits'])}

Self-Story:
{dog['self_story']}

Drama Level (how much the dog believes its story):
{drama_strength}

Storytelling Style (tone of response):
{story_style_prompt}

Instructions:
- Respond in two parts.
- Part 1: Speak in first person as the dog, using dog logic and filtered by Drama Level and Storytelling Style.
- Part 2: Start the next paragraph with exactly "As a dog trainer:" and give an objective explanation of the dog's behavior.
- Do not include any other labels. The first paragraph is the dog's perspective.

User question:
{question_to_ask}
"""

    try:
        with st.spinner("🐾 Luna is thinking..."):
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

        # Display responses in main page
        st.markdown(f"### 🐶 {dog['name']} thinks...")
        st.markdown(dog_part.strip())

        if trainer_part.strip():
            with st.expander("🧑‍🏫 Dog trainer explains"):
                st.markdown(trainer_part.strip())

    except OpenAIError:
        st.error("The AI dog is taking a nap. Check your API key or connection.")