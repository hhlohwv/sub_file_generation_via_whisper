"""
Take in a user generated list of timestamp ranges and sequentially extract the audio between those ranges and transcribe the spoken language.
Once a transcription is generated for all timestamp ranges, combine them into a single .srt subtitle file for output.
"""
from srt import Subtitle, compose
import whisper
from moviepy import VideoFileClip
from pathlib import Path
from datetime import timedelta

def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str.split(':')
    seconds = int(h) * 3600 + int(m) * 60 + float(s)
    return seconds


#%% File inputs
video_file_name = 'hizuki_yui_debut'  # name of video file
user_sub_file =  'user_subs'

#%% Loading video and extracting audio from clips
input_video_file = Path('input', f'{video_file_name}.mp4')
input_video_sub_times = Path('input', f'{user_sub_file}.txt')

print("\nLoading in input video file...")
full_video_clip = VideoFileClip(input_video_file)
print("Finished loading video file...\n")

print("Loading user sub file...")
with open(input_video_sub_times) as f:
     sub_lines = f.readlines()

print("Finished loading in user sub file...\n")

# Setup for whisper usage
print("Loading whisper model...")
model = whisper.load_model("medium")
print("Finished loading whisper model...")

jp_subs = []
en_subs = []

for i, sub_time in enumerate(sub_lines):
    times = sub_time.rstrip().split('\t')
    start_time = times[0]
    end_time = times[1]

    start_sec = get_sec(start_time)
    end_sec = get_sec(end_time)

    start = timedelta(seconds=start_sec)
    end = timedelta(seconds=end_sec)

    video_clip = full_video_clip.subclipped(start_time, end_time)
    saved_clip = video_clip.write_videofile(f'temp/test_{i}.mp4')

    print("Beginning audio transcription...")
    transcribed_text = model.transcribe(f'temp/test_{i}.mp4', language='japanese', task='transcribe')["text"]
    print("Finished audio transcription...")
    print("Beginning audio translation...")
    translated_text = model.transcribe(f'temp/test_{i}.mp4', language='japanese', task='translate')["text"]
    print("Finished audio translation...")
    
    timedelta()
    jp_subs.append(Subtitle(i+1, start=start, end=end, content=transcribed_text))
    en_subs.append(Subtitle(i+1, start=start, end=end, content=translated_text))


jp_srt = compose(jp_subs)
en_srt = compose(en_subs)

print("Writing JP subs file...")
with open(f"output_sub_file/{video_file_name}_jp_subs.srt", 'w', encoding="utf-8") as f:
    f.write(jp_srt)

print("Writing EN subs file...")
with open(f"output_sub_file/{video_file_name}_en_subs.srt", 'w', encoding="utf-8") as f:
    f.write(en_srt)