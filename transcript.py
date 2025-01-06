import cv2

def get_fps(video_path: str) -> float:
    """
    Returns the frames per second (FPS) of a video.
    
    :param video_path: Path to the video file.
    :return: FPS value as a float.
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps

def get_duration(video_path: str) -> float:
    """
    Returns the duration of a video in seconds.
    
    :param video_path: Path to the video file.
    :return: Duration of the video in seconds.
    """
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        raise ValueError(f"Unable to open video file: {video_path}")
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    video.release()
    if fps == 0:
        raise ValueError("FPS value is zero, cannot calculate duration.")
    duration = frame_count / fps
    return duration

def merge_consecutive_subtitles_word_list(subtitles, max_subtitle_words, max_subtitle_words_overlap, max_subtitle_characters):
    """
    Merge consecutive words into a new string.
    """
    merged_data = []
    current_segment = subtitles[0]
    consecutive_count = 1

    for i in range(1, len(subtitles)):
        next_segment = subtitles[i]

        if (next_segment['start'] - current_segment['start'] <= max_subtitle_words_overlap and 
            len(current_segment['word'] + " " + next_segment['word']) <= max_subtitle_characters and 
            consecutive_count < max_subtitle_words and
            not current_segment['word'].strip().endswith('.')):
            # End timestamp of the last merged word is the new end timestamp of the new caption object
            current_segment['end'] = next_segment['end']
            current_segment['word'] += f" {next_segment['word']}"
            consecutive_count += 1
        else:
            merged_data.append(current_segment)
            current_segment = next_segment
            consecutive_count = 1

    merged_data.append(current_segment)
    return merged_data

def prepare_transcript_word_list(transcript, fps, max_subtitle_words, max_subtitle_words_overlap, max_subtitle_characters):
    """
    Organize the transcript into a list of caption strings for remotion captioning.
    """
    subtitles = []
    for segment in transcript['segments']:
        for segment_word in segment['words']:
            subtitles.append(segment_word)
            
    subtitles = merge_consecutive_subtitles_word_list(subtitles, max_subtitle_words, max_subtitle_words_overlap, max_subtitle_characters)

    # convert subtitles timestamps into frames
    subtitles_in_frames = []
    for subtitle in subtitles:
        temp = {
            'start': int(subtitle['start'] * fps),
            'end': int(subtitle['end'] * fps),
            'word': subtitle['word'].strip()
        }
        subtitles_in_frames.append(temp)

    return subtitles_in_frames

def merge_consecutive_subtitles_words_list(subtitles, max_subtitle_words, max_subtitle_words_overlap, max_subtitle_characters):
    """
    Merge consecutive words into a sublist.
    """
    merge_consecutive_subtitles_tuples = []
    temp_tuple = []
    current_char_count = 0

    for i in range(len(subtitles)):
        word_length = len(subtitles[i]['word'])

        if (not temp_tuple or 
            (subtitles[i]['start'] - temp_tuple[-1]['start'] <= max_subtitle_words_overlap and 
             len(temp_tuple) < max_subtitle_words and 
             current_char_count + word_length <= max_subtitle_characters and 
             not temp_tuple[-1]['word'].strip().endswith('.'))):
            temp_tuple.append(subtitles[i])
            current_char_count += word_length
        else:
            merge_consecutive_subtitles_tuples.append(tuple(temp_tuple))
            temp_tuple = [subtitles[i]]
            current_char_count = word_length

    if temp_tuple:
        merge_consecutive_subtitles_tuples.append(tuple(temp_tuple))

    return merge_consecutive_subtitles_tuples

def prepare_transcript_words_list(transcript, fps, max_subtitle_words, max_subtitle_words_overlap, max_subtitle_characters):
    """
    Organize the transcript into a list of word sublists for remotion captioning.
    """
    subtitles = []
    for segment in transcript['segments']:
        for segment_word in segment['words']:
            subtitles.append(segment_word)
            
    subtitles = merge_consecutive_subtitles_words_list(subtitles, max_subtitle_words, max_subtitle_words_overlap, max_subtitle_characters)

    # convert subtitles timestamps into frames
    subtitles_in_frames = []
    for segment in subtitles:
        converted_segment = []
        for entry in segment:
            start_frame = int(entry['start'] * fps)
            end_frame = int(entry['end'] * fps)
            converted_segment.append({'start': start_frame, 'end': end_frame, 'word': entry['word'].strip()})
        subtitles_in_frames.append(list(converted_segment))
    return subtitles_in_frames