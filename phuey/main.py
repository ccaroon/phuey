import argparse

import phuey.version
from phuey.hue_bridge import HueBridge

#-------------------------------------------------------------------------------
def create_username(args):
    print("Please press the <Link Button> on the Hue Bridge now...")
    _ = input("Press Enter to Continue")
    result = HueBridge.create_user(
        args.bridge_url,
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
def usage(args):
    args.app.print_help()
    print("\nSEE ALSO:")
    print("    * README.md")
    print("\nNOTES:")
    print("    * A Work In-Progress...")
#-------------------------------------------------------------------------------
def cli():
    parser = argparse.ArgumentParser(
        description=F'Philips Hue Utility v{phuey.version.VERSION}'
    )
    parser.add_argument('--version', '-v', action='version', version=phuey.version.VERSION)
    parser.set_defaults(func=usage, app=parser)
    subparsers = parser.add_subparsers()

    # create_username
    create_parser = subparsers.add_parser(
        'create-username',
        help='Create a username for use with the Philips Hue REST API')
    create_parser.add_argument(
        "bridge_url", type=str,
        help="The URL of your Philips Hue Bridge.")
    create_parser.add_argument(
        "app_name", type=str,
        help="The name of the application that will be using the username.")
    create_parser.add_argument(
        "device_name", type=str,
        help="The name of the device the application runs on.")
    create_parser.add_argument(
        "--gen-client-key", "-k", action='store_true', default=False,
        help="Also generate a Client Key. Default: False")
    create_parser.set_defaults(func=create_username)

    # Execute Action
    args = parser.parse_args()

    try:
        args.func(args)
    except Exception as e:
        print(e)
