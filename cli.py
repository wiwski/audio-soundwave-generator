import argparse
import pathlib

from audio_soundwave_generator import generate_waveforms

if __name__ == "__main__":
    """This is executed when run from the command line"""
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "input",
        help="The path to an audio file or a folder containing audio files.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "output",
        help="The path to the folder where to generate waveform images.",
        type=pathlib.Path,
    )
    parser.add_argument(
        "--wave-duration",
        default=5,
        help="Chunk music every x seconds.",
    )
    parser.add_argument(
        "--override",
        action="store_true",
        default=False,
        help="Whether to override waveform images present in the output path",
    )

    args = parser.parse_args()

    generate_waveforms(args.input, args.output, args.wave_duration, args.override)
