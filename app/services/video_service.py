"""Video processing service — frame extraction and optional vision analysis."""

import os
import uuid
import cv2
from flask import current_app
from app.services.image_service import analyze_image


ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
MAX_VIDEO_SIZE_MB = 50


def validate_video(file_path: str) -> dict:
    """Validate a video file."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        return {
            "valid": False,
            "error": f"Unsupported video format: {ext}. "
                     f"Supported: {', '.join(ALLOWED_VIDEO_EXTENSIONS)}",
        }

    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_VIDEO_SIZE_MB:
        return {
            "valid": False,
            "error": f"Video too large ({size_mb:.1f} MB). Max: {MAX_VIDEO_SIZE_MB} MB.",
        }

    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            return {"valid": False, "error": "Cannot open video file."}
        fps = cap.get(cv2.CAP_PROP_FPS) or 24
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        max_dur = current_app.config.get("MAX_VIDEO_DURATION_SECONDS", 60)
        if duration > max_dur:
            return {
                "valid": False,
                "error": f"Video too long ({duration:.0f}s). Max: {max_dur}s.",
            }

        return {
            "valid": True,
            "fps": round(fps, 1),
            "frame_count": frame_count,
            "duration_seconds": round(duration, 1),
            "width": width,
            "height": height,
            "size_mb": round(size_mb, 2),
        }
    except Exception as e:
        return {"valid": False, "error": f"Video validation failed: {e}"}


def extract_frames(file_path: str, num_frames: int | None = None) -> dict:
    """Extract evenly spaced frames from a video."""
    validation = validate_video(file_path)
    if not validation["valid"]:
        return {"success": False, "error": validation["error"], "frames": []}

    if num_frames is None:
        num_frames = current_app.config.get("VIDEO_SAMPLE_FRAMES", 5)

    cap = cv2.VideoCapture(file_path)
    total_frames = validation["frame_count"]
    fps = validation["fps"]

    if total_frames <= num_frames:
        frame_indices = list(range(total_frames))
    else:
        step = total_frames / num_frames
        frame_indices = [int(step * i) for i in range(num_frames)]

    upload_dir = current_app.config["UPLOAD_FOLDER"]
    frame_dir = os.path.join(upload_dir, "frames")
    os.makedirs(frame_dir, exist_ok=True)

    frames = []
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        timestamp = round(idx / fps, 2) if fps > 0 else 0
        frame_id = str(uuid.uuid4())[:8]
        frame_name = f"frame_{frame_id}.jpg"
        frame_path = os.path.join(frame_dir, frame_name)
        cv2.imwrite(frame_path, frame)
        frames.append({
            "frame_index": idx,
            "timestamp_seconds": timestamp,
            "file_path": frame_path,
            "file_name": frame_name,
        })

    cap.release()

    return {
        "success": True,
        "video_metadata": validation,
        "frames": frames,
        "total_extracted": len(frames),
    }


def analyze_video(file_path: str, context: str = "") -> dict:
    """Extract frames and optionally analyze them with vision model."""
    extraction = extract_frames(file_path)
    if not extraction["success"]:
        return extraction

    analyses = []
    for frame in extraction["frames"]:
        frame_analysis = analyze_image(
            frame["file_path"],
            context=f"Video frame at {frame['timestamp_seconds']}s. {context}",
        )
        analyses.append({
            "timestamp": frame["timestamp_seconds"],
            "frame_index": frame["frame_index"],
            "analysis": frame_analysis.get("analysis", "Analysis unavailable"),
            "success": frame_analysis.get("success", False),
        })

    # Build event summary
    event_parts = []
    for a in analyses:
        if a["success"]:
            event_parts.append(
                f"**[{a['timestamp']}s]** {a['analysis']}"
            )
        else:
            event_parts.append(
                f"**[{a['timestamp']}s]** Frame analysis unavailable."
            )

    return {
        "success": True,
        "video_metadata": extraction["video_metadata"],
        "frames": extraction["frames"],
        "frame_analyses": analyses,
        "event_summary": "\n\n".join(event_parts) if event_parts else "No frames analyzed.",
        "source": "video_frame_analysis",
        "verification_status": "machine_extracted",
    }
