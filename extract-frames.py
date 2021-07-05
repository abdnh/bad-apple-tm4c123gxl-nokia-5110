import argparse
import os

import cv2

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input video', required=True)
parser.add_argument('--out', help='output directory', default='frames')
parser.add_argument('--frame-per-second', help='the number of frames to extract from the input video per second', default=20)
args = parser.parse_args()

if not os.path.exists(args.out):
    os.mkdir(args.out)

frame_per_second = float(args.frame_per_second)

vidcap = cv2.VideoCapture(args.input)
success, image = vidcap.read()
count = 1
while success:
    cv2.imwrite(os.path.join(args.out, f"{count:04}.jpg"), image)
    vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000 / frame_per_second))
    success, image = vidcap.read()
    count += 1
