# Purpose
Generating a subtitle file for videos using OpenAI Whisper, but with the additional step of using user defined timestamps for isolating the audio segments for transcription.
Intention is to ensure more accurate timing of the subtitles, specifically for further use with subs2srs for generating Anki flashcards with Morphman readability analysis.

# Setup
Required packages:
- OpenAI Whisper (https://github.com/openai/whisper)
```shell
pip install -U openai-whisper
```
- srt (https://pypi.org/project/srt/)
```shell
pip install srt
```
- moviepy (https://pypi.org/project/moviepy/)
```shell
pip install moviepy
```

For trying to streamline the process of getting video times for use timestamp file, using MPV player with an additional script for creating a keybind for putting timestamp into the clipboard for copying into a separate text file (https://github.com/Arieleg/mpv-copyTime).
