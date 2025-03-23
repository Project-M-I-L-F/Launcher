import minecraft_launcher_lib as mll
import subprocess
import os

from src.java_installer import java_installer


DEFAULT_MINECRAFT_FOLDER = "C:/Users/USER/AppData/Roaming/WebSkillMinecraft"
DEFAULT_MINECRAFT_VERSION = "1.20.1"
DEFAULT_MINECRAFT_FORGE_VERSION = "1.20.1-47.3.0"

class MinecraftLan:

#Public methods
    def __init__(
        self, 
        location_minecraft: str = DEFAULT_MINECRAFT_FOLDER,
        version_minecraft: str = DEFAULT_MINECRAFT_VERSION,
        version_forge: str = DEFAULT_MINECRAFT_FORGE_VERSION
    ):
        self.__location_minecraft = location_minecraft
        self.__version_minecraft = version_minecraft
        self.__version_forge = version_forge
        self.__installed = False
        self.__installed_forge = False

        self.__java_installer = java_installer.JavaChecker(reserved_location = "D:/Java")
        self.__java_installer.install()

    def __str__(self):
        return f"MinecraftLan: {self.__location_minecraft}, {self.__version_minecraft}, {self.__version_forge}"

#Custom public methods

    def install_minecraft(self):
        self.__setup_minecraft_directory()
        self.__сheck_and_install_minecraft()
        self.__сheck_and_install_forge()
        return self.__installed and self.__installed_forge
    
    def generate_launch_command(self, auth_data):
        java_home = self.__java_installer.get_location()
        java_bin = "java"
        if java_home:
            java_bin = os.path.join(java_home, "bin", "java")
            if os.name == "nt":
                java_bin += ".exe"

        forge_full_version = mll.forge.find_forge_version(self.__version_forge)
        if forge_full_version is None:
            installed_versions = mll.utils.get_installed_versions(self.__location_minecraft)
            forge_short_version = self.__version_forge.split('-')[1]
            forge_full_version = next((v["id"] for v in installed_versions if "forge" in v["id"] and forge_short_version in v["id"]), None)
            if forge_full_version is None:
                print(f"Встановлені версії в {self.__location_minecraft}: {installed_versions}")
                raise ValueError(f"Forge версія {self.__version_forge} не знайдена після встановлення")
        print(f"Використовується Forge версія: {forge_full_version}")

        options = {
            "username": auth_data["username"],
            "uuid": auth_data["uuid"],
            "access_token": auth_data["access_token"],
            "java_binary": java_bin
        }
        return mll.command.get_minecraft_command(forge_full_version, self.__location_minecraft, options)
    
    def launch_minecraft(command):
        try:
            subprocess.Popen(command)
            print("Minecraft запущено!")
        except Exception as e:
            print(f"Помилка при запуску Minecraft: {e}")
            raise

    def install_and_launch(self, auth_data):
        self.install_minecraft()
        command = self.generate_launch_command(auth_data)
        self.launch_minecraft(command)

#Private methods
    def __setup_minecraft_directory(self):
        if not os.path.exists(self.__location_minecraft):
            self.__installed = False
            self.__installed_forge = False
            os.makedirs(self.__location_minecraft)

    def __сheck_and_install_minecraft (self) -> None:
        if not self.__check_minecraft():
            self.__install_minecraft()
    
    def __сheck_and_install_forge(self):
        if not self.__check_forge():
            self.__install_forge()
#checked methods
    def __check_minecraft(self):
        try:
            installed_versions = mll.utils.get_installed_versions(self.__location_minecraft)
            if not any(v["id"] == self.__version_minecraft for v in installed_versions):
                self.__installed = False
            else:
                self.__installed = True
            return self.__installed
        except Exception as e:
            self.__installed = False
            return self.__installed

    def __check_forge(self):
        try:
            installed_versions = mll.utils.get_installed_versions(self.__location_minecraft)
            forge_full_version = f"{self.__version_minecraft}-forge-{self.__version_forge.split('-')[1]}"
            if not any(v["id"] == forge_full_version for v in installed_versions):
                self.__installed_forge = False                
            else:
                self.__installed_forge = True
            return self.__installed_forge
        except Exception as e:
            self.__installed_forge = False

#install methods
    def __install_minecraft(self):
        mll.install.install_minecraft_version(self.__version_minecraft, self.__location_minecraft)
        self.__installed = True

    def __install_forge(self):
        available_forge_versions = mll.forge.list_forge_versions()
        if self.__version_forge in available_forge_versions and self.__installed:
            mll.forge.install_forge_version(self.__version_forge, self.__location_minecraft)
            self.__installed_forge = True
        else:
            self.__installed_forge = False
