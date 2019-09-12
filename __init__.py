#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Witold"
__version__ = "0.1.0"
__license__ = "MIT"

import argparse
import subprocess
import tempfile
from pathlib import Path

FFMPEG_PATH = Path(__file__).parent.absolute()/"bin/ffmpeg/bin/ffmpeg.exe"
def _convert_to_waveform(input_path:Path, output_path:Path=None, override=False):
    """ Convert an audio file to a waveform image
    If no output path is given, the image will be generated in the same folder as the audio file

    Parameters
    ----------
    input_path : pathlib.Path
        The path to an audio file
    output_path : pathlib.Path
        The path to the image to generate
    output_path : bool, optional
        Whether to override the img file if present

    """
    output_path = output_path or f"{input_path.parent}/{input_path.stem}.png"
    subprocess.run([
        FFMPEG_PATH, 
        "-y" if override else "-n",
        "-i", 
        str(input_path),
        "-filter_complex",
        'compand,showwavespic=s=640x640',
        "-frames:v",
        "1",
        str(output_path)
    ])

def _get_audio_files(path: Path, ext="mp3")->list:
    """Take a path and returns a list of audio files present there.
    If the path is a file, it will return a list with just the file in it.

    Parameters
    ----------
    path : pathlib.Path
        The path to an audio file or folder
    ext : str, optional
        The extensions of the audio files

    Returns
    -------
    list
        a list with path to audio file(s) in it
    """
    if path.is_file():
        return [path]
    return list(path.glob(f"*.{ext}"))

def _split_audio(input_path: Path, duration=5)->tempfile.TemporaryDirectory:
    """Take an audio file and split it into subsequences of n seconds.

    Parameters
    ----------
    input_path : pathlib.Path
        The path to an audio file
    duration : int, optional
        Duration in seconds of audio sequences

    Returns
    -------
    tempfile.TemporaryDirectory
        a path object to the temporary directory where the split audio files are
    """
    temp_dir = tempfile.TemporaryDirectory()
    subprocess.run([
        FFMPEG_PATH, 
        "-i", 
        str(input_path),
        "-f",
        'segment',
        "-segment_time",
        f"{duration}",
        f"{temp_dir.name}/{input_path.stem}%03d.mp3"
    ])
    return temp_dir


def generate_waveforms(input_path:Path, output_path:Path, override_images:bool=False):
    """Take an audio file and split it into subsequences of 5 seconds.

    Parameters
    ----------
    input_path : pathlib.Path
        The path to an audio file or a folder containing audio files
    output_path : pathlib.Path
        The path to the folder where to generate waveform images
    override_images : bool, optional
        Whether to override waveform images present in the output path

    """
    audio_files = _get_audio_files(input_path)
    for file in audio_files:
        tmp_audio_folder = _split_audio(file)
        split_audio_files = _get_audio_files(
            Path(tmp_audio_folder.name)
        )
        for split_file in split_audio_files:
            output_img = (Path(output_path)/split_file.stem.replace('.', '')).with_suffix('.png')
            print(output_img)
            _convert_to_waveform(
                input_path=split_file,
                output_path=output_img,
                override=override_images
            )
