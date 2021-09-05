import time
from rgbxy import Converter, GamutC

class HueLight:
    CONVERTER = Converter(GamutC)

    def __init__(self, bridge, id, data={}):
        self.__bridge = bridge

        self.__id   = id
        self.__data = data
        self.__set_initial_state()

    def __set_initial_state(self):
        self.__initial_state = self.__data.get('state', {'on': False}).copy()
        # fields that are not modifyable
        for fld in ('colormode', 'effect', 'alert', 'mode', 'reachable'):
            if fld in self.__initial_state:
                del self.__initial_state[fld]

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__data['name']

    def reload(self):
        """ Reload the light's info/state/etc """
        resp = self.__bridge.connection.get(F"/lights/{self.id}")

        self.__data = resp.json()
        self.__set_initial_state()

    def reset(self):
        """ Reset the light to it's initial state """
        _ = self.__bridge.connection.put(F"/lights/{self.id}/state", self.__initial_state)
        self.__data['state'] = self.__initial_state

    def color(self, rgb = None):
        """ Get/Set Color """

        if rgb:
            xy = self.CONVERTER.rgb_to_xy(rgb[0], rgb[1], rgb[2])
            self.__bridge.connection.put(F"/lights/{self.id}/state", {
                'xy': xy,
                'on': True
            })

            self.__data['state']['xy'] = xy
        else:
            xy = self.__data['state']['xy']
            return (self.CONVERTER.xy_to_rgb(xy[0], xy[1]))

    # percent: 0 to 100
    def brightness(self, percent:int=None):
        """ Get/Set Brightness """
        if percent is not None:
            # translate percent to value between 0 & 254
            bri_value = int(254 * (percent/100))
            resp = self.__bridge.connection.put(F"/lights/{self.id}/state", {
                'bri': bri_value,
                'on': True
            })

            self.__data['state']['bri'] = bri_value
        else:
            # Value is 0 to 254, Convert to percentage
            bri_percent = (self.__data['state']['bri'] * 100) / 254

            return round(bri_percent)

    def on(self, value=None):
        """ Get/Set Current ON state """
        if value in (True, False):
            resp = self.__bridge.connection.put(F"/lights/{self.id}/state", {
                'on': value
            })

            self.__data['state']['on'] = value
        else:
            return self.__data['state']['on']

    def blink(self, color, count=3):
        self.on(True)
        self.color(color)

        for i in range(0, count):
            self.on(False)
            time.sleep(0.5)
            self.on(True)
            time.sleep(0.5)

        self.reset()
