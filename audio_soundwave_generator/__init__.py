#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Witold Wroblewski"
__version__ = "0.1.0"
__license__ = "MIT"

import tempfile
from pathlib import Path
import ffmpeg


def _convert_to_waveform(input_path: Path, output_path: Path = None, override=False):
    """Convert an audio file to a waveform image
    If no output path is given, the image will be generated in the same folder as the audio file

    Parameters
    ----------
    input_path : pathlib.Path
        The path to an audio file
    output_path : pathlib.Path
        The path to the image to generate
    override : bool, optional
        Whether to override the img file if present

    """
    output_path = output_path or f"{input_path.parent}/{input_path.stem}.png"
    cmd = (
        ffmpeg.input(str(input_path))
        .filter("compand", gain=5)
        .filter("showwavespic", s="640x640")
        .output(str(output_path), vframes=1)
    )
    if override:
        cmd.overwrite_output()
    cmd.run(capture_stdout=True, capture_stderr=True)


def _get_audio_files(path: Path, ext="mp3") -> list:
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


def _split_audio(input_path: Path, duration=5) -> tempfile.TemporaryDirectory:
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
    (
        ffmpeg.input(str(input_path))
        .output(
            f"{temp_dir.name}/{input_path.stem}%03d.mp3",
            format="segment",
            segment_time=duration,
        )
        .run()
    )
    return temp_dir


def generate_waveforms(
    input_path: Path,
    output_path: Path,
    waveform_duration=5,
    override_images: bool = False,
):
    """Take an audio file and split it into subsequences of 5 seconds.

    Parameters
    ----------
    input_path : pathlib.Path
        The path to an audio file or a folder containing audio files
    output_path : pathlib.Path
        The path to the folder where to generate waveform images
    waveform_duration : int
        Waveform duration in seconds.
    override_images : bool, optional
        Whether to override waveform images present in the output path

    """
    audio_files = _get_audio_files(input_path)
    for file in audio_files:
        tmp_audio_folder = _split_audio(file, waveform_duration)
        split_audio_files = _get_audio_files(Path(tmp_audio_folder.name))
        for split_file in split_audio_files:
            output_img = (
                Path(output_path) / split_file.stem.replace(".", "")
            ).with_suffix(".png")
            _convert_to_waveform(
                input_path=split_file, output_path=output_img, override=override_images
            )
