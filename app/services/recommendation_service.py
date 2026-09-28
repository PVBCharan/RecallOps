"""Recommendation engine — synthesizes evidence and generates recommendations."""

from flask import current_app
from app.services.llm_service import generate
from app.services.hindsight_service import retrieve_similar, store_experience
from app.services.database import (
    get_case,
    get_evidence_for_case,
    get_feedback_for_case,
    add_recommendation,
)
from app.domain_rules import get_domain_guardrails


def synthesize_evidence(db_path: str, case_id: str) -> str:
    """Combine case info and evidence into a structured summary."""
    case = get_case(db_path, case_id)
    if not case:
        return "Case not found."

    evidence_list = get_evidence_for_case(db_path, case_id)

    parts = [
        f"## Case: {case['title']}",
        f"**Domain:** {case['domain']}",
        f"**Description:** {case['description']}",
    ]
    if case.get("symptoms"):
        parts.append(f"**Symptoms/Observations:** {case['symptoms']}")
    if case.get("action_taken"):
        parts.append(f"**Action Taken:** {case['action_taken']}")
    if case.get("outcome_text"):
        parts.append(f"**Known Outcome:** {case['outcome_text']}")

    if evidence_list:
        parts.append("\n### Attached Evidence")
        for ev in evidence_list:
            label = ev["evidence_type"].upper()
            parts.append(f"\n**[{label}] {ev.get('original_name', 'Evidence')}**")
            if ev.get("analysis"):
                parts.append(
                    f"*Analysis ({ev['verification']}):* {ev['analysis']}"
                )
            if ev.get("extracted_text"):
                parts.append(f"*Extracted text:* {ev['extracted_text']}")

    case_text = "\n".join(parts)

    # Use LLM to synthesize
    system = (
        "You are a structured evidence analyst for RecallOps. "
        "Synthesize the following case information into a clear, organized summary. "
        "Separate user-provided facts from machine-generated observations. "
        "Flag any conflicting information. "
        "Note what information is missing or uncertain."
    )
    prompt = f"Synthesize the following case evidence into a structured summary:\n\n{case_text}"
    synthesis = generate(prompt, system=system)
    return synthesis


def generate_recommendation(db_path: str, case_id: str) -> dict:
    """Generate a recommendation for the case using evidence + past experiences."""
    case = get_case(db_path, case_id)
    if not case:
        return {"error": "Case not found."}

    # 1. Gather evidence
    evidence_list = get_evidence_for_case(db_path, case_id)
    evidence_summary = synthesize_evidence(db_path, case_id)

    # 2. Retrieve similar past experiences
    search_query = f"{case['title']} {case['description']} {case.get('symptoms', '')}"
    similar = retrieve_similar(db_path, search_query, domain=case["domain"], limit=5)

    # 3. Build prior experience context
    prior_context = ""
    prior_ids = []
    if similar:
        prior_parts = []
        for i, exp in enumerate(similar, 1):
            exp_id = exp.get("id", exp.get("experience_id", "unknown"))
            prior_ids.append(exp_id)
            outcome = exp.get("outcome_status", "unverified")
            context = exp.get("context", exp.get("content", ""))
            action = exp.get("action_taken", "")
            notes = exp.get("outcome_notes", "")
            prior_parts.append(
                f"**Past Experience {i}** (Outcome: {outcome})\n"
                f"Context: {context}\n"
                f"Action: {action}\n"
                f"Notes: {notes}"
            )
        prior_context = "\n\n".join(prior_parts)

    # 4. Get domain guardrails
    guardrails = get_domain_guardrails(case["domain"])

    # 5. Build prompt
    system = (
        "You are RecallOps, an experience-aware AI decision support system. "
        "Generate a recommendation based on the current case evidence and "
        "relevant past experiences. Your response MUST include:\n"
        "1. **Suggested Next Steps** — concrete, actionable options\n"
        "2. **Reasoning** — plain-language explanation\n"
        "3. **Supporting Evidence** — what evidence backs this\n"
        "4. **Relevant Past Experiences** — outcomes of similar cases\n"
        "5. **Uncertainty & Missing Info** — what you don't know\n"
        "6. **Human Review Notice** — remind that this is advisory\n\n"
        f"Domain guardrails:\n{guardrails}\n\n"
        "IMPORTANT: Do NOT present uncertain information as fact. "
        "Distinguish verified outcomes from unverified ones."
    )

    prompt_parts = [
        "## Current Case Evidence Summary",
        evidence_summary,
    ]
    if prior_context:
        prompt_parts.extend([
            "\n## Relevant Past Experiences",
            prior_context,
        ])
    else:
        prompt_parts.append(
            "\nNo directly relevant past experiences were found."
        )
    prompt_parts.append(
        "\nBased on the above, generate a structured recommendation."
    )

    prompt = "\n\n".join(prompt_parts)
    recommendation_text = generate(prompt, system=system)

    # 6. Store the recommendation
    rec = add_recommendation(
        db_path,
        case_id=case_id,
        suggestion=recommendation_text,
        reasoning=evidence_summary,
        prior_cases=prior_ids,
        uncertainty="See recommendation details for uncertainty analysis.",
        evidence_used=[e["id"] for e in evidence_list],
    )

    # 7. Auto-save as experience for future retrieval
    observations = []
    for ev in evidence_list:
        observations.append({
            "observation": ev.get("analysis") or ev.get("extracted_text", ""),
            "source_type": ev["evidence_type"],
            "source_reference": ev.get("original_name", ""),
            "verification_status": ev.get("verification", "machine_extracted"),
        })

    store_experience(
        db_path,
        case_id=case_id,
        domain=case["domain"],
        context=f"{case['title']}: {case['description']}",
        observations=observations,
        action_taken=case.get("action_taken", ""),
        outcome_status="unverified",
        outcome_notes=case.get("outcome_text", ""),
        conditions=[case.get("symptoms", "")],
        limitations=["Automated analysis — requires human verification"],
    )

    return {
        "recommendation": rec,
        "evidence_summary": evidence_summary,
        "prior_experiences": similar,
        "prior_count": len(similar),
    }
