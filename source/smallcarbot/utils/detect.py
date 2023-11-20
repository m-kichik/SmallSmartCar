from ultralytics import YOLO
from PIL import Image

import argparse

def make_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('save_dir')
    parser.add_argument(
        '-m', '--model',
        default='yolov8n.pt'
    )
    return parser


def main(args):
    model = YOLO(args.model)
    img = Image.open(args.source)
    results = model.predict(source=img, stream=True)
    for detection in results:
        print(detection)

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    main(args)