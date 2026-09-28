"""API routes — JSON endpoints for AJAX operations."""

from flask import Blueprint, jsonify, current_app, request
from app.services.database import (
    list_cases, get_case, list_experiences,
    get_evidence_for_case, get_recommendations_for_case,
)
from app.services.llm_service import check_ollama
from app.services.hindsight_service import check_hindsight, retrieve_similar
from app.domain_rules import get_domains

api_bp = Blueprint("api", __name__)


@api_bp.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "ollama": check_ollama(),
        "hindsight": check_hindsight(),
    })


@api_bp.route("/domains")
def domains():
    return jsonify(get_domains())


@api_bp.route("/cases")
def cases():
    domain = request.args.get("domain")
    db = current_app.config["DATABASE_PATH"]
    return jsonify(list_cases(db, domain=domain))


@api_bp.route("/cases/<case_id>")
def case_detail(case_id):
    db = current_app.config["DATABASE_PATH"]
    case = get_case(db, case_id)
    if not case:
        return jsonify({"error": "Not found"}), 404
    case["evidence"] = get_evidence_for_case(db, case_id)
    case["recommendations"] = get_recommendations_for_case(db, case_id)
    return jsonify(case)


@api_bp.route("/experiences")
def experiences():
    domain = request.args.get("domain")
    db = current_app.config["DATABASE_PATH"]
    return jsonify(list_experiences(db, domain=domain))


@api_bp.route("/search")
def search():
    query = request.args.get("q", "")
    domain = request.args.get("domain")
    if not query:
        return jsonify([])
    db = current_app.config["DATABASE_PATH"]
    results = retrieve_similar(db, query, domain=domain, limit=10)
    return jsonify(results)
