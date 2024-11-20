# -*- coding: utf-8 -*-
"""
media_thumbnailer.probing
=====

This module handles probing data from multimedia files.

"""

import dataclasses
import json
import pathlib
import subprocess


@dataclasses.dataclass
class VideoInfo:
    """
    A class that represents information probed from a multimedia file.
    This info is used to decide what frames to extract and what info to display on the final image.
    """

    width: int
    """Width of the video frame in integer pixels"""

    height: int
    """Height of the video frame in integer pixels"""

    duration: float
    """Duration in seconds"""

    codec_name: str
    """Name of the video codec used"""

    container_name: str
    """Name of the container format used"""

    size: int
    """Size of the multimedia file in bytes"""

    fps: float
    """Framerate of the video in frames per second."""


def check_video_info(
    path: pathlib.Path,
    video_stream_index: int = 0
) -> VideoInfo:
    """
    Takes in a path to a video file and returns info about the video contained within.

    Parameters
    ----------
    path: pathlib.Path
        Path to the video file to get metrics for.
    video_stream_index: int
        Which of the video streams in the file to use. Defaults to 0

    Returns
    -------
    VideoInfo
        The width and height of the video in integer pixels, and the length in seconds as a float.
    """

    ffprobe_output = subprocess.check_output(
        ('ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', str(path)),
        timeout=5
    )

    ffprobe_output = json.loads(ffprobe_output)

    video_streams = [stream for stream in ffprobe_output['streams'] if stream['codec_type'] == 'video']

    if not video_streams:
        raise RuntimeError("File selected has no video streams.")

    if len(video_streams) <= video_stream_index:
        raise RuntimeError(f"Video stream index {video_stream_index} was requested but the file only has {len(video_streams)} video stream(s).")

    video_stream = video_streams[video_stream_index]

    rate, base = video_stream['r_frame_rate'].split('/')
    if float(base) == 0:
        fps = float(rate)
    else:
        fps = float(rate) / float(base)

    return VideoInfo(
        width=int(video_stream['width']),
        height=int(video_stream['height']),
        duration=float(video_stream['duration']),
        codec_name=video_stream['codec_long_name'],
        container_name=ffprobe_output['format']['format_long_name'],
        size=int(ffprobe_output['format']['size']),
        fps=fps
    )


def extract_video_frame(
    path: pathlib.Path,
    time: float
):
    """
    Pulls out a single video frame from an input video at the given timestamp.

    Parameters
    ----------
    path: pathlib.Path
        Path to the video file to get the frame from.
    time: float
        The time in seconds, from which to extract the frame.

    Returns
    -------
    bytes
        A byte string containing the frame encoded as PNG data.
    """

    ffmpeg_output = subprocess.check_output(
        ('ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', f"{time:.2f}", '-i', str(path), '-vframes', '1', '-c:v', 'png', '-f', 'image2pipe', '-'),
        timeout=5
    )

    return ffmpeg_output
