
"""Главная утилита"""
import argparse
import sys
from pathlib import Path

# Добавляю папку src в путь поиска модулей
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from geometry import Point
from polygons import shoelace_double_area, point_in_polygon
from hull import convex_hull, hull_perimeter
from closest import closest_dc, closest_brute
from data_loader import load_dataset

def cmd_project(dataset, out_pts, out_dist):
    #Подготовка данных
    pts, rings, lat0, lon0, total, max_c = load_dataset(dataset)
    
    with open(out_pts, 'w', encoding='utf-8') as f:
        for p in pts:
            f.write(f"{p.id} {p.x} {p.y}\n")
            
    with open(out_dist, 'w', encoding='utf-8') as f:
        for i, ring in enumerate(rings):
            for p in ring:
                f.write(f"{p.x} {p.y}\n")
            if i < len(rings) - 1:
                f.write("\n")
                
    print(f"Объектов в выгрузке: {total}")
    print(f"Пропущено: 0")
    print(f"Центр проекции: {lat0:.4f}, {lon0:.4f}")
    print(f"Единица округления: 1 метр")
    print(f"Наибольшая по модулю координата: {max_c}")

def cmd_hull(file):
    #выпуклая оболочка
    pts = [Point(int(p[1]), int(p[2]), p[0]) for line in open(file, encoding='utf-8') if (p := line.split())]
    hull = convex_hull(pts)
    area2 = abs(shoelace_double_area(hull))
    perim = hull_perimeter(hull)
    
    print(f"Число точек: {len(pts)}, различных точек: {len(set(pts))}")
    print(f"Число вершин оболочки: {len(hull)}")
    print("Вершины против часовой стрелки:")
    for p in hull:
        print(f"  {p.id} ({p.x}, {p.y})")
    print(f"Удвоенная площадь (целое): {area2}")
    print(f"Площадь: {area2 / 2_000_000:.4f} км2")
    print(f"Периметр: {perim / 1000:.4f} км")

def cmd_closest(file, brute=False):
    #ближайшая пара точек
    pts = [Point(int(p[1]), int(p[2]), p[0]) for line in open(file, encoding='utf-8') if (p := line.split())]
    if brute:
        d, p1, p2, calcs = closest_brute(pts)
    else:
        d, p1, p2, calcs = closest_dc(pts)
        
    print(f"Расстояние: {d:.4f} м")
    print(f"Объекты: {p1.id} и {p2.id}")
    print(f"Число вычислений расстояния: {calcs}")

def cmd_inside(pts_file, dist_file):
    #подсчет в полигоне
    pts = [Point(int(p[1]), int(p[2])) for line in open(pts_file, encoding='utf-8') if (p := line.split())]
    
    rings, current = [], []
    for line in open(dist_file, encoding='utf-8'):
        line = line.strip()
        if not line:
            if current:
                rings.append(current)
                current = []
        else:
            current.append(Point(*map(int, line.split())))
    if current:
        rings.append(current)
    
    total_area2 = 0
    for i, ring in enumerate(rings):
        a2 = shoelace_double_area(ring)
        total_area2 += a2
        print(f"Удвоенная ориентированная площадь кольца {i}: {a2}")
        
    inside_count = sum(1 for p in pts if point_in_polygon(p, rings))
    print(f"Площадь района: {abs(total_area2) / 2_000_000:.4f} км2")
    print(f"Число точек внутри: {inside_count}")
    print(f"Число точек снаружи: {len(pts) - inside_count}")

def cmd_plot(pts_file, dist_file, out_img):
    #визуализация
    import matplotlib.pyplot as plt
    
    pts = [Point(int(p[1]), int(p[2])) for line in open(pts_file, encoding='utf-8') if (p := line.split())]
    rings, current = [], []
    for line in open(dist_file, encoding='utf-8'):
        line = line.strip()
        if not line:
            if current:
                rings.append(current)
                current = []
        else:
            current.append(Point(*map(int, line.split())))
    if current:
        rings.append(current)
    
    hull = convex_hull(pts)
    _, p1, p2, _ = closest_dc(pts)
    
    plt.figure(figsize=(10, 10))
    plt.scatter([p.x for p in pts], [p.y for p in pts], s=5, c='blue', alpha=0.5, label='Объекты')
    
    if hull:
        hx = [p.x for p in hull] + [hull[0].x]
        hy = [p.y for p in hull] + [hull[0].y]
        plt.plot(hx, hy, c='red', linewidth=2, label='Выпуклая оболочка')
        
    for ring in rings:
        rx = [p.x for p in ring] + [ring[0].x]
        ry = [p.y for p in ring] + [ring[0].y]
        plt.plot(rx, ry, c='green', linewidth=2, label='Граница района')
        
    if p1 and p2:
        plt.plot([p1.x, p2.x], [p1.y, p2.y], c='magenta', linewidth=3, label='Ближайшая пара')
        plt.scatter([p1.x, p2.x], [p1.y, p2.y], c='magenta', s=50, zorder=5)
        
    plt.legend()
    plt.axis('equal')
    plt.savefig(out_img, dpi=150)
    print(f"Файл с изображением сохранен: {out_img}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Утилита ДЗ")
    sub = parser.add_subparsers(dest='cmd')
    
    # project <dataset>
    sp = sub.add_parser('project')
    sp.add_argument('dataset', help='Например: 01-kazan-pharmacy')
    sp.add_argument('--out-points', default='points.txt')
    sp.add_argument('--out-district', default='district.txt')
    
    # hull <points.txt>
    sh = sub.add_parser('hull')
    sh.add_argument('file')
    
    # closest <points.txt> [--brute]
    sc = sub.add_parser('closest')
    sc.add_argument('file')
    sc.add_argument('--brute', action='store_true')
    
    # inside <points.txt> <district.txt>
    si = sub.add_parser('inside')
    si.add_argument('pts')
    si.add_argument('dist')
    
    # plot <points.txt> <district.txt> [--out-img map.png]
    spl = sub.add_parser('plot')
    spl.add_argument('pts')
    spl.add_argument('dist')
    spl.add_argument('--out-img', default='out/map.png')
    
    args = parser.parse_args()
    
    if args.cmd == 'project':
        cmd_project(args.dataset, args.out_points, args.out_district)
    elif args.cmd == 'hull':
        cmd_hull(args.file)
    elif args.cmd == 'closest':
        cmd_closest(args.file, args.brute)
    elif args.cmd == 'inside':
        cmd_inside(args.pts, args.dist)
    elif args.cmd == 'plot':
        cmd_plot(args.pts, args.dist, args.out_img)
    else:
        parser.print_help()
