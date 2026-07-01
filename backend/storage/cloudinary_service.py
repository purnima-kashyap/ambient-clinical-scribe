import os
import asyncio
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


async def upload_audio_to_cloudinary(file_path: str, public_id: str) -> dict:
    """
    Uploads an audio file to Cloudinary and returns its hosted URL + metadata.

    Note: Cloudinary doesn't have a separate "audio" resource_type —
    audio files are uploaded under resource_type="video" since they share
    the same media processing pipeline.
    """
    def _upload():
        return cloudinary.uploader.upload(
            file_path,
            resource_type="video",
            folder="healthcare_scribe/audio",
            public_id=public_id,
            overwrite=True,
        )

    try:
        result = await asyncio.to_thread(_upload)
    except Exception as e:
        raise RuntimeError(f"Cloudinary upload failed: {str(e)}") from e

    return {
        "url": result.get("secure_url"),
        "public_id": result.get("public_id"),
        "duration_seconds": result.get("duration"),
        "format": result.get("format"),
        "bytes": result.get("bytes"),
    }