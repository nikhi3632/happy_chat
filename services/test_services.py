from speech_to_text_service import transcribe_audio
from text_to_speech_service import synthesize_speech
import os

TEST_DIR = os.path.join(os.getcwd() + 'test')

def test(file_path):
    transcription_output_path = os.path.join(TEST_DIR, 'transcription.txt')
    transcription_text = transcribe_audio(file_path, transcription_output_path)
    synthesized_audio_path = os.path.join(TEST_DIR, 'synthesized_audio.wav')
    synthesize_speech(transcription_text, synthesized_audio_path, 'Andrew Chipper', 'en')

if __name__ == "__main__":
    audio_file_path = os.path.join(TEST_DIR, 'input.wav')
    test(audio_file_path)
