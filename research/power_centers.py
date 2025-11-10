#!/usr/bin/env python3
"""
power_centers.py

Deterministic Power Centers Profiler
------------------------------------
Analyzes text for linguistic cues associated with five psychological "energy centers":

1. Cognitive — reasoning, logic, analysis
2. Emotional — feelings, empathy, mood language
3. Relational — connectedness, pronouns, social cues
4. Somatic — body, sensation, movement
5. Spiritual — purpose, unity, transcendence, meaning

Output JSON:
{
  "power_profile": {
    "Cognitive": 8.5,
    "Emotional": 7.2,
    "Relational": 5.8,
    "Somatic": 3.0,
    "Spiritual": 6.9
  },
  "dominant_center": "Cognitive",
  "balance_index": 78.3,
  "interpretive_summary": "Dominant cognitive energy with emotional and spiritual resonance; grounded but slightly low in embodiment."
}

Uses only: re, json, math.
"""

import re
import json
import math

# -------------------------------------------------------
# Keyword dictionaries for each power center
# -------------------------------------------------------

_COGNITIVE = [
    r"\bthink", r"\bthought", r"\banaly", r"\breason", r"\bunderstand",
    r"\bknow", r"\bconcept", r"\bidea", r"\blogic", r"\bplan",
    r"\bconsider", r"\bdecide", r"\bcalculate", r"\bobjective",
    r"\brational", r"\bproblem", r"\bmodel", r"\btheory"
]

_EMOTIONAL = [
    r"\bfeel", r"\bfeeling", r"\bemot", r"\bemotion", r"\bhappy", r"\bsad",
    r"\bangry", r"\bjoy", r"\bfear", r"\bgrief", r"\blove", r"\bheart",
    r"\bcaring", r"\bcompassion", r"\bsympath", r"\bempath", r"\btender",
    r"\btouched", r"\bmood"
]

_RELATIONAL = [
    r"\bwe\b", r"\bus\b", r"\bour\b", r"\bthey\b", r"\bthem\b",
    r"\btogether", r"\bconnect", r"\bshare", r"\bteam", r"\bfriend",
    r"\bhelp", r"\bcommunicat", r"\binteract", r"\bothers\b",
    r"\bcommunity", r"\bsupport", r"\brelation", r"\btrust"
]

_SOMATIC = [
    r"\bbody\b", r"\bbreath", r"\bbreath", r"\bchest\b", r"\bheartbeat",
    r"\bmove", r"\bmoving", r"\bmuscle", r"\btension", r"\brelease",
    r"\btight", r"\brelax", r"\bsense", r"\btouch", r"\bpain", r"\bhunger",
    r"\bposture", r"\bstomach", r"\bshoulder", r"\bground", r"\bwalk"
]

_SPIRITUAL = [
    r"\bspirit", r"\bmeaning", r"\bpurpose", r"\bfaith", r"\bdivine",
    r"\buniverse", r"\bconnected", r"\bone\b", r"\bunity", r"\bpeace",
    r"\btruth", r"\btranscend", r"\bholy", r"\bsacred", r"\bessence",
    r"\bpresence", r"\bmeditat", r"\bconscious", r"\bawareness",
    r"\bsoul", r"\bprayer", r"\binner", r"\bgratitude"
]

# normalization constants
_MAX_SCORE = 10.0
_SIGNAL_FLOOR = 1e-6

# -------------------------------------------------------
# Core analysis helpers
# -------------------------------------------------------

def _count_keywords(patterns, text):
    """Count all matches for the given regex pattern list."""
    count = 0
    for pat in patterns:
        count += len(re.findall(pat, text, flags=re.IGNORECASE))
    return count

def _normalize(value, max_possible):
    """Normalize to 0–10 scale."""
    if max_possible <= 0:
        return 0.0
    scaled = (value / max_possible) * _MAX_SCORE
    return round(min(_MAX_SCORE, scaled), 2)

# -------------------------------------------------------
# Main analytic function
# -------------------------------------------------------

def analyze_text(text):
    """
    Main entry point.
    Input: text string
    Output: dict with power_profile, dominant_center, balance_index, and interpretive_summary.
    """
    if not text or not re.search(r"[A-Za-z]", text):
        # no content -> neutral low scores
        neutral = {k: 0.0 for k in ["Cognitive", "Emotional", "Relational", "Somatic", "Spiritual"]}
        return {
            "power_profile": neutral,
            "dominant_center": "None",
            "balance_index": 0.0,
            "interpretive_summary": "No valid linguistic signal detected."
        }

    # total word count for relative weighting
    words = len(re.findall(r"[A-Za-z']+", text))
    words = max(words, 1)

    # raw counts for each category
    raw_counts = {
        "Cognitive": _count_keywords(_COGNITIVE, text),
        "Emotional": _count_keywords(_EMOTIONAL, text),
        "Relational": _count_keywords(_RELATIONAL, text),
        "Somatic": _count_keywords(_SOMATIC, text),
        "Spiritual": _count_keywords(_SPIRITUAL, text)
    }

    # normalize counts to 0–10 scale; divide by rough expected max per ~1000 words
    scale_base = max(5.0, math.log10(words + 10.0) * 8.0)  # adaptive scaling
    profile = {k: _normalize(v, scale_base) for k, v in raw_counts.items()}

    # compute dominant center
    dominant = max(profile.items(), key=lambda kv: kv[1])[0]

    # compute balance index: 100 - (stddev * scaling)
    vals = list(profile.values())
    mean_val = sum(vals) / len(vals)
    variance = sum((v - mean_val) ** 2 for v in vals) / len(vals)
    stddev = math.sqrt(variance)
    # convert stddev (0..5 roughly) into a 0–100 balance index
    balance_index = max(0.0, 100.0 - (stddev * 20.0))
    balance_index = round(balance_index, 1)

    # interpretive summary
    interpretive_summary = _build_summary(profile, dominant, balance_index)

    # final output
    result = {
        "power_profile": profile,
        "dominant_center": dominant,
        "balance_index": balance_index,
        "interpretive_summary": interpretive_summary
    }

    return result

# -------------------------------------------------------
# Summary builder
# -------------------------------------------------------

def _build_summary(profile, dominant, balance_index):
    """
    Compose interpretive summary from scores.
    """
    desc = {
        "Cognitive": "analytical and reasoning focus",
        "Emotional": "emotionally attuned, empathic focus",
        "Relational": "socially oriented, connection-seeking focus",
        "Somatic": "embodied and sensory-grounded focus",
        "Spiritual": "meaning- and purpose-oriented focus"
    }

    dom_score = profile[dominant]
    # Identify secondary influences
    sorted_centers = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    top_two = [k for k, v in sorted_centers[:2]]
    balance_phrase = "highly balanced" if balance_index >= 85 else \
                     "moderately balanced" if balance_index >= 60 else \
                     "unevenly distributed"

    # Compose text
    summary = (
        f"Dominant {dominant.lower()} center ({dom_score}/10) — {desc[dominant]}. "
        f"Secondary influences: {top_two[1] if len(top_two) > 1 else 'none'}. "
        f"Overall profile appears {balance_phrase} (balance index {balance_index})."
    )
    return summary

# -------------------------------------------------------
# Demo usage
# -------------------------------------------------------

if __name__ == "__main__":
    demo_text = (
        "I think carefully about every decision, yet I feel the emotions of those around me. "
        "We share purpose and gratitude, breathing together to stay grounded in peace."
    )
    result = analyze_text(demo_text)
    print(json.dumps(result, indent=2))

