import math
import os
import random
import shutil
from itertools import zip_longest

import numpy as np

import painter

from PyQt5.QtGui import QColor, QPen, QPixmap
from PyQt5.QtCore import QPointF, QRect

from analyser import get_sound_data
from utils import Perlin2D, QColor_HSV, save
from PIL import Image

MUSIC_FILE = "./songs/Ekonopolis - Another Landscape.wav"


def draw(width, height, color=200, backgroundColor=(0, 0, 0), perlinFactorW=2, perlinFactorH=2, step=0.001):
    seed = random.randint(0, 100000000)

    p = painter.Painter(width, height)

    # Allow smooth drawing
    p.setRenderHint(p.Antialiasing)

    # Draw the background color
    p.fillRect(0, 0, width, height, QColor(*backgroundColor))

    # Set the pen color
    r, g, b = generate_color()
    p.setPen(QPen(QColor(r, g, b, 5), 2))

    print('Creating Noise...')
    p_noise = Perlin2D(width, height, perlinFactorW, perlinFactorH)
    print('Noise Generated!')

    MAX_LENGTH = 2 * width
    STEP_SIZE = step * max(width, height)
    NUM = int(width * height / 100)
    POINTS = [(random.randint(0, width - 1), random.randint(0, height - 1)) for i in range(NUM)]

    for k, (x_s, y_s) in enumerate(POINTS):
        print(f'{100 * (k + 1) / len(POINTS):.1f}'.rjust(5) + '% Complete', end='\r')

        # The current line length tracking variable
        c_len = 0

        # Actually draw the flow field
        while c_len < MAX_LENGTH:
            # Set the pen color for this segment
            sat = 200 * (MAX_LENGTH - c_len) / MAX_LENGTH
            hue = (color + 130 * (height - y_s) / height) % 360
            p.setPen(QPen(QColor_HSV(hue, sat, 255, 20), 2))

            # angle between -pi and pi
            angle = p_noise[int(x_s), int(y_s)] * math.pi

            # Compute the new point
            x_f = x_s + STEP_SIZE * math.cos(angle)
            y_f = y_s + STEP_SIZE * math.sin(angle)

            # Draw the line
            p.drawLine(QPointF(x_s, y_s), QPointF(x_f, y_f))

            # Update the line length
            c_len += math.sqrt((x_f - x_s) ** 2 + (y_f - y_s) ** 2)

            # Break from the loop if the new point is outside our image bounds
            # or if we've exceeded the line length; otherwise update the point
            if x_f < 0 or x_f >= width or y_f < 0 or y_f >= height or c_len > MAX_LENGTH:
                break
            else:
                x_s, y_s = x_f, y_f

    save(p, fname=f'image_{seed}', folder='./img', overwrite=True)


def round_int(x):
    if x in [float("-inf"), float("inf")]: return float("nan")
    return int(round(x))


def generate_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    rgb = [r, g, b]
    print("color: ", rgb)
    return rgb


if __name__ == '__main__':
    if os.path.isdir('img'):
        shutil.rmtree('img')
    os.mkdir('img')
    sound_data, length = get_sound_data(MUSIC_FILE)
    counter = 0
    print("DATA: ")
    print(len(sound_data))
    print("FIN DATA")
    sound_data = sound_data.tolist()
    sound_data = random.sample(sound_data, 10)
    # TODO: generer couleur en rapport avec chaleur du son (couleur froide si son froid etc)
    # TODO: generer nombre de point en fonction du tempo (bpm)

    for n1, n2 in zip_longest(sorted(sound_data), sound_data[1:]):
        print("{} / {}".format(counter, len(sound_data)))

        if n1 is None or n2 is None:
            continue

        if n1 == 0 or n2 == 0:
            continue

        if math.isnan(n1) or math.isnan(n2):
            continue

        n1 = round_int(n1)
        n2 = round_int(n2)

        counter += 1
        if counter % 2 == 0:
            continue

        color = random.randint(1, 300)
        perlinFactorW = 5
        perlinFactorH = 4
        step = random.random()

        # draw(3000, 2000, color=63, perlinFactorW=4, perlinFactorH=5, step=0.35)
        draw(3000, 2000, color=color, perlinFactorW=perlinFactorW, perlinFactorH=perlinFactorH, step=step)

    generated_arts = os.listdir('img')
    first = Image.open('img/' + generated_arts[0])

    for image in generated_arts:
        print("merging {} into  {}...".format(image, first))
        img = Image.open('img/' + image)
        img.show()
