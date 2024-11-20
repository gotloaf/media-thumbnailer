# -*- coding: utf-8 -*-
"""
media_thumbnailer.formatting
=====

This module handles formatting of text information

"""

import math
import pathlib

from .probing import VideoInfo


def format_size(size: int) -> str:
    """
    Formats a size in bytes to be in human readable units.

    Parameters
    ----------
    size: int
        The size to format in bytes.

    Returns
    -------
    str
        A string representing the size (e.g. 12.00 KiB)
    """

    units = (
        'B', 'KiB', 'MiB', 'GiB', 'TiB'
    )

    which_unit = int(min(math.log(max(1, size), 1024), len(units) - 1))
    value = size / (1024.0 ** which_unit)

    return f"{value:.2f} {units[which_unit]}"


def format_duration(duration: float) -> str:
    """
    Formats a duration in seconds to be in human readable units.

    Parameters
    ----------
    duration: float
        The duration to format in seconds.

    Returns
    -------
    str
        A string representing the duration (e.g. 12:04.35)
    """

    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02.0f}:{minutes:02.0f}:{seconds:05.2f}"


def format_video_info(
    filename: pathlib.Path,
    info: VideoInfo
) -> str:
    """
    Takes in the path and info from a video file and creates summary text.

    Parameters
    ----------
    filename: pathlib.Path
        Path to the video file to format info for.
    info: VideoInfo
        Data of the video to represent.

    Returns
    -------
    str
        A multiline string summarizing the multimedia.
    """

    return '\n'.join([
        f"Filename: {filename.name}",
        f"Size: {format_size(info.size)} ({info.size:,} bytes)",
        f"Container: {info.container_name}",
        f"Codec: {info.codec_name}",
        f"Resolution: {info.width}x{info.height}",
        f"Framerate: {info.fps:.2f} fps",
        f"Duration: {format_duration(info.duration)}",
    ])
