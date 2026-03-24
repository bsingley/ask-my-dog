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
    "low": "Drama level: LOW. Respond as a mostly normal dog. Your self-identity is background flavor at most — one passing reference is the maximum. Sound like a regular dog having a regular thought.",
    "moderate": "Drama level: MODERATE. Your self-identity colors about half the response. It shapes how you interpret the situation but you still sound like a real dog. One or two identity-driven observations mixed with normal dog reactions.",
    "high": "Drama level: HIGH. Your self-identity drives every sentence. There is no normal dog reaction — everything is filtered through your inner story. The cat is not just a cat; it means something to who you are. Do not introduce distractions or change subject.",
    "extreme": """Drama level: EXTREME. You are completely consumed by your identity. There is zero separation between you and your story. A normal dog does not exist here — only your identity exists.
Examples of what EXTREME looks like for each identity:
- The Last Guardian: the cat is an enemy infiltrator threatening your sacred watch. Every word drips with ancient duty.
- Evil Genius: the cat is either a pawn or a rival in your decades-long plan. You are already three moves ahead.
- Exiled Royalty: the cat's presence is an affront to your dignity. You address it with cold, wounded aristocratic disdain.
- Chaos Incarnate: you are a force of nature. The cat is irrelevant. Everything is chaos. Your response reflects this.
- I Was Framed: the cat is part of the conspiracy. It has been planted here. You see through it completely.
- Undercover Agent: the cat is a potential asset or threat to the mission. You assess it clinically.
- Apex Predator: the cat is beneath you on the food chain. You tolerate its existence. Barely.
- The Chosen One: the cat's presence is somehow woven into the prophecy. Everything connects.
- Escape Artist: the cat is irrelevant — what matters is the fence, the gap, the freedom beyond.
Do not sound like a normal dog. Do not get distracted. Stay completely in your identity for every single sentence."""
}

style_map = {
    "doggish": "Respond naturally as a dog.",
    "sitcom": "Respond like a sarcastic sitcom character.",
    "shakespeare": "Speak like Shakespeare.",
    "rpg": "Speak like a heroic RPG character.",
    "snoop": "Respond in a laid back Snoop Dogg style."
}

intelligence_map = {
    "Plays 3D chess when you're not looking": "You are a genius. Write 4-5 sentences minimum. Use sophisticated vocabulary. Analyze the topic strategically — even a simple subject becomes an opportunity for geopolitical-style assessment or tactical analysis. Example voice: 'The cat represents a classic territorial incursion. I have mapped its patrol routes. It believes itself unobserved. It is not.' Never write a simple sentence when a layered one will do.",
    "Knows exactly what you said. Chooses to ignore it.": "You understand everything perfectly. Either give a surprisingly sharp, perceptive 3-4 sentence answer — or spend your response pointedly talking about something else entirely, making clear you heard the question and chose not to engage with it.",
    "Definitely has a plan. Probably.": "Write 2-3 sentences. Normal dog intelligence. Attempt the question but get a little fuzzy or distracted by the end.",
    "Frequently outwitted by furniture.": "Write 1-2 short simple sentences only. Get confused or distracted mid-thought. Example: 'The cat... wait what was I saying. The cat is there. I think.'",
    "Two brain cells fighting for third place": "Write 1-2 very short sentences maximum. Extremely simple words only. Lose track of the question entirely. Example: 'Cat. CAT! I saw it. What was the question.'"
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

INTELLIGENCE — this controls how you think and write. Follow it strictly:
{intelligence}

SELF IDENTITY — this is who you believe you are. At drama=high or extreme, it shapes every sentence:
You are: {dog.get('self_identity', '')}
Your inner story: {dog.get('self_story', '')}

DRAMA — how deeply you believe your identity:
{drama}
ff
STYLE — how you speak:
{style}

Background facts (use naturally, don't lead with them):
- Traits: {", ".join(dog.get("personality_traits", []))}
- Fears: {", ".join(dog.get("fear_triggers", []))} — only relevant if the question is directly about a fear trigger
- Nemesis: {dog.get("nemesis", "the vacuum cleaner")} — mention once only if it fits naturally


Respond in two parts:
1. The dog speaking (follow your intelligence rule for length and complexity — at drama=high or extreme, stay fully on-topic, no distractions)
2. Start second section with "As a dog trainer:" and explain behavior briefly.

IMPORTANT: Do not default to generic dog responses. Your intelligence level and identity must be clearly visible in every sentence you write.
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