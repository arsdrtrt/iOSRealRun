import xml.etree.ElementTree as ET
import sys

def gpx_to_route(gpx_file, output_file):
    # Пространство имён GPX
    ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
    
    tree = ET.parse(gpx_file)
    root = tree.getroot()
    
    points = []
    # Ищем все точки трека
    for trkpt in root.findall('.//gpx:trkpt', ns):
        lat = trkpt.get('lat')
        lon = trkpt.get('lon')
        if lat and lon:
            points.append((lon, lat))  # сначала lng, потом lat
    
    if not points:
        print("Не найдено ни одной точки в GPX-файле. Проверь формат.")
        return
    
    # Формируем строку в нужном формате
    objects = [f'{{"lng":"{lng}","lat":"{lat}"}}' for lng, lat in points]
    result = ','.join(objects)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Готово! {len(points)} точек записано в {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python3 gpx2route.py входной.gpx выходной.txt")
        sys.exit(1)
    
    gpx_to_route(sys.argv[1], sys.argv[2])