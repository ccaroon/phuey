import re
from phuey.rest_client import RestClient
from phuey.hue_light import HueLight

class HueBridge:
    def __init__(self, host, token):
        self.client = RestClient(
            F'/api/{token}',
            { 'host': host },
            self.error
        )
        # self.client.debug(True)

    @classmethod
    def create_user(cls):
        pass

    def get_light(self, name):
        light = None
        light_name = self.__normalize_name(name)

        resp = self.client.get('/lights')

        lights = resp.json()
        for id, data in lights.items():
            check_name = self.__normalize_name(data['name'])
            if light_name == check_name:
                light = HueLight(self, id, data)
                break

        if not light:
            raise Exception(F"Light named '{name}' not found.")

        return light

    def __normalize_name(self, name):
        return re.sub("[^\w ]", '-', name)

    def error(self, response):
        """Parse out the error message from the given REST response if any"""

        data = response.json()
        for result in data:
            error_msg = None
            if 'error' in result:
                error = result['error']
                error_msg = F"Status Code: [{response.status_code}] | Reason: [{response.reason}]"
                error_msg += F" | Description: [{error.get('description', '?????')}]"

                raise Exception(error_msg)
