from argparse import ArgumentParser
import os
import sys
import subprocess
import time

import numpy as np
import cv2

sys.path.append(os.path.abspath("/home/jetbot/jetbot"))
from jetbot import Camera

camera = Camera.instance()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("command")
    parser.add_argument("image_path")
    return parser.parse_args()


def process_photo(command, image_path):
    image = camera.value
    image = np.array(image)
    print(image)
    cv2.imwrite(image_path, image)
    print("written")
    if command == "Detect":
        subprocess.call(
            [
                "python",
                "smallcarbot/utils/detect.py",
                f"{image_path}",
                '"smallcar/tmp/"',
                "--model",
                "yolov8n.pt",
            ]
        )
    return image_path


def main():
    args = parse_args()
    process_photo(args.command, args.image_path)


if __name__ == "__main__":
    main()
