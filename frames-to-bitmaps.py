import argparse
import os
import array

from PIL import Image

def to_84x48_binary_image(filename):
    with Image.open(filename).resize((84, 48)).convert('1') as img:
        data = img.getdata()
        converted = bytearray()
        for i in range(6):
            for j in range(84):
                v = 0
                for sh in range(8):
                    b = int(bool(data[84 * 8 * i + 84 * sh + j]))
                    v = v | (b << sh)
                v = ~v & 255
                converted.append(v)

        return converted


def imgs_to_binary_file(files, outfile='bitmaps.bin'):
    outf = open(outfile, "wb")
    for file in files:
        arr = array.array('L', to_84x48_binary_image(file))
        outf.write(arr)


parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input directory')
parser.add_argument('--out', help='output file', default='bitmaps.bin')
args = parser.parse_args()

filenames = sorted(os.path.join(args.input, f) for f in os.listdir(args.input) if os.path.isfile(os.path.join(args.input, f)))
name = os.path.basename(args.out)
name = name[:name.find('.')]
imgs_to_binary_file(filenames, args.out)
