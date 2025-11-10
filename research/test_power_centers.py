#!/usr/bin/env python3
"""
test_power_centers.py

Behavioral and validation tests for power_centers.py

Covers:
- Each of the five power centers (Cognitive, Emotional, Relational, Somatic, Spiritual)
- Blended examples combining multiple centers
- Neutral and nonsense edge cases

Run:
    python3 test_power_centers.py
"""

import json
from power_centers import analyze_text

# -------------------------------------------------
# Test cases
# -------------------------------------------------

TEST_CASES = [
    # 1: Cognitive — reasoning, logic, analysis
    "I think carefully before deciding, analyzing each factor to understand the logical consequences.",
    
    # 2: Emotional — feeling, empathy, affective tone
    "I feel deeply moved by the sadness in her voice and the warmth in her heart.",
    
    # 3: Relational — social, connection, community
    "We share stories together, supporting each other as friends through every challenge.",
    
    # 4: Somatic — body, tension, sensation
    "My shoulders tighten as I breathe; I sense the pulse of my heartbeat through my hands.",
    
    # 5: Spiritual — meaning, transcendence, purpose
    "I meditate on the purpose of my life, feeling one with the universe and grateful for divine presence.",
    
    # 6: Blended — cognitive + emotional
    "I think with my heart, balancing reason with compassion to understand others more clearly.",
    
    # 7: Blended — somatic + spiritual + relational
    "Together we breathe in harmony, grounded in the body yet open to the sacred rhythm of life.",
    
    # 8: Highly cognitive technical tone
    "This theoretical model provides a logical framework for understanding abstract principles of computation.",
    
    # 9: Neutral everyday statement (low signal)
    "The day was fine and I walked to class without much thought.",
    
    # 10: Nonsense / symbols (edge case)
    "@#$% 12345 !!! ???"
]

# -------------------------------------------------
# Runner
# -------------------------------------------------

def run_tests():
    print("\n=== Power Centers Profiler Test ===\n")
    for i, text in enumerate(TEST_CASES, 1):
        print(f"Test {i}: {text[:60]}{'...' if len(text) > 60 else ''}")
        result = analyze_text(text)
        print(json.dumps(result, indent=2))
        print(f"→ Dominant Center: {result['dominant_center']} (Balance Index: {result['balance_index']})")
        print("-" * 70)
    print("\nAll tests complete.\n")

if __name__ == "__main__":
    run_tests()

