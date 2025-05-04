from TTS.api import TTS
from faster_whisper import WhisperModel
import functools

# Instantiate once
# _tts_model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False, gpu=False)
_stt_model = WhisperModel("base", compute_type="int8")

# Singleton pattern with lazy loading for TTS model
# @functools.lru_cache(maxsize=1)
# def get_tts_model():
#     return _tts_model

# Singleton pattern with lazy loading for STT model
@functools.lru_cache(maxsize=1)
def get_stt_model():
    return _stt_model
