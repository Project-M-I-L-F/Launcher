# src/ui/events.py
import pygame
import threading
import webbrowser
import os
import subprocess
from ..core.config_manager import save_user_config, load_game_config
from ..core.mods_manager import check_directory_permissions, check_mods_exist, download_mods_from_github
from ..launcher.launcher import install_and_launch_forge
from ..core.server_manager import add_predefined_server
from .settings import choose_skin

def handle_events(events, running, settings_open, just_opened_settings, left_mouse_pressed, ram_dragging, play_rect, settings_rect, mods_rect, exit_rect, settings_window_rect, input_path_rect, input_username_rect, ram_slider_rect, english_button_rect, ukrainian_button_rect, choose_skin_button_rect, logo_rect, instagram_rect, tiktok_rect, is_loading, input_path_active, input_username_active, input_path_text, input_username_text, ram_value, current_language, skin_path, skin_image, minecraft_directory, update_status, error_message, window_width, window_height, java_home):
    for event in events:
        if event.type == pygame.QUIT:
            running[0] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            left_mouse_pressed[0] = True

            if play_rect.collidepoint(mouse_pos) and not is_loading[0] and not settings_open[0]:
                update_status("Checking directory...")
                if not check_directory_permissions(input_path_text[0]):
                    error_message[0] = "No permissions to directory!"
                    update_status("Permission error")
                    continue
                if not check_mods_exist(input_path_text[0], update_status):
                    update_status("Downloading mods...")
                    if not download_mods_from_github(input_path_text[0], update_status, error_message):
                        update_status("Mods download failed")
                        continue
                else:
                    update_status("Mods already downloaded")
                error_message[0] = None
                is_loading[0] = True
                update_status("Launching game...")
                game_config = load_game_config()
                threading.Thread(target=install_and_launch_forge, args=(input_path_text[0], game_config["minecraft_version"], game_config["forge_version"], {"username": input_username_text[0], "uuid": "", "access_token": ""}, lambda success, msg: on_launch_complete(success, msg, is_loading, update_status, error_message, input_path_text[0]), java_home)).start()

            elif settings_rect.collidepoint(mouse_pos) and not is_loading[0] and not settings_open[0]:
                settings_open[0] = True
                just_opened_settings[0] = True

            elif mods_rect.collidepoint(mouse_pos) and not is_loading[0] and not settings_open[0]:
                open_mods_folder(minecraft_directory, update_status, error_message)

            elif exit_rect.collidepoint(mouse_pos):
                running[0] = False

            if settings_open[0] and not just_opened_settings[0] and not settings_window_rect.collidepoint(mouse_pos):
                settings_open[0] = False

            if settings_open[0]:
                settings_mouse_pos = (mouse_pos[0] - (window_width - 500) // 2, mouse_pos[1] - (window_height - 300) // 2)
                if input_path_rect.collidepoint(settings_mouse_pos):
                    input_path_active[0] = True
                    input_username_active[0] = False
                elif input_username_rect.collidepoint(settings_mouse_pos):
                    input_username_active[0] = True
                    input_path_active[0] = False
                else:
                    input_path_active[0] = False
                    input_username_active[0] = False

                if ram_slider_rect.collidepoint(settings_mouse_pos):
                    ram_dragging[0] = True

                if english_button_rect.collidepoint(settings_mouse_pos):
                    current_language[0] = "en_us"
                    set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
                    save_user_config({
                        "minecraft_directory": input_path_text[0],
                        "username": input_username_text[0],
                        "language": current_language[0],
                        "ram": ram_value[0],
                        "skin_path": skin_path[0]
                    })

                if ukrainian_button_rect.collidepoint(settings_mouse_pos):
                    current_language[0] = "uk_ua"
                    set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
                    save_user_config({
                        "minecraft_directory": input_path_text[0],
                        "username": input_username_text[0],
                        "language": current_language[0],
                        "ram": ram_value[0],
                        "skin_path": skin_path[0]
                    })

                if choose_skin_button_rect.collidepoint(settings_mouse_pos):
                    choose_skin(skin_path, skin_image, input_path_text[0], input_username_text[0], current_language[0], ram_value[0], update_status, error_message)

        elif event.type == pygame.MOUSEBUTTONUP:
            left_mouse_pressed[0] = False
            ram_dragging[0] = False
            just_opened_settings[0] = False

        elif event.type == pygame.MOUSEMOTION and ram_dragging[0] and settings_open[0]:
            settings_mouse_pos = (event.pos[0] - (window_width - 500) // 2, event.pos[1] - (window_height - 300) // 2)
            slider_pos = min(max(settings_mouse_pos[0], ram_slider_rect.x), ram_slider_rect.x + ram_slider_rect.width)
            ram_value[0] = int(1 + (slider_pos - ram_slider_rect.x) / ram_slider_rect.width * (16 - 1))
            set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
            save_user_config({
                "minecraft_directory": input_path_text[0],
                "username": input_username_text[0],
                "language": current_language[0],
                "ram": ram_value[0],
                "skin_path": skin_path[0]
            })

        elif event.type == pygame.KEYDOWN and settings_open[0]:
            if input_path_active[0]:
                if event.key == pygame.K_BACKSPACE:
                    input_path_text[0] = input_path_text[0][:-1]
                elif event.key == pygame.K_RETURN:
                    input_path_active[0] = False
                    minecraft_directory[0] = input_path_text[0]
                    add_predefined_server(minecraft_directory[0], update_status, error_message)
                    set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
                    save_user_config({
                        "minecraft_directory": input_path_text[0],
                        "username": input_username_text[0],
                        "language": current_language[0],
                        "ram": ram_value[0],
                        "skin_path": skin_path[0]
                    })
                else:
                    input_path_text[0] += event.unicode
            elif input_username_active[0]:
                if event.key == pygame.K_BACKSPACE:
                    input_username_text[0] = input_username_text[0][:-1]
                elif event.key == pygame.K_RETURN:
                    input_username_active[0] = False
                    save_user_config({
                        "minecraft_directory": input_path_text[0],
                        "username": input_username_text[0],
                        "language": current_language[0],
                        "ram": ram_value[0],
                        "skin_path": skin_path[0]
                    })
                else:
                    input_username_text[0] += event.unicode
            elif event.key == pygame.K_ESCAPE:
                settings_open[0] = False

    if left_mouse_pressed[0]:
        if instagram_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://www.instagram.com/web.universe.ua/")
        if tiktok_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://www.tiktok.com/@web.universe.ua")
        if logo_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://webuniverseua.com")

def on_launch_complete(success, message, is_loading, update_status, error_message, minecraft_directory):
    is_loading[0] = False
    if success:
        update_status("Forge installed")
        if not check_mods_exist(minecraft_directory, update_status):
            update_status("Downloading mods after Forge install...")
            if not download_mods_from_github(minecraft_directory, update_status, error_message):
                update_status("Mods download failed")
                return
        update_status("Game launched")
        logs_dir = os.path.join(minecraft_directory, "logs")
        latest_log = os.path.join(logs_dir, "latest.log")
        if os.path.exists(latest_log):
            update_status("Log created")
        else:
            update_status("Log not created")
    else:
        error_message[0] = "Game launch failed!"
        update_status("Launch error")

def open_mods_folder(minecraft_directory, update_status, error_message):
    update_status("Opening mods folder...")
    mods_dir = os.path.join(minecraft_directory[0], "mods")
    try:
        os.makedirs(mods_dir, exist_ok=True)
        update_status("Mods folder ready")
    except Exception as e:
        error_message[0] = "Failed to create mods folder!"
        update_status("Mods folder error")
        return

    try:
        if os.name == "nt":
            os.startfile(mods_dir)
        elif sys.platform == "darwin":
            subprocess.run(["open", mods_dir])
        else:
            subprocess.run(["xdg-open", mods_dir])
        update_status("Mods folder opened")
    except Exception as e:
        error_message[0] = "Failed to open mods folder!"
        update_status("Folder open error")

def set_minecraft_options(directory, language, ram, update_status):
    update_status("Saving options...")
    options_path = os.path.join(directory, "options.txt")
    os.makedirs(directory, exist_ok=True)
    lines = []
    if os.path.exists(options_path):
        with open(options_path, "r") as f:
            lines = f.readlines()

    lang_found = False
    ram_found = False
    for i, line in enumerate(lines):
        if line.startswith("lang:"):
            lines[i] = f"lang:{language}\n"
            lang_found = True
        if line.startswith("jvm_args:"):
            lines[i] = f"jvm_args:-Xmx{ram}G\n"
            ram_found = True
    if not lang_found:
        lines.append(f"lang:{language}\n")
    if not ram_found:
        lines.append(f"jvm_args:-Xmx{ram}G\n")

    with open(options_path, "w") as f:
        f.writelines(lines)
    update_status("Options saved")