# media-thumbnailer

`media-thumbnailer` is a CLI tool that produces a grid of thumbnails for a media file in a similar manner to a [contact print](https://en.wikipedia.org/wiki/Contact_print).


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

## Acknowledgements

To guarantee consistent font rendering, `media-thumbnailer` includes a copy of [Iosevka Extended Extrabold](https://fontlibrary.org/en/font/iosevka-extended), which is licensed under the OFL (SIL Open Font License).
