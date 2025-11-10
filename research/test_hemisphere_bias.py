#!/usr/bin/env python3
"""
test_hemisphere_bias.py

Unit and behavior tests for hemisphere_bias.py

Covers a range of linguistic styles:
- Strongly logical / analytical (Left)
- Highly emotional / creative (Right)
- Balanced / mixed
- Nonsense or empty input (Edge cases)

Run:
    python3 test_hemisphere_bias.py
"""

import json
from hemisphere_bias import analyze_text

# --------------------------
# Test samples
# --------------------------

TEST_CASES = [
    # 1: Strongly logical and structured
    "Based on the available data, we can calculate the optimal value through sequential reasoning and verified results.",
    
    # 2: Highly emotional and metaphorical
    "My heart trembles like a leaf in the wind; I feel colors swirling through my dreams.",
    
    # 3: Mixed analytical + intuitive
    "I imagine the solution, then verify it with clear logic and measurable outcomes.",
    
    # 4: Balanced tone
    "Sometimes I think carefully, other times I just go with my gut.",
    
    # 5: Pure nonsense (should default low confidence)
    "1234567890 !@#$%^&*()",
    
    # 6: Empty input
    "",
    
    # 7: Creative artistic language
    "The canvas hums with color and light, whispering secrets through imagination.",
    
    # 8: Technical procedural description
    "First, initialize the array; then calculate each iteration precisely and output the final mean.",
    
    # 9: Reflective spiritual tone (should lean right due to metaphor and emotion)
    "I feel connected to the universe, sensing patterns beyond words or logic.",
    
    # 10: Overly rigid logic and data references
    "Logical operators must follow strict precedence; therefore, each subexpression must be evaluated systematically.",
    
    # 11: Colloquial emotional storytelling
    "It felt like my soul was painting memories in the rain.",
    
    # 12: Random sentence mix (neutral)
    "The book was interesting, and the sunset was nice."
]

# --------------------------
# Run tests
# --------------------------

def run_tests():
    print("\n=== Hemispheric Bias Analyzer Test ===\n")
    for i, text in enumerate(TEST_CASES, 1):
        print(f"Test {i}: {text[:60]}{'...' if len(text) > 60 else ''}")
        result = analyze_text(text)
        print(json.dumps(result, indent=2))
        print(f"→ Dominant Hemisphere: {result['dominant_hemisphere']} (Score: {result['hemispheric_score']}, Confidence: {result['confidence']})")
        print("-" * 70)
    print("\nAll tests complete.\n")

if __name__ == "__main__":
    run_tests()

