import subprocess
import os
import json
import datetime

input_path = 'C:/Code/FtrackStuff/zoo_slate_example.mp4'
output_path = 'C:/Code/FtrackStuff/zoo_slate_example_output.mp4'

# Use ffprobe to get video metadata including SAR
ffprobe_command = [
    'ffprobe', '-v', 'error', '-select_streams', 'v:0',
    '-show_entries', 'stream=width,height,r_frame_rate,display_aspect_ratio,sample_aspect_ratio',
    '-of', 'json', input_path
]

process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Parse the metadata
metadata = json.loads(output.decode('utf-8'))
stream = metadata['streams'][0]

width = stream['width']
height = stream['height']
fps = str(eval(stream['r_frame_rate'].split('/')[0]))
sar = stream.get('sample_aspect_ratio') 
creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(input_path)).strftime('%d %B %Y')



# Extract filename using os.path.basename
filename = os.path.basename(input_path)

# Construct ffmpeg command with metadata including SAR
ffmpeg_command = [
    'ffmpeg', '-i', input_path, '-vf',
    f"drawtext=fontfile=Arial.ttf: text='{filename}_{width}x{height}_{fps}fps_{sar}': x=(w-tw)/2: y=h-25: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: boxborderw=5,"
    f"drawtext=fontfile=Arial.ttf: text='%{{n}}': x=10: y=h-25: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: boxborderw=5,"
    f"drawtext=fontfile=Arial.ttf: text='{creation_date}': x=w-tw-10: y=h-25: fontcolor=white: fontsize=24: box=1: boxcolor=black@0.5: boxborderw=5",
    '-c:a', 'copy',
    output_path
]

process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()
print(sar)