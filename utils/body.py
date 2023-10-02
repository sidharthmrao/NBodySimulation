import utils.constants
from utils.constants import vals

G = 6.67408e-11


class Vector:
    vec = []

    def __init__(self, vec: list):
        """
        Creates a new vector.
        :param vec: List of data in the vector
        """
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
    name: str
    hash: str

    def __init__(self, mass, radius, vec: list, vel: list, color: tuple, name: str = '',
                 hash: str = "0"):
        """
        Creates a new body.
        :param mass: Mass of the object in kg
        :param radius: Radius of the object in m
        :param vec: Position of the object in m as a list
        :param vel: Velocity of the object in m/s as a list
        :param color: Color of the object as a (r, g, b) tuple, 0-255
        :param name: Name of the object to display
        :param hash: Hash of the object
        """

        self.mass = mass
        self.radius = radius
        self.position = Vector(vec)
        self.velocity = Vector(vel)
        self.color = color
        self.name = name
        self.hash = hash

    def calc_accel(self, other: 'Body') -> Vector:
        """
        Calculates the acceleration of this body due to another body.
        :param other: Body to calculate acceleration due to
        :return: Vector of acceleration
        """
        diff = self.position - other.position

        return diff * -G * other.mass / diff.magnitude() ** 3

    def update_velocity(self, others: list['Body']):
        """
        Updates the velocity of this body due to other bodies.
        :param others: List of other bodies
        """
        for other in others:
            if other != self:
                self.velocity += self.calc_accel(other)

    def update_position(self):
        """
        Updates the position of this body due to its velocity.
        """
        self.position += self.velocity * vals.dT


def center_of_mass(bodies: list) -> Vector:
    """
    Calculates the center of mass of a list of bodies.
    :param bodies: List of bodies
    :return: Vector position of center of mass
    """
    total_mass = sum([body.mass for body in bodies])
    weighted_bodies = [body.position * body.mass for body in bodies]
    return Vector([
            sum([weighted_body.vec[x] for weighted_body in weighted_bodies]) / total_mass
            for x in range(len(weighted_bodies[0].vec))
        ]
    )
