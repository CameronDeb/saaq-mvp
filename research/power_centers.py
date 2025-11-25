#!/usr/bin/env python3
"""
power_centers.py

Deterministic Power Centers Profiler
------------------------------------
Analyzes text for linguistic cues associated with eight psychological "energy centers":

1. Cognitive — reasoning, logic, analysis
2. Emotional — feelings, empathy, mood language
3. Relational — connectedness, pronouns, social cues
4. Somatic — body, sensation, movement
5. Spiritual — purpose, unity, transcendence, meaning
6. Vital — physical/sexual energy, strength, health
7. Social/Leadership — teaching, guiding, influence, organization
8. Financial — money, resources, stewardship

Output JSON:
{
  "power_profile": { ... },
  "dominant_center": "...",
  "balance_index": 78.3,
  "interpretive_summary": "..."
}

Uses only: re, json, math.
"""

import re
import json
import math

# -------------------------------------------------------
# Keyword dictionaries for each power center (8 TOTAL)
# -------------------------------------------------------

_COGNITIVE = [
    r"\bthink", r"\bthought", r"\banaly", r"\breason", r"\bunderstand",
    r"\bknow", r"\bconcept", r"\bidea", r"\blogic", r"\bplan",
    r"\bconsider", r"\bdecide", r"\bcalculate", r"\bobjective",
    r"\brational", r"\bproblem", r"\bmodel", r"\btheory", r"\binsight"
]

_EMOTIONAL = [
    r"\bfeel", r"\bfeeling", r"\bemot", r"\bemotion", r"\bhappy", r"\bsad",
    r"\bangry", r"\bjoy", r"\bfear", r"\bgrief", r"\blove", r"\bheart",
    r"\bcaring", r"\bcompassion", r"\bsympath", r"\bempath", r"\btender",
    r"\btouched", r"\bmood", r"\bupset"
]

_RELATIONAL = [
    r"\bwe\b", r"\bus\b", r"\bour\b", r"\bthey\b", r"\bthem\b",
    r"\btogether", r"\bconnect", r"\bshare", r"\bteam", r"\bfriend",
    r"\bhelp", r"\bcommunicat", r"\binteract", r"\bothers\b",
    r"\bcommunity", r"\bsupport", r"\brelation", r"\btrust",
    r"\bparent", r"\bdaughter", r"\bpartner"
]

_SOMATIC = [
    r"\bbody\b", r"\bbreath", r"\bchest\b", r"\bheartbeat",
    r"\bmove", r"\bmoving", r"\bmuscle", r"\btension", r"\brelease",
    r"\btight", r"\brelax", r"\bsense", r"\btouch", r"\bpain\b",
    r"\bhunger", r"\bposture", r"\bstomach", r"\bshoulder",
    r"\bground", r"\bwalk", r"\binjury", r"\bache", r"\bfitness"
]

_SPIRITUAL = [
    r"\bspirit", r"\bmeaning", r"\bpurpose", r"\bfaith", r"\bdivine",
    r"\buniverse", r"\bconnected", r"\bone\b", r"\bunity", r"\bpeace",
    r"\btruth", r"\btranscend", r"\bholy", r"\bsacred", r"\bessence",
    r"\bpresence", r"\bmeditat", r"\bconscious", r"\bawareness",
    r"\bsoul", r"\bprayer", r"\binner", r"\bgratitude", r"\bemtpiness",
    r"\bmeta-aware", r"\bcosmic"
]

# NEWLY ADDED POWER CENTERS

_VITAL = [
    r"\bstrength", r"\benergy\b", r"\bvital", r"\bphysical", r"\bsexual",
    r"\bhealthy", r"\bhealth\b", r"\bbody\b", r"\bmuscle", r"\bworkout",
    r"\btraining", r"\bfitness", r"\bfit\b", r"\binjury", r"\bache"
]

_SOCIAL_LEADERSHIP = [
    r"\blead", r"\bguide", r"\bteach", r"\bcoach", r"\binfluence",
    r"\bmentor", r"\bimpact", r"\bteam", r"\bcommunity", r"\brole model",
    r"\bstructure", r"\bdesign", r"\borganize", r"\bauthority",
    r"\bmanage", r"\bgroup", r"\bretreat", r"\bteacher"
]

_FINANCIAL = [
    r"\bmoney\b", r"\bbudget", r"\bcredit", r"\bdebt", r"\bpay",
    r"\bsave", r"\bspend", r"\bincome", r"\bfinancial", r"\bresources",
    r"\bexpense", r"\bprofit", r"\bwealth", r"\bbankruptcy",
    r"\baccount\b", r"\bcheck balance", r"\bbills"
]

# normalization constants
_MAX_SCORE = 10.0
_SIGNAL_FLOOR = 1e-6

# -------------------------------------------------------
# Core analysis helpers
# -------------------------------------------------------

def _count_keywords(patterns, text):
    """Count all matches for the given regex pattern list."""
    return sum(len(re.findall(p, text, flags=re.IGNORECASE)) for p in patterns)

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
    Input: text string
    Output: dict with power_profile, dominant_center, balance_index, interpretive_summary.
    """
    if not text or not re.search(r"[A-Za-z]", text):
        empty = {k: 0.0 for k in CENTER_NAMES}
        return {
            "power_profile": empty,
            "dominant_center": "None",
            "balance_index": 0.0,
            "interpretive_summary": "No valid linguistic signal detected."
        }

    words = max(1, len(re.findall(r"[A-Za-z']+", text)))
    scale_base = max(5.0, math.log10(words + 10.0) * 8.0)

    # Raw counts across 8 centers
    raw = {
        "Cognitive": _count_keywords(_COGNITIVE, text),
        "Emotional": _count_keywords(_EMOTIONAL, text),
        "Relational": _count_keywords(_RELATIONAL, text),
        "Somatic": _count_keywords(_SOMATIC, text),
        "Spiritual": _count_keywords(_SPIRITUAL, text),
        "Vital": _count_keywords(_VITAL, text),
        "Social/Leadership": _count_keywords(_SOCIAL_LEADERSHIP, text),
        "Financial": _count_keywords(_FINANCIAL, text)
    }

    profile = {k: _normalize(v, scale_base) for k, v in raw.items()}
    dominant = max(profile.items(), key=lambda kv: kv[1])[0]

    vals = list(profile.values())
    mean_val = sum(vals) / len(vals)
    variance = sum((v - mean_val) ** 2 for v in vals) / len(vals)
    stddev = math.sqrt(variance)
    balance_index = round(max(0.0, 100.0 - (stddev * 20.0)), 1)

    summary = _build_summary(profile, dominant, balance_index)
    return {
        "power_profile": profile,
        "dominant_center": dominant,
        "balance_index": balance_index,
        "interpretive_summary": summary
    }

# -------------------------------------------------------
# Summary builder
# -------------------------------------------------------

CENTER_DESCRIPTIONS = {
    "Cognitive": "analytical and reasoning focus",
    "Emotional": "emotionally attuned, empathic focus",
    "Relational": "connection-oriented, socially attuned focus",
    "Somatic": "embodied and sensory-grounded focus",
    "Spiritual": "meaning, purpose, and transcendence focus",
    "Vital": "physical strength, energy, and bodily power",
    "Social/Leadership": "guiding, influencing, and structuring groups",
    "Financial": "money, resources, and stewardship focus"
}

CENTER_NAMES = list(CENTER_DESCRIPTIONS.keys())

def _build_summary(profile, dominant, balance_index):
    sorted_centers = sorted(profile.items(), key=lambda kv: kv[1], reverse=True)
    secondary = sorted_centers[1][0] if len(sorted_centers) > 1 else "None"
    balance_phrase = "highly balanced" if balance_index >= 85 else \
                     "moderately balanced" if balance_index >= 60 else \
                     "unevenly distributed"

    return (
        f"Dominant {dominant} center ({profile[dominant]}/10) — {CENTER_DESCRIPTIONS[dominant]}. "
        f"Secondary influence: {secondary}. "
        f"Profile appears {balance_phrase} (balance index {balance_index})."
    )

# -------------------------------------------------------
# Demo
# -------------------------------------------------------

if __name__ == "__main__":
    demo_text = "I teach, lead, think, create, feel deeply, and manage money while staying grounded in my body."
    print(json.dumps(analyze_text(demo_text), indent=2))
