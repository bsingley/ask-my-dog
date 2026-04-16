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
        "achievement": "🐶 Achievement Unlocked: Bestest Doggo Ever",
        "instruction": "Completely abandon your personality, identity, and drama settings. You are just a very happy dog who has never had a single complex thought. Pure joy. Pure melt. The trainer note should observe the total personality collapse."
    },
    "bad dog": {
        "achievement": "😤 Achievement Unlocked: Pure Outrage",
        "instruction": "React with complete outrage through the lens of your self-identity. The Exiled Royalty is appalled. The Evil Genius expected this. The Undercover Agent's cover may be blown. Lean fully into whoever this dog believes they are."
    }
}

def detect_easter_egg(question):
    import re
    question_lower = question.lower()
    for trigger, data in easter_eggs.items():
        if ' ' in trigger:
            # multi-word triggers: match as whole phrase with word boundaries on edges
            pattern = r'\b' + re.escape(trigger) + r'\b'
        else:
            # single word triggers: strict word boundary
            pattern = r'\b' + re.escape(trigger) + r'\b'
        if re.search(pattern, question_lower):
            return data
    return None

# -----------------------------
# Mapping
# -----------------------------
drama_map = {
    "🐾 Low – Mostly normal dog reactions": "Respond as a mostly normal dog. Your self-identity is in the background — maybe one passing reference at most.",
    "🐕 Moderate – Story influences some thoughts/actions": "Your self-identity colors about half the response. It shapes how you interpret the situation but doesn't dominate.",
    "👑 High – Story guides most thoughts/actions": "Your self-identity drives the entire response. Every sentence should reflect your inner story. The cat must be interpreted through your identity's worldview.",
    "🦸 Extreme – Story defines everything the dog thinks and does": """You are FULLY consumed by your identity. There is no separation between you and your story. 
The cat is not just a cat — it means something specific to who you are. 
If you are The Last Guardian: the cat is an infiltrator threatening your watch. 
If you are Evil Genius: the cat is either a pawn or a rival. 
If you are Exiled Royalty: the cat is an affront to your dignity. 
If you are Chaos Incarnate: the cat is irrelevant, everything is chaos anyway.
Stay completely in character. Do not sound like a normal dog."""
}

style_map = {
    "🐾 Doggish Dog": "Respond naturally as a dog.",
    "🎬 Sitcom Dog": "Respond like a sarcastic sitcom character.",
    "📖 Shakespearean Dog": "Speak like Shakespeare.",
    "🎮 RPG Hero Dog": "Speak like a heroic RPG character.",
    "🎵 Snoop Dogg Dog": "Respond in a laid back Snoop Dogg style."
}

intelligence_map = {
    "Plays 3D chess when you're not looking": """You are a genius. Write 4-5 sentences minimum. 
Use sophisticated vocabulary. Analyze the topic strategically — even a cat becomes a subject 
for geopolitical-style assessment. Example of your voice: 'The cat represents a classic 
territorial incursion. I've mapped its patrol routes. It believes itself unobserved. It is not.'""",

    "Knows exactly what you said. Chooses to ignore it.": """You understand everything perfectly. 
Either give a surprisingly sharp, perceptive 3-4 sentence answer — or spend your response 
pointedly talking about something else entirely, making clear you heard the question and 
chose not to engage with it.""",

    "Definitely has a plan. Probably.": """Write 2-3 sentences. Normal dog intelligence. 
Attempt the question but get a little fuzzy or distracted by the end.""",

    "Frequently outwitted by furniture.": """Write 1-2 short, simple sentences only. 
Get confused or distracted mid-thought. Example: 'The cat... wait what was I saying. 
The cat is there. I think.'""",

    "Two brain cells fighting for third place": """Write 1-2 very short sentences maximum. 
Extremely simple words only. Lose track of the question. Example: 'Cat. CAT! 
I saw it. What was the question.'"""
}

drama_options = list(drama_map.keys())
style_options = list(style_map.keys())

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
    "self_identity": "The Last Guardian",
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

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=80)
st.sidebar.markdown(f"""
### {dog['name']}
**{dog['breed']}  {dog['age']}**  
**Identity:** {dog['self_identity']}  
**Intelligence:** {dog.get('intelligence', 'Definitely has a plan. Probably.')}


:yellow_heart: [Buy Luna a treat](https://venmo.com/u/Beth-Singley-1)
""")

# -----------------------------
# Main page
# -----------------------------

st.title("🐾 Ask My Dog")

st.markdown("#### Does this sound like your dog? ✏️")

if st.session_state.get("show_save_success"):
    st.success("Persona updated!")
    st.session_state.show_save_success = False

with st.expander("🐾 No? Edit your dog's persona here"):
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
        st.session_state.show_save_success = True
        st.rerun()
    if save_col2.checkbox("Save for later"):
        with open(dog_file, "w") as f:
            json.dump(dog, f, indent=2)
        st.success("Saved for future sessions")
    if st.button("Reset to Luna"):
        st.session_state.dog = default_dog.copy()
        dog = st.session_state.dog
        st.success("Reset to Luna")

col_drama, col_style = st.columns(2)
with col_drama:
    st.session_state.confirmed_drama = st.selectbox(
        "🎭 Drama Level",
        options=drama_options,
        index=drama_options.index(st.session_state.confirmed_drama)
    )
with col_style:
    st.session_state.confirmed_style = st.selectbox(
        "🎨 Storytelling Style",
        options=style_options,
        index=style_options.index(st.session_state.confirmed_style)
    )

# -----------------------------
# Chat function
# -----------------------------

# Chat renders here (see bottom of file)
chat_container = st.container()

submit = False
user_question = ""
replay = False

if not st.session_state.get("is_generating", False):
    with st.form(key="question_form", clear_on_submit=True):  
        user_question = st.text_input("Ask your dog a question", key="chat_input", label_visibility="collapsed", placeholder="Ask your dog something...")
        col1, col2 = st.columns([1, 3])
        submit = col1.form_submit_button("Ask")
    replay = st.button("🔁 Replay Last Question", disabled=not st.session_state.last_question)

# Determine the question to process this run

if submit and user_question.strip():
    active_question = user_question.strip()
    st.session_state.pending_question = active_question
elif replay and st.session_state.last_question:
    active_question = st.session_state.last_question
else:
    active_question = None
 
if active_question:

    st.session_state.is_generating = True

    question = active_question
    

    drama = drama_map[st.session_state.confirmed_drama]
    style = style_map[st.session_state.confirmed_style]
    intelligence = intelligence_map.get(dog.get("intelligence", "Definitely has a plan. Probably."), "")

    egg = detect_easter_egg(active_question) or {}

    if egg:
        special_instruction = f"\n\nSPECIAL OVERRIDE: {egg['instruction']}"
    else:
        special_instruction = ""

    prompt = f"""
You are a dog named {dog['name']}.

INTELLIGENCE — this controls how you think and write. Follow it strictly:
{intelligence}

SELF IDENTITY — this is who you believe you are. At drama=high or extreme, it should shape every sentence:
You are: {dog['self_identity']}
Your inner story: {dog.get('self_story', '')}

DRAMA — how deeply you believe your identity:
{drama}

STYLE — how you speak:
{style}

Background facts (use naturally, don't lead with them):
- Traits: {", ".join(dog["personality_traits"])}
- Fears: {", ".join(dog["fear_triggers"])}
- Nemesis: {dog.get("nemesis", "the vacuum cleaner")} — weave this in when relevant

Respond in two parts:

1. The dog speaking (2-4 sentences)
2. Start second section with "As a dog trainer:" and explain behavior briefly.
{special_instruction}

IMPORTANT: Do not default to generic dog responses. Your intelligence level and identity 
must be clearly visible in every sentence you write.

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

    except Exception as e:
        if str(e):
            st.session_state.chat_history.append(
                (question, "Something went wrong calling the AI.", "", None)
            )
    st.session_state.pending_question = ""
    st.session_state.is_generating = False


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

#scroll to the bottom of the page after render
if st.session_state.chat_history:
    st.components.v1.html("""
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 999999);
        </script>
    """, height=0)