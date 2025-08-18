"""
For taking an existing srt file and creating a new text file with rows of only the time intervals contained in the srt file.
Using tabs to separate the start and end timestamps.
Format of hh:mm:ss
"""
from srt import parse

input_file_name = 'hizuki_yui_debut_jp_modified'
input_file = f'input/{input_file_name}.srt'

with open(input_file,'r', encoding="utf-8") as f:
    subs_text = f.read()

subs = parse(subs_text)

user_subs = []
for subtitle in subs:
    start_time = subtitle.start
    end_time = subtitle.end

    user_subs.append(f"{start_time}\t{end_time}\n")


with open(f'output/{input_file_name}_user_sub_times.txt','w') as f:
    for line in user_subs:
        f.writelines(line)