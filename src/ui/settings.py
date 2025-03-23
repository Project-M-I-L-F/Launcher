# src/ui/settings.py
import os
import shutil
import pygame
from tkinter import filedialog
from ..core.config_manager import save_user_config
from .display import draw_text, draw_input_field, draw_settings_button, draw_ram_slider

def draw_settings_window(window, settings_window, mouse_pos, left_pressed, ram_dragging, input_path_rect, input_path_text, input_path_active, input_username_rect, input_username_text, input_username_active, english_button_rect, ukrainian_button_rect, choose_skin_button_rect, ram_slider_rect, ram_value, skin_image, window_width, window_height, purple, white, dark_purple, settings_title_font, button_font, input_font, light_purple, gray):
    settings_window.fill(purple)
    draw_text("Settings", settings_title_font, white, settings_window, 200, 15)
    
    draw_input_field(settings_window, input_path_rect, input_path_text, input_path_active, "Minecraft Directory", input_font, light_purple, gray, white)
    draw_input_field(settings_window, input_username_rect, input_username_text, input_username_active, "Username", input_font, light_purple, gray, white)

    settings_mouse_pos = (mouse_pos[0] - (window_width - 500) // 2, mouse_pos[1] - (window_height - 300) // 2)
    
    is_english_pressed = english_button_rect.collidepoint(settings_mouse_pos) and left_pressed
    is_ukrainian_pressed = ukrainian_button_rect.collidepoint(settings_mouse_pos) and left_pressed
    is_choose_skin_pressed = choose_skin_button_rect.collidepoint(settings_mouse_pos) and left_pressed
    draw_settings_button(settings_window, english_button_rect, "English", button_font, white, dark_purple, pressed=is_english_pressed)
    draw_settings_button(settings_window, ukrainian_button_rect, "Ukrainian", button_font, white, dark_purple, pressed=is_ukrainian_pressed)
    draw_settings_button(settings_window, choose_skin_button_rect, "Choose Skin", button_font, white, dark_purple, pressed=is_choose_skin_pressed)
    
    draw_ram_slider(settings_window, ram_slider_rect, ram_value, 1, 16, ram_dragging, input_font, gray, light_purple, white)
    
    if skin_image:
        draw_text("Current Skin:", input_font, white, settings_window, 375, 175)
        settings_window.blit(skin_image, (375, 195))
    
    window.blit(settings_window, ((window_width - 500) // 2, (window_height - 300) // 2))

def choose_skin(skin_path, skin_image, input_path_text, input_username_text, current_language, ram_value, update_status, error_message):
    update_status("Choosing skin...")
    skins_dir = "skins"
    os.makedirs(skins_dir, exist_ok=True)
    
    file_path = filedialog.askopenfilename(
        initialdir=skins_dir,
        title="Choose a Skin",
        filetypes=[("PNG files", "*.png")]
    )
    
    if file_path:
        skin_path[0] = file_path
        try:
            skin_image[0] = pygame.image.load(skin_path[0])
            skin_image[0] = pygame.transform.scale(skin_image[0], (32, 32))
            update_status("Skin chosen")
            
            minecraft_dir = input_path_text
            target_skin_path = os.path.join(minecraft_dir, "skin.png")
            os.makedirs(minecraft_dir, exist_ok=True)
            shutil.copy(skin_path[0], target_skin_path)
            update_status("Skin copied")
            
            save_user_config({
                "minecraft_directory": input_path_text,
                "username": input_username_text,
                "language": current_language,
                "ram": ram_value,
                "skin_path": skin_path[0]
            })
        except Exception as e:
            error_message[0] = "Failed to load skin!"
            update_status("Skin load error")
            skin_image[0] = None