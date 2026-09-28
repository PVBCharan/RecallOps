"""Hindsight memory service — interface for experience storage and retrieval.

Hindsight is the primary memory layer. This module wraps its API.
When Hindsight is unavailable, falls back to local SQLite keyword search.
"""

import requests
from flask import current_app
from app.services.database import (
    save_experience,
    search_experiences_by_text,
    list_experiences,
)


HINDSIGHT_BASE = "http://localhost:8333"  # Default Hindsight endpoint


def check_hindsight() -> dict:
    """Check if the Hindsight service is reachable."""
    try:
        resp = requests.get(f"{HINDSIGHT_BASE}/health", timeout=3)
        if resp.status_code == 200:
            return {"available": True}
        return {"available": False, "error": f"HTTP {resp.status_code}"}
    except requests.ConnectionError:
        return {"available": False, "error": "Cannot reach Hindsight service"}
    except Exception as e:
        return {"available": False, "error": str(e)}


def store_experience(db_path: str, *, case_id: str, domain: str,
                     context: str, observations: list | None = None,
                     action_taken: str = "",
                     outcome_status: str = "unverified",
                     outcome_notes: str = "",
                     conditions: list | None = None,
                     limitations: list | None = None) -> dict:
    """Store an experience — locally and in Hindsight if available."""
    # Build embedding text for search
    obs_text = " ".join(
        o.get("observation", "") if isinstance(o, dict) else str(o)
        for o in (observations or [])
    )
    embedding_text = f"{context} {obs_text} {action_taken} {outcome_notes}"

    # Always save locally
    experience = save_experience(
        db_path,
        case_id=case_id,
        domain=domain,
        context=context,
        observations=observations,
        action_taken=action_taken,
        outcome_status=outcome_status,
        outcome_notes=outcome_notes,
        conditions=conditions,
        limitations=limitations,
        embedding_text=embedding_text,
    )

    # Try Hindsight
    hindsight_status = check_hindsight()
    if hindsight_status["available"]:
        try:
            payload = {
                "content": embedding_text,
                "metadata": {
                    "case_id": case_id,
                    "domain": domain,
                    "outcome_status": outcome_status,
                    "experience_id": experience["id"],
                },
            }
            resp = requests.post(
                f"{HINDSIGHT_BASE}/memories",
                json=payload,
                timeout=10,
            )
            experience["hindsight_stored"] = resp.status_code == 200
        except Exception:
            experience["hindsight_stored"] = False
    else:
        experience["hindsight_stored"] = False

    return experience


def retrieve_similar(db_path: str, query: str,
                     domain: str | None = None,
                     limit: int = 5) -> list[dict]:
    """Retrieve similar past experiences — from Hindsight or local fallback."""
    # Try Hindsight first
    hindsight_status = check_hindsight()
    if hindsight_status["available"]:
        try:
            params = {"query": query, "limit": limit}
            if domain:
                params["domain"] = domain
            resp = requests.get(
                f"{HINDSIGHT_BASE}/memories/search",
                params=params,
                timeout=10,
            )
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    return results
        except Exception:
            pass

    # Fallback: local keyword search
    return search_experiences_by_text(db_path, query, domain=domain, limit=limit)
