# src/core/server_manager.py
import os
import nbtlib
from nbtlib.tag import Compound, List, String, Int
from .config_manager import load_game_config

def add_predefined_server(directory, update_status, error_message):
    game_config = load_game_config()
    server_data = game_config["server"]
    
    update_status("Adding server...")
    os.makedirs(directory, exist_ok=True)
    servers_file = os.path.join(directory, "servers.dat")
    
    try:
        server_list = List[Compound]()
        if os.path.exists(servers_file):
            try:
                nbt_file = nbtlib.load(servers_file)
                if "servers" in nbt_file:
                    server_list = nbt_file["servers"]
            except Exception as e:
                update_status("Creating new servers.dat")

        server_exists = any(
            server["ip"] == server_data["ip"] and int(server.get("port", 25565)) == server_data["port"]
            for server in server_list
        )

        if not server_exists:
            new_server = Compound({
                "name": String(server_data["name"]),
                "ip": String(server_data["ip"]),
                "port": Int(server_data["port"])
            })
            server_list.append(new_server)
            nbt_data = Compound({"servers": server_list})
            nbt_file = nbtlib.File(nbt_data)
            try:
                nbt_file.save(servers_file, gzipped=False)
            except TypeError:
                nbt_file.save(servers_file)
            update_status("Server added")
        else:
            update_status("Server already exists")

    except Exception as e:
        error_message[0] = "Failed to add server!"
        update_status("Server add error")