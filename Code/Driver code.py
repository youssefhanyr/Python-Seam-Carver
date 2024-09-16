''' This is the driver code for a seam carver from scratch implemntation, what it does in short is that it compresses images
The first two seam carvers carve according to backwards energy, and the the other two to forward energy '''


from VSeamCarver2 import VSeamCarver2
from HSeamCarver2 import HSeamCarver2
from VSeamCarver import VSeamCarver
from HSeamCarver import HSeamCarver
from time import time
from PIL import Image
import numpy as np
from datetime import timedelta
from sys import setrecursionlimit


if __name__ == "__main__":
    setrecursionlimit(2500)
    path = input("Enter the path to the image: ")
    path = path.strip('"')
    horizon = int(input("Enter how much the image should be compressed by height: (0 for none)"))
    vertical = int(input("Enter how much the image should be compressed by width: (0 for none)"))
    pather = input("Enter the path to save the image(leave empty just to show) (have to save on an image file): ")
    pather = pather.strip('"')
    method = input("Forward or backwards? (f/b): ").lower()
    x1, y1, x2, y2 = input("Enter coords of excluded part(-1 for all for none)(spaces between them): ").split()

    if x1 == x2 == y1 == y2 == '-1':
        x1, x2, y1, y2 = None, None, None, None
        ans = 1
    else:
        ans = int(input("Enter the type of protection (-1 to remove part, 1 to protect part): "))
        print(ans)
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    time1 = time()
    imgfile = path                             # awful naming done by me
    w, h = None, None
    table = None
    if method == 'f':
        if vertical:
            for i in range(0, vertical):
                carver = VSeamCarver2(imgfile, ans, table, w, h, x1, y1, x2, y2)
                imgfile, table, w, h, x1, y1, x2, y2 = carver.removeverticalseam(carver.findvseam())

        if horizon:
            if vertical:
                imgfile, table = np.array(imgfile), np.array(table)
                imgfile, table = imgfile.swapaxes(0, 1), table.swapaxes(0, 1)
                imgfile, table = imgfile.tolist(), table.tolist()
            for i in range(0, horizon):
                carver = HSeamCarver2(imgfile, ans, table, w, h, x1, y1, x2, y2)
                imgfile, table, w, h, x1, y1, x2, y2 = carver.removeverticalseam(carver.findvseam())
            imgfile = np.array(imgfile)
            imgfile = imgfile.swapaxes(0, 1)
            imgfile = imgfile.tolist()
    else:
        if vertical:
            for i in range(0, vertical):
                carver = VSeamCarver(imgfile, ans, table, w, h, x1, y1, x2, y2)
                imgfile, table, w, h, x1, y1, x2, y2 = carver.removeverticalseam(carver.findvseam())

        if horizon:
            if vertical:
                imgfile, table = np.array(imgfile), np.array(table)
                imgfile, table = imgfile.swapaxes(0, 1), table.swapaxes(0, 1)
                imgfile, table = imgfile.tolist(), table.tolist()
            for i in range(0, horizon):
                carver = HSeamCarver(imgfile, ans, table, w, h, x1, y1, x2, y2)
                imgfile, table, w, h, x1, y1, x2, y2 = carver.removeverticalseam(carver.findvseam())
            imgfile = np.array(imgfile)
            imgfile = imgfile.swapaxes(0, 1)
            imgfile = imgfile.tolist()

    total = time() - time1
    print(str(timedelta(seconds=total)))
    rgb = np.array(imgfile, dtype=np.uint8)
    temp = Image.fromarray(rgb)
    if pather != "":
        temp.save(pather)
    temp.show()
