import psutil
import winreg
import os
import subprocess
import time
import shutil


def check_steam_running(steam):
    for proc in psutil.process_iter(['name']):
        if "steam.exe" in proc.info['name'].lower():
            print("Steam is still running!\nClosing Steam automatically.\nPlease wait...")
            args = f"{steam}/steam.exe steam://exit"
            subprocess.run(args)
            input("\nPress enter once Steam has closed")
            break


def get_steam_path():
    try:
        location = winreg.HKEY_LOCAL_MACHINE
        path = winreg.OpenKeyEx(location, r"SOFTWARE\Wow6432Node\Valve\Steam")
        steam = winreg.QueryValueEx(path, "InstallPath")[0]
        steam = steam.replace("\\","/")
        if path:
            winreg.CloseKey(path)
        return steam
    except Exception as e:
        print(f"Error: {e}")
        input("Press enter to exit...")
        exit()

def reinstall_steamvr(steam):
    try:
        print("Removing default.vrsettings, steamvr.vrsettings, and lighthousedb.json")
        os.remove(f"{steam}/steamapps/common/SteamVR/resources/settings/default.vrsettings")
        os.remove(f"{steam}/config/steamvr.vrsettings")
        os.remove(f"{steam}/config/lighthouse/lighthousedb.json")
        print("Removed successfully")
    except Exception as e:
        print(f"Failed to delete config files due to error: {e}")

    try:
        print(f'\nYou will be prompted to uninstall SteamVR, press "Uninstall" when asked.')
        time.sleep(3)
        args = f"{steam}/steam.exe steam://uninstall/250820"
        subprocess.Popen(args)
        input("\nPress enter when SteamVR is finished uninstalling...")
    except Exception as e:
        print(f"Failed to uninstall SteamVR due to error: {e}")

    try:
        print("Removing SteamVR folder")
        shutil.rmtree(f"{steam}/steamapps/common/SteamVR")
        print("Removed successfully")
    except Exception as e:
        print(f"Failed to delete SteamVR folder due to error: {e}")

    try:
        print(f'\nYou will now be prompted to install SteamVR, press "Install" when asked.')
        time.sleep(3)
        args = f"{steam}/steam.exe steam://install/250820"
        subprocess.Popen(args)
        input("\nPress enter when finished...")
    except Exception as e:
        print(f"Failed to install SteamVR due to error: {e}")


steam = get_steam_path()
print(steam)
check_steam_running(steam)
reinstall_steamvr(steam)
