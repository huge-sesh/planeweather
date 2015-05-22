import unittest, json, datetime
from api import app

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self): pass

    def test_resolve_lax(self):
        self.assertEqual(
                json.loads(self.app.get('/resolve/lax').data),
                {"location": [33.942499999999995, -118.40805555555556]})

    def test_resolve_json(self):
        self.assertEqual(
                json.loads(self.app.get('/resolve/%208.5,-9%20').data),
                {"location": [8.5, -9]})

    def test_forecast(self):
        response = json.loads(self.app.get('/forecast/LAX/LHR/%s/500/2' % datetime.datetime.now().isoformat()).data)
        self.assertTrue(len(response['forecast']) == 8)

if __name__ == '__main__':
    unittest.main()
