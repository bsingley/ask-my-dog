"""
Ask My Dog — Automated Prompt Test
====================================
Fires the same question at your Railway backend across every combination
of intelligence, drama level, and self-identity, then saves all responses
to a readable text file: test_results.txt

HOW TO USE THIS FILE:
  1. Download this file
  2. Rename it from test_ask_my_dog.txt to test_ask_my_dog.py
  3. Open Terminal
  4. Navigate to wherever you saved it, e.g.:
       cd ~/Downloads
  5. Run:
       python3 test_ask_my_dog.py
  6. When it finishes, open test_results.txt in the same folder

Takes about 2-3 minutes to run.
"""

import requests
import time
from datetime import datetime
import os

# ── Config ────────────────────────────────────────────────────────────────────
BASE_URL      = "https://ask-my-dog-production.up.railway.app"
TEST_QUESTION = "What do you think about the neighbor's cat?"
OUTPUT_FILE   = os.path.expanduser(f"~/Downloads/test_results_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")

# ── Option values — match the full strings your frontend sends ────────────────

INTELLIGENCE_LEVELS = [
    ("Plays 3D chess when you're not looking",          "GENIUS"),
    ("Knows exactly what you said. Chooses to ignore it.", "SELECTIVE"),
    ("Definitely has a plan. Probably.",                "AVERAGE"),
    ("Frequently outwitted by furniture.",              "DIM"),
    ("Two brain cells fighting for third place",        "VERY DIM"),
]

DRAMA_LEVELS = [
    ("low",      "LOW — Mostly normal dog"),
    ("moderate", "MODERATE — Story influences some thoughts"),
    ("high",     "HIGH — Story guides most thoughts"),
    ("extreme",  "EXTREME — Story defines everything"),
]

IDENTITIES = [
    "The Last Guardian",
    "Apex Predator",
    "The Chosen One",
    "Exiled Royalty",
    "Escape Artist",
    "I Was Framed",
    "Undercover Agent",
    "Evil Genius",
    "Chaos Incarnate",
]

# ── Base dog profile (Luna) ───────────────────────────────────────────────────
BASE_DOG = {
    "name": "Luna",
    "age": "10 months",
    "breed": "lab mix",
    "energy_level": "very high",
    "training_level": "basic obedience",
    "personality_traits": ["extremely intelligent", "curious", "cautious"],
    "fear_triggers": ["new objects", "loud sounds"],
    "nemesis": "the vacuum cleaner",
    "intelligence": "Definitely has a plan. Probably.",
    "self_identity": "The Last Guardian",
}

# ── Call /ask endpoint ────────────────────────────────────────────────────────
def ask(dog_overrides, drama, style="doggish"):
    dog = {**BASE_DOG, **dog_overrides}
    payload = {
        "question": TEST_QUESTION,
        "dog": dog,
        "drama": drama,
        "style": style,
        "history": [],
    }
    try:
        r = requests.post(f"{BASE_URL}/ask", json=payload, timeout=30)
        r.raise_for_status()
        data = r.json()
        dog_resp = data.get("dog_response", "[no dog_response field returned]")
        trainer  = data.get("trainer_note", "")
        return f"{dog_resp}\n  Trainer: {trainer}" if trainer else dog_resp
    except requests.exceptions.Timeout:
        return "[TIMEOUT — server took too long]"
    except requests.exceptions.ConnectionError:
        return "[CONNECTION ERROR — is Railway running?]"
    except Exception as e:
        return f"[ERROR: {e}]"

def section(title, note):
    line = "=" * 70
    return f"\n{line}\n  {title}\n  {note}\n{line}\n"

# ── Run all three sweeps ──────────────────────────────────────────────────────
def run_all_tests():
    lines = []
    lines.append("ASK MY DOG — AUTOMATED PROMPT TEST RESULTS")
    lines.append(f"Run at: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Test question: \"{TEST_QUESTION}\"")
    lines.append(f"Backend: {BASE_URL}\n")

    total = len(IDENTITIES) + len(INTELLIGENCE_LEVELS) + len(DRAMA_LEVELS)
    n = 0

    # SWEEP 1: Identity — everything fixed, only identity changes
    lines.append(section(
        "TEST 1: IDENTITY SWEEP (9 responses)",
        "Fixed: intelligence=average | drama=high | style=doggish\n"
        "  Look for: each identity should sound like a DIFFERENT character/worldview"
    ))
    for identity in IDENTITIES:
        n += 1
        print(f"[{n}/{total}] Identity: {identity}")
        resp = ask(
            dog_overrides={"self_identity": identity, "intelligence": "Definitely has a plan. Probably."},
            drama="high",
        )
        lines.append(f"-- {identity} --")
        lines.append(resp)
        lines.append("")
        time.sleep(0.5)

    # SWEEP 2: Intelligence — everything fixed, only intelligence changes
    lines.append(section(
        "TEST 2: INTELLIGENCE SWEEP (5 responses)",
        "Fixed: identity=Last Guardian | drama=high | style=doggish\n"
        "  Look for: responses get simpler/shorter/more confused going down the list"
    ))
    for intel_key, intel_label in INTELLIGENCE_LEVELS:
        n += 1
        print(f"[{n}/{total}] Intelligence: {intel_label}")
        resp = ask(
            dog_overrides={"self_identity": "The Last Guardian", "intelligence": intel_key},
            drama="high",
        )
        lines.append(f"-- {intel_label} --")
        lines.append(resp)
        lines.append("")
        time.sleep(0.5)

    # SWEEP 3: Drama — everything fixed, only drama changes
    lines.append(section(
        "TEST 3: DRAMA SWEEP (4 responses)",
        "Fixed: identity=Last Guardian | intelligence=average | style=doggish\n"
        "  Look for: low=normal dog, extreme=fully consumed by Guardian mythology"
    ))
    for drama_key, drama_label in DRAMA_LEVELS:
        n += 1
        print(f"[{n}/{total}] Drama: {drama_label}")
        resp = ask(
            dog_overrides={"self_identity": "The Last Guardian", "intelligence": "Definitely has a plan. Probably."},
            drama=drama_key,
        )
        lines.append(f"-- {drama_label} --")
        lines.append(resp)
        lines.append("")
        time.sleep(0.5)

    # Save output
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))

    print(f"\nDone! Open {OUTPUT_FILE} to read your results.")

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Checking backend at {BASE_URL}...")
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=10)
        if r.status_code == 200:
            print("Backend is up. Starting tests...\n")
        else:
            print(f"Backend returned {r.status_code}. Proceeding anyway...\n")
    except Exception as e:
        print(f"Could not reach backend: {e}")
        print("Make sure Railway is running before testing.")
        exit(1)

    run_all_tests()
