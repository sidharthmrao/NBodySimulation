import time
from copy import deepcopy

from utils.constants import vals
from utils.body import Body, center_of_mass, check_collision


class frame_renderer:
    def __init__(self, bodies, plot):
        self.current_frame = deepcopy(bodies)

        self.start_time = time.time()
        self.total_elapsed_time = lambda: time.time() - self.start_time

        self.current_frame_start_time = 0
        self.current_frame_time = lambda: time.time() - self.current_frame_start_time

        self.render_frame_start_time = 0
        self.render_frame_time = lambda: time.time() - self.render_frame_start_time

        self.bodies = bodies

        vals.trails = {body.hash: ([], body.color) for body in bodies}
        vals.trails['CM'] = ([], (255, 0, 0))

        vals.pixel_scale = 5 / bodies[0].radius
        vals.pixel_scale = 100 / (bodies[0].position - bodies[1].position).magnitude()

        self.plot = plot

    def update(self, iterations):
        """
        Updates the positions and velocities of the bodies.
        :param iterations: Number of iterations to run
        """
        for _ in range(iterations):
            for _ in range(len(self.bodies)):
                check_collision(self.bodies)

            for body in self.bodies:
                body.update_velocity(self.bodies)

            for body in self.bodies:
                body.update_position()

    async def wait_until(self, condition):
        while not condition():
            pass

    async def calc_next_frame(self):
        self.current_frame_start_time = time.time()

        seconds_per_frame = 1 / vals.frames_per_second
        simulation_seconds = seconds_per_frame * vals.simulation_seconds_per_real_second
        simulation_iters = simulation_seconds / vals.dT

        self.update(int(simulation_iters))

        await self.wait_until(lambda: self.current_frame_time() > 1 / vals.frames_per_second)

        self.current_frame = deepcopy(self.bodies)

    async def render_current_frame(self):
        self.render_frame_start_time = time.time()

        self.plot.clear()

        # Draw bodies and trails
        for i, body in enumerate(self.current_frame):
            self.plot.draw_body(body)

            if vals.trail:
                vals.trails[body.hash][0].append(body.position.vec)
                if len(vals.trails[body.hash][0]) > vals.trail_length:
                    vals.trails[body.hash][0].pop(0)

        if vals.trail:
            for trail in vals.trails.values():
                self.plot.draw_trail(trail[0], trail[1])

        # Draw center of mass
        cm = center_of_mass(self.current_frame)
        vals.trails['CM'][0].append(cm.vec)
        self.plot.draw_point(self.plot.window, cm, 2 * (1 / vals.pixel_scale), (255, 0, 0))
        self.plot.draw_trail(vals.trails['CM'][0], vals.trails['CM'][1])

        # Draw simulation info
        self.plot.draw_text(f'TIME STEP: {vals.simulation_seconds_per_real_second}',
                            10 * (1 / vals.pixel_scale),
                            (60 / vals.pixel_scale, 10 / vals.pixel_scale), (255, 255, 255))
        self.plot.draw_text(f'PRECISION: {vals.dT}', 10 / vals.pixel_scale,
                            (60 / vals.pixel_scale, 20 / vals.pixel_scale), (255, 255, 255))

        self.plot.main_routine()
        self.plot.update()

        await self.wait_until(lambda: self.render_frame_time() > 1 / vals.frames_per_second)
