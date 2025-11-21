"""
Unified SAAQ Metrics Analyzer
Combines all team modules: Stage Detection, Hemispheric Bias, Power Centers, 
Core Aptitudes, Shadow Indicators, and Awareness Quotient
"""
import sys
import os
from typing import Dict, List

# Add research folder to path
research_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'research')
sys.path.insert(0, research_path)

# Import all modules
try:
    from stage_classifier import _score_text as analyze_stage
    from awareness_quotient import _score_awareness as analyze_aq
    from hemisphere_bias import analyze_text as analyze_hemispheric
    from power_centers import analyze_text as analyze_power
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Module import error: {e}")
    MODULES_AVAILABLE = False

# Cameron's Core Aptitudes (from your prototype)
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Initialize sentence transformer for aptitudes
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    TRANSFORMER_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Sentence transformer not available: {e}")
    TRANSFORMER_AVAILABLE = False

# Aptitude patterns (from your prototype)
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
    },
    "autonomy": {
        "patterns": [
            "I make my own decisions independently",
            "I take initiative and lead when needed",
            "I influence outcomes through my actions"
        ],
        "keywords": ["lead", "influence", "independent", "autonomy", "initiative"]
    },
    "achievement": {
        "patterns": [
            "I accomplish what I set out to do",
            "I succeed at challenging tasks",
            "I deliver results consistently"
        ],
        "keywords": ["accomplish", "success", "deliver", "complete", "achieve"]
    }
}

def calculate_aptitude_score(user_text: str, aptitude_patterns: list, keywords: list) -> int:
    """Calculate aptitude score using semantic similarity + keyword density"""
    if not TRANSFORMER_AVAILABLE:
        # Fallback to keyword-only scoring
        keyword_count = sum(1 for kw in keywords if kw in user_text.lower())
        return min(100, int((keyword_count / len(keywords)) * 100))
    
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

def detect_shadow_patterns(text: str) -> Dict:
    """Detect shadow loop patterns using keyword matching"""
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

class UnifiedAnalyzer:
    """Combines all SAAQ metrics into one unified report"""
    
    def __init__(self, responses: List[Dict]):
        """
        responses: List of dicts with keys: q_id, question_text, answer_text
        """
        self.responses = {r['q_id']: r['answer_text'] for r in responses}
        self.combined_text = " ".join(self.responses.values())
    
    def analyze_all(self) -> Dict:
        """Run all analyses and return unified metrics"""
        
        return {
            "stage": self._analyze_stage(),
            "awareness_quotient": self._analyze_aq(),
            "hemispheric_bias": self._analyze_hemispheric(),
            "power_centers": self._analyze_power_centers(),
            "core_aptitudes": self._analyze_aptitudes(),
            "shadow_indicators": self._analyze_shadow(),
        }
    
    def _analyze_stage(self) -> Dict:
        """Harsh's stage classifier"""
        if not MODULES_AVAILABLE:
            return {"error": "Stage classifier not available"}
        
        result = analyze_stage(self.combined_text)
        return {
            "stage": result.get('predicted_stage', 'Unknown'),
            "confidence": result.get('confidence', 0.0),
            "scores": result.get('stage_scores', {}),
            "description": result.get('interpretive_summary', '')
        }
    
    def _analyze_aq(self) -> Dict:
        """Harsh's awareness quotient"""
        if not MODULES_AVAILABLE:
            return {"error": "AQ analyzer not available"}
        
        result = analyze_aq(self.combined_text)
        return {
            "score": result.get('awareness_quotient', 0),
            "category": result.get('aq_category', 'Unknown'),
            "dimensions": result.get('dimensions', {}),
            "description": result.get('interpretive_summary', '')
        }
    
    def _analyze_hemispheric(self) -> Dict:
        """Advik's hemispheric bias analyzer"""
        if not MODULES_AVAILABLE:
            return {"error": "Hemispheric analyzer not available"}
        
        result = analyze_hemispheric(self.combined_text)
        return {
            "score": result.get('hemispheric_score', 0.0),
            "dominant": result.get('dominant_hemisphere', 'Balanced'),
            "confidence": result.get('confidence', 0.0),
            "indicators": result.get('indicators', {}),
            "description": result.get('interpretive_summary', '')
        }
    
    def _analyze_power_centers(self) -> Dict:
        """Advik's power centers profiler"""
        if not MODULES_AVAILABLE:
            return {"error": "Power centers analyzer not available"}
        
        result = analyze_power(self.combined_text)
        return {
            "profile": result.get('power_profile', {}),
            "dominant_center": result.get('dominant_center', 'Unknown'),
            "balance_index": result.get('balance_index', 0.0),
            "description": result.get('interpretive_summary', '')
        }
    
    def _analyze_aptitudes(self) -> Dict:
        """Cameron's core aptitudes scoring"""
        aptitudes = {}
        
        for aptitude_name, config in APTITUDE_PATTERNS.items():
            score = calculate_aptitude_score(
                self.combined_text,
                config['patterns'],
                config['keywords']
            )
            aptitudes[aptitude_name] = score
        
        return {
            "scores": aptitudes,
            "top_aptitude": max(aptitudes.items(), key=lambda x: x[1])[0],
            "average": sum(aptitudes.values()) / len(aptitudes)
        }
    
    def _analyze_shadow(self) -> Dict:
        """Cameron's shadow indicator detection"""
        shadow_scores = detect_shadow_patterns(self.combined_text)
        
        detected_loops = [name for name, score in shadow_scores.items() if score > 50]
        
        return {
            "scores": shadow_scores,
            "detected_loops": detected_loops,
            "primary_pattern": max(shadow_scores.items(), key=lambda x: x[1])[0] if shadow_scores else "none"
        }

# Convenience function
def analyze_intake(responses: List[Dict]) -> Dict:
    """
    Main entry point for analyzing a full intake
    
    Args:
        responses: List of dicts with keys: q_id, question_text, answer_text
    
    Returns:
        Complete metrics dict with all analyses
    """
    analyzer = UnifiedAnalyzer(responses)
    return analyzer.analyze_all()