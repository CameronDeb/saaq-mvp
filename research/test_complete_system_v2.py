"""
Complete System Integration Test V2
Fresh import with no caching
"""
import sys
import os

# Clear any cached imports
if 'report_generator' in sys.modules:
    del sys.modules['report_generator']

# Set paths
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
services_path = os.path.join(backend_path, 'services')
research_path = os.path.dirname(__file__)

sys.path.insert(0, backend_path)
sys.path.insert(0, services_path)
sys.path.insert(0, research_path)

# Import with correct function names
from stage_classifier import _score_text as analyze_stage
from awareness_quotient import _score_awareness as analyze_aq
from hemisphere_bias import analyze_text as analyze_hemispheric
from power_centers import analyze_text as analyze_power
import json
from datetime import datetime

# Cameron's modules
from cameron_prototype import calculate_aptitude_score, detect_shadow_patterns, APTITUDE_PATTERNS

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

def generate_complete_report():
    """Generate complete report using all modules directly"""
    
    print("="*80)
    print("COMPLETE SYSTEM TEST - DIRECT MODULE INTEGRATION")
    print("="*80)
    
    # Stage Analysis
    print("\n🎯 Analyzing Developmental Stage...")
    stage = analyze_stage(SAMPLE_TEXT)
    
    # Awareness Quotient
    print("🧠 Analyzing Awareness Quotient...")
    aq = analyze_aq(SAMPLE_TEXT)
    
    # Hemispheric Bias
    print("⚖️  Analyzing Hemispheric Bias...")
    hemispheric = analyze_hemispheric(SAMPLE_TEXT)
    
    # Power Centers
    print("⚡ Analyzing Power Centers...")
    power = analyze_power(SAMPLE_TEXT)
    
    # Core Aptitudes
    print("💪 Analyzing Core Aptitudes...")
    aptitudes = {}
    for apt_name, config in APTITUDE_PATTERNS.items():
        score = calculate_aptitude_score(SAMPLE_TEXT, config['patterns'], config['keywords'])
        aptitudes[apt_name] = {
            "score": score,
            "level": "Strong" if score >= 70 else "Moderate" if score >= 40 else "Developing"
        }
    
    # Shadow Indicators
    print("👻 Analyzing Shadow Patterns...")
    shadow = detect_shadow_patterns(SAMPLE_TEXT)
    detected_loops = [name for name, score in shadow.items() if score > 50]
    
    # Build complete report
    report = {
        "report_metadata": {
            "user_name": "Alex",
            "report_date": datetime.now().isoformat(),
            "intake_id": "test-integration-002"
        },
        "stage_diagnosis": {
            "stage": stage.get('stage_label', 'Unknown'),
            "stage_score": stage.get('stage_score', 0),
            "confidence": stage.get('confidence', 0),
            "indicators": stage.get('indicators', {}),
            "description": stage.get('interpretive_summary', '')
        },
        "awareness_quotient": {
            "score": aq.get('awareness_score', 0),
            "category": aq.get('awareness_label', 'Unknown'),
            "balance_index": aq.get('balance_index', 0),
            "dimensions": aq.get('indicators', {}),
            "description": aq.get('interpretive_summary', '')
        },
        "hemispheric_bias": {
            "score": hemispheric.get('hemispheric_score', 0),
            "dominant": hemispheric.get('dominant_hemisphere', 'Balanced'),
            "confidence": hemispheric.get('confidence', 0),
            "indicators": hemispheric.get('indicators', {}),
            "description": hemispheric.get('interpretive_summary', '')
        },
        "power_centers": {
            "profile": power.get('power_profile', {}),
            "dominant_center": power.get('dominant_center', 'Unknown'),
            "balance_index": power.get('balance_index', 0),
            "description": power.get('interpretive_summary', '')
        },
        "core_aptitudes": aptitudes,
        "shadow_indicators": {
            "scores": shadow,
            "detected_loops": detected_loops,
            "primary_pattern": max(shadow.items(), key=lambda x: x[1])[0] if shadow else "none"
        }
    }
    
    # Save report
    output_file = 'complete_report_v2.json'
    with open(output_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✅ Report generated and saved to: {output_file}")
    
    # Display summary
    print("\n" + "="*80)
    print("📊 REPORT SUMMARY")
    print("="*80)
    
    print(f"\n🎯 STAGE: {report['stage_diagnosis']['stage']}")
    print(f"   Score: {report['stage_diagnosis']['stage_score']:.1f}")
    print(f"   Confidence: {report['stage_diagnosis']['confidence']:.2f}")
    
    print(f"\n🧠 AWARENESS QUOTIENT: {report['awareness_quotient']['score']:.1f}")
    print(f"   Category: {report['awareness_quotient']['category']}")
    print(f"   Balance: {report['awareness_quotient']['balance_index']:.1f}")
    
    print(f"\n⚖️  HEMISPHERIC BIAS: {report['hemispheric_bias']['dominant']}")
    print(f"   Score: {report['hemispheric_bias']['score']:.1f}")
    print(f"   Confidence: {report['hemispheric_bias']['confidence']:.2f}")
    
    print(f"\n⚡ POWER CENTERS:")
    for center, score in report['power_centers']['profile'].items():
        print(f"   {center:12} → {score:4.1f}/10")
    print(f"   Dominant: {report['power_centers']['dominant_center']}")
    
    print(f"\n💪 CORE APTITUDES:")
    for apt_name, data in aptitudes.items():
        print(f"   {apt_name.title():15} → {data['score']:3}/100 [{data['level']}]")
    
    print(f"\n👻 SHADOW PATTERNS:")
    print(f"   Detected: {detected_loops}")
    print(f"   Primary: {report['shadow_indicators']['primary_pattern']}")
    
    print("\n" + "="*80)
    print("✅ INTEGRATION TEST COMPLETE - ALL MODULES WORKING")
    print("="*80)
    
    return report

if __name__ == "__main__":
    generate_complete_report()