from rgbxy import Converter, GamutC
from faker import Faker

CONVERTER = Converter(GamutC)
FAKER = Faker(['en_US'])

def lights(count=1):
    light_data = {}
    for i in range(0, count):
        (r,g,b) = random_rgb()
        light_data[i] = {
            'id': i,
            'name': FAKER.word(),
            'state': {
                'on': FAKER.boolean(),
                'xy': CONVERTER.rgb_to_xy(r,g,b),
                'bri': FAKER.random_int(0,254),
                'colormode': 'xy'
            }
        }

    return light_data

def random_rgb():
    r = FAKER.random_int(0,255)
    g = FAKER.random_int(0,255)
    b = FAKER.random_int(0,255)

    return (r,g,b)

def convert_xy_to_rgb(xy):
    return CONVERTER.xy_to_rgb(xy[0], xy[1])
