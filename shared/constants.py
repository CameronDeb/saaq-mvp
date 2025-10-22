"""
Shared constants for SAAQ system.
Based on reference documentation and Mark's reports.
"""

# Developmental Stages (S1-S10)
STAGES = {
    "S1": "Impulsive Self",
    "S2": "Boundary-Tester",
    "S3": "Tribal Belonger",
    "S4": "Conscientious Role Self",
    "S5": "Methodic Expert",
    "S6": "Outcome Achiever",
    "S7": "Relational Pluralist",
    "S8": "Authoring Strategist",
    "S9": "Aware Integrator",
    "S10": "Meta-Builder"
}

# Power Centers (8)
POWER_CENTERS = [
    "Vital",
    "Emotional",
    "Relational",
    "Social/Leadership",
    "Financial",
    "Creative",
    "Intellectual",
    "Spiritual"
]

# Core Aptitudes (6)
APTITUDES = [
    "Autonomy/Influence",
    "Drive",
    "Perseverance",
    "Achievement",
    "Alignment",
    "Restraint"
]

# Shadow Loops (4)
SHADOW_LOOPS = [
    "control_reflex",
    "quick_relief",
    "lone_rescuer",
    "satisficer_risk"
]

# Hemispheric Bias Options
HEMISPHERIC_TILTS = ["left", "right", "integrated"]

# Assessment Status Levels
STATUS_LEVELS = [
    "Low", "Med", "High",
    "Strong", "Emerging", "Mixed",
    "Leaking", "Stable", "Healthy",
    "Strained", "Volatile", "Fragile"
]

# QA Rubric Categories (12 total - must all pass)
QA_CATEGORIES = [
    "Framing Section",
    "Developmental Stage Estimate",
    "Hemispheric Bias",
    "Power Center Analysis",
    "Power Center KPIs",
    "Core Aptitudes",
    "Shadow Indicators",
    "Somatic Signature Panel",
    "Awareness Quotient Summary",
    "90-Day Practice Plan",
    "Therapist Handoff Page",
    "Appendix (S1-S10)"
]

# Learning Modes (O'Fallon's STAGES framework)
LEARNING_MODES = [
    "receptive",
    "active",
    "reciprocal",
    "interpenetrative"
]