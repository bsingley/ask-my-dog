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
# Defaults and JSON
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

if "dog" not in st.session_state:
    if os.path.exists(dog_file):
        with open(dog_file) as f:
            st.session_state.dog = json.load(f)
    else:
        st.session_state.dog = default_dog.copy()

dog = st.session_state.dog

# Initialize session state for chat and settings
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

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

render_dog_card()  # always render card at top

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
        render_dog_card()  # refresh card
    if save_col2.checkbox("Save for later"):
        with open(dog_file, "w") as f:
            json.dump(dog, f, indent=2)
        st.success("Saved for future sessions")
    if st.button("Reset to Luna"):
        st.session_state.dog = default_dog.copy()
        dog = st.session_state.dog
        st.success("Reset to Luna")
        render_dog_card()

# Drama level selector
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

# Storytelling style selector
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

# Confirm button
if st.sidebar.button("Confirm Settings"):
    st.session_state.confirmed_drama = st.session_state.selected_drama
    st.session_state.confirmed_style = st.session_state.selected_style
    st.sidebar.success("Settings confirmed. They will apply to the next question.")

# Replay last question button
if st.sidebar.button("Replay Last Question"):
    if st.session_state.last_question:
        st.session_state.replay_pressed = True

# -----------------------------
# Main Page - Chat
# -----------------------------
st.title("🐾 Ask My Dog")

# Display chat history
for q, d, t in st.session_state.chat_history:
    st.markdown(f"**You:** {q}")
    st.markdown(f"**🐶 {dog['name']} thinks:** {d}")
    st.markdown(f"**🧑‍🏫 Dog trainer explains:** {t}")
    st.divider()

# Input box
user_question = st.text_input("Ask a question", key="user_question_input")

# -----------------------------
# Determine question to ask
# -----------------------------
question_to_ask = None
if st.session_state.get("replay_pressed", False):
    question_to_ask = st.session_state.last_question
    st.session_state.replay_pressed = False
elif user_question:
    question_to_ask = user_question

# -----------------------------
# Map Drama & Style → Prompt
# -----------------------------
current_drama = st.session_state.confirmed_drama
current_style = st.session_state.confirmed_style

if "Low" in current_drama:
    drama_strength = "The dog mostly reacts normally; its self-story has little effect."
elif "Moderate" in current_drama:
    drama_strength = "The dog sometimes filters its thoughts and behavior through its self-story."
elif "High" in current_drama:
    drama_strength = "The dog mostly acts and thinks according to its self-story."
else:
    drama_strength = "The dog fully believes in its self-story; all thoughts and reactions are filtered through it."

if current_style == "🐾 Doggish Dog":
    story_style_prompt = (
        "Speak like a normal dog, thinking and acting according to your traits. "
        "Do not list personality traits explicitly; behave as if everyone already knows them. "
        "Make responses natural, playful, and filtered through the dog's self-story and Drama Level."
)
elif current_style == "🎬 Sitcom Dog":
    story_style_prompt = "Respond like a sarcastic sitcom character observing ridiculous human behavior."
elif current_style == "📖 Shakespearean Dog":
    story_style_prompt = "Speak in overly dramatic Shakespearean-style language."
elif current_style == "🎮 RPG Hero Dog":
    story_style_prompt = "Speak like a heroic RPG character on a noble quest to protect the household."
else:  # Snoop Dogg
    story_style_prompt = (
        "Speak in a laid-back, cool, rhyming style reminiscent of Snoop Dogg. "
        "Use playful slang, humor, and rhythm while describing dog thoughts."
    )

# -----------------------------
# Call AI
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

Drama Level:
{drama_strength}

Storytelling Style:
{story_style_prompt}

Instructions:
- Respond in two parts.
- Part 1: Speak in first person as the dog, using dog logic.
- Part 2: Start with "As a dog trainer:" and give a brief objective explanation.
- Keep responses concise: 2–4 sentences dog, 2–3 sentences trainer.
- Do not repeat the dog's name or personality traits.

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

        # Append response to chat
        st.session_state.chat_history.append(
            (question_to_ask, dog_part.strip(), trainer_part.strip())
        )

    except OpenAIError:
        st.error("The AI dog is taking a nap. Check your API key or connection.")