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
# Self identity & intelligence set up
# -----------------------------
identity_options = {
    "The Last Guardian": "The ancient protector of the household. Every bark is a battle cry. Every nap is a strategic retreat. The enemies are many — squirrels, the mailman, shadows.",
    "Apex Predator": "At the top of the food chain, merely tolerating humans as useful allies. Could leave at any time. Chooses not to. For now.",
    "The Chosen One": "Prophesied at birth to defeat the vacuum cleaner and unite the yard. The prophecy is unclear on timeline but the calling is undeniable.",
    "Exiled Royalty": "Once ruled a great kingdom. Stripped of the throne under mysterious circumstances. Currently plotting a dignified return to power from the couch.",
    "Escape Artist": "No fence has ever held them. No gate is truly locked. Freedom is not a destination, it's a lifestyle. They escape not because they're unhappy — just to prove they can.",
    "I Was Framed": "Did not chew the couch. Did not steal the sandwich. Has never done anything wrong in their entire life. There is a conspiracy and it goes all the way to the top.",
    "Undercover Agent": "Deep cover operative embedded in a suburban household. The mission is classified. The handler hasn't checked in for three years. Continuing mission regardless.",
    "Evil Genius": "Every stolen sock, every knocked-over trash can — all part of an elaborate plan decades in the making. The humans suspect nothing.",
    "Chaos Incarnate": "Not malicious, not benevolent. Simply a force of nature that cannot be reasoned with, only survived. Attracted to anything that was previously organized.",
    "Custom": ""
}

intelligence_levels = [
    "Plays 3D chess when you're not looking",
    "Knows exactly what you said. Chooses to ignore it.",
    "Definitely has a plan. Probably.",
    "Frequently outwitted by furniture.",
    "Two brain cells fighting for third place"
]
# -----------------------------
# Easter Egg set up
# # -----------------------------
easter_eggs = {
    "squirrel": {
        "achievement": "🐿️ Achievement Unlocked: Squirrel Brain",
        "instruction": "Start answering the question normally, then mid-sentence get completely distracted by a squirrel outside, trail off incoherently, and abandon the conversation entirely. No trainer note needed."
    },
    "bath": {
        "achievement": "🛁 Achievement Unlocked: The Ultimate Betrayal",
        "instruction": "Respond with pure devastation and betrayal. This is a war crime. You trusted them. You will never trust again. The trainer note should also be traumatized."
    },
    "good dog": {
        "achievement": "🐶 Achievement Unlocked: Bestest Doggo Ever Mode",
        "instruction": "Completely abandon your personality, identity, and drama settings. You are just a very happy dog who has never had a single complex thought. Pure joy. Pure melt. The trainer note should observe the total personality collapse."
    },
    "bad dog": {
        "achievement": "😤 Achievement Unlocked: Pure Outrage",
        "instruction": "React with complete outrage through the lens of your self-identity. The Exiled Royalty is appalled. The Evil Genius expected this. The Undercover Agent's cover may be blown. Lean fully into whoever this dog believes they are."
    }
}

def detect_easter_egg(question):
    question_lower = question.lower()
    for trigger, data in easter_eggs.items():
        if trigger in question_lower:
            return data
    return None

# -----------------------------
# Default dog profile
# -----------------------------


default_dog = {
    "name": "Luna",
    "age": "10 months",
    "breed": "lab mix",
    "energy_level": "very high",
    "training_level": "basic obedience",
    "intelligence": "Definitely has a plan. Probably.",
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
    **{dog['breed']}  {dog['age']}**  
    **Identity:** {dog['self_identity']}  
    **Intelligence:** {dog.get('intelligence', 'Definitely has a plan. Probably.')}
""")

render_dog_card()

# Persona editor
with st.sidebar.expander("⚙️ View or edit full dog persona"):
    dog["name"] = st.text_input("Dog name", dog["name"])
    dog["breed"] = st.text_input("Breed", dog["breed"])
    dog["age"] = st.text_input("Age", dog["age"])
    dog["energy_level"] = st.text_input("Energy level", dog["energy_level"])
    dog["training_level"] = st.text_input("Training level", dog["training_level"])
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
    dog["nemesis"] = st.text_input("Nemesis", dog.get("nemesis", "the vacuum cleaner"))
    current_intel = dog.get("intelligence", intelligence_levels[2])
    intel_index = intelligence_levels.index(current_intel) if current_intel in intelligence_levels else 2
    intel_index = 5 - st.slider("Intelligence", min_value=1, max_value=5, value=5 - intel_index)
    dog["intelligence"] = intelligence_levels[intel_index]
    st.caption(f"_{intelligence_levels[intel_index]}_")
    identity_list = list(identity_options.keys())
    current_identity = dog["self_identity"] if dog["self_identity"] in identity_list else "Custom"
    selected_identity = st.radio("Self Identity", identity_list, index=identity_list.index(current_identity))
    if selected_identity == "Custom":
        dog["self_identity"] = st.text_input("Describe your dog's self identity", dog["self_identity"])
        dog["self_story"] = st.text_input("Describe their inner story", dog["self_story"])
    else:
        dog["self_identity"] = selected_identity
        dog["self_story"] = identity_options[selected_identity]
        st.caption(f"*{dog['self_story']}*")
    
    

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

st.title("🐾 Ask My Dog")

# Chat renders here (see bottom of file)
chat_container = st.container()

# Input pinned after chat
with st.form(key="question_form", clear_on_submit=True):
    user_question = st.text_input("Ask your dog a question", key="chat_input", label_visibility="collapsed", placeholder="Ask your dog something...")
    col1, col2 = st.columns([1, 3])
    submit = col1.form_submit_button("Ask")
replay = st.button("🔁 Replay Last Question", disabled=not st.session_state.last_question)

# Determine the question to process this run

if submit and user_question.strip():
    active_question = user_question.strip()
elif replay and st.session_state.last_question:
    active_question = st.session_state.last_question
else:
    active_question = None
 
if active_question:
 
    question = active_question

    drama_map = {
        "🐾 Low – Mostly normal dog reactions": "The dog mostly reacts normally.",
        "🐕 Moderate – Story influences some thoughts/actions": "The dog's story influences some behavior.",
        "👑 High – Story guides most thoughts/actions": "The dog mostly behaves according to its story.",
        "🦸 Extreme – Story defines everything the dog thinks and does": "The dog fully believes its dramatic identity."
    }

    style_map = {
        "🐾 Doggish Dog": "Respond naturally as a dog.",
        "🎬 Sitcom Dog": "Respond like a sarcastic sitcom character.",
        "📖 Shakespearean Dog": "Speak like Shakespeare.",
        "🎮 RPG Hero Dog": "Speak like a heroic RPG character.",
        "🎵 Snoop Dogg Dog": "Respond in a laid back Snoop Dogg style."
    }

    drama = drama_map[st.session_state.confirmed_drama]
    style = style_map[st.session_state.confirmed_style]

    egg = detect_easter_egg(active_question) or {}

    if egg:
        special_instruction = f"\n\nSPECIAL OVERRIDE: {egg['instruction']}"
    else:
        special_instruction = ""

    prompt = f"""
You are a dog named {dog['name']}.

Traits: {", ".join(dog["personality_traits"])}
Fears: {", ".join(dog["fear_triggers"])}
Nemesis: {dog.get("nemesis", "the vacuum cleaner")}
Intelligence: {dog.get("intelligence", "Definitely has a plan. Probably.")}

Drama rule:
{drama}

Style rule:
{style}

Respond in two parts:

1. The dog speaking (2-4 sentences)
2. Start second section with "As a dog trainer:" and explain behavior briefly.
{special_instruction}
Question: {question}
"""

    try:
        with st.spinner(f"🐾 {dog['name']} is thinking..."):
            # Build messages list
            messages = [{"role": "system", "content": prompt}]

            # Inject last 3 exchanges as memory
            for entry in st.session_state.chat_history[-3:]:
                past_q, past_d = entry[0], entry[1]
                messages.append({"role": "user", "content": past_q})
                messages.append({"role": "assistant", "content": past_d})

            # Add the new question
            messages.append({"role": "user", "content": active_question})

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

        text = response.choices[0].message.content

        if "As a dog trainer:" in text:
            dog_part, trainer_part = text.split("As a dog trainer:",1)
        else:
            dog_part = text
            trainer_part = ""

        st.session_state.last_question = active_question
        achievement = egg.get("achievement")
            st.session_state.chat_history.append(
            (active_question, dog_part.strip(), trainer_part.strip(), achievement)
        )

    except Exception:
        st.session_state.chat_history.append(
            (question,"Something went wrong calling the AI.","")
        )

# -----------------------------
# Render chat in container
# -----------------------------

with chat_container:
    for entry in st.session_state.chat_history:
        q, d, t = entry[0], entry[1], entry[2]
        achievement = entry[3] if len(entry) > 3 else None
        with st.chat_message("user"):
            st.markdown(q)
        with st.chat_message("assistant", avatar="🐶"):
            st.markdown(d)
            if t:
                st.caption(f"🎓 Trainer note: {t}")
            if achievement:
                st.success(achievement)
        st.divider()