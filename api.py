import os, flask, json

app = flask.Flask(__name__)

iata = json.load(open('iata.json'))

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


@app.route('/forecast/<src>/<dest>/<departure_datetime>/<speed_mph>/<time_step>')
def forecast(src, dest, departure_datetime, speed_mph, time_step):
    return flask.Response('not yet implemented')
