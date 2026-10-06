import re
import eviltransform

# Читаем HNroute.txt (это твой маршрут в WGS-84)
with open('HNroute.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Извлекаем все пары lng/lat
pattern = r'\{"lng":"([\d.]+)","lat":"([\d.]+)"\}'
matches = re.findall(pattern, content)
print(f"Найдено {len(matches)} точек")

converted = []
for lng, lat in matches:
    lng_f = float(lng)
    lat_f = float(lat)
    # WGS-84 -> GCJ-02 -> BD-09
    gcj_lat, gcj_lng = eviltransform.wgs2gcj(lat_f, lng_f)
    bd_lat, bd_lng = eviltransform.gcj2bd(gcj_lat, gcj_lng)
    converted.append(f'{{"lng":"{bd_lng:.10f}","lat":"{bd_lat:.10f}"}}')

with open('route_bd09.txt', 'w', encoding='utf-8') as f:
    f.write(','.join(converted))

print("Готово! Первая точка:")
print(converted[0])
print("Последняя точка:")
print(converted[-1])