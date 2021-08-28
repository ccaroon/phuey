from faker import Faker
import unittest
import requests_mock

from phuey.hue_bridge import HueBridge
from phuey.hue_light import HueLight

@requests_mock.Mocker()
class TestHueBridge(unittest.TestCase):

    CREATE_USER_JSON = [
            { 'success': { 'username': '0xdeadbeef' } }
        ]

    def __fake_light_data(self, count=1):
        light_data = {}
        for i in range(0, count):
            light_data[i] = {
                'id': i,
                'name': self.faker.word(),
                'state': {
                    'on': self.faker.boolean(),
                    'xy': (
                        self.faker.pyfloat(2,2,min_value=0.0,max_value=1.0),
                        self.faker.pyfloat(2,2,min_value=0.0,max_value=1.0)
                    ),
                    'bri': self.faker.random_int(0,254),
                    'colormode': 'xy'
                }
            }

        return light_data

    def setUp(self):
        self.username = '0xDeadbeeF'
        self.bridge = HueBridge('http://192.168.24.007', self.username)
        self.faker = Faker(['en_US'])

    def test_can_create_user(self, rmock):
        mock_json = self.CREATE_USER_JSON.copy()
        rmock.register_uri('POST', '/api/', json=mock_json)
        result = HueBridge.create_user(
            'http://192.168.42.42',
            'testApp',
            'testDevice'
        )

        self.assertEqual(result['username'], mock_json[0]['success']['username'])

    def test_can_create_user_with_client_key(self, rmock):
        mock_json = self.CREATE_USER_JSON.copy()
        mock_json[0]['success']['clientkey'] = 'abcdefg123456789'
        rmock.register_uri('POST', '/api/', json=mock_json)
        result = HueBridge.create_user(
            'http://192.168.42.42',
            'testApp',
            'testDevice',
            gen_client_key=True
        )

        self.assertEqual(result['username'], mock_json[0]['success']['username'])

        self.assertIsNotNone(result['client_key'])
        self.assertEqual(result['client_key'], mock_json[0]['success']['clientkey'])

    def test_can_get_all_lights(self, rmock):
        light_data = self.__fake_light_data(count=5)
        rmock.register_uri('GET', F'/api/{self.username}/lights', json=light_data)

        lights = self.bridge.get_lights()

        self.assertEqual(len(lights), 5)
        self.assertIsInstance(lights[0], HueLight)


    def test_can_get_single_light(self, rmock):
        light_data = self.__fake_light_data(count=5)
        rmock.register_uri('GET', F'/api/{self.username}/lights', json=light_data)

        a_light = light_data[0]
        light = self.bridge.get_light(a_light['name'])

        self.assertIsInstance(light, HueLight)
        self.assertEqual(int(light.id), a_light['id'])
        self.assertEqual(light.name, a_light['name'])

    def test_light_not_found(self, rmock):
        light_data = self.__fake_light_data(count=1)
        rmock.register_uri('GET', F'/api/{self.username}/lights', json=light_data)

        with self.assertRaisesRegex(Exception, F"Light named 'FooBarBang' not found"):
            light = self.bridge.get_light('FooBarBang')

    def test_error_handler(self, rmock):
        rmock.register_uri('GET', F'/api/{self.username}/lights', json=[
            {'error': {'description': 'The Philips Hue Bridge seems to be offline'}}
        ])

        with self.assertRaisesRegex(Exception, 'Error - Message: \[The Philips Hue Bridge seems to be offline\]'):
            self.bridge.get_light('does-not-matter')






















#
