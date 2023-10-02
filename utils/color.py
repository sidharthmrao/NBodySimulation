import random


def gen_color():
    """
    Generates a random color
    :return: Random color as a (r, g, b) tuple, 0-255
    """
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def complementary_color(color):
    """
    Returns the complementary color of the given color.
    :param color: Color as a (r, g, b) tuple, 0-255
    :return: Complementary color as a (r, g, b) tuple, 0-255
    """
    if color[0] + color[1] + color[2] > 255 * 3 / 2:
        return 0, 0, 0
    else:
        return 255, 255, 255
