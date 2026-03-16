import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os

api_key = os.environ.get("API_KEY")
client = OpenAI()

st.set_page_config(page_title="Ask My Dog", page_icon="🐾")

# -----------------------------
# Load or Initialize Dog Persona
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
    "self_story": "protector of the household",
    "superhero_identity": "None"
}

dog_file = "dog_profile.json"
if os.path.exists(dog_file):
    with open(dog_file) as f:
        dog = json.load(f)
else:
    dog = default_dog.copy()

# -----------------------------
# Sidebar: Dog Info + Selections
# -----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=120)
    st.markdown(f"### 🐶 {dog['name']}")
    st.caption(f"Self-Story: {dog['self_story']}")
    st.divider()

    # -----------------------------
    # Drama Level (Self-story belief)
    # -----------------------------
    if "drama_level" not in st.session_state:
        st.session_state.drama_level = "🐾 Low – Mostly normal dog reactions"

    drama_level = st.selectbox(
        "🎭 Drama Level",
        [
            "🐾 Low – Mostly normal dog reactions",
            "🐕 Moderate – Story influences some thoughts/actions",
            "👑 High – Story guides most thoughts/actions",
            "🦸 Extreme – Story defines everything the dog thinks and does"
        ],
        index=[
            "🐾 Low – Mostly normal dog reactions",
            "🐕 Moderate – Story influences some thoughts/actions",
            "👑 High – Story guides most thoughts/actions",
            "🦸 Extreme – Story defines everything the dog thinks and does"
        ].index(st.session_state.drama_level),
        key="drama_level"
    )

    # Map Drama Level → Prompt Description
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

    # -----------------------------
    # Storytelling Style (tone/voice)
    # -----------------------------
    if "story_style" not in st.session_state:
        st.session_state.story_style = "🐾 Realistic Dog"

    story_style = st.selectbox(
        "🎨 Storytelling Style",
        [
            "🐾 Doggish Dog",
            "🎬 Sitcom Dog",
            "📖 Shakespearean Dog",
            "🎮 RPG Hero Dog",
            "🎵 Snoop Dogg Dog"
        ],
        index=[
            "🐾 Doggish Dog",
            "🎬 Sitcom Dog",
            "📖 Shakespearean Dog",
            "🎮 RPG Hero Dog",
            "🎵 Snoop Dogg Dog"
        ].index(st.session_state.story_style),
        key="story_style"
    )

    # Map Storytelling Style → Prompt
    if story_style == "Doggish Dog":
        story_style_prompt = "Speak like a normal dog thinking in simple playful thoughts."
    elif story_style == "Sitcom Dog":
        story_style_prompt = "Respond like a sarcastic sitcom character observing ridiculous human behavior."
    elif story_style == "Shakespearean Dog":
        story_style_prompt = "Speak in overly dramatic Shakespearean-style language."
    elif story_style == "RPG Hero Dog":
        story_style_prompt = "Speak like a heroic RPG character on a noble quest to protect the household."
    else:  # Snoop Dogg
        story_style_prompt = (
            "Speak in a laid-back, cool, rhyming style reminiscent of Snoop Dogg. "
            "Use playful slang, humor, and rhythm while describing dog thoughts."
        )

# -----------------------------
# Dog Character Card (Main Page)
# -----------------------------
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=80)
with col2:
    st.markdown(f"""
### 🐶 {dog['name']}

**{dog['breed']} • {dog['age']}**  
**Identity:** {dog['self_identity']}  
**Self-Story:** {dog['self_story']}
""")

st.divider()

# -----------------------------
# Persona Expander
# -----------------------------
with st.expander("⚙️ View or edit full dog persona"):
    st.write(f"**Training Level:** {dog['training_level']}")
    st.write("**Personality Traits:** " + ", ".join(dog['personality_traits']))
    st.write("**Fear Triggers:** " + ", ".join(dog['fear_triggers']))
    st.write(f"**Self Story:** {dog['self_story']}")
    st.write(f"**Superhero Identity:** {dog['superhero_identity']}")

    if st.checkbox("Edit persona"):
        dog["name"] = st.text_input("Dog name", dog["name"])
        dog["breed"] = st.text_input("Breed", dog["breed"])
        dog["age"] = st.text_input("Age", dog["age"])
        dog["energy_level"] = st.text_input("Energy level", dog["energy_level"])
        dog["training_level"] = st.text_input("Training level", dog["training_level"])
        dog["self_identity"] = st.text_input("Self identity", dog["self_identity"])
        dog["self_story"] = st.text_input("Self story", dog["self_story"])
        dog["superhero_identity"] = st.text_input("Superhero identity", dog["superhero_identity"])

        save_col1, save_col2 = st.columns(2)
        if save_col1.button("Save Updates"):
            st.success("Persona updated!")
        if save_col2.checkbox("Save for later"):
            with open(dog_file, "w") as f:
                json.dump(dog, f, indent=2)
            st.success("Saved for future sessions")
        if st.button("Reset to Luna"):
            dog = default_dog.copy()
            st.success("Reset to Luna")

st.divider()

# -----------------------------
# Ask Question
# -----------------------------
st.markdown("### Ask your dog a question")
user_question = st.text_input(f"What would you like to ask {dog['name']}?")

# -----------------------------
# AI Response
# -----------------------------
if user_question:
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
{user_question}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        text = response.output_text.strip()

        # Split into dog / trainer
        if "As a dog trainer:" in text:
            dog_part, trainer_part = text.split("As a dog trainer:", 1)
        else:
            dog_part = text
            trainer_part = ""

        # Display Dog response
        st.markdown(f"### 🐶 {dog['name']} thinks...")
        st.markdown(dog_part.strip())

        # Display Trainer explanation in expander
        if trainer_part.strip():
            with st.expander("🧑‍🏫 Dog trainer explains"):
                st.markdown(trainer_part.strip())

    except OpenAIError:
        st.error("The AI dog is taking a nap. Check your API key or connection.")