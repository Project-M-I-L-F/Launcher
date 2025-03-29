import os
import nbtlib
from nbtlib.tag import Compound, List, String, Int
from .config_manager import load_game_config

def add_predefined_server(directory, update_status, error_message):
    game_config = load_game_config()
    server_data = game_config["server"]
    update_status("Adding predefined server...")
    servers_file = os.path.join(directory, "servers.dat")
    os.makedirs(directory, exist_ok=True)
    try:
        server_list = List[Compound]()
        if os.path.exists(servers_file):
            nbt_file = nbtlib.load(servers_file)
            if "servers" in nbt_file:
                server_list = nbt_file["servers"]
        if not any(server["ip"] == server_data["ip"] and int(server.get("port", 25565)) == server_data["port"] for server in server_list):
            server_list.append(Compound({"name": String(server_data["name"]), "ip": String(server_data["ip"]), "port": Int(server_data["port"])}))
            nbtlib.File({"servers": server_list}).save(servers_file, gzipped=False)
            update_status("Predefined server added")
        else:
            update_status("Predefined server already exists")
    except Exception as e:
        error_message[0] = "Failed to add predefined server!"
        update_status(f"Server add error: {e}")

def add_custom_server(directory, server_ip, update_status, error_message):
    update_status("Adding custom server...")
    servers_file = os.path.join(directory, "servers.dat")
    os.makedirs(directory, exist_ok=True)
    try:
        server_list = List[Compound]()
        if os.path.exists(servers_file):
            nbt_file = nbtlib.load(servers_file)
            if "servers" in nbt_file:
                server_list = nbt_file["servers"]
        server_list.append(Compound({"name": String("Custom Server"), "ip": String(server_ip), "port": Int(25565)}))
        nbtlib.File({"servers": server_list}).save(servers_file, gzipped=False)
        update_status("Custom server added")
    except Exception as e:
        error_message[0] = "Failed to add custom server!"
        update_status(f"Server add error: {e}")