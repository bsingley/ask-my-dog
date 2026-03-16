import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os
import random

# -----------------------------
# Setup
# -----------------------------
api_key = os.environ.get("API_KEY")
client = OpenAI()
st.set_page_config(page_title="Ask My Dog", page_icon="🐾")

# -----------------------------
# Default dog profile
# -----------------------------
default_dog = {
    "name": "Luna",
    "age": "10 months",
    "breed": "lab mix",
    "energy_level": "very high",
    "training_level": "basic obedience",
    "self_identity": "fearless guardian",
    "self_story": "protector of the household",
    "personality_traits": ["extremely intelligent", "curious", "cautious"],
    "fear_triggers": ["new objects", "loud sounds"]
}

dog_file = "dog_profile.json"

if "dog" not in st.session_state:
    if os.path.exists(dog_file):
        with open(dog_file) as f:
            st.session_state.dog = json.load(f)
    else:
        st.session_state.dog = default_dog.copy()

dog = st.session_state.dog

# -----------------------------
# Session state for chat and settings
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "replay_pressed" not in st.session_state:
    st.session_state.replay_pressed = False

if "confirmed_drama" not in st.session_state:
    st.session_state.confirmed_drama = "🐾 Low – Mostly normal dog reactions"

if "confirmed_style" not in st.session_state:
    st.session_state.confirmed_style = "🐾 Doggish Dog"

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("🐾 Dog Profile")

def render_dog_card():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=80)
    st.sidebar.markdown(f"""
### {dog['name']}
**{dog['breed']} • {dog['age']}**  
**Identity:** {dog['self_identity']}
""")

render_dog_card()

# Persona editor
with st.sidebar.expander("⚙️ View or edit full dog persona"):
    dog["name"] = st.text_input("Dog name", dog["name"])
    dog["breed"] = st.text_input("Breed", dog["breed"])
    dog["age"] = st.text_input("Age", dog["age"])
    dog["energy_level"] = st.text_input("Energy level", dog["energy_level"])
    dog["training_level"] = st.text_input("Training level", dog["training_level"])
    dog["self_identity"] = st.text_input("Self identity", dog["self_identity"])
    dog["self_story"] = st.text_input("Self story", dog["self_story"])
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
        render_dog_card()
    if save_col2.checkbox("Save for later"):
        with open(dog_file, "w") as f:
            json.dump(dog, f, indent=2)
        st.success("Saved for future sessions")
    if st.button("Reset to Luna"):
        st.session_state.dog = default_dog.copy()
        dog = st.session_state.dog
        st.success("Reset to Luna")
        render_dog_card()

# Drama level
st.sidebar.markdown("### 🎭 Drama Level")
drama_options = [
    "🐾 Low – Mostly normal dog reactions",
    "🐕 Moderate – Story influences some thoughts/actions",
    "👑 High – Story guides most thoughts/actions",
    "🦸 Extreme – Story defines everything the dog thinks and does"
]
st.session_state.selected_drama = st.sidebar.selectbox(
    "Select Drama Level",
    options=drama_options,
    index=drama_options.index(st.session_state.confirmed_drama)
)

# Storytelling style
st.sidebar.markdown("### 🎨 Storytelling Style")
style_options = [
    "🐾 Doggish Dog",
    "🎬 Sitcom Dog",
    "📖 Shakespearean Dog",
    "🎮 RPG Hero Dog",
    "🎵 Snoop Dogg Dog"
]
st.session_state.selected_style = st.sidebar.selectbox(
    "Select Storytelling Style",
    options=style_options,
    index=style_options.index(st.session_state.confirmed_style)
)

# Confirm settings
if st.sidebar.button("Confirm Settings"):
    st.session_state.confirmed_drama = st.session_state.selected_drama
    st.session_state.confirmed_style = st.session_state.selected_style
    st.sidebar.success("Settings confirmed. They will apply to the next question.")

# Replay last question
if st.sidebar.button("Replay Last Question"):
    if st.session_state.last_question:
        st.session_state.replay_pressed = True

# -----------------------------
# Main page - Chat
# -----------------------------
st.title("🐾 Ask My Dog")

# Display chat history
for q, d, t in st.session_state.chat_history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**🐶 {dog['name']} thinks:** {d}")
    st.markdown(f"**🧑‍🏫 Dog trainer explains:** {t}")
    st.divider()

# Sample questions for placeholder
sample_questions = [
    "What's the best part of your day?",
    "What scares you the most?",
    "How do you feel about new people?",
    "What's your favorite game or toy?",
    "Describe your dream adventure!"
]
placeholder_text = random.choice(sample_questions)

st.markdown("### Ask your dog a question")
user_question = st.text_input(
    "Type your question here",
    key="user_question_input",
    placeholder=random.choice(sample_questions)
)

submit_question = st.button("Ask")

# -----------------------------
# Determine which question to ask
# -----------------------------
question_to_ask = None

if st.session_state.replay_pressed:
    question_to_ask = st.session_state.last_question
    st.session_state.replay_pressed = False
elif submit_question and user_question.strip() != "":
    question_to_ask = user_question.strip()

# -----------------------------
# Map drama & style → prompt
# -----------------------------
current_drama = st.session_state.confirmed_drama
current_style = st.session_state.confirmed_style

drama_map = {
    "🐾 Low – Mostly normal dog reactions": "The dog mostly reacts normally; its self-story has little effect.",
    "🐕 Moderate – Story influences some thoughts/actions": "The dog sometimes filters its thoughts and behavior through its self-story.",
    "👑 High – Story guides most thoughts/actions": "The dog mostly acts and thinks according to its self-story.",
    "🦸 Extreme – Story defines everything the dog thinks and does": "The dog fully believes in its self-story; all thoughts and reactions are filtered through it."
}
drama_strength = drama_map[current_drama]

style_map = {
    "🐾 Doggish Dog": "Speak like a normal dog, thinking and acting according to your traits. Do not list personality traits explicitly; behave as if everyone already knows them. Make responses natural, playful, and filtered through the dog's self-story and Drama Level.",
    "🎬 Sitcom Dog": "Respond like a sarcastic sitcom character observing ridiculous human behavior.",
    "📖 Shakespearean Dog": "Speak in overly dramatic Shakespearean-style language.",
    "🎮 RPG Hero Dog": "Speak like a heroic RPG character on a noble quest to protect the household.",
    "🎵 Snoop Dogg Dog": "Speak in a laid-back, cool, rhyming style reminiscent of Snoop Dogg. Use playful slang, humor, and rhythm while describing dog thoughts."
}
story_style_prompt = style_map[current_style]

# -----------------------------
# Call AI
# -----------------------------
if question_to_ask:
    st.session_state.last_question = question_to_ask
    # Build prompt and call OpenAI here

    prompt = f"""
You are a dog named {dog['name']}.

Background personality information:
Age: {dog['age']}
Breed: {dog['breed']}
Energy level: {dog['energy_level']}
Training level: {dog['training_level']}
Fear triggers: {', '.join(dog['fear_triggers'])}
Personality traits: {', '.join(dog['personality_traits'])}

Self-Story:
{dog['self_story']}

Drama Level:
{drama_strength}

Storytelling Style:
{story_style_prompt}

Instructions:
- Respond in two parts.
- Part 1: Speak in first person as the dog, concise (2–4 sentences), extreme according to Drama Level.
- Part 2: Start with "As a dog trainer:" and give a brief objective explanation (2–3 sentences).
- Do not repeat the dog's name or list traits explicitly.

User question:
{question_to_ask}
"""

    try:
        with st.spinner(f"🐾 {dog['name']} is thinking..."):
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

        st.session_state.chat_history.append(
            (question_to_ask, dog_part.strip(), trainer_part.strip())
        )

    except OpenAIError:
        st.error("The AI dog is taking a nap. Check your API key or connection.")