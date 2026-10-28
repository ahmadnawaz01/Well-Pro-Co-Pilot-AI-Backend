import base64
import httpx
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

OPENROUTER_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"


async def extract_text_from_image(file: UploadFile) -> str:
    """
    Encodes image bytes into base64 and calls OpenRouter Vision API to extract text content.
    """
    try:
        file_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"
        base64_image = base64.b64encode(file_bytes).decode("utf-8")

        payload = {
            "model": settings.OPENROUTER_VISION_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Perform high-accuracy OCR on this document/receipt. Transcribe all text, numbers, dates, merchant names, items, and values clearly in plain English or original language."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.0
        }

        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://wellpro.ai",
            "X-Title": "WellPro Co-Pilot AI",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(OPENROUTER_COMPLETIONS_URL, json=payload, headers=headers)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"OpenRouter Vision API failed with status {response.status_code}: {response.text}"
                )

            res_data = response.json()
            extracted_text = res_data["choices"][0]["message"]["content"].strip()

            if not extracted_text:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="OpenRouter Vision model failed to extract text from the provided image."
                )

            return extracted_text

    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise exc
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image text extraction error: {str(exc)}"
        )