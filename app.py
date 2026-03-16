import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os
import random

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Ask My Dog", page_icon="🐾")
st.title("🐾 Ask My Dog")

api_key = os.environ.get("API_KEY")
client = OpenAI()

# -----------------------------
# Default dog persona
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

# -----------------------------
# Session State Initialization
# -----------------------------
if "dog" not in st.session_state:
    if os.path.exists(dog_file):
        with open(dog_file) as f:
            st.session_state.dog = json.load(f)
    else:
        st.session_state.dog = default_dog.copy()

# Ensure all keys exist
for key, value in default_dog.items():
    if key not in st.session_state.dog:
        st.session_state.dog[key] = value

dog = st.session_state.dog

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Drama and Story options
drama_options = [
    "🐾 Low – Mostly normal dog reactions",
    "🐕 Moderate – Story influences some thoughts/actions",
    "👑 High – Story guides most thoughts/actions",
    "🦸 Extreme – Story defines everything the dog thinks and does"
]
style_options = [
    "🐾 Doggish Dog", 
    "🎬 Sitcom Dog", 
    "📖 Shakespearean Dog", 
    "🎮 RPG Hero Dog", 
    "🎵 Snoop Dogg Dog"
]

if "drama_level" not in st.session_state or st.session_state.drama_level not in drama_options:
    st.session_state.drama_level = "🐕 Moderate – Story influences some thoughts/actions"
if "confirmed_drama" not in st.session_state:
    st.session_state.confirmed_drama = st.session_state.drama_level

if "story_style" not in st.session_state or st.session_state.story_style not in style_options:
    st.session_state.story_style = "🐾 Doggish Dog"
if "confirmed_style" not in st.session_state:
    st.session_state.confirmed_style = st.session_state.story_style

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "placeholder_question" not in st.session_state:
    st.session_state.placeholder_question = random.choice([
        "Why do I chase my tail?",
        "How can I make new friends?",
        "Why do I bark at strangers?",
        "What’s my favorite part of the house?",
        "How can I be a better fetch player?",
        "Why do I get scared of the vacuum?",
        "What’s my favorite toy?",
    ])


# -----------------------------
# Sidebar: Dog Card
# -----------------------------
def render_dog_card():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=80)
    st.sidebar.markdown(f"""
### {dog['name']}
**{dog['breed']} • {dog['age']}**  
**Identity:** {dog['self_identity']}
""")

render_dog_card()  # <-- only call here


# Only render after persona editor to reflect any changes
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
        render_dog_card()  # Refresh card immediately
    if save_col2.checkbox("Save for later"):
        with open(dog_file, "w") as f:
            json.dump(dog, f, indent=2)
        st.success("Saved for future sessions")
    if st.button("Reset to Luna"):
        st.session_state.dog = default_dog.copy()
        dog = st.session_state.dog
        st.success("Reset to Luna")
        render_dog_card()  # Refresh card


# -----------------------------
# Sidebar: Drama & Storytelling Style
# -----------------------------
drama_level = st.sidebar.selectbox(
    "🎭 Drama Level",
    drama_options,
    index=drama_options.index(st.session_state.drama_level),
    key="drama_level"
)
story_style = st.sidebar.selectbox(
    "🎨 Storytelling Style",
    style_options,
    index=style_options.index(st.session_state.story_style),
    key="story_style"
)
if st.sidebar.button("✅ Confirm Settings"):
    st.session_state.confirmed_drama = st.session_state.drama_level
    st.session_state.confirmed_style = st.session_state.story_style
    st.sidebar.success("Settings saved! Will apply to next question.")

# -----------------------------
# Sidebar: Replay Last Question
# -----------------------------
replay_button = False
if st.session_state.last_question:
    replay_button = st.sidebar.button("🔁 Replay Last Question")

# -----------------------------
# Main Page: Display Chat History
# -----------------------------
for i, (q, dog_resp, trainer_resp) in enumerate(st.session_state.chat_history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"🐶 **{dog['name']} thinks:** {dog_resp}")
    if trainer_resp:
        with st.expander("🧑‍🏫 Dog trainer explains"):
            st.markdown(trainer_resp)
    st.divider()



# -----------------------------
# Map confirmed settings to prompt
# -----------------------------
current_drama = st.session_state.confirmed_drama
current_style = st.session_state.confirmed_style

# Drama mapping → compute BEFORE AI call
if "Low" in current_drama:
    drama_strength = "The dog mostly reacts normally; its self-story has little effect."
elif "Moderate" in current_drama:
    drama_strength = "The dog sometimes filters its thoughts and behavior through its self-story."
elif "High" in current_drama:
    drama_strength = "The dog mostly acts and thinks according to its self-story."
else:  # Extreme
    drama_strength = "The dog fully believes in its self-story; all thoughts and reactions are filtered through it."

# Story style mapping → compute BEFORE AI call
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
# Main Page: User Input
# -----------------------------

user_question = st.text_input(
    f"What would you like to ask {dog['name']}?",
    placeholder=f"e.g., {st.session_state.placeholder_question}",
    key="user_question_input"
)

# Determine which question to ask
question_to_ask = None

if st.session_state.get("replay_pressed", False):
    question_to_ask = st.session_state.last_question
    st.session_state.replay_pressed = False  # reset

elif user_question:
    question_to_ask = user_question

# Only call AI if we actually have a question
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
- Part 1: Speak in first person as the dog, using dog logic.
- Make your responses reflect the Drama Level and exaggerate as appropriate.
- Keep dog responses concise: 2–4 sentences max.
- Part 2: Start with "As a dog trainer:" and give a brief objective explanation.
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

        # Append to chat history
        st.session_state.chat_history.append(
            (question_to_ask, dog_part.strip(), trainer_part.strip())
        )

    except OpenAIError:
        st.error("The AI dog is taking a nap. Check your API key or connection.")

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
- Part 1: Speak in first person as the dog, using dog logic.
- Make your responses **reflect the Drama Level** and exaggerate as appropriate.
- Keep dog responses concise: 2–4 sentences max.
- Part 2: Start the next paragraph with exactly "As a dog trainer:" and give an objective explanation of the dog's behavior.
- Keep trainer explanations brief: 2–3 sentences max.
- Do not repeat the dog's name or personality traits.
- First paragraph is the dog's perspective; second is the trainer explanation.

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

        # Append to chat history
        st.session_state.chat_history.append(
            (question_to_ask, dog_part.strip(), trainer_part.strip())
        )

        # No experimental_rerun() here — the next run naturally displays the new response
    except OpenAIError:
        st.error("The AI dog is taking a nap. Check your API key or connection.")