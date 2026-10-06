import sys
import ctypes
import os

from driver import connect

def init():
    # check if root on mac or Administrator on windows
    if sys.platform == "win32":
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("Please run as Administrator")
            sys.exit(1)
    elif sys.platform == "darwin":
        if os.geteuid() != 0:
            print("Please run as root")
            sys.exit(1)
    else:
        print('Linux should also work, if you encounter problems please open an issue')
        if os.geteuid() != 0:
            print("Please run as root")
            sys.exit(1)

    # get lockdown client
    lockdown = connect.get_usbmux_lockdownclient()

    # check version
    version = connect.get_version(lockdown)
    print(f"Your system version is {version}")
    if version.split(".")[0] < "17":
        print(f"Only version 17 and above is supported")
        sys.exit(1)

    # check developer mode status
    developer_mode_status = connect.get_developer_mode_status(lockdown)
    if not developer_mode_status:
        connect.reveal_developer_mode(lockdown)
        print("Developer mode is not enabled. Please go to Settings > Privacy & Security > Developer Mode on your device to enable it. After enabling, you need to restart and enter your password, then run this program again")
        sys.exit(1)