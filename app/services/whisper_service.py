from fastapi import UploadFile, HTTPException, status
from groq import AsyncGroq
from app.core.config import settings

client = AsyncGroq(api_key=settings.GROQ_API_KEY)


async def transcribe_and_translate_audio(file: UploadFile) -> str:
    """
    Sends raw audio bytes to Groq Cloud (whisper-large-v3) and translates 
    any foreign language input directly into strict English text.
    """
    try:
        file_bytes = await file.read()
        filename = file.filename or "audio.mp3"

        # Use Groq's translation endpoint to force output into English
        translation = await client.audio.translations.create(
            file=(filename, file_bytes),
            model="whisper-large-v3",
            response_format="json",
            temperature=0.0
        )

        translated_text = translation.text.strip()
        if not translated_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Transcribed audio resulted in empty text."
            )

        return translated_text

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Groq Whisper transcription failed: {str(exc)}"
        )