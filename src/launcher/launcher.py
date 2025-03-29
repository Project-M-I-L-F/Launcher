import minecraft_launcher_lib as mll
import subprocess
import os

def setup_minecraft_directory(directory_path):
    os.makedirs(directory_path, exist_ok=True)
    return directory_path

def install_minecraft_version(version, directory, java_home=None):
    installed_versions = mll.utils.get_installed_versions(directory)
    if not any(v["id"] == version for v in installed_versions):
        mll.install.install_minecraft_version(version, directory)
    print(f"Версія Minecraft {version} встановлена або вже присутня.")

def generate_launch_command(version, directory, auth_data, java_home=None):
    java_bin = os.path.join(java_home, "bin", "java" + (".exe" if os.name == "nt" else "")) if java_home else "java"
    options = {"username": auth_data["username"], "uuid": auth_data["uuid"], "access_token": auth_data["access_token"], "java_binary": java_bin}
    return mll.command.get_minecraft_command(version, directory, options)

def launch_minecraft(command):
    process = subprocess.Popen(command)
    process.wait()
    return process

def install_and_launch_minecraft(directory, minecraft_version, auth_data, on_complete_callback=None, java_home=None):
    try:
        directory = setup_minecraft_directory(directory)
        install_minecraft_version(minecraft_version, directory, java_home)
        command = generate_launch_command(minecraft_version, directory, auth_data, java_home)
        launch_minecraft(command)
        if on_complete_callback:
            on_complete_callback(True, "Minecraft запущено успішно.")
    except Exception as e:
        if on_complete_callback:
            on_complete_callback(False, f"Помилка: {e}")