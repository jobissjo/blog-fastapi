import os
import asyncio

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile
from fastapi.exceptions import HTTPException
from app.core.settings import settings

class CloudinaryService:
    def __init__(self):
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
        )

    async def upload_image(self, file: UploadFile):
        """
        Upload an image file to Cloudinary.
        """
        try:
            result =await asyncio.to_thread(cloudinary.uploader.upload, file.file, folder="images/", resource_type="image")
                
            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format"),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image upload failed: {e}")

    async def upload_document(self, file: UploadFile):
        """
        Upload a document (PDF, DOCX, etc.) to Cloudinary.
        """
        try:
            filename, ext = os.path.splitext(file.filename)
            result = await asyncio.to_thread(cloudinary.uploader.upload,
                file.file,
                folder="documents/",
                resource_type="raw",  # use raw for non-image files,
                public_id=f"{filename}{ext}",
                unique_filename=True,
                overwrite=False,
            )
            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "bytes": result.get("bytes"),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Document upload failed: {e}")

    
    async def delete_image(self, public_id: str):
        try:
            result = await asyncio.to_thread(cloudinary.uploader.destroy, public_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image deletion failed: {e}")
    
    async def delete_document(self, public_id: str):
        try:
            result = await asyncio.to_thread(cloudinary.uploader.destroy, public_id)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Document deletion failed: {e}")