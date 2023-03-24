# Audio Soundwave Generator

A package to convert audio file into several waveform images of specific duration.
Use ffpmeg to break mp3 in smaller mp3s and convert them into images.

## Install

### Requirements

[Ffmpeg](https://ffmpeg.org/download.html) is required to run this program.

### Install dependencies

```
pip install -r requirements.txt
```

## Usage

### CLI

```
python cli.py <input_path> <output_path>
```

> `python cli.py --help` for details

### Module

```
import pathlib
from audio_soundwave_generator import generate_waveforms

input_path = pathlib.Path(...)
output_path = pathlib.Path(...)

generate_waveforms(input_path, output_path)

```
