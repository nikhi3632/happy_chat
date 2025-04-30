from services import get_stt_model

def transcribe_audio(file_path: str, output_path: str) -> str:
    stt_model = get_stt_model()
    segments, _ = stt_model.transcribe(file_path)
    transcription = " ".join(segment.text for segment in segments)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(transcription)
    return transcription
