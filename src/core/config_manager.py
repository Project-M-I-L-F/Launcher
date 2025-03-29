import json
import os

def load_config(config_path, default_config=None):
    if default_config is None:
        default_config = {}
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
            return config
    return default_config

def save_config(config_path, config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)

def load_game_config():
    return load_config("config/game_config.json", {
        "server": {
            "name": "WebUniverseServer",
            "ip": "ivanl47.aternos.me:42309",
            "port": 42309
        }
    })

def load_java_config():
    return load_config("config/java_config.json", {
        "java_urls": {
            "windows_x64": {
                "url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.6%2B7/OpenJDK21U-jdk_x64_windows_hotspot_21.0.6_7.zip",
                "filename": "OpenJDK21U-jdk_x64_windows_hotspot_21.0.6_7.zip"
            },
            "linux_x64": {
                "url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.6%2B7/OpenJDK21U-jdk_x64_linux_hotspot_21.0.6_7.tar.gz",
                "filename": "OpenJDK21U-jdk_x64_linux_hotspot_21.0.6_7.tar.gz"
            },
            "macos_arm": {
                "url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.6%2B7/OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.6_7.tar.gz",
                "filename": "OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.6_7.tar.gz"
            },
            "macos_x64": {
                "url": "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.6%2B7/OpenJDK21U-jdk_x64_mac_hotspot_21.0.6_7.tar.gz",
                "filename": "OpenJDK21U-jdk_x64_mac_hotspot_21.0.6_7.tar.gz"
            }
        }
    })

def load_user_config():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_config = {
        "minecraft_directory": os.path.join(base_dir, "minecraft_folder"),
        "username": "Player",
        "language": "en_us",
        "ram": 8,
        "minecraft_version": "1.20.1"  # Дефолтна версія 1.20.1
    }
    config = load_config("config/user_config.json", default_config)
    if not os.path.isabs(config["minecraft_directory"]):
        config["minecraft_directory"] = os.path.join(base_dir, config["minecraft_directory"])
    return config

def save_user_config(config):
    save_config("config/user_config.json", config)