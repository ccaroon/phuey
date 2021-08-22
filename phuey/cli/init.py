import os
import yaml

from phuey.hue_bridge import HueBridge
#-------------------------------------------------------------------------------
CONFIG_FILE_NAME = 'phuey.yml'
DEFAULT_CONFIG = {
    'host': '192.168.0.0',
    'username': '0xDeadbEEf'
}
#-------------------------------------------------------------------------------
def init(args, config):
    home_dir = os.getenv('HOME')
    config_path = os.getenv('XDG_CONFIG_HOME', F"{home_dir}/.config")
    config_file = F"{config_path}/{CONFIG_FILE_NAME}"

    config_data = DEFAULT_CONFIG.copy()

    host = None
    if args.bridge_url.startswith('http'):
        host = args.bridge_url
    else:
        host = F"http://{args.bridge_url}"

    config_data['host'] = host
    config_data['username'] = args.username

    with open(config_file, 'w') as file:
        yaml.dump(config_data, file)

#-------------------------------------------------------------------------------
def register(subparsers):
    command = subparsers.add_parser(
        'init',
        help='Initialize Phuey')

    command.add_argument(
        "bridge_url", type=str,
        help="The URL of your Philips Hue Bridge.")
    command.add_argument(
        "username", type=str,
        help="Default username to use when executing commands.")

    command.set_defaults(func=init)
