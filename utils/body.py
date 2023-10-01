import utils.constants
from utils.constants import vals

G = 6.67408e-11


class Vector:
    vec = []

    def __init__(self, vec: list):
        self.vec = vec

    def __add__(self, other: 'Vector | int | float') -> 'Vector':
        if type(other) == int or type(other) == float:
            return Vector([self.vec[x] + other for x in range(len(self.vec))])

        return Vector([self.vec[x] + other.vec[x] for x in range(len(self.vec))])

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector([self.vec[x] - other.vec[x] for x in range(len(self.vec))])

    def __mul__(self, other: float) -> 'Vector':
        return Vector([self.vec[x] * other for x in range(len(self.vec))])

    def __truediv__(self, other: float) -> 'Vector':
        return Vector([self.vec[x] / other for x in range(len(self.vec))])

    def __pow__(self, other: float) -> 'Vector':
        return Vector([self.vec[x] ** other for x in range(len(self.vec))])

    def magnitude(self) -> float:
        return sum((x ** 2 for x in self.vec)) ** 0.5

    def normalize(self) -> 'Vector':
        return self / self.magnitude()

    def int_tuple(self) -> tuple:
        return tuple(int(x) for x in self.vec)


class Body:
    mass: float
    radius: float
    position: Vector
    velocity: Vector
    color: tuple

    def __init__(self, mass, radius, vec: list, vel: list, color: tuple, name: str = ''):
        self.mass = mass
        self.radius = radius
        self.position = Vector(vec)
        self.velocity = Vector(vel)
        self.color = color
        self.name = name

    def calc_accel(self, other: 'Body') -> Vector:
        diff = self.position - other.position

        return diff * -G * other.mass / diff.magnitude() ** 3

    def update_velocity(self, others: list['Body']):
        for other in others:
            if other != self:
                self.velocity += self.calc_accel(other)

    def update_position(self):
        self.position += self.velocity * vals.dT


def center_of_mass(bodies: list) -> Vector:
    total_mass = sum([body.mass for body in bodies])
    weighted_bodies = [body.position * body.mass for body in bodies]
    return Vector([
            sum([weighted_body.vec[x] for weighted_body in weighted_bodies]) / total_mass
            for x in range(len(weighted_bodies[0].vec))
        ]
    )
