#!/usr/bin/env python3
"""
stage_classifier.py

Heuristic stage classifier for SA360-style responses.

Exposes:
    _score_text(text: str) -> dict
        Returns a dict with:
          - stage_score: float (0–100)
          - stage_label: str ("S1 Reactive Self", ..., "S8 Transcendent")
          - confidence: float (0–1)
          - word_count: int
          - indicators: dict of sub-scores

This is a **local heuristic model**, NOT a psychometric or clinical tool.
It’s designed to be:
    - deterministic
    - cheap to run
    - “directionally correct” for SA360-like developmental language.

Key design choices:
    - Empty / noise → S1
    - Short reactive statements → S1–S2
    - Self-regulation without systems/meta → S3–S4
    - Strong self-awareness + regulation + some meta → S5
    - Add systems / paradox / integration → S6+
    - Long reflective essays like “David Carroll full response” are
      **explicitly capped around S5–S6** unless they show strong
      meta + systems + perspective + both/and + decent regulation
      all at once.
"""

import re
from typing import Dict, Any


# ---------------------- Tokenization & Helpers ---------------------- #

WORD_RE = re.compile(r"[A-Za-z']+")


def _tokenize(text: str):
    return WORD_RE.findall(text.lower())


def _count_occurrences(text: str, patterns):
    """Count how many times any of the substrings in `patterns` appear."""
    t = text.lower()
    count = 0
    for p in patterns:
        count += t.count(p)
    return count


def _has_any(text: str, patterns):
    t = text.lower()
    return any(p in t for p in patterns)


# ---------------------- Indicator Extractors ----------------------- #

def _linguistic_complexity(text: str, tokens):
    """
    Very rough complexity proxy:
      - more words (up to a cap)
      - slightly longer words
      - presence of clause markers
    Returns 0–10.
    """
    wc = len(tokens)
    if wc == 0:
        return 0.0

    avg_len = sum(len(t) for t in tokens) / wc

    clause_markers = [
        "because", "although", "however", "therefore",
        "while", "whereas", "if", "then", "despite",
        "on the other hand", "at the same time",
    ]
    clause_hits = _count_occurrences(text, clause_markers)

    # word count component (up to 10 points)
    # 0 at 0 words, ~7 at 150 words, 10 at 400+
    wc_component = min(10.0, (wc / 150.0) * 7.0 + (wc / 400.0) * 3.0)

    # average word length component (up to ~2 points)
    len_component = max(0.0, min(2.0, (avg_len - 3.5) * 0.7))

    # clause component (up to ~3 points)
    clause_component = min(3.0, clause_hits * 0.7)

    score = wc_component + len_component + clause_component
    return max(0.0, min(10.0, score))


def _causal_reasoning(text: str):
    """
    Looks for causal connectors.
    0–10.
    """
    causal_patterns = [
        "because", "so that", "so i could", "so we could",
        "therefore", "as a result", "which led to", "which leads to",
        "this caused", "this creates", "in order to",
    ]
    hits = _count_occurrences(text, causal_patterns)
    if hits == 0:
        return 0.0
    return max(0.0, min(10.0, 3.0 + hits * 1.5))  # cap 10


def _meta_cognition(text: str):
    """
    Expanded meta-cognition detection to handle real SA360 essays.
    """
    t = text.lower()

    strong = [
        "i realize", "i realized",
        "i have noticed", "i notice", "i noticed",
        "i became aware", "i am aware",
        "i distinguish", "i distinguished",
        "i observe", "i observed",
        "i see myself", "i see that i",
        "thinking about my", "reflect on my",
        "inner voice", "internal conflict",
        "cognitive dissonance",
        "i get stuck",
    ]

    soft = [
        "i try to understand", "i am starting to see",
        "i’m learning that", "i’ve been noticing",
        "i take a step back", "i consider",
        "i reflect", "i’m aware",
    ]

    strong_hits = _count_occurrences(t, strong)
    soft_hits = _count_occurrences(t, soft)

    score = strong_hits * 2.5 + soft_hits * 1.2
    return min(10.0, score)



def _abstraction_systems(text: str):
    """
    Expanded systemic/abstract thinking.
    """
    t = text.lower()

    strong = [
        "pattern", "patterns", "underlying", "dynamics",
        "over time", "long-term", "feedback", "cycle",
        "relationship between", "interconnected",
        "everything is connected", "connected to everything",
        "bigger picture", "my relationship to",
    ]

    soft = [
        "how things fit together", "how it all connects",
        "multiple factors", "influence each other",
        "shifts over time", "tensions", "forces",
        "story i'm in", "story that i tell myself",
    ]

    strong_hits = _count_occurrences(t, strong)
    soft_hits = _count_occurrences(t, soft)

    score = strong_hits * 2.0 + soft_hits * 1.0
    return min(10.0, score)


def _emotion_regulation(text: str):
    """
    Expanded emotional regulation (positive & struggle).
    """
    t = text.lower()

    reg = [
        "i pause", "i take a breath", "i breathe",
        "i take a break", "i step away",
        "i choose healthier", "i choose a healthy",
        "respond from love", "respond from compassion",
        "i calm myself", "i regulate",
        "i used to be a good regulator",
    ]

    dys = [
        "i lash out", "i yell", "i shut down",
        "i drink", "acting out", "screw it",
        "avoidance", "isolation",
    ]

    reg_hits = _count_occurrences(t, reg)
    dys_hits = _count_occurrences(t, dys)

    score = reg_hits * 2.0
    if dys_hits > reg_hits:
        score -= 1.0

    return max(-1.0, min(10.0, score))



def _perspective_breadth(text: str):
    """
    Looking at multiple perspectives / empathy / we-ness.
    0–10.
    """
    patterns_strong = [
        "from their perspective", "from their point of view",
        "from her perspective", "from his perspective",
        "from their shoes", "step into their shoes",
        "multiple perspectives", "different perspectives",
        "many viewpoints", "various viewpoints",
        "our perspectives differ", "see where they're coming from",
    ]
    patterns_soft = [
        "they might be", "they may be", "they could be",
        "i can see why they", "i try to understand them",
        "we all have", "we each have", "we both have",
        "empathize with", "empathy for", "common humanity",
        "we as a team", "we as a group",
    ]

    strong_hits = _count_occurrences(text, patterns_strong)
    soft_hits = _count_occurrences(text, patterns_soft)

    score = strong_hits * 3.0 + soft_hits * 1.5
    return max(0.0, min(10.0, score))


def _both_and_thinking(text: str):
    """
    Both/And, paradox, synthesis language.
    0–10.
    """
    t = text.lower()

    explicit_both_and = re.findall(r"\bboth\b.*\band\b", t)
    one_hand_other = re.findall(r"on the one hand.*on the other hand", t)

    patterns_soft = [
        "at the same time", "while also", "even as i",
        "simultaneously", "i can hold", "i hold multiple truths",
        "tension between", "paradox", "seemingly opposite",
        "two things can be true", "multiple things can be true",
    ]

    strong_hits = len(explicit_both_and) + len(one_hand_other)
    soft_hits = _count_occurrences(t, patterns_soft)

    score = strong_hits * 4.0 + soft_hits * 2.0
    return max(0.0, min(10.0, score))


# ---------------------- Aggregation & Staging ---------------------- #

def _compute_indicators(text: str) -> Dict[str, float]:
    tokens = _tokenize(text)
    return {
        "Linguistic Complexity": _linguistic_complexity(text, tokens),
        "Causal Reasoning": _causal_reasoning(text),
        "Meta-cognition": _meta_cognition(text),
        "Abstraction/Systems": _abstraction_systems(text),
        "Emotion Regulation": _emotion_regulation(text),
        "Perspective Breadth": _perspective_breadth(text),
        "Both/And Thinking": _both_and_thinking(text),
    }


def _raw_stage_score(indicators: Dict[str, float]) -> float:
    """
    Weighted sum → [0, 100] (before any caps/adjustments).
    Weights favor meta, systems, perspective, both/and.
    """
    lc = indicators["Linguistic Complexity"]
    cr = indicators["Causal Reasoning"]
    mc = indicators["Meta-cognition"]
    sys = indicators["Abstraction/Systems"]
    er = indicators["Emotion Regulation"]
    pb = indicators["Perspective Breadth"]
    ba = indicators["Both/And Thinking"]

    # Base weighted sum
    weighted = (
        lc * 1.8 +
        cr * 1.2 +
        mc * 3.0 +
        sys * 3.0 +
        max(0.0, er) * 2.0 +   # only positive regulation boosts
        pb * 2.0 +
        ba * 2.0
    )
    # Approximate max if everything = 10 → 1.8+1.2+30+30+20+20+20 = 123
    max_possible = 123.0
    score = (weighted / max_possible) * 100.0
    return max(0.0, min(100.0, score))


def _apply_stage_guards(text: str, indicators: Dict[str, float], score: float) -> float:
    """
    Apply guardrails so we don't give S8 to everything long & reflective.
    In particular, long but self-critical essays like David's should
    land around S5–S6 unless:
      - Meta-cognition is strong
      - AND Systems is strong
      - AND Perspective breadth is strong
      - AND Both/And is present
      - AND Emotion regulation isn't net-negative
    """
    wc = len(_tokenize(text))
    mc = indicators["Meta-cognition"]
    sys = indicators["Abstraction/Systems"]
    pb = indicators["Perspective Breadth"]
    ba = indicators["Both/And Thinking"]
    er = indicators["Emotion Regulation"]

    # If text is short, don't allow very high scores even if language is fancy
    if wc < 40:
        score = min(score, 55.0)  # roughly S5 max for short blurbs

    # If it's a long narrative but systems or meta are weak, keep it mid-range
    if wc >= 200:
        if mc < 4.0 or pb < 3.0:
            score = min(score, 55.0)  # self-aware but not strongly post-conventional
        if sys < 3.0 and ba < 3.0:
            score = min(score, 60.0)

    # Emotional dysregulation should pull down the top-end
    if er < 0:
        score = min(score, 60.0)

    # To get above 70 (S7+), require strong meta + systems + perspective + both/and + at least neutral ER
    if score > 70.0:
        if not (mc >= 6.0 and sys >= 6.0 and pb >= 5.0 and ba >= 4.0 and er >= 0.0):
            score = 70.0  # cap at boundary of S7

    # To get above 80 (deep transpersonal), require very strong signals
    if score > 80.0:
        if not (mc >= 7.5 and sys >= 7.5 and pb >= 7.0 and ba >= 6.0 and er >= 2.0):
            score = 80.0

    return max(0.0, min(100.0, score))


def _score_to_stage_label(score: float) -> str:
    """
    Map numeric score to S1–S8.
    Ranges chosen so:
      S1: 0–9
      S2: 10–19
      S3: 20–29
      S4: 30–39
      S5: 40–54
      S6: 55–69
      S7: 70–84
      S8: 85–100
    """
    if score < 10:
        return "S1 Reactive Self"
    elif score < 20:
        return "S2 Boundary Pusher"
    elif score < 30:
        return "S3 Rule Follower"
    elif score < 40:
        return "S4 Loyal Contributor"
    elif score < 55:
        return "S5 Achiever"
    elif score < 70:
        return "S6 Synthesizer"
    elif score < 85:
        return "S7 Meta-Systemic"
    else:
        return "S8 Transcendent"


def _confidence_from_score(score: float) -> float:
    """
    Simple confidence heuristic:
      - Low near boundaries
      - High in the middle of bands
    """
    # Midpoints of each band
    band_centers = [5, 15, 25, 35, 47, 62, 77, 92]
    # Find nearest center
    nearest = min(band_centers, key=lambda c: abs(score - c))
    dist = abs(score - nearest)

    # 0 distance → 1.0, 10+ away → ~0.4
    conf = max(0.4, 1.0 - (dist / 20.0))
    return round(conf, 2)


# ---------------------- Public API ---------------------- #

def _score_text(text: str) -> Dict[str, Any]:
    """
    Main scoring entry point.
    """
    text = (text or "").strip()
    tokens = _tokenize(text)
    word_count = len(tokens)

    # Handle empty / near-empty
    if word_count == 0:
        indicators = {
            "Linguistic Complexity": 0.0,
            "Causal Reasoning": 0.0,
            "Meta-cognition": 0.0,
            "Abstraction/Systems": 0.0,
            "Emotion Regulation": 0.0,
            "Perspective Breadth": 0.0,
            "Both/And Thinking": 0.0,
        }
        stage_score = 2.0
        stage_label = "S1 Reactive Self"
        confidence = 0.01
        return {
            "stage_score": stage_score,
            "stage_label": stage_label,
            "confidence": confidence,
            "word_count": word_count,
            "indicators": indicators,
        }

    # Base indicators from text
    indicators = _compute_indicators(text)

    # --------------------------------------------------------------
    # Heuristic: long, strongly causal leadership narratives
    # --------------------------------------------------------------
    # For very long SA360-style responses with strong causal reasoning,
    # our keyword-based meta/systems detection can under-read the depth.
    # If word_count is high and Causal Reasoning is strong, but
    # Meta-cognition / Abstraction/Systems / Both-And are very low,
    # we infer some reflective complexity.
    causal = indicators.get("Causal Reasoning", 0.0)
    meta = indicators.get("Meta-cognition", 0.0)
    systems = indicators.get("Abstraction/Systems", 0.0)
    both_and = indicators.get("Both/And Thinking", 0.0)

    if word_count >= 400 and causal >= 5.0:
        # Only intervene when these signals are clearly under-detected
        if meta < 3.0 and systems < 3.0:
            indicators["Meta-cognition"] = max(meta, 6.0)
            indicators["Abstraction/Systems"] = max(systems, 4.0)
        if both_and < 2.0:
            indicators["Both/And Thinking"] = max(both_and, 2.0)

    # Now compute score and label using the (possibly adjusted) indicators
    raw_score = _raw_stage_score(indicators)
    final_score = _apply_stage_guards(text, indicators, raw_score)
    label = _score_to_stage_label(final_score)
    conf = _confidence_from_score(final_score)

    return {
        "stage_score": round(final_score, 2),
        "stage_label": label,
        "confidence": conf,
        "word_count": word_count,
        "indicators": {
            k: (round(v, 2) if isinstance(v, float) else v)
            for k, v in indicators.items()
        },
    }



# ---------------------- Manual CLI Test ---------------------- #

if __name__ == "__main__":
    # Simple manual smoke test if you run:
    #   python3 stage_classifier.py
    sample = (
        "I hold multiple truths and design frameworks that adapt over time. "
        "I notice my reactions and pause intentionally before responding."
    )
    result = _score_text(sample)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
