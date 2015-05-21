# convert comma-separated list of iata codes and latlongs to json
# usage: python code.py code.txt
import json, sys
codes = {}
for line in open(sys.argv[1]).readlines():
    _, iata, _, _, _, lat_deg, lat_min, lat_sec, lat_dir, long_deg, long_min, long_sec, long_dir, _ = line.split(':')
    lat_deg, lat_min, lat_sec, long_deg, long_min, long_sec = map(int, (lat_deg, lat_min, lat_sec, long_deg, long_min, long_sec))
    if iata == 'N/A': continue
    latitude = (1 if lat_dir == 'N' else -1) * (lat_deg + lat_min / 60.0 + lat_sec / 3600.0)
    longitude = (1 if long_dir == 'E' else -1) * (long_deg + long_min / 60.0 + long_sec / 3600.0)
    codes[iata] = [latitude, longitude]

print json.dumps(codes)


