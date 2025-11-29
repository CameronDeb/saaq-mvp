"""
Core Aptitudes & Shadow Indicators Module
Lightweight keyword-based scoring (no transformers needed)
"""
import re
from typing import Dict

# Aptitude keyword patterns
APTITUDE_PATTERNS = {
    "Drive": ["achieve", "goal", "push", "motivated", "strive", "ambition", "succeed"],
    "Perseverance": ["persist", "continue", "keep going", "endure", "resilient", "overcome"],
    "Alignment": ["values", "integrity", "authentic", "principles", "beliefs", "true to"],
    "Restraint": ["pause", "wait", "reflect", "consider", "think before", "patience"],
    "Autonomy": ["lead", "influence", "independent", "initiative", "decide", "control"],
    "Achievement": ["accomplish", "success", "deliver", "complete", "achieve", "done"]
}

# Shadow pattern keywords
SHADOW_PATTERNS = {
    "control_reflex": ["control", "manage", "grip", "maintain", "handle", "fix"],
    "quick_relief": ["numb", "escape", "drink", "avoid", "distract", "forget"],
    "lone_rescuer": ["alone", "myself", "can't trust", "do it all", "on my own"]
}

def score_aptitudes(text: str) -> Dict:
    """
    Score 6 core aptitudes based on keyword density
    Returns dict with scores 0-100 and levels
    """
    text_lower = text.lower()
    results = {}
    
    for aptitude, keywords in APTITUDE_PATTERNS.items():
        # Count keyword matches
        matches = sum(1 for kw in keywords if kw in text_lower)
        
        # Calculate score (0-100)
        # More matches = higher score, cap at 100
        score = min(100, int((matches / len(keywords)) * 150))
        
        # Determine level
        if score >= 70:
            level = "Strong"
        elif score >= 40:
            level = "Moderate"
        else:
            level = "Developing"
        
        results[aptitude] = {
            "score": score,
            "level": level,
            "matches": matches
        }
    
    return results

def detect_shadow(text: str) -> Dict:
    """
    Detect shadow loop patterns
    Returns dict with pattern confidence scores and detected loops
    """
    text_lower = text.lower()
    scores = {}
    
    for pattern, keywords in SHADOW_PATTERNS.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        confidence = min(100, int((matches / len(keywords)) * 100))
        scores[pattern] = confidence
    
    # Identify detected loops (>50% confidence)
    detected = [name for name, score in scores.items() if score > 50]
    primary = max(scores.items(), key=lambda x: x[1])[0] if scores else "none"
    
    return {
        "scores": scores,
        "detected_loops": detected,
        "primary_pattern": primary
    }

def analyze_aptitudes_shadow(text: str) -> Dict:
    """
    Complete analysis combining aptitudes and shadow
    """
    apt = score_aptitudes(text)
    shadow = detect_shadow(text)
    
    # Calculate summary stats
    apt_scores = [v['score'] for v in apt.values()]
    avg_aptitude = sum(apt_scores) / len(apt_scores)
    top_aptitude = max(apt.items(), key=lambda x: x[1]['score'])
    
    return {
        "aptitudes": apt,
        "shadow_indicators": shadow,
        "summary": {
            "average_aptitude": round(avg_aptitude, 1),
            "top_aptitude": top_aptitude[0],
            "shadow_risk": "High" if len(shadow['detected_loops']) >= 2 else "Moderate" if len(shadow['detected_loops']) == 1 else "Low"
        }
    }

# Test
if __name__ == "__main__":
    import json
    
    test_text = """
    I push myself to achieve my goals and persist through challenges. I stay true to my values 
    and principles. When stressed, I try to control everything and isolate myself. I do it all alone.
    """
    
    result = analyze_aptitudes_shadow(test_text)
    print(json.dumps(result, indent=2))