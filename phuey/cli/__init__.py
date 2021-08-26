import phuey.cli.admin
import phuey.cli.config
import phuey.cli.light

def register_commands(subparsers):
    phuey.cli.admin.register(subparsers)
    phuey.cli.config.register(subparsers)
    phuey.cli.light.register(subparsers)
