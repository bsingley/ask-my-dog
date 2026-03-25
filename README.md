# Ask My Dog 🐶

**Ask My Dog** is a playful AI app that answers questions from the perspective of your dog, combining creativity with technical experimentation in AI-driven UX.

Users can:

* Ask their dog questions and get in-character responses
* Customize the dog's full persona including identity, intelligence, and nemesis
* Adjust drama level and storytelling style
* Follow along in a chat-style conversation feed
* Discover hidden easter eggs

**Live demo:** [ask-my-dog.streamlit.app](https://ask-my-dog-syur5g5wj4wxkuke7xtk5p.streamlit.app/)

---

## Current State

The app is live as a Streamlit web app. A native iOS version is in final pre-submission polish.

### Streamlit App Stack
| Layer | Technology |
|---|---|
| UI + Backend | Streamlit + Python |
| AI | OpenAI GPT-4o-mini |

### Native App Stack
| Layer | Technology |
|---|---|
| Mobile UI | React Native + Expo |
| Backend | FastAPI (Python) |
| Hosting | Railway |
| AI | OpenAI GPT-4o-mini |


```

### Native App
```mermaid
flowchart TD
    Phone[React Native App] --> Railway[FastAPI on Railway]
    Railway --> OpenAI[OpenAI API]
    OpenAI --> Railway
    Railway --> Phone

    subgraph Backend logic
        Prompt[Prompt builder]
        Easter[Easter egg detection]
        Memory[Conversation memory]
    end
```

---

## Features

* **Dynamic AI personas:** Fully editable dog profile including name, breed, age, energy level, training level, personality traits, fear triggers, nemesis, and intelligence level
* **Self identity selector:** Nine dramatic preset identities plus a Custom option. Each preset includes a hidden backstory that enriches the AI prompt
* **Intelligence slider:** Five-level scale from "Two brain cells fighting for third place" to "Plays 3D chess when you're not looking"
* **Nemesis field:** Freeform input woven naturally into responses
* **Drama level selector:** Four levels controlling how deeply the dog believes its own story
* **Storytelling styles:** Five voice modes — Doggish, Sitcom, Shakespearean, RPG Hero, Snoop Dogg
* **Conversation memory:** Last 3 exchanges passed into each API call
* **Chat-style feed:** User and assistant bubbles
* **Trainer notes:** Brief objective explanation of dog behavior below each reply
* **Easter eggs:** Four hidden triggers that override AI behavior and unlock achievement banners
* **About tab:** Version number, feedback link, Venmo tip link, privacy policy and terms of use

---

## Easter Eggs

| Trigger | Achievement | Behavior |
|---|---|---|
| "squirrel" | 🐿️ Squirrel Brain | Trails off mid-sentence, gone |
| "bath" | 🛁 The Ultimate Betrayal | Pure devastation. Trust destroyed |
| "good dog" | 🐶 Bestest Doggo Ever Mode | Identity collapses into pure happy dog |
| "bad dog" | 😤 Pure Outrage | Self-identity activates dramatically |

---

## Testing

Ask My Dog uses four layers of testing, developed in collaboration with AI tooling.

### Unit Tests
Covers the easter egg detection logic in isolation — no server or API calls required. Seven tests verify that each easter egg trigger is detected correctly, that detection is case-insensitive, that triggers fire when buried mid-sentence, and that non-trigger input returns cleanly.

### Automated Prompt Tests
Fires a test question at the live Railway backend across all 9 identities, 5 intelligence levels, and 4 drama levels — 18 total calls. Results are saved to a text file for manual review.

Requires the Railway backend to be live. This test is less about pass/fail and more about verifying that AI behavior actually shifts meaningfully across persona settings — a quality check specific to AI-driven UX.

### Manual Smoke Tests
- **Backend:** Hit `/health` on Railway, confirm `{"status":"ok"}`. Use the `/docs` page to verify Luna returns a real response.
- **Mobile:** Run Expo via tunnel, scan QR code in Expo Go, confirm chat and persona editor are working.

### Manual UI Test Suite
A systematically derived test suite covering chat flow, conversation memory, easter egg triggers, persona editing, drama and style controls, and mobile-specific behavior including keyboard handling and tab switching.

---

## Future Improvements

* Dog expression images wired to identity and easter egg states
* Multiple dog profiles with a switcher
* Training tip journal — export trainer notes as PDF
* Voice output via OpenAI TTS
* Mood system — dynamic mood field that shifts responses
* Clear chat and download conversation buttons
* Easter egg animations
* Saved achievements
