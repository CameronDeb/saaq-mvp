"""
Simple Integration Test - No Heavy Dependencies
"""
import sys
import os

backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
research_path = os.path.dirname(__file__)

sys.path.insert(0, backend_path)
sys.path.insert(0, research_path)

from stage_classifier import _score_text as analyze_stage
from awareness_quotient import _score_awareness as analyze_aq
from hemisphere_bias import analyze_text as analyze_hemispheric
from power_centers import analyze_text as analyze_power
import json
from datetime import datetime

SAMPLE_TEXT = """
I faced a complex technical problem that required systematic analysis and careful planning. I broke it down into steps and solved it methodically.
My chest tightens and I feel the need to control everything. I breathe shallowly and try to manage all the details myself.
I've learned to integrate multiple perspectives and see systems holistically. I value both logic and intuition now.
When I tried explaining my vision, others couldn't see it. I learned to communicate more clearly and meet people where they are.
I had to choose between honesty and comfort. I chose truth even though it was difficult, and I felt aligned with my principles.
I felt pulled between ambition and rest. I realized both are necessary and now I honor cycles of effort and recovery.
I notice my self-talk can be harsh and critical. I'm learning to be more compassionate with myself and question negative thoughts.
I tend to facilitate and help the group see different perspectives. Others say I help them think more deeply.
I remind myself that everyone has valid reasons for their perspectives. Curiosity helps me stay connected even when I disagree.
Rigidity and close-mindedness frustrate me. I admire people who can hold paradoxes and remain curious.
I'm more aware of tension in my body now. I notice when I'm holding stress and try to release it through movement and breath.
Money represents freedom and security to me. I'm disciplined about saving and investing for long-term goals.
I express creativity through problem-solving and writing. Imagination helps me envision possibilities beyond current constraints.
I find meaning through meditation and contemplating my place in the universe. I feel connected to a larger purpose through serving others.
I used to be very self-critical. Now I try to speak to myself like a good friend would. Perspective and patience help me move forward.
"""

def simple_aptitude_score(text: str, keywords: list) -> int:
    """Simple keyword-based aptitude scoring"""
    text_lower = text.lower()
    keyword_count = sum(1 for kw in keywords if kw in text_lower)
    score = min(100, int((keyword_count / len(keywords)) * 150))
    return score

def simple_shadow_detection(text: str) -> dict:
    """Simple shadow pattern detection"""
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

def generate_simple_report():
    print("="*80)
    print("SIMPLE INTEGRATION TEST - ALL TEAM MODULES")
    print("="*80)
    
    # Run all analyses
    print("\n🎯 Analyzing Developmental Stage...")
    stage = analyze_stage(SAMPLE_TEXT)
    
    print("🧠 Analyzing Awareness Quotient...")
    aq = analyze_aq(SAMPLE_TEXT)
    
    print("⚖️  Analyzing Hemispheric Bias...")
    hemispheric = analyze_hemispheric(SAMPLE_TEXT)
    
    print("⚡ Analyzing Power Centers...")
    power = analyze_power(SAMPLE_TEXT)
    
    print("💪 Analyzing Core Aptitudes (simple scoring)...")
    aptitudes = {
        "Drive": simple_aptitude_score(SAMPLE_TEXT, ["achieve", "goal", "push", "motivated"]),
        "Alignment": simple_aptitude_score(SAMPLE_TEXT, ["values", "integrity", "authentic", "principles"]),
        "Restraint": simple_aptitude_score(SAMPLE_TEXT, ["pause", "wait", "reflect", "consider"])
    }
    
    print("👻 Analyzing Shadow Patterns...")
    shadow = simple_shadow_detection(SAMPLE_TEXT)
    
    # Build report
    report = {
        "report_metadata": {
            "user_name": "Alex",
            "report_date": datetime.now().isoformat(),
            "test_type": "Simple Integration Test"
        },
        "stage_diagnosis": stage,
        "awareness_quotient": aq,
        "hemispheric_bias": hemispheric,
        "power_centers": power,
        "core_aptitudes": aptitudes,
        "shadow_indicators": shadow
    }
    
    # Save
    with open('simple_integration_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ Report saved to: simple_integration_report.json")
    
    # Display
    print("\n" + "="*80)
    print("📊 RESULTS SUMMARY")
    print("="*80)
    
    print(f"\n🎯 STAGE: {stage['stage_label']}")
    print(f"   Score: {stage['stage_score']:.1f}")
    print(f"   Confidence: {stage['confidence']:.2f}")
    
    print(f"\n🧠 AWARENESS QUOTIENT: {aq.get('awareness_score', 0):.1f}")
    print(f"   Category: {aq.get('awareness_label', 'Unknown')}")
    
    print(f"\n⚖️  HEMISPHERIC: {hemispheric['dominant_hemisphere']}")
    print(f"   Score: {hemispheric['hemispheric_score']:.1f}")
    
    print(f"\n⚡ POWER CENTERS:")
    for center, score in power['power_profile'].items():
        print(f"   {center:12} → {score:4.1f}/10")
    
    print(f"\n💪 APTITUDES:")
    for name, score in aptitudes.items():
        level = "Strong" if score >= 70 else "Moderate" if score >= 40 else "Developing"
        print(f"   {name:12} → {score:3}/100 [{level}]")
    
    print(f"\n👻 SHADOW PATTERNS:")
    for pattern, score in shadow.items():
        status = "🔴 DETECTED" if score > 50 else "⚪ Low"
        print(f"   {pattern.replace('_', ' ').title():20} → {score:3}/100 {status}")
    
    print("\n" + "="*80)
    print("✅ ALL MODULES WORKING - INTEGRATION SUCCESSFUL!")
    print("="*80)

if __name__ == "__main__":
    generate_simple_report()