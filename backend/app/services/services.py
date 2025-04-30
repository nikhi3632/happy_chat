from TTS.api import TTS
from faster_whisper import WhisperModel

# Instantiate once
_tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
_stt_model = WhisperModel("base", compute_type="int8")

def get_tts_model():
    return _tts_model

def get_stt_model():
    return _stt_model
