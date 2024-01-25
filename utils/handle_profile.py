import os
import platform
import readline
import asyncio

def read_file():
    profile = []
    if(platform.system() != "Darwin"):
        window_os_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', 'profiles.ini')
    else: 
        mac_os_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Firefox', 'profiles.ini')

    path_to_read = mac_os_path if platform.system() == "Darwin" else window_os_path

    with open(path_to_read, 'r') as file:
        for line in file:
            profile.append(line)
    if platform.system() == "Darwin":
        profile_mac_os_path = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Firefox', profile[3].split("=")[1].strip())
        return profile_mac_os_path
    else:
        profile_win_os_path = os.path.join(os.getenv('APPDATA'), 'Mozilla', 'Firefox', profile[1].split("=")[1].strip())
        return profile_win_os_path

def read_interface():
    path = read_file()
    return path

