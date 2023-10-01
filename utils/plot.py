import pygame

from utils import constants
from utils.body import Vector, Body
from utils.constants import vals
from utils.color import opposite_color


class Plot:
    def __init__(self, width, height):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

    @staticmethod
    def main_routine():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    constants.vals.simulation_seconds_per_iter *= 2
                if event.key == pygame.K_LEFT:
                    constants.vals.simulation_seconds_per_iter /= 2
                if event.key == pygame.K_UP:
                    constants.vals.dT /= 2
                if event.key == pygame.K_DOWN:
                    constants.vals.dT *= 2

                if event.key == pygame.K_SPACE:
                    constants.vals.normalize = not constants.vals.normalize

            if event.type == pygame.MOUSEWHEEL:
                constants.vals.pixel_scale *= 1.1 if event.y > 0 else 0.9
                constants.vals.meters_transpose = constants.vals.screen_size / 2 / constants.vals.pixel_scale

        if pygame.key.get_pressed()[pygame.K_w]:
            constants.vals.center_y += 10
        if pygame.key.get_pressed()[pygame.K_s]:
            constants.vals.center_y -= 10
        if pygame.key.get_pressed()[pygame.K_a]:
            constants.vals.center_x += 10
        if pygame.key.get_pressed()[pygame.K_d]:
            constants.vals.center_x -= 10

        pygame.display.update()

    def draw_point(self, point: Vector, radius, color):
        point *= vals.pixel_scale
        radius *= vals.pixel_scale
        pygame.draw.circle(self.window, color, (point.vec[0] + vals.center_x, point.vec[1] + vals.center_y),
                           radius)

    def draw_vector(self, point: Vector, vec: Vector, color):
        point *= vals.pixel_scale
        vec *= vals.pixel_scale
        pygame.draw.line(
            self.window, color, (point.vec[0] + vals.center_x, point.vec[1] + vals.center_y),
            (point.vec[0] + vec.vec[0] + vals.center_x, point.vec[1] + vec.vec[1] + vals.center_y)
        )

    def draw_label(self, text, size, pos, color):
        size *= vals.pixel_scale
        pos = (pos[0] * vals.pixel_scale + vals.center_x, pos[1] * vals.pixel_scale + vals.center_y)
        font = pygame.font.SysFont('Arial', int(size))
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = pos[0], pos[1]

        self.window.blit(text, textRect)

    def draw_text(self, text, size, pos, color):
        size *= vals.pixel_scale
        pos = (pos[0] * vals.pixel_scale, pos[1] * vals.pixel_scale)
        font = pygame.font.SysFont('Arial', int(size))
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = pos[0], pos[1]

        self.window.blit(text, textRect)

    def draw_body(self, body: Body):
        self.draw_point(body.position, body.radius, body.color)
        self.draw_vector(body.position,
                         body.velocity.normalize() * (40 / vals.pixel_scale) if
                         vals.normalize else body.velocity * 10, body.color)
        self.draw_label(body.name, body.radius, body.position.int_tuple(),
                       opposite_color(body.color))

    def draw_trail(self, trail: list, color):
        for i in range(len(trail) - 1):
            self.draw_vector(Vector(trail[i]), Vector(trail[i + 1]) - Vector(trail[i]), color)

    def clear(self):
        self.window.fill((0, 0, 0))

    def keep_open(self):
        while True:
            self.main_routine()
