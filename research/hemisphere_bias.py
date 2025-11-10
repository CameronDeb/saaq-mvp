#!/usr/bin/env python3
"""
hemisphere_bias.py

Deterministic, keyword-and-style-based Hemispheric Bias Analyzer.

Outputs a JSON-serializable dict with:
{
  "hemispheric_score": float,   # -100 .. +100
  "dominant_hemisphere": str,   # "Left"|"Right"|"Balanced"
  "confidence": float,          # 0.0 .. 1.0
  "indicators": { ... },        # integer indicator counts
  "interpretive_summary": str
}

Implementation notes:
- Only uses: re, json, math
- Deterministic (no randomness), heuristic and explainable.
- Inspired by the SAAQ Hemispheric Perspective (left analytic <-> right relational/holistic).
"""

import re
import json
import math

# -----------------------
# Config / keyword lists
# -----------------------

# Left-hemisphere keyword hints (analytic, sequential, logical, structural)
_LEFT_KEYWORDS = [
    r"\banalys", r"\banalyze", r"\banalytic", r"\bdata\b", r"\bmeasure", r"\bmetric",
    r"\bquantif", r"\bstat", r"\bevidence\b", r"\btherefore\b", r"\bthus\b",
    r"\bconclude", r"\bcalculate", r"\balgorithm", r"\bstep", r"\bsequence",
    r"\bfirst\b", r"\bsecond\b", r"\bthird\b", r"\bprocedure\b", r"\bprocess\b",
    r"\blogic\b", r"\breason", r"\bobjective\b", r"\bstructured\b", r"\bprecise\b"
]

# Right-hemisphere keyword hints (emotive, sensory, metaphorical, intuitive)
_RIGHT_KEYWORDS = [
    r"\bfeel", r"\bfeels\b", r"\bemot", r"\bemotion", r"\bintuit", r"\bintuition",
    r"\bimage", r"\bimagery\b", r"\bmetaphor", r"\blike a\b", r"\bas if\b",
    r"\bsense\b", r"\bsensory\b", r"\bbeautiful\b", r"\bpoetic\b", r"\bmuse",
    r"\bdream", r"\bcreative\b", r"\bheart\b", r"\bsoul\b", r"\bhazy\b",
    r"\bcolor\b", r"\btexture\b", r"\bvision\b", r"\bwholeness\b", r"\bholistic\b"
]

# Additional small lexical lists for features
_SENSORY_ADJECTIVES = [r"\bbright\b", r"\bdark\b", r"\bsilky\b", r"\brough\b", r"\bwarm\b", r"\bcold\b"]
_SEQUENTIAL_CUES = [r"\bthen\b", r"\bnext\b", r"\bafter that\b", r"\bfinally\b"]
_METAPHOR_CUES = [r"\blike a\b", r"\bas if\b", r"\bfeels like\b", r"\bseems like\b"]

# caps for indicator values (pre-normalization)
_INDICATOR_CAP = 12  # max raw count used for normalization

# weights applied when computing left vs right raw totals
_LEFT_WEIGHTS = {
    "Analytic Thinking": 1.2,
    "Sequential Logic": 1.0,
    "Language Structure": 0.9
}
_RIGHT_WEIGHTS = {
    "Emotional Imagery": 1.2,
    "Creative Association": 1.0,
    "Spatial/Intuitive Reasoning": 0.9
}

# Maximum theoretical raw magnitude used to scale to -100..100
# This is conservative: sum of (cap * weight) for both sides -> used as divisor.
_MAX_RAW = (
    sum(v * _INDICATOR_CAP for v in _LEFT_WEIGHTS.values()) +
    sum(v * _INDICATOR_CAP for v in _RIGHT_WEIGHTS.values())
) / 2.0  # use half-range for sign separation

# minimal signal floor to avoid divide-by-zero
_SIGNAL_FLOOR = 1e-6

# -----------------------
# Utility text functions
# -----------------------

def _tokenize_words(text):
    """Return list of lowercase word tokens (letters, apostrophes kept)."""
    # keep apostrophes inside words, remove other punctuation
    text = text.casefold()
    # replace non-letter/apostrophe sequences with space
    text = re.sub(r"[^a-z'\s]+", " ", text)
    tokens = [t for t in re.split(r"\s+", text) if t]
    return tokens

def _sentence_split(text):
    """Very simple sentence splitter based on ., ?, ! and line breaks."""
    # normalize ellipses
    text = text.replace("...", " . ")
    parts = re.split(r'[.!?]\s+|\n+', text.strip())
    parts = [p.strip() for p in parts if p and re.search(r"[a-zA-Z0-9]", p)]
    return parts

def _count_regex_list(patterns, text):
    """Count total matches across a list of regex patterns (word-boundary aware)."""
    total = 0
    for pat in patterns:
        # ensure pattern is compiled and word-aware if not already anchored
        total += len(re.findall(pat, text, flags=re.IGNORECASE))
    return total

# -----------------------
# Indicator computation
# -----------------------

def _compute_indicators(text):
    """
    Compute raw indicator scores (integers).
    Returns a dict:
    {
      "Analytic Thinking": int,
      "Sequential Logic": int,
      "Language Structure": int,
      "Emotional Imagery": int,
      "Creative Association": int,
      "Spatial/Intuitive Reasoning": int
    }
    """
    if not text or not re.search(r"[A-Za-z0-9]", text):
        # low-signal defaults
        return {
            "Analytic Thinking": 0,
            "Sequential Logic": 0,
            "Language Structure": 0,
            "Emotional Imagery": 0,
            "Creative Association": 0,
            "Spatial/Intuitive Reasoning": 0
        }

    tokens = _tokenize_words(text)
    words = len(tokens)
    sentences = _sentence_split(text)
    sentence_count = max(1, len(sentences))
    avg_sentence_len = float(words) / sentence_count if sentence_count else 0.0

    # Left indicators
    analytic_matches = _count_regex_list(_LEFT_KEYWORDS, text)
    sequential_matches = _count_regex_list(_SEQUENTIAL_CUES, text)
    # Language structure: measured by frequent use of function words, numbers, parentheses, commas,
    # and presence of words like "therefore"/"thus"; approximated by proportion of short words and punctuation density.
    punctuation_density = len(re.findall(r"[,;:()\-]", text))  # structural punctuation markers
    short_word_ratio = sum(1 for t in tokens if len(t) <= 3) / (words + _SIGNAL_FLOOR)
    language_structure_score = int(round((analytic_matches * 0.3) + (punctuation_density * 0.5) + (short_word_ratio * 5.0)))

    # Right indicators
    emotional_matches = _count_regex_list(_RIGHT_KEYWORDS, text)
    sensory_matches = _count_regex_list(_SENSORY_ADJECTIVES, text)
    metaphor_matches = _count_regex_list(_METAPHOR_CUES, text)
    creative_association_score = int(round((emotional_matches * 0.6) + (sensory_matches * 0.6) + (metaphor_matches * 1.2)))

    # Spatial/Intuitive: heuristics such as use of "vision", "sense", "holistic", plus sentence length variability
    spatial_matches = len(re.findall(r"\bvision\b|\bholistic\b|\bsense\b|\bintuit", text, flags=re.IGNORECASE))
    sentence_len_variance = 0.0
    try:
        lens = [len(_tokenize_words(s)) for s in sentences if s]
        if len(lens) >= 2:
            mean = sum(lens) / len(lens)
            sentence_len_variance = sum((l - mean) ** 2 for l in lens) / len(lens)
    except Exception:
        sentence_len_variance = 0.0
    spatial_score = int(round((spatial_matches * 1.0) + math.sqrt(sentence_len_variance + _SIGNAL_FLOOR) * 0.3))

    # Map to indicator dict and clamp
    indicators = {
        "Analytic Thinking": int(min(_INDICATOR_CAP, max(0, analytic_matches))),
        "Sequential Logic": int(min(_INDICATOR_CAP, max(0, sequential_matches))),
        "Language Structure": int(min(_INDICATOR_CAP, max(0, language_structure_score))),
        "Emotional Imagery": int(min(_INDICATOR_CAP, max(0, emotional_matches + metaphor_matches))),
        "Creative Association": int(min(_INDICATOR_CAP, max(0, creative_association_score))),
        "Spatial/Intuitive Reasoning": int(min(_INDICATOR_CAP, max(0, spatial_score))),
    }

    return indicators

# -----------------------
# Scoring & normalization
# -----------------------

def _score_indicators(indicators):
    """
    Compute raw left and right totals using weights, then produce a hemispheric score in -100..100.
    Also compute a confidence value based on signal strength.
    Returns (hemispheric_score, confidence, raw_left, raw_right)
    """
    raw_left = 0.0
    raw_right = 0.0

    # Weighted sums
    raw_left += indicators.get("Analytic Thinking", 0) * _LEFT_WEIGHTS["Analytic Thinking"]
    raw_left += indicators.get("Sequential Logic", 0) * _LEFT_WEIGHTS["Sequential Logic"]
    raw_left += indicators.get("Language Structure", 0) * _LEFT_WEIGHTS["Language Structure"]

    raw_right += indicators.get("Emotional Imagery", 0) * _RIGHT_WEIGHTS["Emotional Imagery"]
    raw_right += indicators.get("Creative Association", 0) * _RIGHT_WEIGHTS["Creative Association"]
    raw_right += indicators.get("Spatial/Intuitive Reasoning", 0) * _RIGHT_WEIGHTS["Spatial/Intuitive Reasoning"]

    # raw_score: positive -> right bias; negative -> left bias
    raw_score = raw_right - raw_left

    # Scale to -100..100
    # Use _MAX_RAW as the divisor (if signal exceed, clamp)
    if _MAX_RAW < _SIGNAL_FLOOR:
        scaled = 0.0
    else:
        ratio = max(-1.0, min(1.0, raw_score / _MAX_RAW))
        scaled = ratio * 100.0

    # Confidence: ratio of signal magnitude to total signal (how clear the tilt is).
    # If both sides have lots of signal but are equal, confidence low (balanced).
    total_signal = raw_left + raw_right
    tilt_strength = abs(raw_score)
    # confidence = tilt_strength / (total_signal + floor) mapped to 0..1, then damped slightly by overall signal
    if total_signal <= _SIGNAL_FLOOR:
        confidence = 0.0
    else:
        # base_conf ranges 0..1 where 1 means all signal on one side
        base_conf = tilt_strength / (total_signal + _SIGNAL_FLOOR)
        # boost a little for stronger absolute signal (more text)
        signal_boost = min(1.0, math.log1p(total_signal) / 6.0)  # gently grows with total_signal
        confidence = base_conf * (0.6 + 0.4 * signal_boost)  # between 0.6 and 1.0 of base_conf depending on signal
        confidence = max(0.0, min(1.0, confidence))

    return scaled, confidence, raw_left, raw_right

# -----------------------
# Interpretive summary builder
# -----------------------

def _build_summary(indicators, hemispheric_score, confidence):
    """
    Create a human-readable interpretive summary describing dominant hemisphere, top indicators, and recommendation tone.
    """
    # Determine dominant hemisphere
    if hemispheric_score >= 10:
        dominant = "Right"
    elif hemispheric_score <= -10:
        dominant = "Left"
    else:
        dominant = "Balanced"

    # Top 2 indicators overall (by absolute value compared to indicator cap)
    sorted_inds = sorted(indicators.items(), key=lambda kv: kv[1], reverse=True)
    top_inds = [f"{k} ({v})" for k, v in sorted_inds[:2] if v > 0]
    top_text = ", ".join(top_inds) if top_inds else "no strong surface indicators"

    # Recommendations phrasing
    if dominant == "Right":
        rec = "Right-hemisphere bias with emphasis on imagery, metaphor, and intuitive associations. Consider integrating structured steps or explicit data points when clarity or execution is needed."
    elif dominant == "Left":
        rec = "Left-hemisphere bias with emphasis on analysis, sequence, and structural language. Consider inviting metaphor, sensory language, or big-picture framing to broaden perspective."
    else:
        rec = "Relatively balanced between analytic and intuitive language. Maintain both structured and evocative practices to preserve flexibility."

    summary = (
        f"{dominant}-hemisphere tilt detected (score {hemispheric_score:.1f}). "
        f"Top surface indicators: {top_text}. {rec} "
        f"Confidence: {confidence:.2f}."
    )
    return summary, dominant

# -----------------------
# Public API
# -----------------------

def analyze_text(text):
    """
    Public function.

    Input: text (string)
    Returns: dict matching requested JSON structure
    """
    if text is None:
        text = ""

    indicators = _compute_indicators(text)
    hemispheric_score, confidence, raw_left, raw_right = _score_indicators(indicators)
    interpretive_summary, dominant = _build_summary(indicators, hemispheric_score, confidence)

    # Round numerical outputs to sensible precision
    result = {
        "hemispheric_score": round(float(hemispheric_score), 2),
        "dominant_hemisphere": dominant,
        "confidence": round(float(confidence), 2),
        "indicators": indicators,
        "interpretive_summary": interpretive_summary
    }

    return result

# -----------------------
# Demo / CLI
# -----------------------
if __name__ == "__main__":
    # small demo when run as script; prints result for an example input
    demo_text = (
        "I feel like the project is a living thing—bright, textured, and moving toward a vision. "
        "I trust my intuition and imagine the outcome; still, we need to set clear milestones and measure progress step by step."
    )
    output = analyze_text(demo_text)
    print(json.dumps(output, indent=2))

