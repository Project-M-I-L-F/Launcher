import subprocess
import os
import platform
import requests
import zipfile
import tarfile
from .config_manager import load_java_config

def check_java(update_status):
    update_status("Checking Java...")
    try:
        result = subprocess.run(["java", "-version"], capture_output=True, text=True, check=True)
        update_status("Java found")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        update_status("Java not found")
        return False

def download_and_install_java(install_dir, update_status, error_message):
    java_config = load_java_config()
    java_urls = java_config["java_urls"]
    system = platform.system().lower()
    arch = platform.machine().lower()
    
    if system == "windows":
        if "64" in arch:
            java_url = java_urls["windows_x64"]["url"]
            java_filename = java_urls["windows_x64"]["filename"]
        else:
            error_message[0] = "Only 64-bit Windows supported!"
            update_status("Unsupported system")
            return None
    elif system == "linux":
        if "64" in arch:
            java_url = java_urls["linux_x64"]["url"]
            java_filename = java_urls["linux_x64"]["filename"]
        else:
            error_message[0] = "Only 64-bit Linux supported!"
            update_status("Unsupported system")
            return None
    elif system == "darwin":
        if "arm" in arch:
            java_url = java_urls["macos_arm"]["url"]
            java_filename = java_urls["macos_arm"]["filename"]
        else:
            java_url = java_urls["macos_x64"]["url"]
            java_filename = java_urls["macos_x64"]["filename"]
    else:
        error_message[0] = "Unsupported OS!"
        update_status("Unsupported system")
        return None

    os.makedirs(install_dir, exist_ok=True)
    java_zip_path = os.path.join(install_dir, java_filename)

    update_status("Downloading Java...")
    response = requests.get(java_url, stream=True)
    with open(java_zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    update_status("Java downloaded")

    update_status("Extracting Java...")
    if java_filename.endswith(".zip"):
        with zipfile.ZipFile(java_zip_path, "r") as zip_ref:
            zip_ref.extractall(install_dir)
    elif java_filename.endswith(".tar.gz"):
        with tarfile.open(java_zip_path, "r:gz") as tar_ref:
            tar_ref.extractall(install_dir)
    update_status("Java extracted")

    os.remove(java_zip_path)

    java_home = None
    for item in os.listdir(install_dir):
        item_path = os.path.join(install_dir, item)
        if os.path.isdir(item_path) and "jdk" in item.lower():
            java_home = item_path
            break

    if not java_home:
        error_message[0] = "Java folder not found!"
        update_status("Java extraction error")
        return None

    java_bin = os.path.join(java_home, "bin", "java")
    if system == "windows":
        java_bin += ".exe"
    try:
        result = subprocess.run([java_bin, "-version"], capture_output=True, text=True, check=True)
        update_status("Java installed")
        return java_home
    except subprocess.CalledProcessError as e:
        error_message[0] = "Java verification failed!"
        update_status("Java error")
        return None

def ensure_java(update_status, error_message):
    if check_java(update_status):
        return None
    install_dir = os.path.join(os.path.expanduser("~"), "custom_java")
    update_status("Installing Java...")
    java_home = download_and_install_java(install_dir, update_status, error_message)
    return java_home