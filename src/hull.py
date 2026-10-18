"""Выпуклая оболочка: алгоритм монотонной цепочки."""
from geometry import Point, cross_product, dist

def convex_hull(points: list[Point]) -> list[Point]:
    """Алгоритм монотонной цепочки Эндрю"""
    pts = sorted(list(set(points)))
    if len(pts) <= 2:
        return pts

    # Нижняя оболочка
    lower = []
    for p in pts:
        while len(lower) >= 2 and cross_product(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    
    # Верхняя оболочка
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross_product(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    
    # Объединяем, убирая последнюю точку каждой части
    return lower[:-1] + upper[:-1]

def hull_perimeter(hull: list[Point]) -> float:
    """Периметр выпуклой оболочки"""
    if len(hull) < 2:
        return 0.0
    return sum(dist(hull[i], hull[(i+1) % len(hull)]) for i in range(len(hull)))
