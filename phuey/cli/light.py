import yaml
from phuey.hue_bridge import HueBridge
#-------------------------------------------------------------------------------
def light(args, **kwargs):
    args.cmd.print_help()
#-------------------------------------------------------------------------------
def cmd_list(args, **kwargs):
    bridge = kwargs.get('bridge')
    lights = bridge.get_lights()

    for light in lights:
        on_off = 'ON' if light.on() else 'OFF'
        print(F"{light.id:2} - {light.name:25} [{on_off}]")
#-------------------------------------------------------------------------------
def cmd_get(args, **kwargs):
    bridge = kwargs.get('bridge')
    light = bridge.get_light(args.name)

    if args.fields:
        fields = args.fields.split(',')
        for fld in fields:
            value = light.data

            parts = fld.split(':')
            for p in parts:
                    value = value.get(p)

            if isinstance(value, str):
                print(value)
            else:
                print(yaml.dump(value))
    else:
        print(yaml.dump(light.data))
#-------------------------------------------------------------------------------
def cmd_set(args, **kwargs):
    bridge = kwargs.get('bridge')

    light = bridge.get_light(args.name)

    if args.brightness:
        percent = args.brightness
        if percent > 100:
            percent = 100
        elif percent < 0:
            percent = 0
        light.brightness(percent)

    # Color
    if args.color:
        rgb = args.color.split(',')
        rgb = [int(x) for x in rgb]
        light.color(rgb)

    # ON or OFF
    if args.on == args.off:
        light.on(args.on and args.off)
#-------------------------------------------------------------------------------
def register(subparsers):
    command = subparsers.add_parser(
        'light',
        help='Control your lights.')
    command.set_defaults(func=light, cmd=command)

    # Init Sub-commands
    sub_commands = command.add_subparsers()

    # list
    list_cmd = sub_commands.add_parser('list',
        help='List all the lights known to a Philips Hue Bridge')
    list_cmd.set_defaults(func=cmd_list)

    # get
    get_cmd = sub_commands.add_parser('get',
        help='Get the state of a Hue light.')
    get_cmd.add_argument(
        "name", type=str,
        help="Light Name")
    get_cmd.add_argument(
        "--fields", "-f", type=str, default=None,
        help="Fields to View")
    get_cmd.set_defaults(func=cmd_get)

    # set
    set_cmd = sub_commands.add_parser('set',
        help='Set the state of a Hue light.')
    set_cmd.add_argument(
        "name", type=str,
        help="Light Name")
    set_cmd.add_argument(
        "--on", action='store_true',
        help="Turn Light ON")
    set_cmd.add_argument(
        "--off", action='store_false',
        help="Turn Light OFF")
    set_cmd.add_argument(
        "--color", "-c", type=str, default=None,
        help="Set Light's Color: R,G,B")
    set_cmd.add_argument(
        "--brightness", "-b", type=int, default=None,
        help="Set Light's Brightness. Percent 0 to 100")
    set_cmd.set_defaults(func=cmd_set)
