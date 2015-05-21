import os, flask, json

app = flask.Flask(__name__)

iata = json.load(open('iata.json'))

@app.route('/resolve/<string:location>')
def resolve(location):
    if location.upper() in iata:
        return flask.Response(json.dumps({'location': iata[location.upper()]}), mimetype='application/json')
    else:
        try:
            return flask.Response(json.dumps({'location': json.loads('[%s]' % location)}), mimetype='application/json')
        except Exception:
            return flask.Response(json.dumps({'error': 'invalid location: %s' % location}), status=500, mimetype='application/json')
