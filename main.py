import asyncio
import time
import random

from utils.constants import vals
from utils.plot import Plot
from utils.body import Vector, Body, center_of_mass
from utils.color import gen_color
import cProfile

from utils.render import frame_renderer

import threading

center = 0

# bodies = [
#     Body(1e10, 5, [0, 0, 100], [.3, .5, 0], gen_color(), 'A', hash=str(random.getrandbits(128))),
#     Body(1e10, 5, [100, 200, 100], [-.8, 0, 0], gen_color(), 'B', hash=str(random.getrandbits(128))),
#     Body(1e10, 5, [50, 100, 200], [-4, 4, 0], gen_color(), 'C', hash=str(random.getrandbits(128))),
#     # Body(1e10, 5, [150, 110, 100], [.5, 4, 0], gen_color(), 'D'),
# ]

bodies = [
    Body(1e10, 1, [-15, 0, 0], [0, -4, 0], gen_color(), 'A', hash=str(random.getrandbits(128))),
    Body(1e10, 1, [-50, 10, 0], [12, 0, 0], gen_color(), 'B', hash=str(random.getrandbits(128))),
    Body(1e10, 1, [50, 10, 0], [-4, -8, 0], gen_color(), 'C', hash=str(random.getrandbits(128))),
]  # CHAOS

# bodies = [
#     Body(5e5, .1, [0, 0, 0], [-2 * 1, -.2 * 1, 0], gen_color(), 'A'),
#     Body(5e5, .1, [1, 0, 0], [1, 1, 0], gen_color(), 'B'),
#     Body(5e5, .1, [-1, 0, 0], [1, 1, 0], gen_color(), 'C'),
# ]

# bodies = [
#     Body(5.972e24, 6.371e6, [center, center, 0], [0, 0, 0], (0, 0, 255), 'Earth'),
#     Body(7.34767309e22, 1.737e6, [center + 3.84e8, center, 0], [0, 1020, 0], (255, 255, 255),
#          'Moon'),
#     # Body(1.989e30, 6.957e8, [center + 1.496e11, center, 0], [0, 0, 0], (255, 255, 0), 'Sun'),
# ]  # Earth Moon System

plot = Plot(vals.screen_size, vals.screen_size)
renderer = frame_renderer(bodies, plot)


async def calc():
    while True:
        await renderer.calc_next_frame()


async def render():
    while True:
        await asyncio.gather(
            renderer.render_current_frame(),
            renderer.calc_next_frame()
        )

# loop = asyncio.get_event_loop()
# loop.create_task(calc())
# loop.create_task(render())
# loop.run_forever()

asyncio.run(render())