# src/core/mods_manager.py
import os
import requests
from .config_manager import load_mods_config

def check_directory_permissions(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        test_file = os.path.join(directory, "test_permissions.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print(f"Directory permissions OK: {directory}")
        return True
    except Exception as e:
        print(f"Directory permissions error: {e}")
        return False

def check_mods_exist(minecraft_directory, update_status):
    update_status("Checking mods...")
    mods_dir = os.path.join(minecraft_directory, "mods")
    if not os.path.exists(mods_dir):
        update_status("Mods folder not found")
        return False
    files = os.listdir(mods_dir)
    for file in files:
        if file.endswith(".jar"):
            update_status("Mods found")
            return True
    update_status("No mods found")
    return False

def download_mods_from_github(minecraft_directory, update_status, error_message):
    mods_config = load_mods_config()
    repo_owner = mods_config["mods_repo"]["owner"]
    repo_name = mods_config["mods_repo"]["name"]
    branch = mods_config["mods_repo"]["branch"]
    folder_path = mods_config["mods_repo"]["folder_path"]
    mods_dir = os.path.join(minecraft_directory, "mods")
    
    update_status("Checking mods directory...")
    if not check_directory_permissions(mods_dir):
        error_message[0] = "No permissions to mods directory!"
        update_status("Permission error")
        return False
    
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}?ref={branch}"
    update_status("Requesting mods from GitHub...")
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        files = response.json()
        
        if not files:
            error_message[0] = "Mods folder empty!"
            update_status("No mods in repository")
            return False
        
        for file in files:
            if file["type"] == "file" and file["name"].endswith(".jar"):
                file_url = file["download_url"]
                file_name = file["name"]
                file_path = os.path.join(mods_dir, file_name)
                
                if not os.path.exists(file_path):
                    update_status(f"Downloading {file_name}...")
                    file_response = requests.get(file_url, stream=True)
                    file_response.raise_for_status()
                    
                    with open(file_path, "wb") as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    update_status(f"Downloaded {file_name}")
                else:
                    update_status(f"{file_name} already exists")
        
        if check_mods_exist(minecraft_directory, update_status):
            update_status("Mods downloaded successfully")
            return True
        else:
            error_message[0] = "No mods downloaded!"
            update_status("Mods download failed")
            return False
                
    except requests.exceptions.RequestException as e:
        error_message[0] = "Failed to download mods!"
        update_status("Download error")
        return False
    except Exception as e:
        error_message[0] = "Unknown error while downloading mods!"
        update_status("Unknown error")
        return False