"""Загрузка и проекция данных"""
import json
from pathlib import Path
from geometry import Point, project

def load_dataset(dataset_name: str):
    """Загружает данные набора и возвращает спроецированные точки и кольца"""
    base = Path('data') / 'data' / dataset_name
    
    # 1. Загрузка точек
    with open(base / 'points.json', encoding='utf-8') as f:
        data = json.load(f)
    
    points_raw, lats, lons = [], [], []
    for el in data.get('elements', []):
        lat = el.get('lat') or el.get('center', {}).get('lat')
        lon = el.get('lon') or el.get('center', {}).get('lon')
        if lat and lon:
            points_raw.append({'id': f"{el['type']}/{el['id']}", 'lat': lat, 'lon': lon})
            lats.append(lat)
            lons.append(lon)
            
    # 2. Загрузка района
    with open(base / 'district.geojson', encoding='utf-8') as f:
        geo = json.load(f)
    
    rings_raw = []
    for feat in geo.get('features', []):
        geom = feat['geometry']
        coords = geom['coordinates']
        if geom['type'] == 'Polygon': 
            rings_raw.extend(coords)
        elif geom['type'] == 'MultiPolygon': 
            for poly in coords: rings_raw.extend(poly)
            
    # 3. Вычисление центра проекции
    lat0 = (min(lats) + max(lats)) / 2
    lon0 = (min(lons) + max(lons)) / 2
    
    # 4. Проекция в целые метры
    proj_points = [Point(*project(p['lat'], p['lon'], lat0, lon0), p['id']) for p in points_raw]
    
    # В GeoJSON порядок координат: [lon, lat] 
    proj_rings = [[Point(*project(lat, lon, lat0, lon0)) for lon, lat in ring] for ring in rings_raw]
    
    max_coord = max((max(abs(p.x), abs(p.y)) for p in proj_points), default=0)
    
    return proj_points, proj_rings, lat0, lon0, len(points_raw), max_coord
