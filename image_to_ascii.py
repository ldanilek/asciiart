from PIL import Image
import re
import numpy as np
from font import parse_font, bitmap_font, parse_tff
from image import parse_image
import sys
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('image_path', type=str,
                    help='path of image to convert')
parser.add_argument('--symbols', dest='symbols', action='store_const',
                    const=True, default=False,
                    help='allow unicode symbols in addition to ascii')
parser.add_argument('--boxes', dest='boxes', action='store_const',
                    const=True, default=False,
                    help='allow unicode box symbols')

args = parser.parse_args()


bitmap = parse_font(bitmap_font)

im = Image.open(args.image_path)

def encode_image(image, bitmap):
    shape = bitmap[' '].shape
    s = ''
    # cut off image at a multiple of shape
    char_height = image.shape[0]//shape[0]
    char_width = image.shape[1]//shape[1]
    image = image[:char_height*shape[0], :char_width*shape[1]]
    extended_bitmaps = {c: np.tile(b, [char_height, char_width, 1]) for c, b in bitmap.items()}
    # compute differences with one sweep
    diffs = {c: (image - b) for c, b in extended_bitmaps.items()}
    for row in range(0, image.shape[0], shape[0]):
        for col in range(0, image.shape[1], shape[1]):
            min_norm = float('inf')
            min_char = ' '
            for c, diff in diffs.items():
                # TODO: can we do this once for the whole image?
                diff_norm = np.linalg.norm(diff[row:row+shape[0], col:col+shape[1]])
                if diff_norm < min_norm:
                    min_char = c
                    min_norm = diff_norm
            s += min_char
        s += '\n'
    return s
        


image = parse_image(im)

tff_bitmap = parse_tff(args.symbols, args.boxes)

encoded = encode_image(image, tff_bitmap)
    

print(encoded)

