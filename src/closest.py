"""Поиск ближайшей пары точек: разделяй и властвуй + перебор."""
from geometry import Point, dist


def closest_brute(points: list[Point]) -> tuple[float, Point, Point, int]:
    """Перебор всех пар. O(n²)"""
    min_d, p1, p2, calcs = float('inf'), None, None, 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            calcs += 1
            d = dist(points[i], points[j])
            if d < min_d:
                min_d, p1, p2 = d, points[i], points[j]
    return min_d, p1, p2, calcs


def closest_dc(points: list[Point]) -> tuple[float, Point, Point, int]:
    """Разделяй и властвуй. O(n log n)"""
    calcs = 0

    def solve(pts_x):
        nonlocal calcs
        n = len(pts_x)
        
        # База рекурсии: малое количество точек решаем перебором
        if n <= 3:
            min_d = float('inf')
            best_pair = (None, None)
            for i in range(n):
                for j in i + 1, n: 
                    pass 
            
            # база рекурсии
            for i in range(n):
                for j in range(i + 1, n):
                    calcs += 1
                    d = dist(pts_x[i], pts_x[j])
                    if d < min_d:
                        min_d = d
                        best_pair = (pts_x[i], pts_x[j])
            return min_d, best_pair[0], best_pair[1]

        mid = n // 2
        mid_x = pts_x[mid].x

        # Рекурсивные вызовы 
        dl, pl1, pl2 = solve(pts_x[:mid])
        dr, pr1, pr2 = solve(pts_x[mid:])

        if dl < dr:
            d, best_pair = dl, (pl1, pl2)
        else:
            d, best_pair = dr, (pr1, pr2)

        # Проверка точек в полосе
        strip = [p for p in pts_x if abs(p.x - mid_x) < d]
        strip.sort(key=lambda p: p.y)

        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and (strip[j].y - strip[i].y) < d:
                calcs += 1
                d_strip = dist(strip[i], strip[j])
                if d_strip < d:
                    d = d_strip
                    best_pair = (strip[i], strip[j])
                j += 1

        return d, best_pair[0], best_pair[1]

    # рекурсия и возвращаю итоговый счётчик
    d, p1, p2 = solve(sorted(points))
    return d, p1, p2, calcs
