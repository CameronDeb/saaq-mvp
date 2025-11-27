import re
import statistics


def _normalize_score(value, max_value=10.0):
    """
    Clamp a raw indicator score into [0, max_value].
    Default cap is 10 to avoid everything saturating.
    """
    return max(0.0, min(max_value, value))


def _regex_count(text, patterns):
    """Count regex hits across a list of patterns."""
    return sum(len(re.findall(p, text)) for p in patterns)


def _count_phrases(text, phrases):
    """Count occurrences of simple keyword phrases (case-insensitive)."""
    t = text.lower()
    return sum(t.count(p) for p in phrases)


def _score_awareness(text: str):
    """
    Heuristic Awareness Quotient for SA360-style narratives.

    Returns:
        {
          awareness_score: 0–100 (continuous),
          awareness_label: "Low" / "Moderate" / "High" / "Exceptional",
          indicators: {
            "Self-Awareness": 0–10,
            "Emotional Regulation": 0–10,
            "Perspective Awareness": 0–10,
            "Meta-Awareness": 0–10,
            "Systemic Awareness": 0–10,
            "Integrative Awareness": 0–10,
          },
          balance_index: 0–100 (higher = more even profile),
          interpretive_summary: str,
          word_count: int
        }
    """
    if not text or not text.strip():
        return {
            "awareness_score": 0.0,
            "awareness_label": "No Awareness Detected",
            "indicators": {
                k: 0.0 for k in [
                    "Self-Awareness",
                    "Emotional Regulation",
                    "Perspective Awareness",
                    "Meta-Awareness",
                    "Systemic Awareness",
                    "Integrative Awareness",
                ]
            },
            "balance_index": 0.0,
            "interpretive_summary": "No content provided.",
            "word_count": 0,
        }

    text = text.strip()
    lowered = text.lower()
    words = re.findall(r"\b\w+\b", lowered)
    wc = len(words)

    # ---------------- Pattern banks ---------------- #

    # These are intentionally broad but not insane — we’d rather under-detect
    # slightly than hallucinate awareness where there is none.

    self_awareness = [
        r"\bi\s*(notice|realize|recognize|observe|feel|acknowledg(e|ing)|become\s*aware|catch\s*myself)\b",
        r"\b(self[-\s]*aware(ness)?|aware\s*of\s*(my|myself|my\s*(feelings|reactions|patterns)))\b",
    ]

    emotional_reg = [
        r"\b(pause|breathe|calm|compose|ground|center|soothe|regulat(e|ion|ing)|slow\s*down)\b",
        r"\b(stay|remain|keep)\s*(calm|balanced|grounded|steady|present)\b",
        r"\brespond\s*(with|from)\s*(love|care|intention|curiosity)\b",
    ]

    perspective = [
        r"\b(others?|their|they)\s*(view|perspective|experience|opinion|feelings?)\b",
        r"\bi\s*(understand|see|consider|empathi[sz]e|respect)\s*(others?|their)\b",
        r"\bfrom\s*(another|different|broader)\s*perspective\b",
        r"\b(step\s*into|walk\s*in)\s*(their|someone else's)\s*(shoes|experience)\b",
    ]

    meta_awareness = [
        r"\b(thinking\s*about\s*my\s*thinking|self[-\s]*reflect(ion|ing)|meta[-\s]*cognit(ion|ive))\b",
        r"\bi\s*(question|analy[sz]e|examine|observe|witness)\s*my\s*(thoughts?|reactions?|stories?|assumptions?)\b",
        r"\b(take|took|taking)\s*a\s*step\s*back\b",
        r"\bnotice\s*the\s*(story|narrative)\s*i\s*am\s*telling\b",
    ]

    systemic = [
        r"\b(system(s)?|pattern(s)?|feedback\s*loop(s)?|interconnect(ed|ion|ivity)?|dynamic(s)?|structure|relationship(s)?|ecosystem|network(s)?)\b",
        r"\b(root\s*cause|cause\s*and\s*effect|underlying\s*dynamics|systems\s*thinking|ripple\s*effects?)\b",
        r"\bover\s*time\b",
    ]

    integrative = [
        r"\b(paradox(ical|es)?|integrat(e|ion|ing)|synthesi[sz](e|ing)|coexist(ence)?|both[-\s]*and)\b",
        r"\b(balance|harmony|polarity|tension)\b",
        r"\b(bring|combine|bridge|weave)\s*(different|opposing|contradictory|multiple|divergent)\b",
    ]

    # Phrase banks (non-regex, additive boosts)
    self_phrases = [
        "i am aware of", "i became aware", "i catch myself",
        "notice my reactions", "aware of my triggers",
    ]
    perspective_phrases = [
        "others may see", "others might see", "others may feel",
        "see the situation differently", "from their perspective",
        "from their point of view", "step into their shoes",
        "empathize with them", "understand where they are coming from",
        "multiple perspectives", "different perspectives",
    ]
    meta_phrases = [
        "thinking about my thinking", "question my assumptions",
        "challenge my assumptions", "reflect on my thinking",
        "observe my reactions", "noticing my thought pattern",
        "take a step back", "stepping back",
    ]
    systemic_phrases = [
        "feedback loop", "feedback loops", "ripple effect", "ripple effects",
        "interconnected system", "interconnected systems", "patterns over time",
        "long-term dynamics", "long term dynamics", "across the system",
        "systemic pattern", "systemic patterns",
    ]
    emotional_phrases = [
        "take a breath", "take a deep breath", "slow my breathing",
        "calm myself", "calm down", "ground myself", "stay grounded",
        "regain my composure", "stay present", "remain present",
        "respond instead of react",
    ]
    integrative_phrases = [
        "both and", "both/and", "hold paradox", "hold the paradox",
        "integrate complexity", "bridge opposing needs",
        "balance structure and flexibility", "harmonize tensions",
        "weave together", "synthesize perspectives",
        "paradox of", "coexist with",
    ]

    # ---------------- Raw regex-based scores ---------------- #

    scores = {
        "Self-Awareness": _normalize_score(_regex_count(lowered, self_awareness) * 4.0),
        "Emotional Regulation": _normalize_score(_regex_count(lowered, emotional_reg) * 4.0),
        "Perspective Awareness": _normalize_score(_regex_count(lowered, perspective) * 4.0),
        "Meta-Awareness": _normalize_score(_regex_count(lowered, meta_awareness) * 5.0),
        "Systemic Awareness": _normalize_score(_regex_count(lowered, systemic) * 5.0),
        "Integrative Awareness": _normalize_score(_regex_count(lowered, integrative) * 5.0),
    }

    # ---------------- Phrase-based boosts (smaller than before) ---------------- #

    scores["Self-Awareness"] += _count_phrases(lowered, self_phrases) * 1.5
    scores["Emotional Regulation"] += _count_phrases(lowered, emotional_phrases) * 1.5
    scores["Perspective Awareness"] += _count_phrases(lowered, perspective_phrases) * 1.7
    scores["Meta-Awareness"] += _count_phrases(lowered, meta_phrases) * 1.7
    scores["Systemic Awareness"] += _count_phrases(lowered, systemic_phrases) * 1.7
    scores["Integrative Awareness"] += _count_phrases(lowered, integrative_phrases) * 1.7

    # ---------------- Contextual cues (light-touch) ---------------- #

    if "others" in lowered and " i " in f" {lowered} ":
        scores["Perspective Awareness"] += 1.0
    if "step into" in lowered and "shoes" in lowered:
        scores["Perspective Awareness"] += 1.5
    if "pattern" in lowered and "system" in lowered:
        scores["Systemic Awareness"] += 1.0
    if "feedback" in lowered and "loop" in lowered:
        scores["Systemic Awareness"] += 1.0
    if "over time" in lowered or "across time" in lowered:
        scores["Systemic Awareness"] += 0.8
    if "balance" in lowered and ("both" in lowered or "and yet" in lowered):
        scores["Integrative Awareness"] += 1.0
    if re.search(r"\bboth\b.*\band\b", lowered):
        scores["Integrative Awareness"] += 2.0
    if "synthesis" in lowered or "integrat" in lowered:
        scores["Integrative Awareness"] += 1.0
    if "reflect" in lowered or "reflection" in lowered:
        scores["Meta-Awareness"] += 1.0
    if "question" in lowered and "assumption" in lowered:
        scores["Meta-Awareness"] += 1.5
    if "pause" in lowered or "breathe" in lowered or "breath" in lowered:
        scores["Emotional Regulation"] += 1.0
    if "grounded" in lowered and ("compassion" in lowered or "clarity" in lowered):
        scores["Emotional Regulation"] += 0.7

    # ---------------- Light length / spread bonuses ---------------- #

    # Mild scaling only; we *avoid* the heavy multipliers that forced everything to 14.
    if wc > 100:
        for k in scores:
            scores[k] *= 1.05  # 5% nudge only

    active_dims = sum(1 for v in scores.values() if v > 1.0)
    if active_dims >= 4:
        for k in scores:
            scores[k] *= 1.05  # again, just a 5% cohesion nudge

    # Clamp after adjustments
    scores = {k: _normalize_score(v) for k, v in scores.items()}

    # ---------------- Awareness score (0–100) ---------------- #

    # Weight meta, systemic, integrative slightly higher (as in your original intent)
    weights = {
        "Self-Awareness": 1.1,
        "Emotional Regulation": 1.1,
        "Perspective Awareness": 1.15,
        "Meta-Awareness": 1.4,
        "Systemic Awareness": 1.4,
        "Integrative Awareness": 1.4,
    }

    total_weight = sum(weights.values())
    weighted_sum = sum(scores[k] * weights[k] for k in scores)

    # Now compute a weighted *mean* in [0,10] then map linearly to [0,100]
    mean_indicator = weighted_sum / (total_weight or 1.0)  # 0–10-ish
    awareness_score = (mean_indicator / 10.0) * 100.0
    awareness_score = max(0.0, min(100.0, awareness_score))

    # ---------------- Labeling ---------------- #

    max_dim = max(scores.values()) if scores else 0.0

    if awareness_score < 25 and max_dim < 5:
        label = "Low Awareness"
    elif awareness_score < 55:
        label = "Moderate Awareness"
    elif awareness_score < 80:
        label = "High Awareness"
    else:
        label = "Exceptional Awareness"

    # ---------------- Balance Index (0–100) ---------------- #

    non_zero = [v for v in scores.values() if v > 0]
    if len(non_zero) >= 4:
        std_dev = statistics.stdev(non_zero)
        mean_val = sum(non_zero) / len(non_zero)
        if mean_val > 0:
            raw_balance = 1.0 - (std_dev / (mean_val + 1e-6))
            balance_index = max(0.0, min(1.0, raw_balance))
        else:
            balance_index = 0.0
    else:
        balance_index = 0.0

    # Scale to 0–100 for readability
    balance_index_scaled = round(balance_index * 100.0, 2)

    # ---------------- Interpretive Summary ---------------- #

    high_dims = [k for k, v in scores.items() if v > 7.5]
    low_dims = [k for k, v in scores.items() if v < 2.0]

    if label == "Low Awareness":
        summary = "Low awareness with limited reflection. Few signs of emotional or meta-cognitive regulation."
    elif label == "Moderate Awareness":
        summary = (
            f"Moderate awareness, showing development in "
            f"{', '.join(high_dims) if high_dims else 'some domains'}, "
            f"but still uneven across others."
        )
    elif label == "High Awareness":
        summary = (
            f"High awareness with notable strength in "
            f"{', '.join(high_dims) if high_dims else 'multiple domains'}. "
            f"Could benefit from balancing "
            f"{', '.join(low_dims) if low_dims else 'remaining areas'}."
        )
    else:
        summary = (
            f"Exceptional awareness integrating "
            f"{', '.join(high_dims) if high_dims else 'key domains'} "
            f"with strong systemic and reflective depth."
        )

    return {
        "awareness_score": round(awareness_score, 2),
        "awareness_label": label,
        "indicators": {k: round(v, 2) for k, v in scores.items()},
        "balance_index": balance_index_scaled,
        "interpretive_summary": summary,
        "word_count": wc,
    }


if __name__ == "__main__":
    sample = (
        "I integrate feedback across perspectives, recognize emerging patterns in the system, "
        "and reflect on my assumptions so I can respond with more balance and less reactivity."
    )
    print(_score_awareness(sample))
