
---

```markdown
# 🧠 SAAQ Backend — Hemispheric Bias & Power Centers Modules

These two self-contained psychometric modules extend the **SAAQ (Self-Awareness Assessment & Quotient)** framework by analyzing reflective writing for cognitive–emotional balance and energetic focus.

Both modules run entirely **offline**, require **no APIs or external libraries**, and use deterministic, explainable logic based on linguistic and keyword scoring.

---

## 📁 Project Structure

```

backend/  
├── hemisphere_bias.py - Core logic for left/right hemispheric balance detection  
├── test_hemisphere_bias.py - Local test suite for Hemispheric Bias Analyzer  
├── power_centers.py - Core logic for Power Centers Profiler (5-center model)  
├── test_power_centers.py - Local test suite for Power Centers Profiler  
└── README.md - Documentation and usage guide

```

---

## ⚙️ Setup Instructions

1. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
```

2. **Install dependencies**  
    _(All are standard Python libraries — no external installs required)_
    
    ```bash
    pip install -r requirements.txt   # optional
    ```
    
3. **Run tests**
    
    ```bash
    python3 test_hemisphere_bias.py
    python3 test_power_centers.py
    ```
    

---

## Module 1 — Hemispheric Bias Analyzer

### Purpose

Analyzes text to estimate **left-brain vs. right-brain bias**, detecting linguistic signals of analytic reasoning versus intuitive creativity.

### Output Example

```json
{
  "hemispheric_score": 63.2,
  "dominant_hemisphere": "Right",
  "confidence": 0.82,
  "indicators": {
    "Analytic Thinking": 4,
    "Sequential Logic": 2,
    "Language Structure": 3,
    "Emotional Imagery": 9,
    "Creative Association": 8,
    "Spatial/Intuitive Reasoning": 7
  },
  "interpretive_summary": "Right-hemisphere bias with high emotional and creative association, moderate logical grounding."
}
```

### How It Works

- Scans text using **regex-based keyword and style analysis**
    
- Groups linguistic cues into six sub-indicators:
    
    - **Left Hemisphere:** Analytic Thinking, Sequential Logic, Language Structure
        
    - **Right Hemisphere:** Emotional Imagery, Creative Association, Spatial/Intuitive Reasoning
        
- Computes a **−100 → +100 score**:
    
    - Negative = left-leaning (logical, structured)
        
    - Positive = right-leaning (emotional, creative)
        
- Includes **confidence (0–1)** and an interpretive summary.
    

### Design Highlights

- Pure Python (`re`, `json`, `math`)
    
- Fully deterministic and reproducible
    
- Uses sentence structure and stylistic patterns for subtle cues
    
- Built for reflective writing and cognitive–emotional profiling
    

---

##  Module 1 Tests — `test_hemisphere_bias.py`

### Includes

- 12 diverse cases:
    
    - Logical, emotional, artistic, balanced, nonsense, and empty
        
- Pretty-printed JSON output
    
- Bias classification summaries for each
    

### Run

```bash
python3 test_hemisphere_bias.py
```

---

##  Module 2 — Power Centers Profiler

### Purpose

Analyzes text for energetic and psychological “power centers” —  
the five main channels through which awareness expresses itself:

1. **Cognitive** — reasoning, logic, analysis
    
2. **Emotional** — feeling, empathy, mood
    
3. **Relational** — connectedness, “we/us” language
    
4. **Somatic** — body, movement, sensation
    
5. **Spiritual** — meaning, transcendence, unity
    

### Output Example

```json
{
  "power_profile": {
    "Cognitive": 8.5,
    "Emotional": 7.2,
    "Relational": 5.8,
    "Somatic": 3.0,
    "Spiritual": 6.9
  },
  "dominant_center": "Cognitive",
  "balance_index": 78.3,
  "interpretive_summary": "Dominant cognitive energy with emotional and spiritual resonance; grounded but slightly low in embodiment."
}
```

### How It Works

- Searches text for keyword patterns linked to each center
    
- Converts raw matches to a **0–10 scale** (adjusted for text length)
    
- Identifies the **dominant center** (highest score)
    
- Calculates a **balance index (0–100)** measuring overall energetic harmony
    
- Returns a clear, human-readable summary
    

### Why Only 5 Centers?

While the theoretical model includes **8 total centers** (Cognitive, Emotional, Relational, Somatic, Spiritual, Creative, Willpower, Integrative),  
this version uses **5** because they are:

- **Most visible** in natural language
    
- **Simpler and more reliable** to detect
    
- **Sufficient** for written self-reflection analysis
    

The remaining three (Creative, Willpower, Integrative) rely on tone and meta-awareness that require more advanced modeling.

---

##  Module 2 Tests — `test_power_centers.py`

### Includes

- 10 test sentences:
    
    - One for each of the five centers
        
    - Three blended examples
        
    - One neutral and one nonsense input
        
- Prints formatted JSON and summary line per test
    

### Run

```bash
python3 test_power_centers.py
```

---

## 🔬 Technical Summary

|Attribute|Hemispheric Bias|Power Centers|
|---|---|---|
|**Analysis Type**|Left/Right hemispheric language|5-dimensional energy mapping|
|**Core Method**|Weighted keyword + linguistic cues|Regex keyword frequency & normalization|
|**Output Format**|JSON|JSON|
|**Scales**|−100 → +100|0 → 10 per center|
|**Balance Metric**|Confidence (0–1)|Balance Index (0–100)|
|**Libraries**|`re`, `json`, `math`|`re`, `json`, `math`|
|**Offline Operation**|✅|✅|
|**Deterministic Output**|✅|✅|

---

## 🧩 Interpretation Guidelines

|Metric|Meaning|
|---|---|
|**Hemispheric Score**|Negative = Left (analytic), Positive = Right (intuitive)|
|**Dominant Hemisphere**|Side showing strongest linguistic bias|
|**Confidence**|How strongly the text leans one way|
|**Power Profile (0–10)**|Strength of each energy type|
|**Dominant Center**|Main energetic mode expressed|
|**Balance Index (0–100)**|How evenly distributed the energies are|
|**Interpretive Summary**|Short narrative of findings|

---

## 💡 Conceptual Background

These modules derive from the **SAAQ (Self-Awareness Assessment & Quotient)** framework, which blends:

- **Cognitive science:** left/right hemisphere specialization
    
- **Psychodynamics:** emotional and somatic awareness
    
- **Developmental psychology:** balance across awareness dimensions
    
- **Linguistic analysis:** meaning extraction through word and style patterns
    

They are **reflective tools**, not diagnostic instruments — meant for self-analysis, coaching, and research on awareness dynamics.

---

## 🧱 Design Goals

- Fully **offline** and **deterministic**
    
- **Explainable logic** (no black-box AI)
    
- **JSON output** for dashboards or integration
    
- **Modular functions** for easy upgrades
    

---

## 🔮 Future Extensions

|Planned Module|Purpose|
|---|---|
|**Creative Center**|Detect artistic and imaginative expression|
|**Willpower Center**|Detect intent, focus, and commitment language|
|**Integrative Center**|Capture meta-awareness and synthesis|
|**Unified Meta-Assessment API**|Combine all SAAQ analyzers|
|**Visualization Dashboard**|Plot hemispheric and energetic maps dynamically|

---

## 👤 Author

Developed by **Advik Bargoti**  
University of Arizona — Computational Psychology Research Track  
AI–Psychology Integration Project (SAAQ Framework)

---

## 🧰 Requirements

```
Python 3.10+
Standard libraries:
- re
- json
- math
```


