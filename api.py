import os, flask, json, dateutil.parser, time, math, requests

app = flask.Flask(__name__)
iata = json.load(open('iata.json'))
EARTH_CIRCUMFERENCE = 24901
FORECAST_API = 'https://api.forecast.io/forecast/fb36105e650d6436e4d6a7ebd2d97ce0'

class ResolveException(Exception): pass
def _resolve(location):
    if location.upper() in iata:
        return iata[location.upper()]
    else:
        # location must be a json lat/long pair
        try:
            return json.loads('[%s]' % location)
        except Exception:
            raise ResolveException()

@app.route('/resolve/<string:location>')
def resolve(location):
    try:
        return flask.Response(json.dumps({'location': _resolve(location)}), mimetype='application/json')
    except ResolveException:
        return flask.Response(json.dumps({'error': 'invalid location: %s' % location}), status=500, mimetype='application/json')

def weather(location, time):
    data = requests.get('%s/%s,%s,%s' % (FORECAST_API, location[0], location[1], time)).json()
    ret = {
        "incomplete": False,
        "location": location,
        "location_rnd": map(lambda x: round(x, 2), location),
        "time": time,
        "time_rnd": (time // 3600) * 3600
    }
    try: ret["time_offset"] = data['offset']
    except KeyError: ret['incomplete'] = True
    for key, foreign_key in [('temperature', 'temperature'), ('humidity', 'humidity'), ('wind_speed', 'windSpeed')]:
        try: ret[key] = data['currently'][foreign_key]
        except KeyError: ret['incomplete'] = True
    return ret


@app.route('/forecast/<src>/<dest>/<departure_datetime>/<speed_mph>/<time_step>')
def forecast(src, dest, departure_datetime, speed_mph, time_step):
    src, dest = _resolve(src), _resolve(dest)
    departure_datetime = dateutil.parser.parse(departure_datetime)
    speed_mph, time_step = float(speed_mph), int(time_step)
    angular_speed = speed_mph / EARTH_CIRCUMFERENCE * 360

    vector = [dest[0] - src[0], dest[1] - src[1]]
    if vector[0] > 180: vector[0] -= 360
    if vector[1] > 180: vector[1] -= 360
    distance = math.sqrt(vector[0]**2 + vector[1]**2)
    hours = distance / angular_speed
    print src, dest, angular_speed, vector, distance, hours

    intervals = []
    for t in range(0, int(hours), time_step):
        location = [src[0] + vector[0] * t / hours, src[1] + vector[1] * t / hours]
        intervals.append(weather(location, int(time.time()) + t * 3600))

    return flask.Response(json.dumps({'forecast': intervals}), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)

