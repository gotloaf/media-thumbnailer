# media-thumbnailer

`media-thumbnailer` is a CLI tool that produces a grid of thumbnails for a media file in a similar manner to a [contact print](https://en.wikipedia.org/wiki/Contact_print).

![Demo of a thumbnail grid image](.github/artefacts/demo.png)

## Prerequisites

`media-thumbnailer` requires FFmpeg and FFprobe to be installed and available on your system so that it can handle a wide array of multimedia content. It's available via standard package managers on Linux (e.g. `apt` or `pacman`) or macOS (e.g. `brew`), and on Windows it is available via Chocolatey and `winget`.
If the above options do not work, or you need support for a different platform, you can check for available FFmpeg builds on their [website](https://www.ffmpeg.org/download.html).


## Installation

To install from PyPI:
```bash
pip install -U media-thumbnailer
```

To install for development and testing purposes, either install directly via git:
```bash
pip install -U "media-thumbnailer @ git+https://github.com/gotloaf/media-thumbnailer@main"
```

Or, clone the repository and install in editable mode:
```bash
git clone https://github.com/gotloaf/media-thumbnailer.git
cd media-thumbnailer
pip install -U -e .
```

## Usage

You can use the utility like so:
```bash
media_thumbnailer video.mp4 --output grid.png
```

There are more arguments available:

> #### `--output`
> Location of the file to output to, as PNG. You can pass `-` to have the image sent to stdout instead.
>
> #### `--include-info`/`--exclude-info`
> Whether to include the media summary text at the top or not. Defaults to including it.
>
> #### `--include-head`/`--exclude-head`
> Whether to include the first frame of the video in the grid. Defaults to including it.
>
> #### `--include-tail`/`--exclude-tail`
> Whether to include the last frame of the video in the grid. Defaults to excluding it.
>
> #### `--column-count`
> How many columns to include in the grid. The number of thumbnails is calculated automatically based on the row and column count.
>
> #### `--row-count`
> How many rows to include in the grid. The number of thumbnails is calculated automatically based on the row and column count.
>
> #### `--padding`
> Padding in pixels around the video frames and summary text.
>
> #### `--font-size`
> Font size in pixels to use for the summary and timestamp text.

## Acknowledgements

To guarantee consistent font rendering, `media-thumbnailer` includes a copy of [Iosevka Extended Extrabold](https://fontlibrary.org/en/font/iosevka-extended), which is licensed under the OFL (SIL Open Font License).
