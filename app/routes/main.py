"""Main routes — landing page, dashboard, system status."""

from flask import Blueprint, render_template, current_app
from app.services.database import list_cases, list_experiences
from app.services.llm_service import check_ollama
from app.services.hindsight_service import check_hindsight
from app.domain_rules import get_domains

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    domains = get_domains()
    cases = list_cases(current_app.config["DATABASE_PATH"])
    experiences = list_experiences(current_app.config["DATABASE_PATH"])

    stats = {
        "total_cases": len(cases),
        "open_cases": sum(1 for c in cases if c["status"] == "open"),
        "resolved_cases": sum(1 for c in cases if c["status"] == "resolved"),
        "total_experiences": len(experiences),
        "domains": {},
    }
    for key in domains:
        domain_cases = [c for c in cases if c["domain"] == key]
        stats["domains"][key] = {
            "case_count": len(domain_cases),
            "resolved": sum(1 for c in domain_cases if c["status"] == "resolved"),
        }

    return render_template(
        "index.html",
        domains=domains,
        stats=stats,
        recent_cases=cases[:5],
    )


@main_bp.route("/status")
def system_status():
    ollama = check_ollama()
    hindsight = check_hindsight()
    return render_template(
        "status.html",
        ollama=ollama,
        hindsight=hindsight,
    )
