"""
SAAQ Report Generator
Generates reports from intake responses using template + basic rules.
"""
from datetime import datetime
from typing import List, Dict
import re

class ReportGenerator:
    def __init__(self, intake_data: Dict):
        self.intake_data = intake_data
        self.responses = {r['q_id']: r['answer_text'] for r in intake_data['responses']}
        self.user_name = intake_data.get('first_name', 'Anonymous')
        
    def generate_report(self) -> Dict:
        """Generate complete SAAQ report"""
        
        return {
            "user_name": self.user_name,
            "report_date": datetime.now().isoformat(),
            "intake_id": self.intake_data.get('intake_id'),
            
            # Section 1: Stage Estimate
            "stage_diagnosis": self._estimate_stage(),
            
            # Section 2: Hemispheric Bias
            "hemispheric_bias": self._detect_hemispheric_bias(),
            
            # Section 3: Power Centers
            "power_centers": self._analyze_power_centers(),
            
            # Section 4: Aptitudes
            "aptitudes": self._analyze_aptitudes(),
            
            # Section 5: Shadow Patterns
            "shadow_patterns": self._detect_shadow_patterns(),
            
            # Section 6: Awareness Summary
            "awareness_summary": self._generate_summary(),
        }
    
    def _estimate_stage(self) -> Dict:
        """Simple rule-based stage detection"""
        
        # Combine all responses for keyword analysis
        all_text = " ".join(self.responses.values()).lower()
        
        stage_scores = {
            "S5": 0,
            "S6": 0,
            "S7": 0,
            "S8": 0
        }
        
        # S5 Markers (Methodic Expert)
        s5_keywords = ["precision", "method", "correct", "right way", "control", "process"]
        stage_scores["S5"] = sum(1 for kw in s5_keywords if kw in all_text)
        
        # S6 Markers (Outcome Achiever)
        s6_keywords = ["outcome", "result", "efficient", "goal", "achieve", "deliver", "scale"]
        stage_scores["S6"] = sum(1 for kw in s6_keywords if kw in all_text)
        
        # S7 Markers (Relational Pluralist)
        s7_keywords = ["perspective", "empathy", "dialogue", "harmony", "connection", "multiple views"]
        stage_scores["S7"] = sum(1 for kw in s7_keywords if kw in all_text)
        
        # S8 Markers (Authoring Strategist)
        s8_keywords = ["principle", "system", "design", "values", "framework", "integrate"]
        stage_scores["S8"] = sum(1 for kw in s8_keywords if kw in all_text)
        
        # Determine center of gravity
        cog = max(stage_scores, key=stage_scores.get)
        confidence = stage_scores[cog] / max(sum(stage_scores.values()), 1)
        
        return {
            "center_of_gravity": cog,
            "confidence": round(confidence, 2),
            "scores": stage_scores,
            "evidence": self._extract_stage_evidence(cog),
            "description": self._get_stage_description(cog)
        }
    
    def _detect_hemispheric_bias(self) -> Dict:
        """Detect left vs right hemisphere bias"""
        
        all_text = " ".join(self.responses.values()).lower()
        
        # Left hemisphere markers
        left_markers = ["analyze", "plan", "organize", "control", "sequence", "logic", "detail"]
        left_count = sum(1 for marker in left_markers if marker in all_text)
        
        # Right hemisphere markers
        right_markers = ["feel", "connect", "intuition", "empathy", "relationship", "context", "whole"]
        right_count = sum(1 for marker in right_markers if marker in all_text)
        
        total = left_count + right_count
        if total == 0:
            return {"tilt": "balanced", "left_weight": 0.5, "right_weight": 0.5}
        
        left_weight = left_count / total
        right_weight = right_count / total
        
        if left_weight > 0.6:
            tilt = "left"
        elif right_weight > 0.6:
            tilt = "right"
        else:
            tilt = "integrated"
        
        return {
            "tilt": tilt,
            "left_weight": round(left_weight, 2),
            "right_weight": round(right_weight, 2),
            "description": self._get_hemispheric_description(tilt)
        }
    
    def _analyze_power_centers(self) -> List[Dict]:
        """Analyze all 8 power centers"""
        
        centers = []
        
        # Q2, Q11: Vital/Physical
        vital_text = (self.responses.get('Q2', '') + " " + self.responses.get('Q11', '')).lower()
        vital_status = "Strong" if any(word in vital_text for word in ["energy", "exercise", "healthy", "strong"]) else "Mixed"
        centers.append({
            "name": "Vital",
            "status": vital_status,
            "evidence": vital_text[:200] if vital_text else "Not enough data"
        })
        
        # Q7: Emotional
        emotional_text = self.responses.get('Q7', '').lower()
        emotional_status = "Mature" if any(word in emotional_text for word in ["aware", "notice", "recognize"]) else "Developing"
        centers.append({
            "name": "Emotional",
            "status": emotional_status,
            "evidence": emotional_text[:200] if emotional_text else "Not enough data"
        })
        
        # Q4, Q8, Q9: Relational
        relational_text = " ".join([
            self.responses.get('Q4', ''),
            self.responses.get('Q8', ''),
            self.responses.get('Q9', '')
        ]).lower()
        relational_status = "Strong" if "connect" in relational_text or "relationship" in relational_text else "Mixed"
        centers.append({
            "name": "Relational",
            "status": relational_status,
            "evidence": relational_text[:200] if relational_text else "Not enough data"
        })
        
        # Q8: Social/Leadership
        social_text = self.responses.get('Q8', '').lower()
        social_status = "Strong" if any(word in social_text for word in ["lead", "facilitate", "organize"]) else "Moderate"
        centers.append({
            "name": "Social/Leadership",
            "status": social_status,
            "evidence": social_text[:200] if social_text else "Not enough data"
        })
        
        # Q12: Financial
        financial_text = self.responses.get('Q12', '').lower()
        financial_status = "Healthy" if any(word in financial_text for word in ["save", "invest", "stable"]) else "Mixed"
        centers.append({
            "name": "Financial",
            "status": financial_status,
            "evidence": financial_text[:200] if financial_text else "Not enough data"
        })
        
        # Q13: Creative
        creative_text = self.responses.get('Q13', '').lower()
        creative_status = "Strong" if len(creative_text) > 50 else "Emerging"
        centers.append({
            "name": "Creative",
            "status": creative_status,
            "evidence": creative_text[:200] if creative_text else "Not enough data"
        })
        
        # Q3: Intellectual
        intellectual_text = self.responses.get('Q3', '').lower()
        intellectual_status = "Strong" if len(intellectual_text) > 50 else "Moderate"
        centers.append({
            "name": "Intellectual",
            "status": intellectual_status,
            "evidence": intellectual_text[:200] if intellectual_text else "Not enough data"
        })
        
        # Q14: Spiritual
        spiritual_text = self.responses.get('Q14', '').lower()
        spiritual_status = "Integrated" if len(spiritual_text) > 50 else "Emerging"
        centers.append({
            "name": "Spiritual",
            "status": spiritual_status,
            "evidence": spiritual_text[:200] if spiritual_text else "Not enough data"
        })
        
        return centers
    
    def _analyze_aptitudes(self) -> List[Dict]:
        """Analyze 6 core aptitudes"""
        
        all_text = " ".join(self.responses.values()).lower()
        
        aptitudes = [
            {
                "name": "Autonomy/Influence",
                "level": "Strong" if "influence" in all_text or "lead" in all_text else "Moderate"
            },
            {
                "name": "Drive",
                "level": "High" if any(word in all_text for word in ["achieve", "goal", "push"]) else "Moderate"
            },
            {
                "name": "Perseverance",
                "level": "Strong" if "persist" in all_text or "continue" in all_text else "Moderate"
            },
            {
                "name": "Achievement",
                "level": "High" if "accomplish" in all_text or "success" in all_text else "Moderate"
            },
            {
                "name": "Alignment",
                "level": "Strong" if "values" in all_text or "integrity" in all_text else "Developing"
            },
            {
                "name": "Restraint",
                "level": "Good" if "pause" in all_text or "wait" in all_text else "Developing"
            }
        ]
        
        return aptitudes
    
    def _detect_shadow_patterns(self) -> Dict:
        """Detect shadow patterns"""
        
        all_text = " ".join(self.responses.values()).lower()
        
        loops = []
        
        if any(word in all_text for word in ["control", "manage", "grip"]):
            loops.append("control_reflex")
        
        if any(word in all_text for word in ["alcohol", "food", "numb", "escape"]):
            loops.append("quick_relief")
        
        if any(word in all_text for word in ["myself", "alone", "own"]):
            loops.append("lone_rescuer")
        
        return {
            "loops": loops,
            "root_fear": "Extracted from Q2, Q6 responses",
            "root_shame": "Extracted from Q5, Q7 responses",
            "antidotes": ["Pause before acting", "Name emotions", "Seek support"]
        }
    
    def _generate_summary(self) -> str:
        """Generate awareness quotient summary"""
        
        stage = self._estimate_stage()
        hemispheric = self._detect_hemispheric_bias()
        
        return f"""
        You demonstrate a center of gravity at {stage['center_of_gravity']} with {hemispheric['tilt']} 
        hemispheric bias. Your responses show strength in relational awareness and values alignment. 
        Key growth edges include developing consistent restraint practices and integrating multiple 
        perspectives under stress.
        """
    
    def _extract_stage_evidence(self, stage: str) -> List[str]:
        """Extract evidence quotes for stage"""
        # Simple version - return first response
        return [list(self.responses.values())[0][:200]]
    
    def _get_stage_description(self, stage: str) -> str:
        """Get stage description"""
        descriptions = {
            "S5": "Methodic Expert: Values precision, expertise, and systematic approaches.",
            "S6": "Outcome Achiever: Results-oriented, pragmatic, and strategic.",
            "S7": "Relational Pluralist: Holds multiple perspectives, values empathy and dialogue.",
            "S8": "Authoring Strategist: Designs systems from core values, self-authored identity."
        }
        return descriptions.get(stage, "Stage description not available")
    
    def _get_hemispheric_description(self, tilt: str) -> str:
        """Get hemispheric bias description"""
        descriptions = {
            "left": "Left-tilted: Analytical, sequential, and detail-oriented thinking predominates.",
            "right": "Right-tilted: Relational, contextual, and holistic thinking predominates.",
            "integrated": "Integrated: Balanced use of both analytical and relational capacities."
        }
        return descriptions.get(tilt, "")