import os
import yaml
#-------------------------------------------------------------------------------
CONFIG_FILE_NAME = 'phuey.yml'
DEFAULT_CONFIG = {
    'host': '192.168.0.0',
    'username': '0xDeadbEEf'
}
#-------------------------------------------------------------------------------
def config(args, **kwargs):
    args.cmd.print_help()
#-------------------------------------------------------------------------------
def cmd_init(args, **kwargs):
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
        'config',
        help='Manage Phuey Config File')
    command.set_defaults(func=config, cmd=command)

    # Init Sub-commands
    sub_commands = command.add_subparsers()

    # create-username
    init_cmd = sub_commands.add_parser(
        'init',
        help='Create Your Phuey Config File')
    init_cmd.add_argument(
        "bridge_url", type=str,
        help="The URL of your Philips Hue Bridge.")
    init_cmd.add_argument(
        "username", type=str,
        help="Default username to use when executing commands.")
    init_cmd.set_defaults(func=cmd_init)
