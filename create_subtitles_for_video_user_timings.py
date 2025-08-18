"""
Take in a user generated list of timestamp ranges and sequentially extract the audio between those ranges and transcribe the spoken language.
Once a transcription is generated for all timestamp ranges, combine them into a single .srt subtitle file for output.
"""
import os
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
print("Finished loading whisper model...\n")

jp_subs = []
en_subs = []

for i, sub_time in enumerate(sub_lines):
    print(f"===== Working on segment {i+1}/{len(sub_lines)} =====\n")
    times = sub_time.rstrip().split('\t')
    start_time = times[0]
    end_time = times[1]

    start_sec = get_sec(start_time)
    end_sec = get_sec(end_time)

    start = timedelta(seconds=start_sec)
    end = timedelta(seconds=end_sec)

    video_clip = full_video_clip.subclipped(start_time, end_time)
    clip_name = f'temp/clip_{i}.mp4'
    saved_clip = video_clip.write_videofile(clip_name)

    print("\nBeginning audio transcription...")
    transcribed_text = model.transcribe(clip_name, language='japanese', task='transcribe')["text"]
    print("Finished audio transcription...")
    print("Beginning audio translation...")
    translated_text = model.transcribe(clip_name, language='japanese', task='translate')["text"]
    print("Finished audio translation...\n")
    
    jp_subs.append(Subtitle(i+1, start=start, end=end, content=transcribed_text))
    en_subs.append(Subtitle(i+1, start=start, end=end, content=translated_text))

    # Write temporary files in case there is a crash/fail somewhere along the line
    temp_jp_subs = compose(jp_subs)
    with open(f"temp/temp_{video_file_name}_jp_subs.srt", 'w', encoding="utf-8") as f:
        f.write(temp_jp_subs)

    temp_en_subs = compose(en_subs)
    with open(f"temp/temp_{video_file_name}_en_subs.srt", 'w', encoding="utf-8") as f:
        f.write(temp_en_subs)


jp_srt = compose(jp_subs)
en_srt = compose(en_subs)

print("Writing JP subs file...")
try:
    with open(f"output/{video_file_name}_jp_subs.srt", 'w', encoding="utf-8") as f:
        f.write(jp_srt)
except:
    with open(f"{video_file_name}_jp_subs.srt", 'w', encoding="utf-8") as f:
        f.write(jp_srt)

print("Writing EN subs file...")
try:
    with open(f"output/{video_file_name}_en_subs.srt", 'w', encoding="utf-8") as f:
        f.write(en_srt)
except:
    with open(f"{video_file_name}_en_subs.srt", 'w', encoding="utf-8") as f:
        f.write(en_srt)

# clear all files saved in temp
for file in os.listdir('temp'):
    os.remove(f'temp/{file}')