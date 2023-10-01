import time
import random

from utils.constants import vals
from utils.plot import Plot
from utils.body import Vector, Body, center_of_mass
from utils.color import gen_color

center = 0

bodies = [
    Body(1e10, 5, [0, 0, 100], [.3, .5, 0], gen_color(), 'A'),
    Body(1e10, 5, [100, 200, 100], [-.8, 0, 0], gen_color(), 'B'),
    Body(1e10, 5, [50, 100, 200], [-4, 4, 0], gen_color(), 'C'),
    # Body(1e10, 5, [150, 110, 100], [.5, 4, 0], gen_color(), 'D'),
]

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

vals.trails = {body.name: ([], body.color) for body in bodies}
vals.trails['CM'] = ([], (255, 0, 0))

vals.pixel_scale = 5 / bodies[0].radius
vals.pixel_scale = 100 / (bodies[0].position - bodies[1].position).magnitude()

plot = Plot(vals.screen_size, vals.screen_size)


def check_collision(bodies):
    for body in bodies:
        for other in bodies:
            if body != other and (
                    body.position - other.position).magnitude() <= body.radius + other.radius:
                print('collision')
                bodies.remove(body)
                bodies.remove(other)

                new_body = Body(
                    body.mass + other.mass,
                    ((body.radius + other.radius) + (body.radius if body.mass > other.mass else
                                                     other.radius)) / 2,
                    center_of_mass([body, other]).vec,
                    [0 for _ in body.position.vec],
                    body.color if body.mass > other.mass else other.color,
                    body.name if body.mass > other.mass else other.name
                )

                momentum = body.velocity * body.mass + other.velocity * other.mass
                new_body.velocity = momentum / new_body.mass

                bodies.append(new_body)
                break


def update(bodies, iterations):
    for _ in range(iterations):
        for _ in range(len(bodies)):
            check_collision(bodies)

        for body in bodies:
            body.update_velocity(bodies)

        for body in bodies:
            body.update_position()


while True:
    start = time.time()

    update(bodies, iterations=int(vals.simulation_seconds_per_iter / vals.time_per_iter))

    plot.clear()

    for i, body in enumerate(bodies):
        plot.draw_body(body)

        if vals.trail:
            vals.trails[body.name][0].append(body.position.vec)
            if len(vals.trails[body.name][0]) > vals.trail_length:
                vals.trails[body.name][0].pop(0)

    if vals.trail:
        for trail in vals.trails.values():
            plot.draw_trail(trail[0], trail[1])

    cm = center_of_mass(bodies)
    vals.trails['CM'][0].append(cm.vec)
    plot.draw_point(plot.window, cm, 2 * (1 / vals.pixel_scale), (255, 0, 0))
    plot.draw_trail(vals.trails['CM'][0], vals.trails['CM'][1])

    plot.draw_text(f'TIME STEP: {vals.simulation_seconds_per_iter}', 10 * (1 / vals.pixel_scale),
                   (60 / vals.pixel_scale, 10 / vals.pixel_scale), (255, 255, 255))
    plot.draw_text(f'PRECISION: {vals.dT}', 10 / vals.pixel_scale,
                   (60 / vals.pixel_scale, 20 / vals.pixel_scale), (255, 255, 255))

    plot.main_routine()
    plot.update()

    diff = time.time() - start
    time.sleep(vals.time_per_iter - diff if diff < vals.time_per_iter else 0)
