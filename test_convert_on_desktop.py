
import subprocess
import os
import json
import datetime

# Define paths
input_path = 'C:/Code/FtrackStuff/zoo_slate_example.mp4'
output_path = 'C:/Code/FtrackStuff/zoo_slate_example_output.mp4'
intro_image_path = 'C:/Code/FtrackStuff/intro_frame.png'
intro_video_path = 'C:/Code/FtrackStuff/intro_frame.mp4'
temp_video_path = 'C:/Code/FtrackStuff/temp_video.mp4'
concat_list_path = 'C:/Code/FtrackStuff/concat_list.txt'

# Use ffprobe to get video metadata
ffprobe_command = [
    'ffprobe', '-v', 'error', '-select_streams', 'v:0',
    '-show_entries', 'stream=width,height,r_frame_rate,display_aspect_ratio,sample_aspect_ratio,nb_frames,duration,pix_fmt,codec_name,time_base',
    '-of', 'json', input_path
]

process = subprocess.Popen(ffprobe_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()

# Parse the metadata
metadata = json.loads(output.decode('utf-8'))
stream = metadata['streams'][0]
width = stream['width']
height = stream['height']
fps = eval(stream['r_frame_rate'])  # This evaluates the fraction correctly
single_frame_duration = 1 / fps  
total_frames = stream.get('nb_frames')
duration = stream.get('duration') 
total_duration = float(duration) + single_frame_duration
input_format = stream.get('pix_fmt', 'unknown')
input_codec = stream.get('codec_name', 'unknown')
input_time_base = stream.get('time_base', 'unknown')
input_timescale = input_time_base.split('/')[-1]
font_size = min(width, height) * 0.02

creation_date = datetime.datetime.fromtimestamp(os.path.getmtime(input_path)).strftime('%d %B %Y')
filename = os.path.basename(input_path)


# Calculate the dimensions for the color bars
color_bar_height = int(height * 0.15)
color_bar_width = int(width * 0.3)

# Generate an image with color bars on a black background and add "Shot: filename" text
generate_image_command = [
    'ffmpeg', '-f', 'lavfi', 
    '-i', f'color=c=#232323@1:s={width}x{height}',  # Generate a black background with the original dimensions
    '-f', 'lavfi', '-i', f'color=0xbebebe:s={color_bar_width//7}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0xc0be00:s={color_bar_width//7}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0x00bebd:s={color_bar_width//7}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0x00bc00:s={color_bar_width//7}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0xbe00bf:s={color_bar_width//7}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0xbf0000:s={color_bar_width//7}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0x0000bf:s={color_bar_width//7}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0x000000:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0x141414:s={color_bar_width//14}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0x272727:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0x3b3b3b:s={color_bar_width//14}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0x4e4e4e:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0x626262:s={color_bar_width//14}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0x767676:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0x898989:s={color_bar_width//14}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0x9d9d9d:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0xb0b0b0:s={color_bar_width//14}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0xc4c4c4:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0xd8d8d8:s={color_bar_width//14}x{color_bar_height//2}', 
    '-f', 'lavfi', '-i', f'color=0xebebeb:s={color_bar_width//14}x{color_bar_height//2}',
    '-f', 'lavfi', '-i', f'color=0xffffff:s={color_bar_width//14}x{color_bar_height//2}',
    '-filter_complex', 
    f"""
    [1][2][3][4][5][6][7]hstack=7[top_colors];
    [8][9][10][11][12][13][14][15][16][17][18][19][20][21]hstack=14[bottom_colors];
[top_colors][bottom_colors]vstack=2[color_bars];
[0:v][color_bars]overlay=x=0:y=main_h-overlay_h,

drawtext=text='Show\\: Netflix VFX Templates':x=10:y=10:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Version Name\\: nflx_101_001_0020_slate_VND_v001':x=10:y=10+2*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Date\\: 2021-05-11':x=10:y=10+4*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Shot Description\\: If a description field is required, it goes on the left to provide more space.':x=10:y=10+6*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Submission Note\\: Submitting as an example with all template fields filled out. As well as the additional fields; shot description, Episode, Scene, and Version # that were requested specifically by production.':x=10:y=10+8*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,

drawtext=text='Shot Name\\: nflx_101_001_0020':x=w-{int(width*0.3)}:y=10:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Sequence Name\\: 001':x=w-{int(width*0.3)}:y=10+2*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Scene\\: 001':x=w-{int(width*0.3)}:y=10+4*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Frames\\: 1000 - 1030 (30)':x=w-{int(width*0.3)}:y=10+6*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Media Color\\: rec709 with show lut':x=w-{int(width*0.3)}:y=10+8*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5,
drawtext=text='Vendor Logo':x=w-{int(width*0.3)}:y=10+10*{int(font_size*1.5+10)}:fontcolor=white:fontsize={int(font_size*1.5)}:box=1:boxcolor=black@0.5:boxborderw=5""",
'-frames:v', '1', intro_image_path
]
subprocess.run(generate_image_command)

# Step 2: Create a video from this frame with a single frame duration

create_video_command = [
    'ffmpeg', '-loop', '1', '-i', intro_image_path, '-t', str(single_frame_duration), '-r', str(fps),
    '-vf', f"fps={fps},format={input_format}", '-video_track_timescale', input_timescale, intro_video_path
]
subprocess.run(create_video_command)



# Adjusted Step 3: Concatenate the frame with the original video without applying text overlays yet
with open(concat_list_path, 'w') as f:
    f.write(f"file '{intro_video_path}'\n")  # Add intro video
    f.write(f"file '{input_path}'\n")  # Add input video

concat_command = [
    'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_path, '-c:v', 'copy', '-c:a', 'copy', temp_video_path  # Use temp_video_path for concatenated video
]
subprocess.run(concat_command)

# Adjusted Step 4: Apply text overlays to the concatenated video with text within the black bar, all in uppercase
bar_height = int(font_size) + 15  # Adjust the 10 value as needed for padding
apply_text_overlays_command = [
    'ffmpeg', '-i', temp_video_path, '-vf',
    f"drawbox=y=ih-{bar_height}:color=#232323@1:width=iw:height={bar_height}:t=fill,"  # Draw the black bar at the bottom
    f"drawtext=enable='gte(n,1)':fontfile=SourceCodePro-Regular.ttf: text='{filename.upper()}_{width}x{height}_{fps}FPS': x=(w-tw)/2: y=h-{bar_height}/2-(th/2): fontcolor=white: fontsize={int(font_size)},"  # Center text horizontally and vertically within the bar
    f"drawtext=enable='gte(n,1)':fontfile=SourceCodePro-Regular.ttf: text='%{{n}}': x=10: y=h-{bar_height}/2-(th/2): fontcolor=white: fontsize={int(font_size)},"  # Adjust y position for frame number text
    f"drawtext=enable='gte(n,1)':fontfile=SourceCodePro-Regular.ttf: text='{creation_date.upper()}': x=w-tw-10: y=h-{bar_height}/2-(th/2): fontcolor=white: fontsize={int(font_size)}",  # Center date text within the bar
    '-c:v', input_codec, '-c:a', 'copy', output_path  # Output the final video with overlays
]

subprocess.run(apply_text_overlays_command)


# Clean up temporary files
os.remove(intro_image_path)
os.remove(intro_video_path)
os.remove(temp_video_path)  # Ensure this is the correct file to delete after confirming it's no longer needed
os.remove(concat_list_path)










