"""Точки, векторы, повороты."""
from dataclasses import dataclass
from typing import Optional
import math


@dataclass
class Point:
    x: int
    y: int
    id: Optional[str] = None

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __repr__(self):
        if self.id:
            return f"Point({self.id}: {self.x}, {self.y})"
        return f"Point({self.x}, {self.y})"


@dataclass
class Vector:
    dx: int
    dy: int

    @staticmethod
    def from_points(a: Point, b: Point) -> 'Vector':
        return Vector(b.x - a.x, b.y - a.y)

    def length_sq(self) -> int:
        return self.dx * self.dx + self.dy * self.dy

    def length(self) -> float:
        return math.sqrt(self.length_sq())

    def cross(self, other: 'Vector') -> int:
        return self.dx * other.dy - self.dy * other.dx

    def dot(self, other: 'Vector') -> int:
        return self.dx * other.dx + self.dy * other.dy


@dataclass
class Segment:
    a: Point
    b: Point

    def vector(self) -> Vector:
        return Vector.from_points(self.a, self.b)

    def length_sq(self) -> int:
        return self.vector().length_sq()

    def length(self) -> float:
        return self.vector().length()


def cross_product(o: Point, a: Point, b: Point) -> int:
    """Предикат поворота: >0 — против ЧС, <0 — по ЧС, 0 — коллинеарны."""
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def dist_sq(p1: Point, p2: Point) -> int:
    """Квадрат расстояния (целочисленный)."""
    return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2


def dist(p1: Point, p2: Point) -> float:
    """Евклидово расстояние."""
    return math.sqrt(dist_sq(p1, p2))


def project(lat: float, lon: float, lat0: float, lon0: float, R: float = 6371000) -> tuple[int, int]:
    """Равнопромежуточная проекция в целые метры."""
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    lat0_rad = math.radians(lat0)
    lon0_rad = math.radians(lon0)
    x = int(round(R * (lon_rad - lon0_rad) * math.cos(lat0_rad)))
    y = int(round(R * (lat_rad - lat0_rad)))
    return x, y
