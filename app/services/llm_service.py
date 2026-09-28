"""LLM service — communicates with Ollama for local inference."""

import json
import requests
from flask import current_app


def _ollama_url() -> str:
    return current_app.config.get("OLLAMA_BASE_URL", "http://localhost:11434")


def _model() -> str:
    return current_app.config.get("OLLAMA_MODEL", "llama3.2")


def _vision_model() -> str:
    return current_app.config.get("OLLAMA_VISION_MODEL", "llava")


def check_ollama() -> dict:
    """Check if Ollama is reachable and return available models."""
    try:
        resp = requests.get(f"{_ollama_url()}/api/tags", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            models = [m["name"] for m in data.get("models", [])]
            return {"available": True, "models": models}
        return {"available": False, "models": [], "error": f"HTTP {resp.status_code}"}
    except requests.ConnectionError:
        return {"available": False, "models": [], "error": "Cannot reach Ollama"}
    except Exception as e:
        return {"available": False, "models": [], "error": str(e)}


def generate(prompt: str, system: str = "", temperature: float = 0.3) -> str:
    """Generate a text response from the local LLM."""
    payload = {
        "model": _model(),
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if system:
        payload["system"] = system

    try:
        resp = requests.post(
            f"{_ollama_url()}/api/generate",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.ConnectionError:
        return _fallback_generate(prompt, system)
    except Exception as e:
        return f"[LLM Error] {e}"


def generate_with_image(prompt: str, image_base64: str,
                        system: str = "") -> str:
    """Generate a response using a vision model and a base64-encoded image."""
    payload = {
        "model": _vision_model(),
        "prompt": prompt,
        "images": [image_base64],
        "stream": False,
        "options": {"temperature": 0.3},
    }
    if system:
        payload["system"] = system

    try:
        resp = requests.post(
            f"{_ollama_url()}/api/generate",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.ConnectionError:
        return "[Vision model unavailable] Ollama is not running. Please start Ollama to enable image analysis."
    except Exception as e:
        return f"[Vision Error] {e}"


def generate_structured(prompt: str, system: str = "") -> dict:
    """Generate and attempt to parse as JSON."""
    raw = generate(prompt, system=system)
    # Try to extract JSON from the response
    try:
        # Handle ```json ... ``` blocks
        if "```json" in raw:
            start = raw.index("```json") + 7
            end = raw.index("```", start)
            raw = raw[start:end].strip()
        elif "```" in raw:
            start = raw.index("```") + 3
            end = raw.index("```", start)
            raw = raw[start:end].strip()
        return json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return {"raw_response": raw}


def _fallback_generate(prompt: str, system: str = "") -> str:
    """Provide a rule-based fallback when Ollama is unavailable.
    This lets the app demo core workflow without a running LLM."""
    lines = prompt.lower()

    if "synthesize" in lines or "evidence summary" in lines:
        return (
            "**Evidence Summary (Generated without LLM)**\n\n"
            "The case contains the user-provided description and any uploaded "
            "evidence. Since the local LLM (Ollama) is not available, this is a "
            "structured passthrough of the submitted information.\n\n"
            "- Review the description and attached evidence manually.\n"
            "- Start Ollama for AI-powered synthesis."
        )

    if "recommend" in lines:
        return (
            "**Recommendation (Generated without LLM)**\n\n"
            "Without a running local LLM, RecallOps cannot generate AI-powered "
            "recommendations. However, the system has retrieved any relevant past "
            "experiences for your review.\n\n"
            "**Suggested next step:** Review the past experiences listed below "
            "and apply your professional judgment.\n\n"
            "**Uncertainty:** High — this is a template response, not an AI analysis.\n\n"
            "*Start Ollama to enable full recommendation generation.*"
        )

    return (
        "[Ollama unavailable] The local LLM is not running. "
        "Start Ollama (`ollama serve`) to enable AI-powered features. "
        "Core case management and evidence storage still work without it."
    )
