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
    toto = input("Enter the path to the image: ")
    toto = toto.strip('"')
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
    dada = toto
    w, h = None, None
    table = None
    if method == 'f':
        if vertical:
            for i in range(0, vertical):
                tata = VSeamCarver2(dada, ans, table, w, h, x1, y1, x2, y2)
                dada, table, w, h, x1, y1, x2, y2 = tata.removeverticalseam(tata.findvseam())

        if horizon:
            if vertical:
                dada, table = np.array(dada), np.array(table)
                dada, table = dada.swapaxes(0, 1), table.swapaxes(0, 1)
                dada, table = dada.tolist(), table.tolist()
            for i in range(0, horizon):
                tata = HSeamCarver2(dada, ans, table, w, h, x1, y1, x2, y2)
                dada, table, w, h, x1, y1, x2, y2 = tata.removeverticalseam(tata.findvseam())
            dada = np.array(dada)
            dada = dada.swapaxes(0, 1)
            dada = dada.tolist()
    else:
        if vertical:
            for i in range(0, vertical):
                tata = VSeamCarver(dada, ans, table, w, h, x1, y1, x2, y2)
                dada, table, w, h, x1, y1, x2, y2 = tata.removeverticalseam(tata.findvseam())

        if horizon:
            if vertical:
                dada, table = np.array(dada), np.array(table)
                dada, table = dada.swapaxes(0, 1), table.swapaxes(0, 1)
                dada, table = dada.tolist(), table.tolist()
            for i in range(0, horizon):
                tata = HSeamCarver(dada, ans, table, w, h, x1, y1, x2, y2)
                dada, table, w, h, x1, y1, x2, y2 = tata.removeverticalseam(tata.findvseam())
            dada = np.array(dada)
            dada = dada.swapaxes(0, 1)
            dada = dada.tolist()

    total = time() - time1
    print(str(timedelta(seconds=total)))
    rgb = np.array(dada, dtype=np.uint8)
    temp = Image.fromarray(rgb)
    if pather != "":
        temp.save(pather)
    temp.show()
