import sys
sys.path.insert(0, '.')

from stage_classifier import _score_text as analyze_stage
from awareness_quotient import _score_awareness as analyze_aq
from hemisphere_bias import analyze_text as analyze_hemispheric
from power_centers import analyze_text as analyze_power
from cameron_aptitudes_shadow import analyze_aptitudes_shadow
import json
from datetime import datetime
from typing import Dict

MARK_TEXT = """
I'll tell you about my divorce. It happened four years ago. But in a sense I'm still working through it. During Covid and even the years leading up, I was struggling with my now ex-wife, Lynda. Lynda and I did not see eye to eye on money management. She was a prolific over spender. We were going through some lean times, and Covid didn't help. During the initial years of our marriage, I let Lynda handle the finances, and I made the money. She worked very little. She took care of our daughter, Alana, but also had a housekeeper and babysitter. It was my neglect of not keeping an eye on the budget and her over spending that led to progressive debt. Lynda came into the marriage after a bankruptcy and had poor credit. I on the other hand, had a credit score above 800. But I don't want to blame this all on Lynda. I should've kept an eye on the books. Because I didn't, we got into some credit card debt that we had no reasonable way of paying off. Because of that situation, I lived with a lot of stress and developed some stress related illnesses. I was looking for away out when I met a man named David Cota. I'd always had the dream of opening my own retreat facility. He made himself out as a wealthy entrepreneur, eager to help me with my dream. I took some extraordinary risks to make that happen but the deal ultimately didn't go through. That plunged us into more debt - debt I'm still paying off. Somewhere during that time (2020-2021) Lynda met someone and had an affair. She gaslighted me through the whole experience. I knew something was amiss, and I was trying to repair the marriage, but she just strung me along until she was able to make the jump to this other guy. The guy who is now her boyfriend is wealthy. The affair was devastating. I've never experienced betrayal trauma like that. I got so sick that I got down to 112 pounds. My normal weight is 135. I got a flu in January 2022 that nearly killed me. It's been a long road back. Lots of introspection, shadow work, and diving deep into my spiritual practice. Fast forward to June of this year, Lynda moved to Alaska with her boyfriend, leaving me to parent Alana full-time during the school year. Deep down there's still anger over the choices Lynda has made and how it's affected me and Alana. But I'm more angry about how it's affected Alana. For me, I can gain perspective and see this as a heroes journey, a developmental task that I asked for before this incarnation. So that's how I'm handling it, as a spiritual challenge. I tell myself, "I'm the one." That simple phrase keeps me from kvetching and complaining and focuses me forward on doing what's right and turning this difficulty into something beautiful.

Strong emotions open my awareness. Quite the opposite of fixating me and losing myself, I become more aware. My awareness includes awareness of my surroundings, my body sensations, and my mental activity. I'm aware that I'm aware. And I breathe, and I feel, and I let things flow. In that state, wise actions, the next right thing, a better way to handle things, usually arises for me. I trust the Universe has my back.

Money is a symbol. Money is energy. Money is a projection. Money is a means by which we transact. Money is an image. Money is an aspiration. The quest for it can bind someone to Samsara. Money unites, money divides. Money builds, and it destroys. It's like the energy of the sun. We need it to survive, but too much can cause cancer.

I'm a content creator. There isn't a day that goes by that I'm not making something beautiful, good, and true for the purpose of helping others and the world. I'm a health and wellness artist.

Consciousness is the ground of all being. Information is the only thing that truly exists, if you can call it existing. I have no way of explaining the evanescent and ineffable Universe or life that lives in it. Life is The LIFE, All that is, consciousness. "I" exists as a perspective. As do we all. A person is a perspective.

What gives my life meaning is this drive to wake up and become a better version of myself. I want to turn everything I learn that helps me overcome my challenges into content that helps others. That feels like a good life to me.
"""

def generate_complete_report(text: str, user_name: str = "Anonymous") -> Dict:
    
    stage = analyze_stage(text)
    aq = analyze_aq(text)
    hemispheric = analyze_hemispheric(text)
    power = analyze_power(text)
    apt_shadow = analyze_aptitudes_shadow(text)
    
    report = {
        "report_metadata": {
            "user_name": user_name,
            "report_date": datetime.now().isoformat(),
            "analysis_version": "team-integrated-v1"
        },
        "stage_diagnosis": stage,
        "awareness_quotient": aq,
        "hemispheric_bias": hemispheric,
        "power_centers": power,
        "core_aptitudes": apt_shadow['aptitudes'],
        "shadow_indicators": apt_shadow['shadow_indicators'],
        "executive_summary": _generate_summary(stage, aq, hemispheric, power, apt_shadow)
    }
    
    return report

def _generate_summary(stage, aq, hemispheric, power, apt_shadow):
    
    summary = f"""
Developmental Stage: {stage['stage_label']} (confidence: {stage['confidence']:.2f})
Awareness Quotient: {aq['awareness_score']:.1f} ({aq['awareness_label']})
Hemispheric Dominance: {hemispheric['dominant_hemisphere']} (score: {hemispheric['hemispheric_score']:.1f})
Dominant Power Center: {power['dominant_center']} ({power['power_profile'][power['dominant_center']]:.1f}/10)
Top Aptitude: {apt_shadow['summary']['top_aptitude']}
Shadow Risk: {apt_shadow['summary']['shadow_risk']}

This profile shows {stage['stage_label']} development with {aq['awareness_label']}. 
The individual demonstrates {hemispheric['dominant_hemisphere'].lower()} hemispheric processing 
and strong {power['dominant_center'].lower()} energy expression.
""".strip()
    
    return summary

def display_report(report: Dict):
    print("="*80)
    print("COMPLETE SAAQ INTEGRATION REPORT")
    print("="*80)
    
    print(f"\nUser: {report['report_metadata']['user_name']}")
    print(f"Date: {report['report_metadata']['report_date'][:10]}")
    
    stage = report['stage_diagnosis']
    print(f"\n🎯 STAGE: {stage['stage_label']}")
    print(f"   Score: {stage['stage_score']:.1f}")
    print(f"   Confidence: {stage['confidence']:.2f}")
    
    aq = report['awareness_quotient']
    print(f"\n🧠 AWARENESS QUOTIENT: {aq['awareness_score']:.1f}")
    print(f"   Category: {aq['awareness_label']}")
    
    hem = report['hemispheric_bias']
    print(f"\n⚖️  HEMISPHERIC: {hem['dominant_hemisphere']}")
    print(f"   Score: {hem['hemispheric_score']:.1f}")
    
    power = report['power_centers']
    print(f"\n⚡ POWER CENTERS:")
    for center, score in power['power_profile'].items():
        bar = "█" * int(score) + "░" * (10 - int(score))
        print(f"   {center:20} {bar} {score:4.1f}/10")
    print(f"   Dominant: {power['dominant_center']}")
    
    print(f"\n💪 CORE APTITUDES:")
    for apt_name, apt_data in report['core_aptitudes'].items():
        print(f"   {apt_name:15} → {apt_data['score']:3}/100  [{apt_data['level']}]")
    
    shadow = report['shadow_indicators']
    print(f"\n👻 SHADOW INDICATORS:")
    for pattern, score in shadow['scores'].items():
        status = "🔴 DETECTED" if score > 50 else "⚪ Low"
        print(f"   {pattern.replace('_', ' ').title():20} → {score:3}/100 {status}")
    
    print(f"\n📋 EXECUTIVE SUMMARY:")
    print(report['executive_summary'])
    
    print("\n" + "="*80)

if __name__ == "__main__":
    
    print("Generating complete report for Mark Pirtle...")
    
    report = generate_complete_report(MARK_TEXT, "Mark Pirtle")
    
    with open('complete_integrated_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    display_report(report)
    
    print(f"\n✅ Complete report saved to: complete_integrated_report.json")