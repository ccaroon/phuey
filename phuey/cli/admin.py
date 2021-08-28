import yaml
from phuey.hue_bridge import HueBridge
#-------------------------------------------------------------------------------
def admin(args, **kwargs):
    args.cmd.print_help()
#-------------------------------------------------------------------------------
def cmd_create_username(args, **kwargs):
    print("Please press the <Link Button> on the Hue Bridge now...")
    _ = input("Press Enter to Continue")

    config = kwargs.get('config')

    result = HueBridge.create_user(
        config['host'],
        args.app_name,
        args.device_name,
        gen_client_key=args.gen_client_key
    )

    print("-------------------------------------------------------------------")
    print(F"* Username: {result['username']}")
    print(F"* Client Key: {result.get('client_key', 'N/A')}")
    print("""
Please keep these values secret and in a safe place.

In order to deactive this username you will need to visit
https://account.meethue.com/apps and click the Deactive button on the relevant App name.
    """)
#-------------------------------------------------------------------------------
def register(subparsers):
    command = subparsers.add_parser(
        'admin',
        help='Admin Tasks')
    command.set_defaults(func=admin, cmd=command)

    # Init Sub-commands
    sub_commands = command.add_subparsers()

    # create-username
    create_user_cmd = sub_commands.add_parser(
        'create-username',
        help='Create a username for use with the Philips Hue REST API')
    create_user_cmd.add_argument(
        "app_name", type=str,
        help="The name of the application that will be using the username.")
    create_user_cmd.add_argument(
        "device_name", type=str,
        help="The name of the device the application runs on.")
    create_user_cmd.add_argument(
        "--gen-client-key", "-k", action='store_true', default=False,
        help="Also generate a Client Key. Default: False")
    create_user_cmd.set_defaults(func=cmd_create_username)
