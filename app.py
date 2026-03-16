import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os

# -----------------------------
# Setup
# -----------------------------
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

# Load or initialize dog
if "dog" not in st.session_state:
    if os.path.exists(dog_file):
        with open(dog_file) as f:
            st.session_state.dog = json.load(f)
    else:
        st.session_state.dog = default_dog.copy()
dog = st.session_state.dog

# -----------------------------
# Session state
# -----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "confirmed_drama" not in st.session_state:
    st.session_state.confirmed_drama = "🐾 Low – Mostly normal dog reactions"

if "confirmed_style" not in st.session_state:
    st.session_state.confirmed_style = "🐾 Doggish Dog"

if "current_input" not in st.session_state:
    st.session_state.current_input = ""

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
        t.strip() for t in st.text_input(
            "Personality Traits (comma-separated)",
            ", ".join(dog["personality_traits"])
        ).split(",")
    ]
    dog["fear_triggers"] = [
        t.strip() for t in st.text_input(
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

# -----------------------------
# Input box + AI call
# -----------------------------
st.session_state.current_input = st.text_input(
    "Ask your dog a question",
    value=st.session_state.current_input
)
submit_question = st.button("Ask")

# Determine question to ask
question_to_ask = None
if submit_question and st.session_state.current_input.strip() != "":
    question_to_ask = st.session_state.current_input.strip()
    st.session_state.last_question = question_to_ask

    # Map drama & style → prompt text
    drama_map = {
        "🐾 Low – Mostly normal dog reactions": "The dog mostly reacts normally; its self-story has little effect.",
        "🐕 Moderate – Story influences some thoughts/actions": "The dog sometimes filters its thoughts and behavior through its self-story.",
        "👑 High – Story guides most thoughts/actions": "The dog mostly acts and thinks according to its self-story.",
        "🦸 Extreme – Story defines everything the dog thinks and does": "The dog fully believes in its self-story; all thoughts and reactions are filtered through it."
    }
    drama_strength = drama_map[st.session_state.confirmed_drama]

    style_map = {
        "🐾 Doggish Dog": "Speak naturally according to your traits; do not list traits explicitly; behave as if everyone already knows them.",
        "🎬 Sitcom Dog": "Respond like a sarcastic sitcom character observing ridiculous human behavior.",
        "📖 Shakespearean Dog": "Speak in overly dramatic Shakespearean-style language.",
        "🎮 RPG Hero Dog": "Speak like a heroic RPG character on a noble quest to protect the household.",
        "🎵 Snoop Dogg Dog": "Speak in a laid-back, cool, rhyming style reminiscent of Snoop Dogg."
    }
    story_style_prompt = style_map[st.session_state.confirmed_style]

    prompt = build_prompt(dog, question_to_ask, drama_strength, story_style_prompt)

    # Call AI first
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

        # Append fully generated response
        st.session_state.chat_history.append((
            question_to_ask,
            dog_part.strip(),
            trainer_part.strip()
        ))

        # Reset input box
        st.session_state.current_input = ""

    except OpenAIError:
        st.session_state.chat_history.append((
            question_to_ask,
            "AI dog is taking a nap. Check your API key or connection.",
            ""
        ))