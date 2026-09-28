"""SQLite database layer for RecallOps case metadata."""

import sqlite3
import json
import uuid
from datetime import datetime, timezone


def _get_conn(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(db_path: str) -> None:
    """Create tables if they don't exist."""
    conn = _get_conn(db_path)
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id              TEXT PRIMARY KEY,
            title           TEXT NOT NULL,
            domain          TEXT NOT NULL,
            description     TEXT NOT NULL,
            symptoms        TEXT DEFAULT '',
            action_taken    TEXT DEFAULT '',
            outcome_text    TEXT DEFAULT '',
            status          TEXT DEFAULT 'open',
            created_at      TEXT NOT NULL,
            updated_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS evidence (
            id              TEXT PRIMARY KEY,
            case_id         TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            evidence_type   TEXT NOT NULL,       -- text | image | video | csv
            file_path       TEXT DEFAULT '',
            original_name   TEXT DEFAULT '',
            extracted_text  TEXT DEFAULT '',
            analysis        TEXT DEFAULT '',
            verification    TEXT DEFAULT 'machine_extracted',
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS recommendations (
            id              TEXT PRIMARY KEY,
            case_id         TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            suggestion      TEXT NOT NULL,
            reasoning       TEXT DEFAULT '',
            prior_cases     TEXT DEFAULT '[]',   -- JSON array
            uncertainty     TEXT DEFAULT '',
            evidence_used   TEXT DEFAULT '[]',   -- JSON array
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS outcome_feedback (
            id              TEXT PRIMARY KEY,
            case_id         TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            recommendation_id TEXT REFERENCES recommendations(id),
            status          TEXT NOT NULL,        -- successful | unsuccessful | mixed | unverified
            notes           TEXT DEFAULT '',
            verification_method TEXT DEFAULT '',
            created_at      TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS experiences (
            id              TEXT PRIMARY KEY,
            case_id         TEXT NOT NULL REFERENCES cases(id) ON DELETE CASCADE,
            domain          TEXT NOT NULL,
            context         TEXT NOT NULL,
            observations    TEXT DEFAULT '[]',    -- JSON
            action_taken    TEXT DEFAULT '',
            outcome_status  TEXT DEFAULT 'unverified',
            outcome_notes   TEXT DEFAULT '',
            conditions      TEXT DEFAULT '[]',    -- JSON
            limitations     TEXT DEFAULT '[]',    -- JSON
            embedding_text  TEXT DEFAULT '',
            created_at      TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


# ── Case CRUD ───────────────────────────────────────────────────────────

def create_case(db_path: str, *, title: str, domain: str, description: str,
                symptoms: str = "", action_taken: str = "",
                outcome_text: str = "") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    case_id = str(uuid.uuid4())
    conn = _get_conn(db_path)
    conn.execute(
        """INSERT INTO cases
           (id, title, domain, description, symptoms, action_taken,
            outcome_text, status, created_at, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (case_id, title, domain, description, symptoms, action_taken,
         outcome_text, "open", now, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    conn.close()
    return dict(row)


def get_case(db_path: str, case_id: str) -> dict | None:
    conn = _get_conn(db_path)
    row = conn.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_cases(db_path: str, domain: str | None = None) -> list[dict]:
    conn = _get_conn(db_path)
    if domain:
        rows = conn.execute(
            "SELECT * FROM cases WHERE domain=? ORDER BY created_at DESC",
            (domain,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM cases ORDER BY created_at DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_case_status(db_path: str, case_id: str, status: str) -> None:
    now = datetime.now(timezone.utc).isoformat()
    conn = _get_conn(db_path)
    conn.execute(
        "UPDATE cases SET status=?, updated_at=? WHERE id=?",
        (status, now, case_id),
    )
    conn.commit()
    conn.close()


def delete_case(db_path: str, case_id: str) -> None:
    conn = _get_conn(db_path)
    conn.execute("DELETE FROM cases WHERE id=?", (case_id,))
    conn.commit()
    conn.close()


# ── Evidence CRUD ───────────────────────────────────────────────────────

def add_evidence(db_path: str, *, case_id: str, evidence_type: str,
                 file_path: str = "", original_name: str = "",
                 extracted_text: str = "", analysis: str = "",
                 verification: str = "machine_extracted") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    eid = str(uuid.uuid4())
    conn = _get_conn(db_path)
    conn.execute(
        """INSERT INTO evidence
           (id, case_id, evidence_type, file_path, original_name,
            extracted_text, analysis, verification, created_at)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (eid, case_id, evidence_type, file_path, original_name,
         extracted_text, analysis, verification, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM evidence WHERE id=?", (eid,)).fetchone()
    conn.close()
    return dict(row)


def get_evidence_for_case(db_path: str, case_id: str) -> list[dict]:
    conn = _get_conn(db_path)
    rows = conn.execute(
        "SELECT * FROM evidence WHERE case_id=? ORDER BY created_at",
        (case_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Recommendation CRUD ────────────────────────────────────────────────

def add_recommendation(db_path: str, *, case_id: str, suggestion: str,
                       reasoning: str = "", prior_cases: list | None = None,
                       uncertainty: str = "",
                       evidence_used: list | None = None) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    rid = str(uuid.uuid4())
    conn = _get_conn(db_path)
    conn.execute(
        """INSERT INTO recommendations
           (id, case_id, suggestion, reasoning, prior_cases, uncertainty,
            evidence_used, created_at)
           VALUES (?,?,?,?,?,?,?,?)""",
        (rid, case_id, suggestion, reasoning,
         json.dumps(prior_cases or []), uncertainty,
         json.dumps(evidence_used or []), now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM recommendations WHERE id=?", (rid,)).fetchone()
    conn.close()
    result = dict(row)
    result["prior_cases"] = json.loads(result["prior_cases"])
    result["evidence_used"] = json.loads(result["evidence_used"])
    return result


def get_recommendations_for_case(db_path: str, case_id: str) -> list[dict]:
    conn = _get_conn(db_path)
    rows = conn.execute(
        "SELECT * FROM recommendations WHERE case_id=? ORDER BY created_at",
        (case_id,),
    ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["prior_cases"] = json.loads(d["prior_cases"])
        d["evidence_used"] = json.loads(d["evidence_used"])
        results.append(d)
    return results


# ── Outcome feedback CRUD ──────────────────────────────────────────────

def add_outcome_feedback(db_path: str, *, case_id: str,
                         recommendation_id: str | None = None,
                         status: str = "unverified",
                         notes: str = "",
                         verification_method: str = "") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    fid = str(uuid.uuid4())
    conn = _get_conn(db_path)
    conn.execute(
        """INSERT INTO outcome_feedback
           (id, case_id, recommendation_id, status, notes,
            verification_method, created_at)
           VALUES (?,?,?,?,?,?,?)""",
        (fid, case_id, recommendation_id, status, notes,
         verification_method, now),
    )
    conn.commit()
    # Also update the case status
    status_map = {
        "successful": "resolved",
        "unsuccessful": "unresolved",
        "mixed": "partial",
        "unverified": "open",
    }
    update_case_status(db_path, case_id, status_map.get(status, "open"))
    row = conn.execute(
        "SELECT * FROM outcome_feedback WHERE id=?", (fid,)
    ).fetchone()
    conn.close()
    return dict(row)


def get_feedback_for_case(db_path: str, case_id: str) -> list[dict]:
    conn = _get_conn(db_path)
    rows = conn.execute(
        "SELECT * FROM outcome_feedback WHERE case_id=? ORDER BY created_at",
        (case_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Experience CRUD (local mirror of what goes to Hindsight) ───────────

def save_experience(db_path: str, *, case_id: str, domain: str,
                    context: str, observations: list | None = None,
                    action_taken: str = "",
                    outcome_status: str = "unverified",
                    outcome_notes: str = "",
                    conditions: list | None = None,
                    limitations: list | None = None,
                    embedding_text: str = "") -> dict:
    now = datetime.now(timezone.utc).isoformat()
    eid = str(uuid.uuid4())
    conn = _get_conn(db_path)
    conn.execute(
        """INSERT INTO experiences
           (id, case_id, domain, context, observations, action_taken,
            outcome_status, outcome_notes, conditions, limitations,
            embedding_text, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (eid, case_id, domain, context,
         json.dumps(observations or []), action_taken,
         outcome_status, outcome_notes,
         json.dumps(conditions or []),
         json.dumps(limitations or []),
         embedding_text, now),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM experiences WHERE id=?", (eid,)).fetchone()
    conn.close()
    result = dict(row)
    for key in ("observations", "conditions", "limitations"):
        result[key] = json.loads(result[key])
    return result


def list_experiences(db_path: str, domain: str | None = None) -> list[dict]:
    conn = _get_conn(db_path)
    if domain:
        rows = conn.execute(
            "SELECT * FROM experiences WHERE domain=? ORDER BY created_at DESC",
            (domain,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM experiences ORDER BY created_at DESC"
        ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        for key in ("observations", "conditions", "limitations"):
            d[key] = json.loads(d[key])
        results.append(d)
    return results


def get_experience(db_path: str, experience_id: str) -> dict | None:
    conn = _get_conn(db_path)
    row = conn.execute(
        "SELECT * FROM experiences WHERE id=?", (experience_id,)
    ).fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    for key in ("observations", "conditions", "limitations"):
        d[key] = json.loads(d[key])
    return d


def search_experiences_by_text(db_path: str, query: str,
                               domain: str | None = None,
                               limit: int = 5) -> list[dict]:
    """Simple keyword search across experience context and observations.
    This is a fallback when Hindsight is not available — it uses SQLite LIKE."""
    conn = _get_conn(db_path)
    pattern = f"%{query}%"
    if domain:
        rows = conn.execute(
            """SELECT * FROM experiences
               WHERE domain=? AND (context LIKE ? OR observations LIKE ?
                     OR embedding_text LIKE ?)
               ORDER BY created_at DESC LIMIT ?""",
            (domain, pattern, pattern, pattern, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            """SELECT * FROM experiences
               WHERE context LIKE ? OR observations LIKE ?
                     OR embedding_text LIKE ?
               ORDER BY created_at DESC LIMIT ?""",
            (pattern, pattern, pattern, limit),
        ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        for key in ("observations", "conditions", "limitations"):
            d[key] = json.loads(d[key])
        results.append(d)
    return results
