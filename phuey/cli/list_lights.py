from phuey.hue_bridge import HueBridge
#-------------------------------------------------------------------------------
def list_lights(args, config):
    bridge = HueBridge(config['host'], config['username'])
    lights = bridge.get_lights()

    for light in lights:
        on_off = 'ON' if light.on() else 'OFF'
        print(F"{light.id:2} - {light.name:25} [{on_off}]")
#-------------------------------------------------------------------------------
def register(subparsers):
    command = subparsers.add_parser(
        'list-lights',
        help='List all the lights known to a Philips Hue Bridge')
    command.set_defaults(func=list_lights)
