"""Независимая проверка через библиотеку Shapely."""
from shapely.geometry import Point, MultiPoint, Polygon

def main():
    # 1. Читаем наши точки
    points = []
    with open('points.txt', 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            if len(parts) >= 3:
                points.append((int(parts[1]), int(parts[2])))

    # 2. Читаем наш район (кольца)
    rings = []
    current_ring = []
    with open('district.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                if current_ring:
                    rings.append(current_ring)
                    current_ring = []
            else:
                coords = line.split()
                if len(coords) >= 2:
                    current_ring.append((int(coords[0]), int(coords[1])))
    if current_ring:
        rings.append(current_ring)

    # 3. Проверка выпуклой оболочки
    mp = MultiPoint([Point(p) for p in points])
    hull = mp.convex_hull
    
    # Shapely замыкает полигон, поэтому последняя точка дублирует первую. Вычитаем 1.
    shapely_vertices = len(hull.exterior.coords) - 1
    shapely_area2 = int(hull.area * 2)
    
    print(f"Shapely вершин оболочки: {shapely_vertices}")
    print(f"Shapely удвоенная площадь: {shapely_area2}")

    # 4. Проверка точек внутри района
    if len(rings) > 0:
        shell = rings[0]
        holes = rings[1:] if len(rings) > 1 else []
        poly = Polygon(shell, holes)
        
        inside_count = sum(1 for p in points if poly.contains(Point(p)) or poly.touches(Point(p)))
        print(f"Shapely точек внутри: {inside_count}")
    else:
        print("Район пуст")

if __name__ == "__main__":
    main()
