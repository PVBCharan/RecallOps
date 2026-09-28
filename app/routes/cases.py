"""Case routes — create, view, list, feedback, and delete cases."""

import os
import uuid
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, current_app, jsonify,
)
from app.services.database import (
    create_case, get_case, list_cases, delete_case,
    add_evidence, get_evidence_for_case,
    get_recommendations_for_case, add_outcome_feedback,
    get_feedback_for_case, update_case_status,
)
from app.services.recommendation_service import (
    synthesize_evidence, generate_recommendation,
)
from app.services.data_analysis_service import analyze_csv
from app.services.image_service import analyze_image
from app.services.video_service import analyze_video
from app.domain_rules import get_domains, get_domain_config

cases_bp = Blueprint("cases", __name__)

ALLOWED_EXTENSIONS = {
    "image": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"},
    "video": {".mp4", ".avi", ".mov", ".mkv", ".webm"},
    "csv": {".csv"},
}


def _save_upload(file, subfolder: str = "") -> tuple[str, str]:
    """Save an uploaded file and return (saved_path, original_name)."""
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    if subfolder:
        upload_dir = os.path.join(upload_dir, subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    original = file.filename
    ext = os.path.splitext(original)[1].lower()
    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    return filepath, original


def _detect_file_type(filename: str) -> str | None:
    ext = os.path.splitext(filename)[1].lower()
    for ftype, exts in ALLOWED_EXTENSIONS.items():
        if ext in exts:
            return ftype
    return None


@cases_bp.route("/")
def case_list():
    domain_filter = request.args.get("domain")
    domains = get_domains()
    cases = list_cases(current_app.config["DATABASE_PATH"], domain=domain_filter)
    return render_template(
        "case_list.html",
        cases=cases,
        domains=domains,
        current_domain=domain_filter,
    )


@cases_bp.route("/new", methods=["GET", "POST"])
def new_case():
    domains = get_domains()
    selected_domain = request.args.get("domain", "commercial_operations")

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        domain = request.form.get("domain", "commercial_operations")
        description = request.form.get("description", "").strip()
        symptoms = request.form.get("symptoms", "").strip()
        action_taken = request.form.get("action_taken", "").strip()
        outcome_text = request.form.get("outcome_text", "").strip()

        # Validate
        errors = []
        if not title:
            errors.append("Case title is required.")
        if not description:
            errors.append("Description is required.")
        if domain not in domains:
            errors.append("Invalid domain selected.")

        if errors:
            for e in errors:
                flash(e, "error")
            return render_template(
                "new_case.html",
                domains=domains,
                selected_domain=domain,
                form_data=request.form,
            )

        # Create case
        db = current_app.config["DATABASE_PATH"]
        case = create_case(
            db,
            title=title,
            domain=domain,
            description=description,
            symptoms=symptoms,
            action_taken=action_taken,
            outcome_text=outcome_text,
        )

        # Handle file uploads
        files = request.files.getlist("evidence_files")
        for f in files:
            if f and f.filename:
                ftype = _detect_file_type(f.filename)
                if not ftype:
                    flash(f"Unsupported file: {f.filename}", "warning")
                    continue
                filepath, original = _save_upload(f, subfolder=case["id"])
                analysis = ""
                extracted = ""

                if ftype == "csv":
                    result = analyze_csv(filepath)
                    if result["success"]:
                        analysis = result["narrative"]
                        extracted = str(result["summary_stats"])
                    else:
                        analysis = f"CSV analysis failed: {result['error']}"

                elif ftype == "image":
                    result = analyze_image(filepath, context=description)
                    if result["success"]:
                        analysis = result["analysis"]
                    else:
                        analysis = f"Image analysis: {result.get('error', 'unavailable')}"

                elif ftype == "video":
                    result = analyze_video(filepath, context=description)
                    if result["success"]:
                        analysis = result.get("event_summary", "")
                    else:
                        analysis = f"Video analysis: {result.get('error', 'unavailable')}"

                add_evidence(
                    db,
                    case_id=case["id"],
                    evidence_type=ftype,
                    file_path=filepath,
                    original_name=original,
                    extracted_text=extracted,
                    analysis=analysis,
                )

        flash("Case created successfully!", "success")
        return redirect(url_for("cases.view_case", case_id=case["id"]))

    return render_template(
        "new_case.html",
        domains=domains,
        selected_domain=selected_domain,
        form_data={},
    )


@cases_bp.route("/<case_id>")
def view_case(case_id):
    db = current_app.config["DATABASE_PATH"]
    case = get_case(db, case_id)
    if not case:
        flash("Case not found.", "error")
        return redirect(url_for("cases.case_list"))

    domains = get_domains()
    domain_config = get_domain_config(case["domain"])
    evidence = get_evidence_for_case(db, case_id)
    recommendations = get_recommendations_for_case(db, case_id)
    feedback = get_feedback_for_case(db, case_id)

    return render_template(
        "view_case.html",
        case=case,
        domain_config=domain_config,
        domains=domains,
        evidence=evidence,
        recommendations=recommendations,
        feedback=feedback,
    )


@cases_bp.route("/<case_id>/analyze", methods=["POST"])
def analyze_case(case_id):
    db = current_app.config["DATABASE_PATH"]
    case = get_case(db, case_id)
    if not case:
        flash("Case not found.", "error")
        return redirect(url_for("cases.case_list"))

    result = generate_recommendation(db, case_id)
    if "error" in result:
        flash(f"Analysis error: {result['error']}", "error")
    else:
        flash("Recommendation generated successfully!", "success")

    return redirect(url_for("cases.view_case", case_id=case_id))


@cases_bp.route("/<case_id>/feedback", methods=["POST"])
def submit_feedback(case_id):
    db = current_app.config["DATABASE_PATH"]
    case = get_case(db, case_id)
    if not case:
        flash("Case not found.", "error")
        return redirect(url_for("cases.case_list"))

    status = request.form.get("outcome_status", "unverified")
    notes = request.form.get("outcome_notes", "")
    method = request.form.get("verification_method", "")
    rec_id = request.form.get("recommendation_id")

    add_outcome_feedback(
        db,
        case_id=case_id,
        recommendation_id=rec_id if rec_id else None,
        status=status,
        notes=notes,
        verification_method=method,
    )

    flash("Outcome feedback recorded.", "success")
    return redirect(url_for("cases.view_case", case_id=case_id))


@cases_bp.route("/<case_id>/delete", methods=["POST"])
def remove_case(case_id):
    db = current_app.config["DATABASE_PATH"]
    delete_case(db, case_id)
    flash("Case deleted.", "info")
    return redirect(url_for("cases.case_list"))
