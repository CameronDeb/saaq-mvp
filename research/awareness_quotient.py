import re
import statistics

def _normalize_score(value, max_value=14):
    return max(0.0, min(max_value, value))

def _regex_count(text, patterns):
    return sum(len(re.findall(p, text)) for p in patterns)

def _score_awareness(text: str):
    if not text or not text.strip():
        return {
            "awareness_score": 0.0,
            "awareness_label": "No Awareness Detected",
            "indicators": {k: 0.0 for k in [
                "Self-Awareness","Emotional Regulation","Perspective Awareness",
                "Meta-Awareness","Systemic Awareness","Integrative Awareness"]},
            "balance_index": 0.0,
            "interpretive_summary": "No content provided.",
            "word_count": 0
        }

    text = text.lower().strip()
    words = re.findall(r"\b\w+\b", text)
    wc = len(words)

    # --- Pattern banks ---
    self_awareness = [
        r"\bi\s*(notice|realize|recognize|observe|feel|acknowledg(e|ing)|become\s*aware)\b",
        r"\b(self[-\s]*aware(ness)?|aware\s*of\s*(my|myself))\b"]
    emotional_reg = [
        r"\b(pause|breathe|calm|compose|ground|manage|reframe|center|soothe|regulat(e|ion|ing))\b",
        r"\b(stay|remain|keep)\s*(calm|balanced|grounded|steady)\b"]
    perspective = [
        r"\b(others?|their|they)\s*(view|perspective|experience|opinion|feelings?)\b",
        r"\bi\s*(understand|see|consider|empathi[sz]e|respect)\s*(others?|their)\b",
        r"\bfrom\s*(another|different|broader)\s*perspective\b"]
    meta_awareness = [
        r"\b(thinking\s*about\s*my\s*thinking|meta|reflection|self[-\s]*reflect(ion|ing)|assumption(s)?|bias(es)?)\b",
        r"\bi\s*(question|analy[sz]e|examine|observe)\s*my\s*(thoughts?|reactions?)\b"]
    systemic = [
        r"\b(system(s)?|pattern(s)?|feedback\s*loop(s)?|interconnect(ed|ion|ivity)?|dynamic(s)?|structure|relationship(s)?|emerg(ent|ence)|ecosystem|holistic|network(s)?)\b",
        r"\b(root\s*cause|cause\s*and\s*effect|underlying\s*dynamics|systems\s*thinking)\b"]
    integrative = [
        r"\b(both|and\s*yet|paradox(ical|es)?|integrat(e|ion|ing)|synthesi[sz](e|ing)|coexist(ence)?|balance|harmony|polarity|complexity|unify|merge|blend|align|fusion)\b",
        r"\b(bring|combine)\s*(different|opposing|contradictory|multiple)\b",
        r"\b(paradoxical\s*unity|integrative\s*thinking)\b"]

    # --- Raw scores ---
    scores = {
        "Self-Awareness": _normalize_score(_regex_count(text,self_awareness)*8),
        "Emotional Regulation": _normalize_score(_regex_count(text,emotional_reg)*8),
        "Perspective Awareness": _normalize_score(_regex_count(text,perspective)*8),
        "Meta-Awareness": _normalize_score(_regex_count(text,meta_awareness)*12),
        "Systemic Awareness": _normalize_score(_regex_count(text,systemic)*12),
        "Integrative Awareness": _normalize_score(_regex_count(text,integrative)*12),
    }

    # --- Contextual cues ---
    if "others" in text and "i" in text: scores["Perspective Awareness"] += 2
    if "pattern" in text and "system" in text: scores["Systemic Awareness"] += 2
    if "balance" in text and ("both" in text or "and" in text): scores["Integrative Awareness"] += 2
    if "reflect" in text: scores["Meta-Awareness"] += 1.5
    if "feedback" in text and "loop" in text: scores["Systemic Awareness"] += 1
    if "synthesis" in text or "integrat" in text: scores["Integrative Awareness"] += 1.5

    # --- Spread bonuses ---
    if wc > 20:
        for k in scores: scores[k] *= 1.1
    active = sum(1 for v in scores.values() if v > 1)
    if active >= 4:
        for k in scores: scores[k] *= 1.15
    if active >= 5:
        for k in scores: scores[k] *= 1.25

    # --- Weighting ---
    weights = {
        "Self-Awareness":1.1,"Emotional Regulation":1.1,"Perspective Awareness":1.15,
        "Meta-Awareness":1.4,"Systemic Awareness":1.4,"Integrative Awareness":1.4
    }

    weighted=sum(scores[k]*weights[k] for k in scores)
    awareness_score=(weighted/sum(weights.values()))*12.5

    # --- Label ---
    if awareness_score<25: label="Low Awareness"
    elif awareness_score<55: label="Moderate Awareness"
    elif awareness_score<80: label="High Awareness"
    else: label="Exceptional Awareness"

    # --- Balance Index ---
    non_zero=[v for v in scores.values() if v>0]
    if len(non_zero)>1:
        std_dev=statistics.stdev(non_zero)
        mean_val=sum(non_zero)/len(non_zero)
        balance_index=round((1 - (std_dev/(mean_val+1e-6))),3)
        balance_index = max(0.0, min(1.0, balance_index))
    else:
        balance_index=0.0

    # --- Interpretive Summary ---
    high_dims=[k for k,v in scores.items() if v>8]
    low_dims=[k for k,v in scores.items() if v<2]
    if awareness_score<25:
        summary=f"Low awareness with limited reflection. Few signs of emotional or meta-cognitive regulation."
    elif awareness_score<55:
        summary=f"Moderate awareness, showing development in {', '.join(high_dims) or 'some domains'}, but still uneven across others."
    elif awareness_score<80:
        summary=f"High awareness with notable strength in {', '.join(high_dims) or 'multiple domains'}. Could benefit from balancing {', '.join(low_dims) or 'remaining areas'}."
    else:
        summary=f"Exceptional awareness integrating {', '.join(high_dims) or 'all key domains'} with strong systemic and reflective depth."

    return {
        "awareness_score":round(awareness_score,2),
        "awareness_label":label,
        "indicators":{k:round(v,2) for k,v in scores.items()},
        "balance_index":round(balance_index*100,2),
        "interpretive_summary":summary,
        "word_count":wc
    }

if __name__=="__main__":
    text="I integrate feedback across perspectives, recognizing emerging patterns in the system and reflecting to act with balance."
    print(_score_awareness(text))
