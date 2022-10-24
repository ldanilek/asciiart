from PIL import Image
import numpy as np
        
def pixel_repr(p):
    return [p[0], p[1], p[2]]

def parse_image(im):
    pix = im.load()
    return np.array(
        [
            [pixel_repr(pix[x, y]) for x in range(im.size[0])]
            for y in range(im.size[1])
        ],
        np.int8
    )
