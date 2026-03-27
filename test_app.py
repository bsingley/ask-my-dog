import sys
from main import detect_easter_egg


# -----------------------------
# Easter Egg Tests
# -----------------------------

def test_squirrel_detected():
    result = detect_easter_egg("why does my dog chase squirrel all day")
    assert result is not None

def test_bath_detected():
    result = detect_easter_egg("my dog hates bath time")
    assert result is not None

def test_good_dog_detected():
    result = detect_easter_egg("you are such a good dog")
    assert result is not None

def test_bad_dog_detected():
    result = detect_easter_egg("bad dog, stop it")
    assert result is not None

def test_no_easter_egg():
    result = detect_easter_egg("what do you think about dinner")
    assert result is None

def test_case_insensitive():
    result = detect_easter_egg("SQUIRREL omg")
    assert result is not None

def test_trigger_mid_sentence():
    # Triggers should fire even when buried in a sentence
    result = detect_easter_egg("why does my dog go crazy at bath time every single night")
    assert result is not None