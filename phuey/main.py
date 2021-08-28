import argparse
import os
import sys
import yaml

import phuey.cli
import phuey.version

from phuey.hue_bridge import HueBridge
#-------------------------------------------------------------------------------
def __usage(args, **kwargs):
    args.app.print_help()
    print("\nSEE ALSO:")
    print("    * README.md")
    print("\nNOTES:")
    print("    * ...This is a Work-In-Progress...")
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
        print("Config File Not Found. Please run `phuey config init` and try again.")
        sys.exit(1)

    return data
#-------------------------------------------------------------------------------
def cli():
    parser = argparse.ArgumentParser(
        description=F'Philips Hue Utility v{phuey.version.VERSION}'
    )
    parser.add_argument('--version', '-v', action='version', version=phuey.version.VERSION)
    parser.set_defaults(func=__usage, app=parser)

    # Register Commands
    subparsers = parser.add_subparsers()
    phuey.cli.register_commands(subparsers)

    args = parser.parse_args()

    # Read Config
    bridge = None
    config = None
    if args.func != phuey.cli.config.cmd_init:
        config = __read_config()
        bridge = HueBridge(config['host'], config['username'])

    # Execute the command
    args.func(args, config=config, bridge=bridge)
