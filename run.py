import argparse
import os, errno
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import random as rnd

from load_data import load_hangul, load_num, load_fonts
from data_generator import data_generator

def margins(margin):
    margins = margin.split(",")
    if len(margins) == 1:
        return [margins[0]] * 4
    return [int(m) for m in margins]


def parse_arguments():
    """
        Parse the command line arguments of the program.
    """

    parser = argparse.ArgumentParser(
        description="Generate synthetic text dicts for text recognition."
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        help="The output directory",
        default="out/"
    )
    parser.add_argument(
        "-n",
        "--num",
        type=int,
        help="The number of images to be created.",
        default=3
    )
    parser.add_argument(
        "-t",
        "--license_plate_type",
        type=int,
        help="Setting license plate type"
             "0: type 1, 1: type 2, .. 6: all of them",
        default=0
    )
    parser.add_argument(
        "-a",
        "--augmentation",
        type=int,
        help="Setting data augmentation options for skewing, distortion, blurring and brightness"
             "0: no use, 1: skewing, 2: distortion, 3: blurring, 4: brightness, 5: all of them",
        default=1
    )

    parser.add_argument(
        "-hf",
        "--hangul_file",
        type=str,
        help="hangul label file",
        default="kr.txt"
    )
    parser.add_argument(
        "-nf",
        "--number_file",
        type=str,
        help="number label file",
        default="num.txt"
    )
    parser.add_argument(
        "-ff",
        "--font_file",
        type=str,
        help="Font file location for character creation",
        default="data/fonts/"
    )
    parser.add_argument(
        "-tf",
        "--text_format",
        type=int,
        help="Define the height of the produced images if horizontal",
        default=32
    )
    parser.add_argument(
        "-fr",
        "--format_ratio",
        type=float,
        help="Ratio of decreasing the size of hangul",
        default=0.9
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        help="Define the extension to save the image with",
        default="jpg"
    )
    parser.add_argument(
        "-sw",
        "--space_width",
        type=float,
        nargs="?",
        help="Define the width of the spaces between words. 2.0 means twice the normal space width",
        default=1
    )
    parser.add_argument(
        "-cs",
        "--character_spacing",
        type=int,
        nargs="?",
        help="Define the width of the spaces between characters. 2 means two pixels",
        default=3
    )
    parser.add_argument(
        "-r",
        "--radius",
        type=int,
        help="Setting background rounded corner size",
        default=5
    )
    parser.add_argument(
        "-m",
        "--margins",
        type=margins,
        nargs="?",
        help="Define the margins around the text when rendered. In pixels",
        default=(5, 15, 5, 15)
    )
    return parser.parse_args()


def main():
    # Argument parsing
    args = parse_arguments()

    # Create the directory if it does not exist.
    os.makedirs(args.output_dir, exist_ok=True)

    # Creating hangul list
    hangul_list = load_hangul(args.hangul_file)

    # Creating number list
    num_list = load_num(args.number_file)

    # Create font path list
    font_list = load_fonts(args.font_file)

    license_plate_len = 6

    for i in range(args.num):
        data_generator(
            i,
            hangul_list,
            num_list,
            font_list[rnd.randrange(0, len(font_list))],
            args.output_dir,
            args.text_format,
            args.format_ratio,
            rnd.randrange(0, license_plate_len) if args.license_plate_type == 6 else args.license_plate_type,
            args.extension,
            args.space_width,
            args.character_spacing,
            args.radius,
            args.margins
        )
        print()

if __name__ == "__main__":
    main()
