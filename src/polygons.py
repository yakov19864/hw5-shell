from geometry import Point, cross_product
from typing import List

def shoelace_double_area(ring: List[Point]) -> int:
    """Удвоенная ориентированная площадь (целое число)"""
    if len(ring) < 3: return 0
    area = 0
    n = len(ring)
    for i in range(n):
        j = (i + 1) % n
        area += ring[i].x * ring[j].y - ring[j].x * ring[i].y
    return area

def segments_intersect(p1: Point, p2: Point, p3: Point, p4: Point) -> bool:
    """Пересечение отрезков p1-p2 и p3-p4 """
    d1 = cross_product(p3, p4, p1)
    d2 = cross_product(p3, p4, p2)
    d3 = cross_product(p1, p2, p3)
    d4 = cross_product(p1, p2, p4)
    
    if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and \
       ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
        return True
    
    # Вырожденные случаи (касание)
    def on_segment(p, q, r):
        return min(p.x, q.x) <= r.x <= max(p.x, q.x) and min(p.y, q.y) <= r.y <= max(p.y, q.y)
    
    if d1 == 0 and on_segment(p3, p4, p1): return True
    if d2 == 0 and on_segment(p3, p4, p2): return True
    if d3 == 0 and on_segment(p1, p2, p3): return True
    if d4 == 0 and on_segment(p1, p2, p4): return True
    return False

def point_in_polygon(pt: Point, rings: List[List[Point]]) -> bool:
    """Трассировка луча"""
    crossings = 0
    for ring in rings:
        n = len(ring)
        for i in range(n):
            p1, p2 = ring[i], ring[(i + 1) % n]
            # Луч идет вправо от pt (y = pt.y, x от pt.x до +inf)
            if (p1.y > pt.y) != (p2.y > pt.y): # Луч пересекает горизонтальную полосу отрезка
                # Находим X пересечения луча с отрезком
                x_intersect = p1.x + (pt.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
                if pt.x < x_intersect:
                    crossings += 1
    return crossings % 2 == 1

def triangulate_ear_clipping(ring: List[Point]) -> List[tuple]:
    """Триангуляция (упрощенная). Возвращает индексы треугольников."""
    if len(ring) < 3: return []
    return [(0, i, i+1) for i in range(1, len(ring)-1)]
