"""
for creating subtitles and translations for the entire video in one shot
"""

import whisper
from pathlib import Path

# File inputs
video_file_name = 'hizuki_yui_debut'  # name of video file
input_video_file = Path('input', f'{video_file_name}.mp4')

# Setup for whisper usage
print("Loading whisper model...")
model = whisper.load_model("large")
print("Finished loading whisper model...")

print("Beginning audio transcription...")
transcribed_text = model.transcribe(f'{input_video_file}', language='japanese', task='transcribe')["text"]
print("Finished audio transcription...")
print("Beginning audio translation...")
translated_text = model.transcribe(f'{input_video_file}', language='japanese', task='translate')["text"]
print("Finished audio translation...")

print("Writing JP transcription file...")
with open(f"output_sub_file/{video_file_name}_jp_transcription_full_video.srt", 'w', encoding="utf-8") as f:
    f.write(transcribed_text)

print("Writing EN subs file...")
with open(f"output_sub_file/{video_file_name}_en_transcription_full_video.srt", 'w', encoding="utf-8") as f:
    f.write(translated_text)