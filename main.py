# main.py
import sys
import os

# Додаємо кореневий каталог проекту до sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import pygame
import tkinter as tk
from src.core.config_manager import load_user_config, load_game_config, save_user_config
from src.core.java_manager import ensure_java
from src.core.server_manager import add_predefined_server
from src.ui.display import draw_text, draw_button, draw_icon_button, draw_status_message
from src.ui.settings import draw_settings_window
from src.ui.events import handle_events
from src.utils.helpers import resource_path, update_status

# Ініціалізація Pygame
pygame.init()

# Ініціалізація Tkinter (для вибору файлу)
root = tk.Tk()
root.withdraw()

# Налаштування вікна (960x540)
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("WEB UNIVERSE LAUNCHER")

# Кольори
WHITE = (255, 255, 255)
PURPLE = (147, 112, 219)
DARK_PURPLE = (75, 0, 130)
GRAY = (200, 200, 200)
LIGHT_PURPLE = (200, 162, 255)

# Завантаження шрифту
font_path = resource_path("source/fonts/Minecraft.ttf")
title_font = pygame.font.Font(font_path, 50)
button_font = pygame.font.Font(font_path, 20)
profile_font = pygame.font.Font(font_path, 20)
settings_title_font = pygame.font.Font(font_path, 16)
input_font = pygame.font.Font(font_path, 18)

# Завантаження зображень
cloud_image = pygame.image.load(resource_path("source/images/cloud.png"))
rocket_icon = pygame.image.load(resource_path("source/images/WU_rocket.png"))
settings_icon = pygame.image.load(resource_path("source/images/WU_space.png"))
logo_icon = pygame.image.load(resource_path("source/images/WU_logo.png"))
instagram_icon = pygame.image.load(resource_path("source/images/WU_instagram.png"))
tiktok_icon = pygame.image.load(resource_path("source/images/WU_tiktok.png"))

# Зміна розміру хмари
base_height = WINDOW_HEIGHT
scale_factor = 1.32
new_height = int(base_height * scale_factor)
new_width = int(cloud_image.get_width() * (new_height / cloud_image.get_height()))
cloud_image = pygame.transform.scale(cloud_image, (new_width, new_height))

# Завантаження конфігурації
config = load_user_config()
minecraft_directory = [config["minecraft_directory"]]
input_path_text = [config["minecraft_directory"]]
input_username_text = [config["username"]]
current_language = [config["language"]]
ram_value = [config["ram"]]
skin_path = [config["skin_path"]]

# Ініціалізація стану
is_loading = [False]
status_message = [""]
error_message = [None]
settings_open = [False]
just_opened_settings = [False]
left_mouse_pressed = [False]
ram_dragging = [False]
input_path_active = [False]
input_username_active = [False]
running = [True]

# Ініціалізація скіна
skin_image = [None]
if skin_path[0] and os.path.exists(skin_path[0]):
    try:
        skin_image[0] = pygame.image.load(skin_path[0])
        skin_image[0] = pygame.transform.scale(skin_image[0], (32, 32))
    except Exception as e:
        print(f"Failed to load skin: {e}")
        skin_image[0] = None

# Визначення прямокутників для кнопок і полів вводу
play_rect = pygame.Rect(50, 150, 200, 50)
settings_rect = pygame.Rect(50, 210, 200, 50)
mods_rect = pygame.Rect(50, 270, 200, 50)
exit_rect = pygame.Rect(50, 330, 200, 50)
input_path_rect = pygame.Rect(25, 50, 450, 25)
input_username_rect = pygame.Rect(25, 100, 450, 25)
english_button_rect = pygame.Rect(25, 150, 150, 30)
ukrainian_button_rect = pygame.Rect(200, 150, 150, 30)
choose_skin_button_rect = pygame.Rect(375, 150, 100, 30)
ram_slider_rect = pygame.Rect(25, 200, 150, 10)

# Налаштування вікна налаштувань
settings_window = pygame.Surface((500, 300))
settings_window_rect = pygame.Rect((WINDOW_WIDTH - 500) // 2, (WINDOW_HEIGHT - 300) // 2, 500, 300)

# Ініціалізація прямокутників для іконок (перед циклом)
logo_rect = None
instagram_rect = None
tiktok_rect = None

# Початкові налаштування
java_home = ensure_java(lambda msg: update_status(msg, status_message), error_message)
add_predefined_server(minecraft_directory[0], lambda msg: update_status(msg, status_message), error_message)

# Основний цикл
clock = pygame.time.Clock()
while running[0]:
    events = pygame.event.get()

    # Малюємо іконки та оновлюємо їх прямокутники перед обробкою подій
    window.fill(WHITE)
    window.blit(cloud_image, (0, -110))

    # Напис
    draw_text("WEB UNIVERSE", title_font, PURPLE, window, 500, 50)
    draw_text("LAUNCHER", title_font, PURPLE, window, 500, 100)

    # Логотипи
    logo_rect = draw_icon_button(window, logo_icon, 750, 450, 70)
    instagram_rect = draw_icon_button(window, instagram_icon, 830, 450, 50)
    tiktok_rect = draw_icon_button(window, tiktok_icon, 890, 450, 50)

    # Обробка подій (тепер logo_rect, instagram_rect, tiktok_rect визначені)
    handle_events(events, running, settings_open, just_opened_settings, left_mouse_pressed, ram_dragging, play_rect, settings_rect, mods_rect, exit_rect, settings_window_rect, input_path_rect, input_username_rect, ram_slider_rect, english_button_rect, ukrainian_button_rect, choose_skin_button_rect, logo_rect, instagram_rect, tiktok_rect, is_loading, input_path_active, input_username_active, input_path_text, input_username_text, ram_value, current_language, skin_path, skin_image, minecraft_directory, lambda msg: update_status(msg, status_message), error_message, WINDOW_WIDTH, WINDOW_HEIGHT, java_home)

    # Малюємо кнопки
    is_play_pressed = play_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0]
    is_settings_pressed = settings_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0]
    is_mods_pressed = mods_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0]
    is_exit_pressed = exit_rect.collidepoint(pygame.mouse.get_pos()) and left_mouse_pressed[0]

    draw_button(window, play_rect, "PLAY", button_font, WHITE, DARK_PURPLE, rocket_icon, is_play_pressed)
    draw_button(window, settings_rect, "SETTINGS", button_font, WHITE, DARK_PURPLE, settings_icon, is_settings_pressed)
    draw_button(window, mods_rect, "MODS", button_font, WHITE, DARK_PURPLE, pressed=is_mods_pressed)
    draw_button(window, exit_rect, "EXIT", button_font, WHITE, DARK_PURPLE, pressed=is_exit_pressed)

    # Відображаємо статус або помилку
    draw_status_message(window, status_message[0], error_message[0], profile_font, WINDOW_WIDTH, WINDOW_HEIGHT)

    if settings_open[0]:
        draw_settings_window(window, settings_window, pygame.mouse.get_pos(), left_mouse_pressed[0], ram_dragging[0], input_path_rect, input_path_text[0], input_path_active[0], input_username_rect, input_username_text[0], input_username_active[0], english_button_rect, ukrainian_button_rect, choose_skin_button_rect, ram_slider_rect, ram_value[0], skin_image[0], WINDOW_WIDTH, WINDOW_HEIGHT, PURPLE, WHITE, DARK_PURPLE, settings_title_font, button_font, input_font, LIGHT_PURPLE, GRAY)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()