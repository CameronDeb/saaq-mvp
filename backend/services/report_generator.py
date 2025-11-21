"""
SAAQ Report Generator - Polished Version
Generates complete SAAQ reports using unified metrics from all team modules
"""
from datetime import datetime
from typing import List, Dict
import sys
import os

# Add research folder to path for module imports
research_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'research')
sys.path.insert(0, research_path)

# Import all team modules
try:
    from stage_classifier import _score_text as analyze_stage
    from awareness_quotient import _score_awareness as analyze_aq
    from hemisphere_bias import analyze_text as analyze_hemispheric
    from power_centers import analyze_text as analyze_power
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Module import error: {e}")
    MODULES_AVAILABLE = False

# Cameron's aptitudes and shadow detection
try:
    from sentence_transformers import SentenceTransformer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    model = SentenceTransformer('all-MiniLM-L6-v2')
    TRANSFORMER_AVAILABLE = True
except Exception:
    TRANSFORMER_AVAILABLE = False

# Aptitude patterns
APTITUDE_PATTERNS = {
    "autonomy": {
        "patterns": [
            "I make my own decisions independently",
            "I take initiative and lead when needed",
            "I influence outcomes through my actions"
        ],
        "keywords": ["lead", "influence", "independent", "autonomy", "initiative"]
    },
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
    "achievement": {
        "patterns": [
            "I accomplish what I set out to do",
            "I succeed at challenging tasks",
            "I deliver results consistently"
        ],
        "keywords": ["accomplish", "success", "deliver", "complete", "achieve"]
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

def calculate_aptitude_score(user_text: str, patterns: list, keywords: list) -> int:
    """Calculate aptitude score using semantic similarity + keyword density"""
    if not TRANSFORMER_AVAILABLE:
        keyword_count = sum(1 for kw in keywords if kw in user_text.lower())
        return min(100, int((keyword_count / len(keywords)) * 100))
    
    pattern_embeddings = model.encode(patterns)
    user_embedding = model.encode([user_text])
    similarities = cosine_similarity(user_embedding, pattern_embeddings)
    max_similarity = np.max(similarities)
    keyword_count = sum(1 for kw in keywords if kw in user_text.lower())
    keyword_density = min(keyword_count / len(keywords), 1.0)
    score = (0.6 * max_similarity) + (0.4 * keyword_density)
    return int(score * 100)

def detect_shadow_patterns(text: str) -> Dict:
    """Detect shadow loop patterns"""
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

class ReportGenerator:
    def __init__(self, intake_data: Dict):
        self.intake_data = intake_data
        self.responses = intake_data['responses']
        self.user_name = intake_data.get('first_name', 'Anonymous')
        self.combined_text = " ".join([r['answer_text'] for r in self.responses])
        
    def generate_report(self) -> Dict:
        """Generate complete SAAQ report"""
        
        return {
            # Metadata
            "report_metadata": {
                "user_name": self.user_name,
                "report_date": datetime.now().isoformat(),
                "intake_id": self.intake_data.get('intake_id'),
                "intake_version": self.intake_data.get('intake_version')
            },
            
            # Section 1: Developmental Stage (Harsh)
            "stage_diagnosis": self._analyze_stage(),
            
            # Section 2: Awareness Quotient (Harsh)
            "awareness_quotient": self._analyze_aq(),
            
            # Section 3: Hemispheric Bias (Advik)
            "hemispheric_bias": self._analyze_hemispheric(),
            
            # Section 4: Power Centers (Advik)
            "power_centers": self._analyze_power_centers(),
            
            # Section 5: Core Aptitudes (Cameron)
            "core_aptitudes": self._analyze_aptitudes(),
            
            # Section 6: Shadow Indicators (Cameron)
            "shadow_indicators": self._analyze_shadow(),
            
            # Section 7: Executive Summary
            "executive_summary": self._generate_executive_summary()
        }
    
    def _analyze_stage(self) -> Dict:
        """Harsh's stage classifier"""
        if not MODULES_AVAILABLE:
            return self._fallback_stage()
        
        try:
            result = analyze_stage(self.combined_text)
            return {
                "stage": result.get('stage_label', 'Unknown'),
                "stage_score": result.get('stage_score', 0),
                "confidence": result.get('confidence', 0.0),
                "indicators": result.get('indicators', {}),
                "description": self._get_stage_description(result.get('stage_label', 'Unknown'))
            }
        except Exception as e:
            print(f"Stage analysis error: {e}")
            return self._fallback_stage()
    
    def _analyze_aq(self) -> Dict:
        """Harsh's awareness quotient"""
        if not MODULES_AVAILABLE:
            return {"score": 0, "category": "Unknown"}
        
        try:
            result = analyze_aq(self.combined_text)
            return {
                "score": result.get('awareness_score', 0),
                "category": result.get('awareness_label', 'Unknown'),
                "balance_index": result.get('balance_index', 0),
                "dimensions": result.get('indicators', {}),
                "description": result.get('interpretive_summary', '')
            }
        except Exception as e:
            print(f"AQ analysis error: {e}")
            return {"score": 0, "category": "Unknown"}
    
    def _analyze_hemispheric(self) -> Dict:
        """Advik's hemispheric bias analyzer"""
        if not MODULES_AVAILABLE:
            return self._fallback_hemispheric()
        
        try:
            result = analyze_hemispheric(self.combined_text)
            return {
                "score": result.get('hemispheric_score', 0.0),
                "dominant": result.get('dominant_hemisphere', 'Balanced'),
                "confidence": result.get('confidence', 0.0),
                "indicators": result.get('indicators', {}),
                "description": result.get('interpretive_summary', '')
            }
        except Exception as e:
            print(f"Hemispheric analysis error: {e}")
            return self._fallback_hemispheric()
    
    def _analyze_power_centers(self) -> List[Dict]:
        """Advik's power centers profiler"""
        if not MODULES_AVAILABLE:
            return self._fallback_power_centers()
        
        try:
            result = analyze_power(self.combined_text)
            profile = result.get('power_profile', {})
            
            centers = []
            for name, score in profile.items():
                if score >= 7:
                    status = "Strong"
                elif score >= 4:
                    status = "Moderate"
                else:
                    status = "Developing"
                
                centers.append({
                    "name": name,
                    "score": round(score, 1),
                    "status": status
                })
            
            # Add metadata
            centers.append({
                "metadata": {
                    "dominant_center": result.get('dominant_center', 'Unknown'),
                    "balance_index": result.get('balance_index', 0),
                    "description": result.get('interpretive_summary', '')
                }
            })
            
            return centers
        except Exception as e:
            print(f"Power centers analysis error: {e}")
            return self._fallback_power_centers()
    
    def _analyze_aptitudes(self) -> List[Dict]:
        """Cameron's core aptitudes scoring"""
        aptitudes = []
        
        for apt_name, config in APTITUDE_PATTERNS.items():
            score = calculate_aptitude_score(
                self.combined_text,
                config['patterns'],
                config['keywords']
            )
            
            if score >= 70:
                level = "Strong"
            elif score >= 40:
                level = "Moderate"
            else:
                level = "Developing"
            
            aptitudes.append({
                "name": apt_name.replace('_', ' ').title(),
                "score": score,
                "level": level
            })
        
        return aptitudes
    
    def _analyze_shadow(self) -> Dict:
        """Cameron's shadow indicator detection"""
        shadow_scores = detect_shadow_patterns(self.combined_text)
        detected_loops = [name for name, score in shadow_scores.items() if score > 50]
        
        return {
            "scores": shadow_scores,
            "detected_loops": detected_loops,
            "primary_pattern": max(shadow_scores.items(), key=lambda x: x[1])[0] if shadow_scores else "none",
            "antidotes": self._get_shadow_antidotes(detected_loops)
        }
    
    def _generate_executive_summary(self) -> str:
        """Generate high-level executive summary"""
        stage = self._analyze_stage()
        aq = self._analyze_aq()
        hem = self._analyze_hemispheric()
        shadow = self._analyze_shadow()
        
        stage_label = stage.get('stage', 'Unknown')
        aq_score = aq.get('score', 0)
        hem_dominant = hem.get('dominant', 'Balanced')
        detected_loops = shadow.get('detected_loops', [])
        
        summary = f"""{self.user_name} demonstrates a developmental center of gravity at {stage_label} with an Awareness Quotient of {aq_score:.1f}. Their cognitive style shows {hem_dominant} hemispheric processing."""
        
        if detected_loops:
            summary += f"\n\nKey growth edges include addressing {', '.join(detected_loops).replace('_', ' ')} patterns."
        
        summary += "\n\nRecommended focus areas: Continue developing reflective capacity, integrate insights across multiple perspectives, and maintain practices that support ongoing development."
        
        return summary.strip()
    
    # Fallback methods
    def _fallback_stage(self) -> Dict:
        """Fallback stage detection using simple keyword analysis"""
        all_text = self.combined_text.lower()
        stage_scores = {
            "S5": sum(1 for kw in ["precision", "method", "correct", "process"] if kw in all_text),
            "S6": sum(1 for kw in ["outcome", "result", "goal", "achieve"] if kw in all_text),
            "S7": sum(1 for kw in ["perspective", "empathy", "connection"] if kw in all_text),
            "S8": sum(1 for kw in ["principle", "system", "integrate", "values"] if kw in all_text)
        }
        cog = max(stage_scores, key=stage_scores.get)
        confidence = stage_scores[cog] / max(sum(stage_scores.values()), 1)
        
        return {
            "stage": cog,
            "stage_score": stage_scores[cog] * 10,
            "confidence": round(confidence, 2),
            "indicators": stage_scores,
            "description": self._get_stage_description(cog)
        }
    
    def _fallback_hemispheric(self) -> Dict:
        """Fallback hemispheric bias detection"""
        return {
            "score": 0.0,
            "dominant": "Balanced",
            "confidence": 0.0,
            "indicators": {},
            "description": "Hemispheric analysis unavailable"
        }
    
    def _fallback_power_centers(self) -> List[Dict]:
        """Fallback power centers"""
        return [
            {"name": "Cognitive", "score": 5.0, "status": "Moderate"},
            {"name": "Emotional", "score": 5.0, "status": "Moderate"},
            {"name": "Relational", "score": 5.0, "status": "Moderate"},
            {"name": "Somatic", "score": 5.0, "status": "Moderate"},
            {"name": "Spiritual", "score": 5.0, "status": "Moderate"}
        ]
    
    def _get_stage_description(self, stage: str) -> str:
        """Get stage description"""
        descriptions = {
            "S1 Reactive Self": "Reactive, impulsive responses to immediate needs",
            "S2 Egocentric": "Self-focused, seeking immediate gratification",
            "S3 Socialized": "Conforming to group norms and external expectations",
            "S4 Loyal Contributor": "Committed to role and group loyalty",
            "S5 Achiever": "Goal-oriented, strategic, outcome-focused",
            "S6 Synthesizer": "Integrating multiple perspectives systematically",
            "S7 Integrative": "Self-authoring with principled flexibility",
            "S8 Transcendent": "Meta-systemic awareness, holding paradox"
        }
        return descriptions.get(stage, "Stage description not available")
    
    def _get_shadow_antidotes(self, loops: List[str]) -> List[str]:
        """Get antidotes for detected shadow patterns"""
        antidotes = {
            "control_reflex": "Practice letting go; notice when you're gripping",
            "quick_relief": "Pause before seeking escape; name the discomfort",
            "lone_rescuer": "Ask for help; delegate; trust others' capacity"
        }
        return [antidotes.get(loop, "Develop awareness") for loop in loops]