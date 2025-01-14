import mimetypes
from typing import Literal
import sieve
import shutil
import os
import subprocess
import requests
from crop_background import crop_image_vertical, crop_video_vertical
from transcript import get_duration, get_fps, prepare_transcript_word_list, prepare_transcript_words_list

def start_remotion_server(command, target_message):
    """
    Starts a remotion server process and and once server starts running returns the process.
    """
    try:
        # Start the server process
        server_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
        if not server_process.stdout:
            raise RuntimeError("Failed to capture subprocess output streams.")
        
        # Monitor the output for the target message
        while True:
            output = server_process.stdout.readline()
            if output == "" and server_process.poll() is not None:
                raise RuntimeError("Server process exited unexpectedly.")
            if target_message in output:
                print("Server Outputs:", output.strip())
                break
            print(output, end="")

        return server_process

    except Exception as e:
        print(f"Error: {e}")
        return None

SubtitleOptions = Literal["glowing", "background_tracking", "color_tracking", "typing_background"]

metadata = sieve.Metadata(
    title="Enhance reels",
    description="Enhance a 9:16 reel video by updating the background and incorporating captions",
    code_url = 'https://github.com/sieve-community/auto-reel-edit',
    tags=["Video", "Caption", "Subtitle"],
    image=sieve.Image(
        path="logo.webp"
    ),
    readme=open("README.md", "r").read(),
)

@sieve.function(
    name="auto-reel-edit",
    system_packages=[
        "ffmpeg",
		"nodejs",
        "npm",
        "libnss3", 
        "libdbus-1-3", 
        "libatk1.0-0", 
        "libasound2", 
        "libxrandr2", 
        "libxkbcommon-dev", 
        "libxfixes3", 
        "libxcomposite1", 
        "libxdamage1", 
        "libgbm-dev", 
        "libatk-bridge2.0-0", 
	],
    python_version="3.12.3",
    python_packages=['opencv-python-headless'],
    metadata=metadata
)
def auto_reel_edit(
    file: sieve.File,
    subtitle_type: SubtitleOptions = "typing_background",
    background_media: sieve.File = sieve.File(path="redwave_background.mp4"), 
    ):
    """
    Enhance a 9:16 reel video by updating the background and incorporating captions for better engagement.

    :param file: The 9:16 reel for editing
    :param subtitle_type: The style of the subtitle
    :param background_media: The image or video to use in the background
    :return: The edited video
    """
    
    print("Starting...")

    original_directory = os.getcwd()
    os.chdir("captions")

    """
    Run `npm i` to install packages and start the remotion server with `node server.js`.
    Ensure it's fully running before sending a POST request to the Remotion server.    
    These commands can be run asynchronously if you can ensure the server starts before the POST request to it is made.
    """

    npm_process = subprocess.Popen(["npm", "i"]) # asynchronous
    npm_process.wait() # Makes it synchronous
    print("NPM install completed")

    server_process = start_remotion_server(["node", "server.js"], "Server is running!")
    print("Remotion server started and running in the background")

    os.chdir(original_directory)
    transcribe = sieve.function.get("sieve/transcribe")
    background_removal = sieve.function.get("sieve/background-removal")

    transcription_output = transcribe.push(file, backend = "stable-ts-whisper-large-v3-turbo", word_level_timestamps = True, segmentation_backend = 'none')
    print('Transcription starting...')

    background_media_path = background_media.path
    background_media_type = 'Image' if (mime := mimetypes.guess_type(background_media_path)[0]) and mime.startswith('image') else ('Video' if mime and mime.startswith('video') else 'Unknown')
    
    if background_media_type == 'Image':
        background_media_file = crop_image_vertical(background_media_path)
    elif background_media_type == 'Video':
        background_media_file = crop_video_vertical(background_media_path)

    print("background_media_file", background_media_file)
    background_removal_output = background_removal.push(
        file,
        backend="parallax",
        background_media=sieve.File(path = background_media_file),
        output_type="masked_frame",
        video_output_format="mp4",
        vanish_allow_scene_splitting=True
    )
    
    print('Changing up the background...')
    
    transcript = next(transcription_output.result())
    print('Transcription completed')

    background_removal_output_object = next(background_removal_output.result())
    print('Background change completed')

    video_file = background_removal_output_object.path
    original_fps = get_fps(video_file)
    fps = int(original_fps)
    duration = int(get_duration(video_file) * fps)

    if subtitle_type == "glowing":
        data_subtitles = prepare_transcript_word_list(transcript = transcript, fps = fps, max_subtitle_words = 2, max_subtitle_words_overlap = 0.6, max_subtitle_characters = 12)
    if subtitle_type == "background_tracking":
        data_subtitles = prepare_transcript_words_list(transcript = transcript, fps = fps, max_subtitle_words = 3, max_subtitle_words_overlap = 1, max_subtitle_characters = 18)
    if subtitle_type == "color_tracking":
        data_subtitles = prepare_transcript_words_list(transcript = transcript, fps = fps, max_subtitle_words = 4, max_subtitle_words_overlap = 2, max_subtitle_characters = 20)
    if subtitle_type == "typing_background":
        data_subtitles = prepare_transcript_words_list(transcript = transcript, fps = fps, max_subtitle_words = 6, max_subtitle_words_overlap = 2.5, max_subtitle_characters = 28)
    print(f"Chosen subtitle style is {subtitle_type}")

    payload = {
        "video_file" : os.path.basename(video_file),
        "fps" : fps,
        "durationInFrames" : duration,
        "data_subtitles" : data_subtitles,
        "subtitle_type" : subtitle_type,       
    }

    remotion_folder = 'captions'
    remotion_bundle_folder = f"{remotion_folder}/bundle/public/"
    os.makedirs(remotion_bundle_folder, exist_ok=True)
    shutil.move(background_removal_output_object.path, remotion_bundle_folder)
    
    # Make post request to remotion server
    headers = {
        "Content-Type": "application/json"
    }
    url = "http://localhost:4505/caption-video"

    print("Remotion server called")
    response = requests.post(url=url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Request captioning successful")
        print("Reel creation completed")
        return sieve.File(path = f"{remotion_folder}/{response.json().get('outputLocation')}")
    else:
        print(f"Remotion captioning failed {response.status_code}")
        print(response.text)
        print("Reel captioning failed")
    return sieve.File(path = video_file)

if __name__ == "__main__":
    print("Edited Reel:", auto_reel_edit(file=sieve.File(path="TEST.mp4"), subtitle_type="typing_background", background_media=sieve.File(path="redwave_background.mp4")))