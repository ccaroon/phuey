import argparse
import os
import sys
import yaml

import phuey.version

# Commands
import phuey.cli.init
import phuey.cli.create_username
import phuey.cli.list_lights

#-------------------------------------------------------------------------------
def __usage(args, config):
    args.app.print_help()
    print("\nSEE ALSO:")
    print("    * README.md")
    print("\nNOTES:")
    print("    * A Work In-Progress...")
#-------------------------------------------------------------------------------
def __read_config():
    home_dir = os.getenv('HOME')
    config_path = os.getenv('XDG_CONFIG_HOME', F"{home_dir}/.config")
    config_file = F"{config_path}/phuey.yml"

    data = None
    try:
        with open(config_file, 'r') as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        print("Config File Not Found. Please run `phuey init` and try again.")
        sys.exit(1)

    return data
#-------------------------------------------------------------------------------
def cli():
    parser = argparse.ArgumentParser(
        description=F'Philips Hue Utility v{phuey.version.VERSION}'
    )
    parser.add_argument('--version', '-v', action='version', version=phuey.version.VERSION)
    parser.set_defaults(func=__usage, app=parser)
    subparsers = parser.add_subparsers()

    # Register Commands
    phuey.cli.init.register(subparsers)
    phuey.cli.create_username.register(subparsers)
    phuey.cli.list_lights.register(subparsers)

    args = parser.parse_args()

    # Read Config
    config = None
    if args.func != phuey.cli.init.init:
        config = __read_config()

    # Execute the command
    args.func(args, config)
