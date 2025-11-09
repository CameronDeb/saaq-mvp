"""
Cameron's Metrics Prototype
Core Aptitudes + Shadow Indicators + KPIs.
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ===== CORE APTITUDES =====

def calculate_aptitude_score(user_text: str, aptitude_patterns: list, keywords: list) -> int:
    """
    Calculate aptitude score using semantic similarity + keyword density
    Returns: 0-100 score
    """
    # Embed patterns and user text
    pattern_embeddings = model.encode(aptitude_patterns)
    user_embedding = model.encode([user_text])
    
    # Calculate max similarity
    similarities = cosine_similarity(user_embedding, pattern_embeddings)
    max_similarity = np.max(similarities)
    
    # Calculate keyword density
    keyword_count = sum(1 for kw in keywords if kw in user_text.lower())
    keyword_density = min(keyword_count / len(keywords), 1.0)
    
    # Combine (60% similarity, 40% keywords)
    score = (0.6 * max_similarity) + (0.4 * keyword_density)
    return int(score * 100)


# Define patterns for each aptitude
APTITUDE_PATTERNS = {
    "drive": {
        "patterns": [
            "I push myself to achieve goals",
            "I'm motivated by results and outcomes",
            "I set ambitious targets and work hard"
        ],
        "keywords": ["achieve", "goal", "push", "motivated", "strive", "drive"]
    },
    "perseverance": {
        "patterns": [
            "I keep going even when things are difficult",
            "I don't give up easily on important goals",
            "I persist through challenges and setbacks"
        ],
        "keywords": ["persist", "continue", "keep going", "endure", "resilient"]
    },
    "alignment": {
        "patterns": [
            "I act according to my core values",
            "My actions reflect my beliefs and principles",
            "I stay true to what matters most to me"
        ],
        "keywords": ["values", "integrity", "authentic", "principles", "beliefs"]
    },
    "restraint": {
        "patterns": [
            "I pause before reacting to difficult situations",
            "I take time to reflect before making decisions",
            "I can wait and observe before acting"
        ],
        "keywords": ["pause", "wait", "reflect", "consider", "think before"]
    }
}


# ===== SHADOW INDICATORS =====

def detect_shadow_patterns(text: str) -> dict:
    """
    Detect shadow loop patterns using keyword matching
    Returns: Dict with pattern names and confidence scores
    """
    text_lower = text.lower()
    
    patterns = {
        "control_reflex": ["control", "manage", "grip", "maintain", "handle", "fix"],
        "quick_relief": ["numb", "escape", "drink", "avoid", "distract", "forget"],
        "lone_rescuer": ["alone", "myself", "can't trust", "do it all", "on my own"]
    }
    
    results = {}
    for pattern_name, keywords in patterns.items():
        matches = sum(1 for kw in keywords if kw in text_lower)
        confidence = min(matches / len(keywords), 1.0) * 100
        results[pattern_name] = int(confidence)
    
    return results


# ===== MAIN TEST =====

if __name__ == "__main__":
    print("=" * 60)
    print("CAMERON'S METRICS PROTOTYPE TEST")
    print("=" * 60)
    
    # Sample user responses
    test_responses = {
        "drive": "I always strive to meet my objectives and exceed expectations in my work",
        "perseverance": "Even when projects get tough, I find ways to push through and complete them",
        "alignment": "I make decisions based on my core values of honesty and integrity",
        "restraint": "I try to pause and think things through before reacting emotionally",
        "shadow": "When I'm stressed, I need to control everything and do it all myself to feel safe"
    }
    
    # Test Core Aptitudes
    print("\n📊 CORE APTITUDES SCORES:")
    print("-" * 60)
    
    for aptitude in ["drive", "perseverance", "alignment", "restraint"]:
        score = calculate_aptitude_score(
            test_responses[aptitude],
            APTITUDE_PATTERNS[aptitude]["patterns"],
            APTITUDE_PATTERNS[aptitude]["keywords"]
        )
        print(f"{aptitude.title():15} → {score}/100")
    
    # Test Shadow Indicators
    print("\n👻 SHADOW INDICATORS:")
    print("-" * 60)
    
    shadow_scores = detect_shadow_patterns(test_responses["shadow"])
    for pattern, score in shadow_scores.items():
        indicator = "🔴 DETECTED" if score > 50 else "⚪ Low"
        print(f"{pattern.replace('_', ' ').title():20} → {score}/100 {indicator}")
    
    print("\n" + "=" * 60)
    print("✅ Prototype test complete!")
    print("=" * 60)