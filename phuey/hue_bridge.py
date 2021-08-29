import re
from phuey.rest_client import RestClient
from phuey.hue_light import HueLight

class HueBridge:
    def __init__(self, host, username):
        self.client = RestClient(
            F'/api/{username}',
            { 'host': host },
            HueBridge.error
        )
        # self.client.debug(True)

    @classmethod
    def create_user(cls, bridge_url, app_name, device_name, **kwargs):
        """Creates a 'username' for use with Philip Hue REST API calls"""

        client = RestClient('/api', {'host': bridge_url }, cls.error)
        # client.debug(True)
        # POST /api `{"devicetype":"<APP_NAME>#<DEVICE_NAME>"}`
        data = {
            'devicetype': F"{app_name}#{device_name}"
        }

        gen_client_key = kwargs.get('gen_client_key', False)
        if gen_client_key:
            data['generateclientkey'] = True

        resp = client.post('/', data)

        result = {
            'username': resp.json()[0]['success']['username'],
        }
        if gen_client_key:
            result['client_key'] = resp.json()[0]['success']['clientkey']

        return (result)

    def get_light(self, name):
        found_light = None
        light_name = self.__normalize_name(name)

        all_lights = self.get_lights()

        for light in all_lights:
            check_name = self.__normalize_name(light.name)
            if light_name == check_name:
                found_light = light
                break

        if not found_light:
            raise Exception(F"Light named '{name}' not found.")

        return found_light

    def get_lights(self):
        resp = self.client.get('/lights')
        light_data = resp.json()

        lights = []
        for id, data in light_data.items():
            lights.append(HueLight(self, id, data))

        return lights

    def __normalize_name(self, name):
        return re.sub("[^\w ]", '-', name)

    def error(response):
        """Parse out the error message from the given REST response if any"""

        data = response.json()
        for result in data:
            error_msg = None
            if 'error' in result:
                error = result['error']
                error_msg = "Error - "
                if response.status_code >= 300:
                    error_msg += F"Status Code: [{response.status_code}] | Reason: [{response.reason}] | "
                error_msg += F"Message: [{error.get('description', '?????')}]"

                raise Exception(error_msg)
