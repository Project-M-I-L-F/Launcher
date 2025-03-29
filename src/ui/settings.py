import pygame
from .display import draw_text, draw_input_field, draw_settings_button, draw_ram_slider

def draw_settings_window(window, settings_window, mouse_pos, left_pressed, ram_dragging, input_path_rect, input_path_text, input_path_active, input_username_rect, input_username_text, input_username_active, input_version_rect, minecraft_version, input_version_active, input_server_ip_rect, server_ip, input_server_ip_active, english_button_rect, ukrainian_button_rect, add_server_button_rect, ram_slider_rect, ram_value, window_width, window_height, purple, white, dark_purple, settings_title_font, button_font, input_font, light_purple, gray):
    settings_window.fill(purple)
    draw_text("Settings", settings_title_font, white, settings_window, 200, 15)
    
    draw_input_field(settings_window, input_path_rect, input_path_text, input_path_active, "Minecraft Directory", input_font, light_purple, gray, white)
    draw_input_field(settings_window, input_username_rect, input_username_text, input_username_active, "Username", input_font, light_purple, gray, white)
    draw_input_field(settings_window, input_version_rect, minecraft_version, input_version_active, "Minecraft Version", input_font, light_purple, gray, white)
    draw_input_field(settings_window, input_server_ip_rect, server_ip, input_server_ip_active, "Server IP", input_font, light_purple, gray, white)

    settings_mouse_pos = (mouse_pos[0] - (window_width - 500) // 2, mouse_pos[1] - (window_height - 350) // 2)
    is_english_pressed = english_button_rect.collidepoint(settings_mouse_pos) and left_pressed
    is_ukrainian_pressed = ukrainian_button_rect.collidepoint(settings_mouse_pos) and left_pressed
    is_add_server_pressed = add_server_button_rect.collidepoint(settings_mouse_pos) and left_pressed
    draw_settings_button(settings_window, english_button_rect, "English", button_font, white, dark_purple, is_english_pressed)
    draw_settings_button(settings_window, ukrainian_button_rect, "Ukrainian", button_font, white, dark_purple, is_ukrainian_pressed)
    draw_settings_button(settings_window, add_server_button_rect, "Add Server", button_font, white, dark_purple, is_add_server_pressed)
    
    draw_ram_slider(settings_window, ram_slider_rect, ram_value, 1, 16, ram_dragging, input_font, gray, light_purple, white)
    window.blit(settings_window, ((window_width - 500) // 2, (window_height - 350) // 2))