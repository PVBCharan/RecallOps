"""Image processing service — upload validation and vision analysis."""

import os
import base64
from PIL import Image
from app.services.llm_service import generate_with_image

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
MAX_IMAGE_SIZE_MB = 10


def validate_image(file_path: str) -> dict:
    """Validate an image file and return metadata."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        return {
            "valid": False,
            "error": f"Unsupported image format: {ext}. "
                     f"Supported: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}",
        }

    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        return {
            "valid": False,
            "error": f"Image too large ({size_mb:.1f} MB). Max: {MAX_IMAGE_SIZE_MB} MB.",
        }

    try:
        img = Image.open(file_path)
        img.verify()
        img = Image.open(file_path)  # Re-open after verify
        width, height = img.size
        return {
            "valid": True,
            "width": width,
            "height": height,
            "format": img.format,
            "size_mb": round(size_mb, 2),
        }
    except Exception as e:
        return {"valid": False, "error": f"Invalid image file: {e}"}


def analyze_image(file_path: str, context: str = "") -> dict:
    """Analyze an image using the local vision model."""
    validation = validate_image(file_path)
    if not validation["valid"]:
        return {"success": False, "error": validation["error"]}

    # Resize if very large to save memory
    try:
        img = Image.open(file_path)
        max_dim = 1024
        if max(img.size) > max_dim:
            ratio = max_dim / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
            # Save resized version temporarily
            resized_path = file_path + "_resized.jpg"
            img.save(resized_path, "JPEG", quality=85)
            analysis_path = resized_path
        else:
            analysis_path = file_path
    except Exception:
        analysis_path = file_path

    # Encode to base64
    try:
        with open(analysis_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        return {"success": False, "error": f"Failed to read image: {e}"}
    finally:
        # Clean up resized file
        resized = file_path + "_resized.jpg"
        if os.path.exists(resized):
            os.remove(resized)

    system_prompt = (
        "You are an evidence analysis assistant for RecallOps. "
        "Describe what you observe in the image factually and concisely. "
        "Identify key objects, text, error messages, anomalies, or "
        "relevant details. Label your observations as visual interpretations "
        "that may require human verification. "
        "Do NOT diagnose medical conditions or make safety-critical claims."
    )

    prompt = "Describe what you observe in this image."
    if context:
        prompt = (
            f"Context: {context}\n\n"
            "Based on this context, describe what you observe in the image. "
            "Focus on details relevant to the described situation."
        )

    analysis_text = generate_with_image(prompt, image_base64, system=system_prompt)

    return {
        "success": True,
        "analysis": analysis_text,
        "metadata": validation,
        "source": "vision_model",
        "verification_status": "machine_extracted",
    }
