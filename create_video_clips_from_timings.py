"""
Create clips from a video file using user defined timings.
Wanted to have this so I can easily break a video down into multiple clips
"""
from moviepy import VideoFileClip
from pathlib import Path

video_file_name = 'video'  # name of video file
user_timings_file =  'user_times'

#%% Loading video and extracting audio from clips
input_video_file = Path('input', f'{video_file_name}.mp4')
input_video_sub_times = Path('input', f'{user_timings_file}.txt')

print("\nLoading in input video file...")
full_video = VideoFileClip(input_video_file)
print("Finished loading video file...\n")

print("Loading user timing file...")
with open(input_video_sub_times) as f:
     time_lines = f.readlines()

print("Finished loading in user timing file...\n")

for i, line in enumerate(time_lines):
    print(f"===== Working on segment {i+1}/{len(time_lines)} =====\n")
    times = line.rstrip().split('\t')
    start_time = times[0]
    end_time = times[1]

    video_clip = full_video.subclipped(start_time, end_time)
    clip_name = f'output/{video_file_name}_part{i+1}.mp4'
    saved_clip = video_clip.write_videofile(clip_name)