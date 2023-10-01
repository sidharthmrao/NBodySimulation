import random


def gen_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def opposite_color(color):
    if color[0] + color[1] + color[2] > 255 * 3 / 2:
        return 0, 0, 0
    else:
        return 255, 255, 255
