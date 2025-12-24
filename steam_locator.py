import os
import winreg
import vdf
from datetime import datetime

class SteamLocator:
    def __init__(self):
        self.steam_path = self._find_steam_path()
        self.library_folders = []

    def _find_steam_path(self):
        """Finds the Steam installation path using Windows Registry."""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
            path, _ = winreg.QueryValueEx(key, "SteamPath")
            return path
        except FileNotFoundError:
            # Fallback to default path
            default_path = r"C:\Program Files (x86)\Steam"
            if os.path.exists(default_path):
                return default_path
            return None

    def get_library_folders(self):
        """Reads libraryfolders.vdf to get all game installation paths."""
        if not self.steam_path:
            return []

        library_vdf_path = os.path.join(self.steam_path, "steamapps", "libraryfolders.vdf")
        if not os.path.exists(library_vdf_path):
            # Fallback: Just the main steamapps folder
            return [os.path.join(self.steam_path, "steamapps")]

        try:
            with open(library_vdf_path, "r", encoding="utf-8") as f:
                data = vdf.load(f)
            
            paths = []
            # VDF structure is usually keys like "0", "1", etc.
            if "libraryfolders" in data:
                for key, value in data["libraryfolders"].items():
                    if isinstance(value, dict) and "path" in value:
                        paths.append(os.path.join(value["path"], "steamapps"))
                    elif isinstance(value, str): # Old format
                         paths.append(os.path.join(value, "steamapps"))
            return paths
        except Exception as e:
            print(f"Error reading libraryfolders.vdf: {e}")
            return [os.path.join(self.steam_path, "steamapps")]

    def get_installed_games(self):
        """Scans all library folders for appmanifest_*.acf files."""
        games = []
        library_paths = self.get_library_folders()

        for lib_path in library_paths:
            if not os.path.exists(lib_path):
                continue

            for filename in os.listdir(lib_path):
                if filename.startswith("appmanifest_") and filename.endswith(".acf"):
                    filepath = os.path.join(lib_path, filename)
                    game_info = self._parse_acf(filepath)
                    if game_info:
                        games.append(game_info)
        return games

    def _parse_acf(self, filepath):
        """Parses a single .acf file to get game details."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = vdf.load(f)
            
            app_state = data.get("AppState", {})
            
            appid = app_state.get("appid")
            name = app_state.get("name")
            size_bytes = app_state.get("SizeOnDisk", 0)
            last_updated = app_state.get("LastUpdated", 0) # This might be install time or update time
            
            # Note: appmanifest files don't consistently store "LastPlayed". 
            # We rely on file modification time of the .acf file itself as a proxy for activity 
            # because Steam updates this file when the game is played or updated.
            file_mod_time = os.path.getmtime(filepath)

            return {
                "id": appid,
                "name": name,
                "size_gb": round(int(size_bytes) / (1024**3), 2),
                "last_updated_timestamp": file_mod_time, # Using file mod time as proxy
                "last_updated_str": datetime.fromtimestamp(file_mod_time).strftime('%Y-%m-%d %H:%M'),
                "path": filepath
            }
        except Exception as e:
            print(f"Error parsing {filepath}: {e}")
            return None

if __name__ == "__main__":
    locator = SteamLocator()
    print(f"Steam Path: {locator.steam_path}")
    games = locator.get_installed_games()
    for game in games:
        print(f"{game['name']} - {game['size_gb']} GB - {game['last_updated_str']}")
