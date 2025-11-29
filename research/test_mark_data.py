"""
Test all modules on Mark's actual SA360 responses
"""
import sys
sys.path.insert(0, '.')

from stage_classifier import _score_text as analyze_stage
from awareness_quotient import _score_awareness as analyze_aq
from hemisphere_bias import analyze_text as analyze_hemispheric
from power_centers import analyze_text as analyze_power
import json

# Mark's full SA360 responses (from document 4)
MARK_TEXT = """
I'll tell you about my divorce. It happened four years ago. But in a sense I'm still working through it. During Covid and even the years leading up, I was struggling with my now ex-wife, Lynda. Lynda and I did not see eye to eye on money management. She was a prolific over spender. We were going through some lean times, and Covid didn't help. During the initial years of our marriage, I let Lynda handle the finances, and I made the money. She worked very little. She took care of our daughter, Alana, but also had a housekeeper and babysitter. It was my neglect of not keeping an eye on the budget and her over spending that led to progressive debt. Lynda came into the marriage after a bankruptcy and had poor credit. I on the other hand, had a credit score above 800. But I don't want to blame this all on Lynda. I should've kept an eye on the books. Because I didn't, we got into some credit card debt that we had no reasonable way of paying off. Because of that situation, I lived with a lot of stress and developed some stress related illnesses. I was looking for away out when I met a man named David Cota. I'd always had the dream of opening my own retreat facility. He made himself out as a wealthy entrepreneur, eager to help me with my dream. I took some extraordinary risks to make that happen but the deal ultimately didn't go through. That plunged us into more debt - debt I'm still paying off. Somewhere during that time (2020-2021) Lynda met someone and had an affair. She gaslighted me through the whole experience. I knew something was amiss, and I was trying to repair the marriage, but she just strung me along until she was able to make the jump to this other guy. The guy who is now her boyfriend is wealthy. The affair was devastating. I've never experienced betrayal trauma like that. I got so sick that I got down to 112 pounds. My normal weight is 135. I got a flu in January 2022 that nearly killed me. It's been a long road back. Lots of introspection, shadow work, and diving deep into my spiritual practice. Fast forward to June of this year, Lynda moved to Alaska with her boyfriend, leaving me to parent Alana full-time during the school year. Deep down there's still anger over the choices Lynda has made and how it's affected me and Alana. But I'm more angry about how it's affected Alana. For me, I can gain perspective and see this as a heroes journey, a developmental task that I asked for before this incarnation. So that's how I'm handling it, as a spiritual challenge. I tell myself, "I'm the one." That simple phrase keeps me from kvetching and complaining and focuses me forward on doing what's right and turning this difficulty into something beautiful.

Strong emotions open my awareness. Quite the opposite of fixating me and losing myself, I become more aware. My awareness includes awareness of my surroundings, my body sensations, and my mental activity. I'm aware that I'm aware. And I breathe, and I feel, and I let things flow. In that state, wise actions, the next right thing, a better way to handle things, usually arises for me. I trust the Universe has my back.

Money is a symbol. Money is energy. Money is a projection. Money is a means by which we transact. Money is an image. Money is an aspiration. The quest for it can bind someone to Samsara. Money unites, money divides. Money builds, and it destroys. It's like the energy of the sun. We need it to survive, but too much can cause cancer.

I'm a content creator. There isn't a day that goes by that I'm not making something beautiful, good, and true for the purpose of helping others and the world. I'm a health and wellness artist.

Consciousness is the ground of all being. Information is the only thing that truly exists, if you can call it existing. I have no way of explaining the evanescent and ineffable Universe or life that lives in it. Life is The LIFE, All that is, consciousness. "I" exists as a perspective. As do we all. A person is a perspective.

What gives my life meaning is this drive to wake up and become a better version of myself. I want to turn everything I learn that helps me overcome my challenges into content that helps others. That feels like a good life to me.
"""

print("="*80)
print("TESTING ALL MODULES ON MARK'S ACTUAL SA360 RESPONSES")
print("="*80)

# Run all analyses
print("\n🎯 Stage Classification...")
stage = analyze_stage(MARK_TEXT)

print("🧠 Awareness Quotient...")
aq = analyze_aq(MARK_TEXT)

print("⚖️  Hemispheric Bias...")
hemispheric = analyze_hemispheric(MARK_TEXT)

print("⚡ Power Centers (8-center model)...")
power = analyze_power(MARK_TEXT)

# Build complete report
report = {
    "subject": "Mark Pirtle (SA360 Creator)",
    "stage_diagnosis": stage,
    "awareness_quotient": aq,
    "hemispheric_bias": hemispheric,
    "power_centers": power
}

# Save
with open('mark_complete_analysis.json', 'w') as f:
    json.dump(report, f, indent=2)

# Display summary
print("\n" + "="*80)
print("📊 MARK'S COMPLETE PROFILE")
print("="*80)

print(f"\n🎯 STAGE: {stage['stage_label']}")
print(f"   Score: {stage['stage_score']:.1f}")
print(f"   Confidence: {stage['confidence']:.2f}")

print(f"\n🧠 AWARENESS QUOTIENT: {aq['awareness_score']:.1f}")
print(f"   Category: {aq['awareness_label']}")
print(f"   Balance: {aq['balance_index']:.1f}")

print(f"\n⚖️  HEMISPHERIC: {hemispheric['dominant_hemisphere']}")
print(f"   Score: {hemispheric['hemispheric_score']:.1f}")
print(f"   Confidence: {hemispheric['confidence']:.2f}")

print(f"\n⚡ POWER CENTERS (8-CENTER MODEL):")
for center, score in power['power_profile'].items():
    bar = "█" * int(score) + "░" * (10 - int(score))
    print(f"   {center:20} {bar} {score:4.1f}/10")

print(f"\n   Dominant: {power['dominant_center']}")
print(f"   Balance: {power['balance_index']:.1f}")

print(f"\n💾 Full analysis saved to: mark_complete_analysis.json")
print("="*80)