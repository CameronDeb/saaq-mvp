from awareness_quotient import _score_awareness
import json, time

tests = {
    "Reactive / Low Awareness": "I just react when things go wrong and blame others immediately.",
    "Basic Self-Awareness": "I notice when I get frustrated and try to calm myself before responding.",
    "Perspective Awareness": "I understand that others may see the situation differently than I do.",
    "Meta-Awareness": "I realized that my assumptions might be shaping how I interpret this issue.",
    "Systemic Awareness": "I see how patterns in our workflow create repeated bottlenecks over time.",
    "Integrative Awareness": "I try to balance structure and flexibility, knowing both are valuable in different contexts.",
    "Deep Reflective Awareness": "I question my thoughts and emotions, integrating feedback from others to evolve my perspective.",
    "Holistic Awareness": "I notice my reactions, understand others' views, and see how interconnected systems create outcomes we all influence.",
    "Transcendent Awareness": "I hold paradoxes without judgment, integrating complexity while staying grounded in compassion and clarity.",
}

print("Running Awareness Quotient Tests...\n")

results = []
start = time.time()

for label, text in tests.items():
    start_time = time.time()
    result = _score_awareness(text)
    elapsed = (time.time() - start_time) * 1000
    print(f"--- {label} --- ({elapsed:.1f} ms)")
    print(json.dumps(result, indent=2))
    print()

    results.append({
        "label": label,
        "score": result["awareness_score"],
        "category": result["awareness_label"]
    })

print("✅ All tests complete.")
print(f"Total runtime: {(time.time() - start):.2f}s")
print("\nSummary:")
for r in results:
    print(f"{r['label']}: {r['score']:.2f} → {r['category']}")

