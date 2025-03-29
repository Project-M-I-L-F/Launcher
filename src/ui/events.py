import pygame
import threading
import webbrowser
import os
import sys
import subprocess
from ..core.config_manager import save_user_config
from ..launcher.launcher import install_and_launch_minecraft
from ..core.server_manager import add_custom_server, add_predefined_server

def handle_events(events, running, settings_open, just_opened_settings, left_mouse_pressed, ram_dragging, play_rect, settings_rect, exit_rect, settings_window_rect, input_path_rect, input_username_rect, input_version_rect, input_server_ip_rect, ram_slider_rect, english_button_rect, ukrainian_button_rect, add_server_button_rect, logo_rect, instagram_rect, tiktok_rect, is_loading, input_path_active, input_username_active, input_version_active, input_server_ip_active, input_path_text, input_username_text, minecraft_version, server_ip, ram_value, current_language, minecraft_base_directory, minecraft_directory, update_status, error_message, window_width, window_height, java_home):
    for event in events:
        if event.type == pygame.QUIT:
            running[0] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            left_mouse_pressed[0] = True
            if play_rect.collidepoint(mouse_pos) and not is_loading[0] and not settings_open[0]:
                update_status("Checking directory...")
                # Логуємо шлях для дебагу
                print(f"Checking directory: {input_path_text[0]}")
                # Створюємо папку, якщо вона не існує
                try:
                    os.makedirs(input_path_text[0], exist_ok=True)
                except Exception as e:
                    error_message[0] = f"Failed to create directory: {e}"
                    update_status("Directory creation error")
                    continue
                # Перевіряємо права доступу
                if not os.access(input_path_text[0], os.W_OK):
                    error_message[0] = f"No permissions to directory: {input_path_text[0]}"
                    update_status("Permission error")
                    continue
                error_message[0] = None
                is_loading[0] = True
                update_status("Launching game...")
                minecraft_directory[0] = os.path.join(input_path_text[0], minecraft_version[0])
                add_predefined_server(minecraft_directory[0], update_status, error_message)
                threading.Thread(target=install_and_launch_minecraft, args=(minecraft_directory[0], minecraft_version[0], {"username": input_username_text[0], "uuid": "", "access_token": ""}, lambda success, msg: on_launch_complete(success, msg, is_loading, update_status, error_message, running), java_home)).start()
            elif settings_rect.collidepoint(mouse_pos) and not is_loading[0] and not settings_open[0]:
                settings_open[0] = True
                just_opened_settings[0] = True
            elif exit_rect.collidepoint(mouse_pos):
                running[0] = False
            if settings_open[0] and not just_opened_settings[0] and not settings_window_rect.collidepoint(mouse_pos):
                settings_open[0] = False
            if settings_open[0]:
                settings_mouse_pos = (mouse_pos[0] - (window_width - 500) // 2, mouse_pos[1] - (window_height - 350) // 2)
                if input_path_rect.collidepoint(settings_mouse_pos):
                    input_path_active[0], input_username_active[0], input_version_active[0], input_server_ip_active[0] = True, False, False, False
                elif input_username_rect.collidepoint(settings_mouse_pos):
                    input_path_active[0], input_username_active[0], input_version_active[0], input_server_ip_active[0] = False, True, False, False
                elif input_version_rect.collidepoint(settings_mouse_pos):
                    input_path_active[0], input_username_active[0], input_version_active[0], input_server_ip_active[0] = False, False, True, False
                    minecraft_directory[0] = os.path.join(minecraft_base_directory[0], minecraft_version[0])
                elif input_server_ip_rect.collidepoint(settings_mouse_pos):
                    input_path_active[0], input_username_active[0], input_version_active[0], input_server_ip_active[0] = False, False, False, True
                else:
                    input_path_active[0], input_username_active[0], input_version_active[0], input_server_ip_active[0] = False, False, False, False
                if ram_slider_rect.collidepoint(settings_mouse_pos):
                    ram_dragging[0] = True
                if english_button_rect.collidepoint(settings_mouse_pos):
                    current_language[0] = "en_us"
                    set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
                    save_user_config({"minecraft_directory": input_path_text[0], "username": input_username_text[0], "language": current_language[0], "ram": ram_value[0], "minecraft_version": minecraft_version[0]})
                if ukrainian_button_rect.collidepoint(settings_mouse_pos):
                    current_language[0] = "uk_ua"
                    set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
                    save_user_config({"minecraft_directory": input_path_text[0], "username": input_username_text[0], "language": current_language[0], "ram": ram_value[0], "minecraft_version": minecraft_version[0]})
                if add_server_button_rect.collidepoint(settings_mouse_pos) and server_ip[0]:
                    add_custom_server(minecraft_directory[0], server_ip[0], update_status, error_message)
                    server_ip[0] = ""
        elif event.type == pygame.MOUSEBUTTONUP:
            left_mouse_pressed[0], ram_dragging[0], just_opened_settings[0] = False, False, False
        elif event.type == pygame.MOUSEMOTION and ram_dragging[0] and settings_open[0]:
            settings_mouse_pos = (event.pos[0] - (window_width - 500) // 2, event.pos[1] - (window_height - 350) // 2)
            ram_value[0] = int(1 + (min(max(settings_mouse_pos[0], ram_slider_rect.x), ram_slider_rect.x + ram_slider_rect.width) - ram_slider_rect.x) / ram_slider_rect.width * (16 - 1))
            set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
            save_user_config({"minecraft_directory": input_path_text[0], "username": input_username_text[0], "language": current_language[0], "ram": ram_value[0], "minecraft_version": minecraft_version[0]})
        elif event.type == pygame.KEYDOWN and settings_open[0]:
            if input_path_active[0]:
                if event.key == pygame.K_BACKSPACE:
                    input_path_text[0] = input_path_text[0][:-1]
                elif event.key == pygame.K_RETURN:
                    input_path_active[0] = False
                    minecraft_base_directory[0] = input_path_text[0]
                    minecraft_directory[0] = os.path.join(minecraft_base_directory[0], minecraft_version[0])
                    set_minecraft_options(minecraft_directory[0], current_language[0], ram_value[0], update_status)
                    save_user_config({"minecraft_directory": input_path_text[0], "username": input_username_text[0], "language": current_language[0], "ram": ram_value[0], "minecraft_version": minecraft_version[0]})
                else:
                    input_path_text[0] += event.unicode
            elif input_username_active[0]:
                if event.key == pygame.K_BACKSPACE:
                    input_username_text[0] = input_username_text[0][:-1]
                elif event.key == pygame.K_RETURN:
                    input_username_active[0] = False
                    save_user_config({"minecraft_directory": input_path_text[0], "username": input_username_text[0], "language": current_language[0], "ram": ram_value[0], "minecraft_version": minecraft_version[0]})
                else:
                    input_username_text[0] += event.unicode
            elif input_version_active[0]:
                if event.key == pygame.K_BACKSPACE:
                    minecraft_version[0] = minecraft_version[0][:-1]
                elif event.key == pygame.K_RETURN:
                    input_version_active[0] = False
                    minecraft_directory[0] = os.path.join(minecraft_base_directory[0], minecraft_version[0])
                    save_user_config({"minecraft_directory": input_path_text[0], "username": input_username_text[0], "language": current_language[0], "ram": ram_value[0], "minecraft_version": minecraft_version[0]})
                else:
                    minecraft_version[0] += event.unicode
            elif input_server_ip_active[0]:
                if event.key == pygame.K_BACKSPACE:
                    server_ip[0] = server_ip[0][:-1]
                elif event.key == pygame.K_RETURN:
                    input_server_ip_active[0] = False
                else:
                    server_ip[0] += event.unicode
            elif event.key == pygame.K_ESCAPE:
                settings_open[0] = False
    if left_mouse_pressed[0]:
        if instagram_rect and instagram_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://www.instagram.com/web.universe.ua/")
        if tiktok_rect and tiktok_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://www.tiktok.com/@web.universe.ua")
        if logo_rect and logo_rect.collidepoint(pygame.mouse.get_pos()):
            webbrowser.open("https://webuniverseua.com")

def on_launch_complete(success, message, is_loading, update_status, error_message, running):
    is_loading[0] = False
    update_status("Game launched" if success else "Launch error")
    if success:
        running[0] = False
        pygame.quit()
        subprocess.Popen([sys.executable, sys.argv[0]])
        sys.exit()
    else:
        error_message[0] = "Game launch failed!"

def set_minecraft_options(directory, language, ram, update_status):
    update_status("Saving options...")
    options_path = os.path.join(directory, "options.txt")
    os.makedirs(directory, exist_ok=True)
    lines = []
    if os.path.exists(options_path):
        with open(options_path, "r") as f:
            lines = f.readlines()
    lang_found = ram_found = False
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