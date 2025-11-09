#!/usr/bin/env python3
"""
Local test harness for stage_classifier.py
------------------------------------------
Runs many diverse text samples directly through _score_text()
without using FastAPI or any HTTP calls.
"""

from stage_classifier import _score_text
import json
import time

# Diverse test cases (edge cases + typical responses)
TEST_CASES = {
    # 1️⃣ Empty and minimal
    "Empty string": "",
    "Whitespace only": "   ",
    "Only punctuation": "!!! ??? ...",
    "Single word": "Okay.",
    "Emojis": "😔😤🔥",

    # 2️⃣ Early stage (S1–S2)
    "Reactive anger": "I get angry when things go wrong and I yell immediately.",
    "Victim mindset": "Nothing ever works out for me; people always take advantage.",
    "Control seeking": "If things aren’t my way, I feel lost and frustrated.",

    # 3️⃣ Mid stage (S3–S6)
    "Compliance": "I follow what my supervisor expects and meet the deadlines.",
    "Checklist thinker": "When something fails, we review the process and fix it next time.",
    "Self-regulation": "I pause before reacting and think through how to respond logically.",
    "Outcome focused": "I optimize systems and measure results to refine execution.",
    "Systems lens": "I notice how structures influence recurring behaviors.",

    # 4️⃣ High stage (S7–S10)
    "Paradoxical unity": "I see contradictions as natural parts of a deeper pattern.",
    "Meta-systems": "I explore how systems evolve and self-correct through tension.",
    "Complex integration": "I hold multiple truths and adapt frameworks dynamically.",

    # 5️⃣ Weird edge cases
    "Sarcasm": "Oh sure, I'm totally enlightened when I spill my coffee.",
    "Nonsense": "Bananas swim faster than my feelings under red umbrellas.",
    "HTML noise": "<p>I try to improve myself</p><script>alert('x')</script>",
    "Mixed languages": "I reflect y también analizo los patrones del sistema.",
    "Profanity": "I mess things up and feel like ****, but try to analyze why.",
    "Repetition flood": "system " * 200 + " perspective " * 200 + " plan " * 200,
}

# ---------------------- Runner ----------------------

def run_tests():
    print(f"Running {len(TEST_CASES)} local tests...\n")
    results = []
    for name, text in TEST_CASES.items():
        t0 = time.perf_counter()
        try:
            result = _score_text(text)
        except Exception as e:
            result = {"error": str(e)}
        elapsed = (time.perf_counter() - t0) * 1000
        results.append({
            "case": name,
            "latency_ms": round(elapsed, 2),
            "result": result,
        })
        print(f"--- {name} --- ({elapsed:.1f} ms)")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print()
    return results

if __name__ == "__main__":
    all_results = run_tests()
    # Optional: write results to file for record
    with open("local_stage_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("✅ All tests complete. Results saved to local_stage_results.json")

