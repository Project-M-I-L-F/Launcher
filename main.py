import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pygame
import tkinter as tk
from src.core.config_manager import load_user_config, save_user_config
from src.core.java_manager import ensure_java
from src.core.server_manager import add_predefined_server
from src.ui.display import draw_text, draw_button, draw_icon_button, draw_status_message
from src.ui.settings import draw_settings_window
from src.ui.events import handle_events
from src.utils.helpers import resource_path, update_status

pygame.init()
root = tk.Tk()
root.withdraw()

WINDOW_WIDTH, WINDOW_HEIGHT = 960, 540
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("WEB UNIVERSE LAUNCHER")

WHITE, PURPLE, DARK_PURPLE, GRAY, LIGHT_PURPLE = (255, 255, 255), (147, 112, 219), (75, 0, 130), (200, 200, 200), (200, 162, 255)

font_path = resource_path("source/fonts/Minecraft.ttf")
title_font, button_font, profile_font, settings_title_font, input_font = pygame.font.Font(font_path, 60), pygame.font.Font(font_path, 20), pygame.font.Font(font_path, 20), pygame.font.Font(font_path, 16), pygame.font.Font(font_path, 18)

cloud_image = pygame.transform.scale(pygame.image.load(resource_path("source/images/cloud.png")), (int(960 * 1.32 / 540 * 960), int(540 * 1.32)))
rocket_icon, settings_icon, logo_icon, instagram_icon, tiktok_icon = pygame.image.load(resource_path("source/images/WU_rocket.png")), pygame.image.load(resource_path("source/images/WU_space.png")), pygame.image.load(resource_path("source/images/WU_logo.png")), pygame.image.load(resource_path("source/images/WU_instagram.png")), pygame.image.load(resource_path("source/images/WU_tiktok.png"))

config = load_user_config()
minecraft_base_directory, input_path_text, input_username_text, current_language, ram_value, minecraft_version = [config["minecraft_directory"]], [config["minecraft_directory"]], [config["username"]], [config["language"]], [config["ram"]], [config.get("minecraft_version", "1.20.1")]  # Дефолтна версія 1.20.1
server_ip = [""]

# Формуємо шлях до папки з версією
minecraft_directory = [os.path.join(minecraft_base_directory[0], minecraft_version[0])]

is_loading, status_message, error_message, settings_open, just_opened_settings, left_mouse_pressed, ram_dragging = [False], [""], [None], [False], [False], [False], [False]
input_path_active, input_username_active, input_version_active, input_server_ip_active = [False], [False], [False], [False]
running = [True]

play_rect, settings_rect, exit_rect = pygame.Rect(50, 150, 200, 50), pygame.Rect(50, 210, 200, 50), pygame.Rect(50, 270, 200, 50)
input_path_rect, input_username_rect, input_version_rect, input_server_ip_rect = pygame.Rect(25, 50, 450, 25), pygame.Rect(25, 100, 450, 25), pygame.Rect(25, 150, 450, 25), pygame.Rect(25, 200, 450, 25)
english_button_rect, ukrainian_button_rect, add_server_button_rect, ram_slider_rect = pygame.Rect(25, 250, 150, 30), pygame.Rect(195, 250, 150, 30), pygame.Rect(365, 250, 110, 30), pygame.Rect(25, 300, 150, 10)

settings_window = pygame.Surface((500, 350))
settings_window_rect = pygame.Rect((WINDOW_WIDTH - 500) // 2, (WINDOW_HEIGHT - 350) // 2, 500, 350)

java_home = ensure_java(lambda msg: update_status(msg, status_message), error_message)

clock = pygame.time.Clock()
while running[0]:
    events = pygame.event.get()
    window.fill(WHITE)
    window.blit(cloud_image, (0, -110))
    
    web_universe_text = title_font.render("WEB UNIVERSE", True, WHITE)
    launcher_text = title_font.render("LAUNCHER", True, WHITE)
    web_universe_rect = web_universe_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
    launcher_rect = launcher_text.get_rect(center=(WINDOW_WIDTH // 2, 110))
    window.blit(web_universe_text, web_universe_rect)
    window.blit(launcher_text, launcher_rect)

    logo_rect = draw_icon_button(window, logo_icon, 750, 450, 70)
    instagram_rect = draw_icon_button(window, instagram_icon, 830, 450, 50)
    tiktok_rect = draw_icon_button(window, tiktok_icon, 890, 450, 50)

    handle_events(events, running, settings_open, just_opened_settings, left_mouse_pressed, ram_dragging, play_rect, settings_rect, exit_rect, settings_window_rect, input_path_rect, input_username_rect, input_version_rect, input_server_ip_rect, ram_slider_rect, english_button_rect, ukrainian_button_rect, add_server_button_rect, logo_rect, instagram_rect, tiktok_rect, is_loading, input_path_active, input_username_active, input_version_active, input_server_ip_active, input_path_text, input_username_text, minecraft_version, server_ip, ram_value, current_language, minecraft_base_directory, minecraft_directory, lambda msg: update_status(msg, status_message), error_message, WINDOW_WIDTH, WINDOW_HEIGHT, java_home)

    is_play_pressed, is_settings_pressed, is_exit_pressed = play_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0], settings_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0], exit_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0]
    draw_button(window, play_rect, "PLAY", button_font, WHITE, DARK_PURPLE, rocket_icon, is_play_pressed)
    draw_button(window, settings_rect, "SETTINGS", button_font, WHITE, DARK_PURPLE, settings_icon, is_settings_pressed)
    draw_button(window, exit_rect, "EXIT", button_font, WHITE, DARK_PURPLE, pressed=is_exit_pressed)

    draw_status_message(window, status_message[0], error_message[0], profile_font, WINDOW_WIDTH, WINDOW_HEIGHT)
    if settings_open[0]:
        draw_settings_window(window, settings_window, pygame.mouse.get_pos(), left_mouse_pressed[0], ram_dragging[0], input_path_rect, input_path_text[0], input_path_active[0], input_username_rect, input_username_text[0], input_username_active[0], input_version_rect, minecraft_version[0], input_version_active[0], input_server_ip_rect, server_ip[0], input_server_ip_active[0], english_button_rect, ukrainian_button_rect, add_server_button_rect, ram_slider_rect, ram_value[0], WINDOW_WIDTH, WINDOW_HEIGHT, PURPLE, WHITE, DARK_PURPLE, settings_title_font, button_font, input_font, LIGHT_PURPLE, GRAY)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()