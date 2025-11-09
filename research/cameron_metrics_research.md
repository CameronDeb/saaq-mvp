\# Cameron's Metrics Research

\*\*Assignment:\*\* Core Aptitudes + Shadow Indicators + KPIs

\*\*Date:\*\* 11/9/25



---



\## Objectives



Extract quantitative metrics from user text responses for:



1\. \*\*Core Aptitudes (6 metrics)\*\*

&nbsp;  - Autonomy/Influence

&nbsp;  - Drive

&nbsp;  - Perseverance

&nbsp;  - Achievement

&nbsp;  - Alignment

&nbsp;  - Restraint



2\. \*\*Shadow Indicators\*\*

&nbsp;  - Trigger patterns (control reflex, quick relief, lone rescuer)

&nbsp;  - Root fears/shame detection

&nbsp;  - Emotional loops



3\. \*\*KPIs (Leadership Effectiveness)\*\*

&nbsp;  - Stress response patterns

&nbsp;  - Decision-making consistency

&nbsp;  - Values alignment under pressure



---



\## Approach: Emotion Clustering + Transformer Embeddings + Rule-Based Detection



\### Tools to Explore



1\. \*\*Transformer Embeddings\*\*

&nbsp;  - Sentence-Transformers (all-MiniLM-L6-v2)

&nbsp;  - OpenAI text-embedding-3-small

&nbsp;  - Use case: Semantic similarity to reference patterns



2\. \*\*Emotion Detection\*\*

&nbsp;  - Hugging Face: `j-hartmann/emotion-english-distilroberta-base`

&nbsp;  - Detects: joy, sadness, anger, fear, surprise, disgust, neutral

&nbsp;  - Use case: Shadow pattern detection, trigger identification



3\. \*\*Rule-Based Pattern Matching\*\*

&nbsp;  - Regex + keyword lexicons

&nbsp;  - Use case: Quick detection of known shadow loops



---



\## Phase 1: Core Aptitudes Scoring



\### Method: Semantic Similarity + Keyword Density



\*\*Example for "Drive" aptitude:\*\*



Reference patterns:

\- "I push myself to achieve goals"

\- "I'm motivated by results and outcomes"

\- "I set ambitious targets and work hard to hit them"



\*\*Algorithm:\*\*

1\. Embed user response using sentence-transformers

2\. Calculate cosine similarity to reference patterns

3\. Extract keyword density (achieve, goal, push, motivated)

4\. Combine: `score = (0.6 \* similarity) + (0.4 \* keyword\_density)`

5\. Output: 0-100 scale



\*\*Code Prototype:\*\*

```python

from sentence\_transformers import SentenceTransformer

from sklearn.metrics.pairwise import cosine\_similarity

import numpy as np



model = SentenceTransformer('all-MiniLM-L6-v2')



\# Reference patterns for "Drive"

drive\_patterns = \[

&nbsp;   "I push myself to achieve goals",

&nbsp;   "I'm motivated by results and outcomes",

&nbsp;   "I set ambitious targets and work hard to hit them"

]



\# User response

user\_text = "I always strive to meet my objectives and exceed expectations"



\# Embed

drive\_embeddings = model.encode(drive\_patterns)

user\_embedding = model.encode(\[user\_text])



\# Calculate similarity

similarities = cosine\_similarity(user\_embedding, drive\_embeddings)

max\_similarity = np.max(similarities)



\# Keyword density

drive\_keywords = \["achieve", "goal", "push", "motivated", "strive", "exceed"]

keyword\_count = sum(1 for kw in drive\_keywords if kw in user\_text.lower())

keyword\_density = min(keyword\_count / 3, 1.0)  # Normalize



\# Final score

drive\_score = (0.6 \* max\_similarity) + (0.4 \* keyword\_density)

drive\_score\_100 = int(drive\_score \* 100)



print(f"Drive Score: {drive\_score\_100}/100")

```



---



\## Phase 2: Shadow Indicators Detection



\### Method: Emotion Classification + Pattern Matching



\*\*Shadow Loops to Detect:\*\*

1\. \*\*Control Reflex\*\* - Fear of losing control

2\. \*\*Quick Relief\*\* - Avoidance through substances/distractions

3\. \*\*Lone Rescuer\*\* - "I must do it all myself"



\*\*Algorithm:\*\*

1\. Run emotion classification on responses

2\. Check for high fear/anger in stress-related questions (Q2, Q6)

3\. Look for avoidance keywords (numb, escape, alcohol, distract)

4\. Detect self-reliance patterns (alone, myself, can't trust)



\*\*Code Prototype:\*\*

```python

from transformers import pipeline



\# Load emotion classifier

emotion\_classifier = pipeline(

&nbsp;   "text-classification",

&nbsp;   model="j-hartmann/emotion-english-distilroberta-base",

&nbsp;   return\_all\_scores=True

)



\# User response to Q2 (stress/fear question)

stress\_response = "When I'm overwhelmed I tend to shut down and handle things alone"



\# Classify emotions

emotions = emotion\_classifier(stress\_response)\[0]

emotion\_dict = {e\['label']: e\['score'] for e in emotions}



\# Check for shadow patterns

control\_keywords = \["control", "manage", "grip", "maintain"]

avoidance\_keywords = \["numb", "escape", "drink", "distract", "avoid"]

lone\_rescuer\_keywords = \["alone", "myself", "can't trust", "do it all"]



has\_control = any(kw in stress\_response.lower() for kw in control\_keywords)

has\_avoidance = any(kw in stress\_response.lower() for kw in avoidance\_keywords)

has\_lone\_rescuer = any(kw in stress\_response.lower() for kw in lone\_rescuer\_keywords)



\# Combine with emotion scores

shadow\_score = {

&nbsp;   "control\_reflex": int((emotion\_dict\['fear'] + (1 if has\_control else 0)) \* 50),

&nbsp;   "quick\_relief": int((emotion\_dict\['sadness'] + (1 if has\_avoidance else 0)) \* 50),

&nbsp;   "lone\_rescuer": int((emotion\_dict\['anger'] + (1 if has\_lone\_rescuer else 0)) \* 50)

}



print("Shadow Indicators:", shadow\_score)

```



---



\## Phase 3: KPIs (Leadership Effectiveness)



\### Method: Cross-Question Analysis + Consistency Scoring



\*\*KPIs to Calculate:\*\*

1\. \*\*Stress Resilience\*\* - How well do they handle overwhelm?

2\. \*\*Values Consistency\*\* - Do actions align with stated values?

3\. \*\*Perspective Integration\*\* - Can they hold multiple viewpoints?



\*\*Algorithm:\*\*

1\. Compare Q5 (values tested) with Q6 (internal conflict)

2\. Check for consistency in word choice and themes

3\. Calculate "integration score" based on complexity of reasoning



\*\*Code Prototype:\*\*

```python

\# Compare responses for consistency

values\_response = "I believe in honesty and transparency above all"

conflict\_response = "I lied to protect someone's feelings"



\# Check for contradiction

values\_keywords = extract\_keywords(values\_response)

conflict\_keywords = extract\_keywords(conflict\_response)



\# Calculate overlap

overlap = len(set(values\_keywords) \& set(conflict\_keywords))

consistency\_score = overlap / max(len(values\_keywords), 1)



\# Integration complexity (measure sentence structure diversity)

from textstat import flesch\_reading\_ease



complexity = flesch\_reading\_ease(conflict\_response)

integration\_score = min(complexity / 100, 1.0)



print(f"Values Consistency: {int(consistency\_score \* 100)}/100")

print(f"Perspective Integration: {int(integration\_score \* 100)}/100")

```



---



\## Next Steps



1\. \*\*Install required libraries:\*\*

```bash

&nbsp;  pip install sentence-transformers transformers scikit-learn textstat

```



2\. \*\*Test prototypes on sample responses\*\*



3\. \*\*Refine scoring thresholds based on reference reports\*\*



4\. \*\*Document findings for team sync\*\*



---



\## Tools Summary



| Tool | Purpose | Use Case |

|------|---------|----------|

| Sentence-Transformers | Semantic similarity | Aptitude matching |

| Hugging Face Emotion | Emotion classification | Shadow detection |

| Regex + Keywords | Pattern matching | Quick loop detection |

| OpenAI Embeddings | Advanced similarity | Optional upgrade |

| TextStat | Readability metrics | Complexity analysis |



---



\## Questions for Team



\- Should we use OpenAI embeddings or open-source sentence-transformers?

\- What confidence threshold for shadow indicators? (>60%, >70%?)

\- How do we weight keyword matching vs semantic similarity?



---



\## References



\- SA360 sample reports (in `/docs/reference\_reports/`)

\- Hugging Face models: https://huggingface.co/models

\- Sentence-Transformers: https://www.sbert.net/

