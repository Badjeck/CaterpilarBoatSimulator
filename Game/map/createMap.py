import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)
f = open("map.txt", "a")


x, y = np.arange(500), np.arange(500)
xpix, ypix = 500, 500
pic = []

for i in x:
    if i % 500 == 0:
        print(i)
    row = []
    for j in y:
        noise_val =         noise1([i/xpix, j/ypix])
        noise_val += 1  * noise2([i/xpix, j/ypix])
        noise_val += 0.5 * noise3([i/xpix, j/ypix])
        noise_val += 0.25* noise4([i/xpix, j/ypix])
        oui = round(((noise_val+1)*100)/2)
        if oui <= 20:
            #marrai
            f.write("0")
        elif oui > 20 and oui < 30:
            #marrai mais pas trop
            f.write("1")
        elif oui > 30 and oui <= 40:
            #foret mais pas trop
            f.write("2")
        elif oui > 40 and oui <=50:
            #foret profonde
            f.write("3")
        elif oui > 50 and oui <=60:
            #foret bien profonde
            f.write("4")
        elif oui > 50 and oui <=60:
            #debut montagne
            f.write("5")
        elif oui > 60 and oui <=70:
            #montagne
            f.write("6")
        elif oui > 70 and oui <=80:
            #grosse montagne
            f.write("7")
        else:
            #sommet
            f.write("8")        
    f.write("\n")

f.close()
