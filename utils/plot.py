import pygame

from utils import constants
from utils.body import Vector, Body
from utils.constants import vals
from utils.color import complementary_color


class Plot:
    def __init__(self, width, height):
        """
        Creates a new plot.
        :param width: Width of the plot in pixels
        :param height: Height of the plot in pixels
        """
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height

    @staticmethod
    def main_routine():
        """
        Main routine for the plot, runs every display iteration. Handles events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    constants.vals.simulation_seconds_per_real_second *= 2
                if event.key == pygame.K_LEFT:
                    constants.vals.simulation_seconds_per_real_second /= 2
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

    @staticmethod
    def update():
        """
        Updates the display.
        """
        pygame.display.update()

    @staticmethod
    def draw_point(screen, point: Vector, radius, color):
        """
        Draws a point on the screen.
        :param screen: Screen to draw on
        :param point: Vector position of the point
        :param radius: Radius of the point
        :param color: Color of the point as a (r, g, b) tuple, 0-255
        """
        point *= vals.pixel_scale
        radius *= vals.pixel_scale
        pygame.draw.circle(screen, color,
                           (point.vec[0] + vals.center_x, point.vec[1] + vals.center_y),
                           radius)

    @staticmethod
    def draw_vector(screen, point: Vector, vec: Vector, color, width=1, alpha=255):
        """
        Draws a vector on the screen.
        :param screen: Screen to draw on
        :param point: Vector position of the start of the vector
        :param vec: Vector direction of the vector
        :param color: Color of the vector as a (r, g, b) tuple, 0-255
        :param width: Width of the vector
        :param alpha: Opacity of the vector, 0-255
        """
        point *= vals.pixel_scale
        vec *= vals.pixel_scale
        pygame.draw.line(
            screen, color, (point.vec[0] + vals.center_x, point.vec[1] + vals.center_y),
            (point.vec[0] + vec.vec[0] + vals.center_x, point.vec[1] + vec.vec[1] + vals.center_y),
            width
        )

    def draw_label(self, text, size, pos, color):
        """
        Draws a label of a body on the screen.
        :param text: Text to draw
        :param size: Size of the text
        :param pos: Screen position of the center of the text
        :param color: Color of the text as a (r, g, b) tuple, 0-255
        """
        size *= vals.pixel_scale
        pos = (pos[0] * vals.pixel_scale + vals.center_x, pos[1] * vals.pixel_scale + vals.center_y)
        font = pygame.font.SysFont('Arial', int(size))
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = pos[0], pos[1]

        self.window.blit(text, textRect)

    def draw_text(self, text, size, pos, color):
        """
        Draws text on the screen.
        :param text: Text to draw
        :param size: Size of the text
        :param pos: Screen position of the center of the text
        :param color: Color of the text as a (r, g, b) tuple, 0-255
        """
        size *= vals.pixel_scale
        pos = (pos[0] * vals.pixel_scale, pos[1] * vals.pixel_scale)
        font = pygame.font.SysFont('Arial', int(size))
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = pos[0], pos[1]

        self.window.blit(text, textRect)

    def draw_body(self, body: Body):
        """
        Draws a body on the screen.
        :param body: Body to draw
        """
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_point(screen, body.position, body.radius, body.color + (100,))
        self.window.blit(screen, (0, 0))

        self.draw_point(self.window, body.position, body.radius * .8, body.color)
        self.draw_vector(self.window, body.position,
                         body.velocity.normalize() * (40 / vals.pixel_scale) if
                         vals.normalize else body.velocity * 10, body.color)
        self.draw_label(body.name, body.radius, body.position.int_tuple(),
                        complementary_color(body.color))

    def draw_trail(self, trail: list, color):
        """
        Draws a trail on the screen.
        :param trail: List of vector trails to draw
        :param color: Color of the trail as a (r, g, b) tuple, 0-255
        """
        screen = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for i in range(len(trail) - 1):
            ratio = i / len(trail)
            new_color = [x * ratio for x in color]
            new_color.append(100)

            self.draw_vector(
                self.window,
                Vector(trail[i]),
                Vector(trail[i + 1]) - Vector(trail[i]),
                (255, 255, 255),
                1
            )
            self.draw_vector(
                screen,
                Vector(trail[i]),
                Vector(trail[i + 1]) - Vector(trail[i]),
                new_color,
                6
            )

        self.window.blit(screen, (0, 0))

    def clear(self):
        """
        Clears the screen.
        """
        self.window.fill((0, 0, 0))

    def keep_open(self):
        """
        Keeps the window open.
        """
        while True:
            self.main_routine()
