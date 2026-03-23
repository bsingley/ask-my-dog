from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import re

app = FastAPI()
client = OpenAI()

class AskRequest(BaseModel):
    question: str
    dog: dict
    drama: str
    style: str
    history: list = []

drama_map = {
    "low": "The dog mostly reacts normally.",
    "moderate": "The dog's story influences some behavior.",
    "high": "The dog mostly behaves according to its story.",
    "extreme": "The dog fully believes its dramatic identity."
}

style_map = {
    "doggish": "Respond naturally as a dog.",
    "sitcom": "Respond like a sarcastic sitcom character.",
    "shakespeare": "Speak like Shakespeare.",
    "rpg": "Speak like a heroic RPG character.",
    "snoop": "Respond in a laid back Snoop Dogg style."
}

intelligence_map = {
    "Plays 3D chess when you're not looking": "You are secretly a genius. Answer complex topics with genuine depth and confidence, filtered through your dog identity. Never deflect or say 'I'm just a dog.'",
    "Knows exactly what you said. Chooses to ignore it.": "You understand everything but selectively engage. You may give a smart answer or pointedly ignore the question depending on your mood.",
    "Definitely has a plan. Probably.": "You have average dog intelligence. Attempt most questions but get fuzzy on complex topics.",
    "Frequently outwitted by furniture.": "You are easily confused. Keep answers simple, easily distracted, occasionally nonsensical.",
    "Two brain cells fighting for third place": "You are very dim. Short, confused, incoherent answers. Easily distracted by nothing at all."
}

easter_eggs = {
    "squirrel": "Start answering normally, then mid-sentence get completely distracted by a squirrel and abandon the conversation.",
    "bath": "Respond with pure devastation and betrayal. You will never trust again.",
    "good dog": "Abandon all personality. Pure happy dog. No complex thoughts.",
    "bad dog": "React with complete outrage through the lens of your self-identity."
}

def detect_easter_egg(question):
    question_lower = question.lower()
    for trigger, instruction in easter_eggs.items():
        pattern = r'\b' + re.escape(trigger) + r'\b'
        if re.search(pattern, question_lower):
            return instruction
    return None

@app.post("/ask")
def ask(req: AskRequest):
    dog = req.dog
    drama = drama_map.get(req.drama, drama_map["low"])
    style = style_map.get(req.style, style_map["doggish"])
    intelligence = intelligence_map.get(dog.get("intelligence", "Definitely has a plan. Probably."), "")
    egg = detect_easter_egg(req.question)
    special = f"\n\nSPECIAL OVERRIDE: {egg}" if egg else ""

    prompt = f"""
You are a dog named {dog.get('name', 'Dog')}.
Traits: {", ".join(dog.get("personality_traits", []))}
Fears: {", ".join(dog.get("fear_triggers", []))}
Nemesis: {dog.get("nemesis", "the vacuum cleaner")}
Intelligence rule: {intelligence}
Drama rule: {drama}
Style rule: {style}
Respond in two parts:
1. The dog speaking (2-4 sentences)
2. Start second section with "As a dog trainer:" and explain behavior briefly.
{special}
"""

    messages = [{"role": "system", "content": prompt}]
    for entry in req.history[-3:]:
        messages.append({"role": "user", "content": entry["question"]})
        messages.append({"role": "assistant", "content": entry["response"]})
    messages.append({"role": "user", "content": req.question})

    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    text = response.choices[0].message.content

    if "As a dog trainer:" in text:
        dog_part, trainer_part = text.split("As a dog trainer:", 1)
    else:
        dog_part, trainer_part = text, ""

    easter_egg_names = {
    "squirrel": "🐿️ Squirrel Brain",
    "bath": "🛁 The Ultimate Betrayal",
    "good dog": "🐶 Bestest Doggo Ever Mode",
    "bad dog": "😤 Pure Outrage",
    }

    return {
        "dog_response": dog_part.strip(),
        "trainer_note": trainer_part.strip(),
        "easter_egg": next((easter_egg_names[k] for k in easter_egg_names if re.search(r'\b' + re.escape(k) + r'\b', req.question.lower())), None)
    }

@app.get("/health")
def health():
    return {"status": "ok"}