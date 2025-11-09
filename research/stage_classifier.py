import re
import math
from typing import Dict


# --------------------------------------------------
# Utility
# --------------------------------------------------

def word_count(text: str) -> int:
    words = re.findall(r"\b\w+\b", text)
    return len(words)


# --------------------------------------------------
# Indicator Functions
# --------------------------------------------------

def indicator_linguistic_complexity(text: str) -> float:
    words = word_count(text)
    avg_len = sum(len(w) for w in re.findall(r"\b\w+\b", text)) / (words or 1)
    return round(min(10.0, (avg_len / 6.0) * 10.0), 2)


def indicator_causal_reasoning(text: str) -> float:
    causal_terms = re.findall(r"\b(because|since|therefore|thus|due to|as a result)\b", text.lower())
    return min(10.0, len(causal_terms) * 2.5)


def indicator_meta_cognition(text: str) -> float:
    meta_terms = re.findall(r"\b(thought|reflect|aware|notice|observe|understand|realize|insight)\b", text.lower())
    return min(10.0, len(meta_terms) * 2.5)


def indicator_abstraction_systems(text: str) -> float:
    systems_terms = re.findall(
        r"\b(system|structure|pattern|feedback|process|loop|framework|emerge|dynamic|complex)\b",
        text.lower(),
    )
    return min(10.0, len(systems_terms) * 2.5)


def indicator_emotion_regulation(text: str) -> float:
    reg_terms = re.findall(r"\b(calm|pause|regulate|compose|control|manage emotion|center)\b", text.lower())
    react_terms = re.findall(r"\b(angry|mad|furious|upset|yell|rage)\b", text.lower())
    score = len(reg_terms) * 3.0 - len(react_terms) * 2.0
    return max(0.0, min(10.0, score))


def indicator_perspective_breadth(text: str) -> float:
    perspective_terms = re.findall(
        r"\b(others|team|we|they|different views|perspective|stakeholder|worldview)\b",
        text.lower(),
    )
    return min(10.0, len(perspective_terms) * 2.0)


def indicator_both_and(text: str) -> float:
    if re.search(r"\bon the one hand\b.*\bon the other hand\b", text.lower()) or \
       re.search(r"\bboth\b.*\band\b", text.lower()):
        return 6.0
    if "paradox" in text.lower() or "coexist" in text.lower() or "balance" in text.lower():
        return 4.0
    return 0.0


# --------------------------------------------------
# Weights
# --------------------------------------------------

WEIGHTS = {
    "Linguistic Complexity": 1.0,
    "Causal Reasoning": 1.3,
    "Meta-cognition": 2.0,
    "Abstraction/Systems": 2.2,
    "Emotion Regulation": 1.5,
    "Perspective Breadth": 1.5,
    "Both/And Thinking": 1.8,
}


# --------------------------------------------------
# Score Function
# --------------------------------------------------

def score_from_indicators(ind: Dict[str, float], wc: int) -> float:
    weighted = sum(ind[k] * WEIGHTS[k] for k in WEIGHTS)
    if wc == 0:
        return 0.0

    # Normalization
    if wc < 8:
        norm = 0.7
    elif wc < 60:
        norm = 1.0
    elif wc < 250:
        norm = 0.85
    else:
        norm = 0.7

    # Synergy effect for multiple cognitive indicators
    high_signals = sum(
        1 for k in ("Meta-cognition", "Abstraction/Systems", "Both/And Thinking", "Perspective Breadth")
        if ind[k] > 0
    )
    synergy = 1.0 + min(0.4, 0.1 * max(0, high_signals - 1))

    raw = weighted * norm * synergy
    scaled = 100 * (1 - math.exp(-raw / 7.5))  # smoother curve
    return max(0.0, min(100.0, round(scaled, 2)))


# --------------------------------------------------
# Stage Mapping
# --------------------------------------------------

STAGE_MAP = [
    (0, 10, "S1 Reactive Self"),
    (10, 20, "S2 Boundary Pusher"),
    (20, 30, "S3 Rule Follower"),
    (30, 40, "S4 Loyal Contributor"),
    (40, 55, "S5 Achiever"),
    (55, 70, "S6 Synthesizer"),
    (70, 85, "S7 Integrative"),
    (85, 100, "S8 Transcendent"),
]


def label_stage(score: float) -> str:
    for low, high, label in STAGE_MAP:
        if low <= score < high:
            return label
    return "S8 Transcendent"


# --------------------------------------------------
# Main Function
# --------------------------------------------------

def _score_text(raw: str) -> Dict:
    wc = word_count(raw)

    indicators = {
        "Linguistic Complexity": indicator_linguistic_complexity(raw),
        "Causal Reasoning": indicator_causal_reasoning(raw),
        "Meta-cognition": indicator_meta_cognition(raw),
        "Abstraction/Systems": indicator_abstraction_systems(raw),
        "Emotion Regulation": indicator_emotion_regulation(raw),
        "Perspective Breadth": indicator_perspective_breadth(raw),
        "Both/And Thinking": indicator_both_and(raw),
    }

    t_low = raw.lower()

    # --- Soft boosts for abstract/meta systems ---
    if re.search(r"multiple truths|synthesis|integrate|meta[- ]system|adaptive framework", t_low):
        indicators["Meta-cognition"] += 4
        indicators["Abstraction/Systems"] += 4
    if re.search(r"feedback loop|evolve the system|systemic|complex adaptive", t_low):
        indicators["Abstraction/Systems"] += 3
    if re.search(r"paradox|contradiction|balance|coexist|dialectic", t_low):
        indicators["Both/And Thinking"] += 3

    # --- Penalty for emotional reactivity ---
    if re.search(r"angry|mad|furious|upset|yell", t_low):
        indicators["Emotion Regulation"] -= 2

    score = score_from_indicators(indicators, wc)
    stage = label_stage(score)

    # --- Gentle hierarchical overrides ---
    if re.search(r"multiple truths|synthesis|integrate|meta[- ]system", t_low):
        if score < 65:
            stage = "S6 Synthesizer"
            score = max(score, 65)
    elif re.search(r"feedback loop|systemic|evolve the system", t_low):
        if score < 55:
            stage = "S5 Achiever"
            score = max(score, 55)
    elif re.search(r"paradox|contradiction|balance|coexist", t_low):
        if score < 50:
            stage = "S4 Loyal Contributor"
            score = max(score, 50)

    confidence = round(min(1.0, score / 100), 2)
    return {
        "stage_score": score,
        "stage_label": stage,
        "confidence": confidence,
        "word_count": wc,
        "indicators": indicators,
    }


# --------------------------------------------------
# Manual Quick Test
# --------------------------------------------------

if __name__ == "__main__":
    samples = [
        "I get angry when things go wrong and I yell immediately.",
        "I notice my reactions and pause intentionally before responding.",
        "I explore how feedback loops in our system create recurring outcomes.",
        "On the one hand we need speed, on the other hand we need safety.",
        "I hold multiple truths and design frameworks that adapt over time.",
        "I integrate feedback across perspectives to evolve the system iteratively.",
        "I see paradoxes as signals for synthesis between competing values.",
    ]
    for s in samples:
        print(f"\n{s}\n→ {_score_text(s)}")
