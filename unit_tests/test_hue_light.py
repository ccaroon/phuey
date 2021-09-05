import unittest
import random
import requests_mock

import mock_bridge

from phuey.hue_bridge import HueBridge
from phuey.hue_light import HueLight

@requests_mock.Mocker()
class TestHueLight(unittest.TestCase):

    def setUp(self):
        self.username = '0xDeadbeeF'
        self.bridge = HueBridge('http://192.168.24.007', self.username)

        light_data = mock_bridge.lights(count=1)
        self.light_data = light_data[0]
        self.light = HueLight(self.bridge, light_data[0]['id'], light_data[0])

    def test_get_name(self, rmock):
        self.assertEqual(self.light.name, self.light_data['name'])

    def test_get_color(self, rmock):
        color = self.light.color()
        xy = self.light_data['state']['xy']
        expected_color = mock_bridge.convert_xy_to_rgb(xy)

        self.assertEqual(color, expected_color)

    def test_set_color(self, rmock):
        rmock.register_uri(
            'PUT',
            F"{self.bridge.url}/lights/{self.light.id}/state",
            json={}
        )

        new_color = (255, 128, 64)
        self.light.color(new_color)

        color = self.light.color()

        # When converted from RGB -> XY -> RGB the RGB colors do not match exactly
        for i in range(0,3):
            self.assertAlmostEqual(color[i], new_color[i], delta=8)

    def test_get_brightness(self, rmock):
        bri = self.light.brightness()
        expected_bri = round((self.light_data['state']['bri'] * 100) / 254)

        self.assertEqual(bri, expected_bri)



    def test_set_brightness(self, rmock):
        rmock.register_uri(
            'PUT',
            F"{self.bridge.url}/lights/{self.light.id}/state",
            json={}
        )

        new_bri = random.randint(0,100)
        self.light.brightness(new_bri)

        bri = self.light.brightness()
        self.assertEqual(bri, new_bri)

    def test_reset_state(self, rmock):
        rmock.register_uri(
            'PUT',
            F"{self.bridge.url}/lights/{self.light.id}/state",
            json={}
        )

        orig_color = self.light.color()
        new_color = (64,128,254)
        self.light.color(new_color)
        self.assertNotEqual(orig_color, new_color)

        orig_bri = self.light.brightness()
        new_bri = random.randint(0,254)
        self.light.brightness(new_bri)
        self.assertNotEqual(orig_bri, new_bri)

        orig_on = self.light.on()
        new_on = not orig_on
        self.light.on(new_on)
        self.assertNotEqual(orig_on, new_on)

        self.light.reset()

        self.assertEqual(self.light.color(), orig_color)
        self.assertEqual(self.light.brightness(), orig_bri)
        self.assertEqual(self.light.on(), orig_on)


    def test_reload(self, rmock):
        light_data = mock_bridge.lights(count=1)[0]
        rmock.register_uri(
            'GET',
            F"{self.bridge.url}/lights/{self.light.id}",
            json=light_data
        )

        self.light.reload()

        self.assertEqual(self.light.id, light_data['id'])
        self.assertEqual(self.light.name, light_data['name'])
        self.assertEqual(self.light.color(), mock_bridge.convert_xy_to_rgb(light_data['state']['xy']))

        new_bri = round((light_data['state']['bri'] * 100) / 254)
        self.assertEqual(self.light.brightness(), new_bri)
