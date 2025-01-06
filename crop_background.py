import subprocess
import cv2

def crop_video_vertical(file_path):
    """
    Crop video into 9:16 aspect ratio.
    """

    ffprobe_cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        file_path
    ]
    result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise ValueError(f"Error getting video info: {result.stderr}")

    width, height = map(int, result.stdout.strip().split(","))

    if abs(width / height - 9 / 16) < 0.01:
        return file_path

    new_width = min(width, height * 9 // 16)
    new_height = min(height, width * 16 // 9)

    x_offset = (width - new_width) // 2
    y_offset = (height - new_height) // 2
    output_file = "background.mp4"
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", file_path,
        "-vf", f"crop={new_width}:{new_height}:{x_offset}:{y_offset}",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-strict", "experimental",
        output_file
    ]

    result = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise ValueError(f"Error processing video: {result.stderr}")

    return output_file


def crop_image_vertical(image_path):
    """
    Crop image into 9:16 aspect ratio.
    """
    image = cv2.imread(image_path)
    
    height, width = image.shape[:2]
    
    if width / height == 9 / 16:
        return image_path
    
    new_width = int(height * 9 / 16)
    
    start_x = (width - new_width) // 2
    start_y = 0
    
    cropped_image = image[start_y:start_y + height, start_x:start_x + new_width]
    
    output_path = "background.png"
    cv2.imwrite(output_path, cropped_image)
    
    return output_path