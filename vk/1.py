import psutil
import time
import re
import winreg
import os

def get_steam_path():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
        steam_path, _ = winreg.QueryValueEx(reg_key, "SteamPath")
        return steam_path
    except FileNotFoundError:
        print("Steam не найден в реестре.")
        return None

def get_downloading_game(steam_path):
    log_file_path = os.path.join(steam_path, 'logs', 'content_log.txt')
    if not os.path.exists(log_file_path):
        return None
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if "Downloading" in line:
                match = re.search(r'"(.+?)"', line)
                if match:
                    return match.group(1)
    return None

def get_download_speed(steam_path):
    try:
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            if 'steam.exe' in proc.info['name'].lower():
                for conn in proc.connections(kind='inet'):
                    if conn.status == psutil.CONN_ESTABLISHED:
                        return conn.raddr[1]  # Возвращаем скорость загрузки
    except Exception as e:
        print(f"Ошибка при получении скорости: {e}")
    return 0

def track_download():
    steam_path = get_steam_path()
    if not steam_path:
        print("Steam не установлен или не найден.")
        return
    
    downloading_game = get_downloading_game(steam_path)
    if not downloading_game:
        print("Нет загружаемой игры.")
        return

    print(f"Загружается: {downloading_game}")
    start_time = time.time()
    while time.time() - start_time < 300:  
        download_speed = get_download_speed(steam_path)
        print(f"Скорость загрузки: {download_speed} KB/s")
        time.sleep(60)

if __name__ == "__main__":
    track_download()
