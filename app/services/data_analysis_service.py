"""Data analysis service — CSV parsing, statistics, and chart generation."""

import os
import uuid
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
from flask import current_app


def analyze_csv(file_path: str) -> dict:
    """Parse a CSV file and return a structured analysis."""
    result = {
        "success": False,
        "file": os.path.basename(file_path),
        "columns": [],
        "row_count": 0,
        "summary_stats": {},
        "missing_values": {},
        "trends": [],
        "anomalies": [],
        "chart_path": None,
        "narrative": "",
        "error": None,
    }

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        result["error"] = f"Failed to parse CSV: {e}"
        return result

    if df.empty:
        result["error"] = "The CSV file is empty."
        return result

    result["success"] = True
    result["columns"] = list(df.columns)
    result["row_count"] = len(df)

    # ── Summary statistics ──────────────────────────────────────────
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        stats = df[numeric_cols].describe().round(2).to_dict()
        result["summary_stats"] = stats

    # ── Missing values ──────────────────────────────────────────────
    missing = df.isnull().sum()
    result["missing_values"] = {
        col: int(count) for col, count in missing.items() if count > 0
    }

    # ── Simple trend detection ──────────────────────────────────────
    trends = []
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 3:
            continue
        first_half = series.iloc[: len(series) // 2].mean()
        second_half = series.iloc[len(series) // 2 :].mean()
        if first_half == 0:
            continue
        change_pct = ((second_half - first_half) / abs(first_half)) * 100
        if abs(change_pct) > 10:
            direction = "increasing" if change_pct > 0 else "decreasing"
            trends.append({
                "column": col,
                "direction": direction,
                "change_percent": round(change_pct, 1),
                "first_half_mean": round(first_half, 2),
                "second_half_mean": round(second_half, 2),
            })
    result["trends"] = trends

    # ── Anomaly detection (IQR) ─────────────────────────────────────
    anomalies = []
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 4:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outliers = series[(series < lower) | (series > upper)]
        if len(outliers) > 0:
            anomalies.append({
                "column": col,
                "outlier_count": len(outliers),
                "lower_bound": round(lower, 2),
                "upper_bound": round(upper, 2),
                "outlier_values": outliers.head(5).tolist(),
            })
    result["anomalies"] = anomalies

    # ── Generate chart ──────────────────────────────────────────────
    if numeric_cols:
        try:
            chart_path = _generate_chart(df, numeric_cols)
            result["chart_path"] = chart_path
        except Exception:
            pass

    # ── Build narrative ─────────────────────────────────────────────
    narrative_parts = [
        f"**Dataset:** {result['file']} — {result['row_count']} rows, "
        f"{len(result['columns'])} columns.",
    ]
    if result["missing_values"]:
        missing_str = ", ".join(
            f"{col} ({cnt})" for col, cnt in result["missing_values"].items()
        )
        narrative_parts.append(f"**Missing values:** {missing_str}")

    for t in trends:
        narrative_parts.append(
            f"**Trend:** `{t['column']}` is {t['direction']} "
            f"({t['change_percent']:+.1f}% from first half to second half)."
        )

    for a in anomalies:
        narrative_parts.append(
            f"**Potential anomaly:** `{a['column']}` has "
            f"{a['outlier_count']} outlier(s) outside the expected range "
            f"[{a['lower_bound']}, {a['upper_bound']}]."
        )

    result["narrative"] = "\n\n".join(narrative_parts)
    return result


def _generate_chart(df: pd.DataFrame, numeric_cols: list[str]) -> str:
    """Create a simple line/bar chart and save it."""
    chart_dir = current_app.config["CHART_FOLDER"]
    chart_id = str(uuid.uuid4())[:8]
    filename = f"chart_{chart_id}.png"
    filepath = os.path.join(chart_dir, filename)

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(10, 5))

    cols_to_plot = numeric_cols[:4]  # Limit to 4 series
    colors = ["#6366f1", "#22d3ee", "#f59e0b", "#ef4444"]

    if len(df) > 30:
        for i, col in enumerate(cols_to_plot):
            ax.plot(df.index, df[col], label=col, color=colors[i % len(colors)],
                    linewidth=1.5, alpha=0.9)
    else:
        x = np.arange(len(df))
        width = 0.8 / len(cols_to_plot)
        for i, col in enumerate(cols_to_plot):
            ax.bar(x + i * width, df[col], width, label=col,
                   color=colors[i % len(colors)], alpha=0.85)

    ax.legend(framealpha=0.3)
    ax.set_xlabel("Index", color="#94a3b8")
    ax.set_ylabel("Value", color="#94a3b8")
    ax.tick_params(colors="#64748b")
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#1e293b")
    ax.grid(True, alpha=0.15)

    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches="tight",
                facecolor="#0f172a", edgecolor="none")
    plt.close(fig)

    return f"img/charts/{filename}"
