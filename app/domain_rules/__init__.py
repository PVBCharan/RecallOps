"""Domain rules and guardrails for RecallOps."""

DOMAIN_CONFIG = {
    "commercial_operations": {
        "label": "Commercial Operations",
        "icon": "⚙️",
        "color": "#6366f1",
        "description": "Incident response, troubleshooting, and operational knowledge.",
        "guardrails": (
            "- Treat all recommendations as advisory.\n"
            "- Require authorization before changing production systems or equipment.\n"
            "- Do not automatically execute remediation actions.\n"
            "- Log all recommended actions for traceability."
        ),
        "fields": {
            "symptoms_label": "Observed Symptoms / Error Messages",
            "action_label": "Actions Already Taken",
            "outcome_label": "Known Outcome",
        },
        "example": {
            "title": "Database connection timeout in payment service",
            "description": (
                "The payment processing service started returning HTTP 503 errors "
                "at 14:30 UTC. Connection pool metrics show all 50 connections "
                "are in use. Application logs show 'Connection timeout after 30s' "
                "messages."
            ),
            "symptoms": "503 errors, connection pool exhaustion, 30s timeouts",
            "action_taken": "Restarted the payment service container",
            "outcome": "Service recovered temporarily but issue recurred after 2 hours",
        },
    },
    "healthcare": {
        "label": "Healthcare",
        "icon": "🏥",
        "color": "#22d3ee",
        "description": "Longitudinal patient information and supervised clinical decision support.",
        "guardrails": (
            "- This system is NOT a diagnostic tool and must NOT prescribe treatment.\n"
            "- Use synthetic data for demonstrations.\n"
            "- Keep recommendations limited to information organization and "
            "supervised decision support.\n"
            "- All output requires review by a qualified healthcare professional.\n"
            "- Do NOT present AI-generated observations as clinical findings."
        ),
        "fields": {
            "symptoms_label": "Reported Symptoms / Measurements",
            "action_label": "Current Treatment / Interventions",
            "outcome_label": "Observed Response",
        },
        "example": {
            "title": "Synthetic patient — elevated blood glucose trend",
            "description": (
                "Synthetic patient case: 55-year-old presenting with fasting "
                "blood glucose readings trending upward over 6 months. "
                "HbA1c measurements and dietary logs available as CSV."
            ),
            "symptoms": "Fasting glucose: 110→145 mg/dL over 6 months, fatigue reported",
            "action_taken": "Dietary modification recommended at month 2",
            "outcome": "Partial improvement in month 3, then resumed upward trend",
        },
    },
    "defence": {
        "label": "Defence",
        "icon": "🛡️",
        "color": "#f59e0b",
        "description": "Equipment maintenance and approved procedural support.",
        "guardrails": (
            "- Limited to maintenance and support scenarios only.\n"
            "- Must NOT support autonomous weapons, targeting, or combat decisions.\n"
            "- Require authorized human review before any maintenance action.\n"
            "- Use synthetic maintenance scenarios and approved procedural information.\n"
            "- All recommendations are advisory and require chain-of-command approval."
        ),
        "fields": {
            "symptoms_label": "Equipment Condition / Inspection Findings",
            "action_label": "Maintenance Actions Performed",
            "outcome_label": "Post-Maintenance Status",
        },
        "example": {
            "title": "Synthetic — Generator vibration anomaly",
            "description": (
                "Synthetic scenario: Routine inspection of backup generator unit "
                "BG-04 detected unusual vibration patterns. Sensor CSV data shows "
                "vibration amplitude exceeding baseline by 40%."
            ),
            "symptoms": "Elevated vibration at 120 Hz, mild oil temperature increase",
            "action_taken": "Visual inspection completed, no visible damage",
            "outcome": "Awaiting further analysis and maintenance scheduling",
        },
    },
    "education": {
        "label": "Education",
        "icon": "📚",
        "color": "#10b981",
        "description": "Personalized learning support and misconception tracking.",
        "guardrails": (
            "- Treat learning assessments as estimates based on observed work.\n"
            "- Do NOT equate a single correct answer with durable understanding.\n"
            "- Allow users to correct inaccurate records of their learning history.\n"
            "- Base progress tracking on demonstrated evidence, not passive viewing.\n"
            "- Suggestions should encourage learning, not discourage."
        ),
        "fields": {
            "symptoms_label": "Learning Difficulty / Misconceptions Observed",
            "action_label": "Study Activities / Exercises Tried",
            "outcome_label": "Assessment Results",
        },
        "example": {
            "title": "Python recursion misconception — stack overflow confusion",
            "description": (
                "Student submitted a recursive fibonacci implementation that "
                "causes a RecursionError. Their explanation shows confusion between "
                "the call stack and an explicit stack data structure."
            ),
            "symptoms": "RecursionError, confuses call stack with stack data structure",
            "action_taken": "Reviewed Python recursion tutorial, attempted exercise",
            "outcome": "Second attempt still missing base case",
        },
    },
}


def get_domains() -> dict:
    return DOMAIN_CONFIG


def get_domain_config(domain_key: str) -> dict | None:
    return DOMAIN_CONFIG.get(domain_key)


def get_domain_guardrails(domain_key: str) -> str:
    config = DOMAIN_CONFIG.get(domain_key)
    if config:
        return config["guardrails"]
    return "Treat all recommendations as advisory. Require human review."
