# -*- coding: utf-8 -*-
"""
media_thumbnailer.__main__
=====

This is the implementation of the main CLI, and where the image compositing occurs.

"""

import io
import pathlib

import click
from PIL import Image, ImageDraw, ImageFont

from .formatting import format_duration, format_video_info
from .probing import check_video_info, extract_video_frame


@click.command()
@click.argument('filename', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', '-o', type=click.File('wb'))
@click.option('--include-info/--exclude-info', '/-e', default=True)
@click.option('--include-head/--exclude-head', default=True)
@click.option('--include-tail/--exclude-tail', default=False)
@click.option('--column-count', '--col', '-c', default=4, type=click.IntRange(1, 16))
@click.option('--row-count', '--row', '-r', default=4, type=click.IntRange(1, 16))
@click.option('--padding', default=16, type=click.IntRange(0, max_open=True))
@click.option('--font-size', default=32, type=click.IntRange(8, max_open=True))
def main(
    filename: str,
    output: io.BytesIO,
    include_info: bool = True,
    include_head: bool = True,
    include_tail: bool = False,
    column_count: int = 4,
    row_count: int = 4,
    padding: int = 16,
    font_size: int = 32,
):
    """
    Generates a grid of thumbnails for a multimedia file in a similar form to a contact print.

    For a visual representation of what the arguments do, check out the README:
    https://github.com/gotloaf/media-thumbnailer/blob/main/README.md
    """

    filename = pathlib.Path(filename)

    video_info = check_video_info(filename)
    summary = format_video_info(filename, video_info)

    font = ImageFont.truetype('arial.ttf', font_size, encoding='unic')

    width = padding + ((video_info.width + padding) * column_count)
    line_count = len(summary.split('\n'))

    if include_info:
        top_of_contact_print = padding + (font_size * line_count) + padding
    else:
        top_of_contact_print = padding

    height = top_of_contact_print + ((video_info.height + padding) * row_count)

    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    if include_info:
        draw.text((padding, padding), text=summary, font=font, fill=(0, 0, 0))

    # Calculate the timestamps to clip video content from
    thumbnail_count = row_count * column_count
    thumbnail_times = [
        video_info.duration * ((i if include_head else i + 1) / (thumbnail_count + (0 if include_head else 1) - (1 if include_tail else 0)))
        for i in range(thumbnail_count)
    ]

    for index, time in enumerate(thumbnail_times):
        row = index // column_count
        column = index % column_count

        video_frame_data = extract_video_frame(filename, time)
        frame = Image.open(io.BytesIO(video_frame_data))

        left = padding + (column * (padding + video_info.width))
        top = top_of_contact_print + (row * (padding + video_info.height))

        # Paste it in place
        image.paste(frame, (left, top))

        # Draw timestamp on top
        stroke_width = font_size / 4
        draw.text(
            (left + video_info.width - stroke_width, top + video_info.height - stroke_width),
            text=format_duration(time),
            font=font,
            fill=(255, 255, 255),
            stroke_width=stroke_width,
            stroke_fill=(0, 0, 0),
            anchor='rs'
        )

    output_data = io.BytesIO()
    image.save(output_data, format='png')
    output_data.seek(0)

    output.write(output_data.read())


if __name__ == '__main__':
    main()
