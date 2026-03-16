import streamlit as st
from openai import OpenAI, OpenAIError
import json
import os

st.set_page_config(page_title="Ask My Dog", page_icon="🐾")

st.title("🐾 Ask My Dog")

client = OpenAI()

# -----------------------------
# Default Dog
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

dog_file = "dog_profile.json"

if os.path.exists(dog_file):
    with open(dog_file) as f:
        dog = json.load(f)
else:
    dog = default_dog.copy()

# -----------------------------
# Dog Character Card
# -----------------------------

col1, col2 = st.columns([1,4])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=80)

with col2:
    st.markdown(f"""
### 🐶 {dog['name']}

**{dog['breed']} • {dog['age']}**

**Identity:** {dog['self_identity']}  
**Confidence Mode:** {confidence_choice}
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
# Dog Confidence Selector
# -----------------------------

confidence_choice = st.selectbox(
    "How does this dog view themselves?",
    [
        "🐶 Nervous Puppy",
        "🐕 Normal Dog",
        "👑 Very Important Dog",
        "🦸 Legendary Household Guardian"
    ],
    help="Controls how dramatic your dog's internal monologue will be."
)

st.caption(f"Current mindset: **{confidence_choice}**")

if "Nervous Puppy" in confidence_choice:
    confidence_style = "The dog is slightly unsure and cautious."
elif "Normal Dog" in confidence_choice:
    confidence_style = "The dog has normal playful dog confidence."
elif "Very Important Dog" in confidence_choice:
    confidence_style = "The dog believes they are responsible for important household decisions."
else:
    confidence_style = "The dog believes they are the heroic protector of the household."

st.divider()

# -----------------------------
# Ask Question
# -----------------------------

st.markdown("### Ask your dog a question")

user_question = st.text_input(
    f"What would you like to ask {dog['name']}?"
)

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
Self identity: {dog['self_identity']}
Self story: {dog['self_story']}
Superhero identity: {dog['superhero_identity']}

Confidence style:
{confidence_style}

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

        st.divider()

        st.markdown(f"### 🐶 {dog['name']} thinks...")

        st.markdown(dog_part)

        st.markdown("### 🧑‍🏫 Dog trainer explains")

        st.markdown(trainer_part)

    except OpenAIError:

        st.error("The AI dog is taking a nap. Check your API key or connection.")