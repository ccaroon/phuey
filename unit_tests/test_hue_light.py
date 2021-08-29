import unittest
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

    def test_can_get_name(self, rmock):
        self.assertEqual(self.light.name, self.light_data['name'])

    def test_can_get_color(self, rmock):
        color = self.light.color()
        xy = self.light_data['state']['xy']
        expected_color = mock_bridge.convert_xy_to_rgb(xy)

        self.assertEqual(color, expected_color)

    def test_can_set_color(self, rmock):
        rmock.register_uri(
            'PUT',
            F"{self.bridge.client.base_url()}/lights/{self.light.id}/state",
            json={}
        )

        new_color = (255, 128, 64)
        self.light.color(new_color)

        color = self.light.color()

        # When converted from RGB -> XY -> RGB the RGB colors do not match exactly
        for i in range(0,3):
            self.assertAlmostEqual(color[i], new_color[i], delta=8)
