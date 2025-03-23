# src/ui/display.py
import pygame

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def draw_button(window, rect, text, font, color, text_color, icon=None, pressed=False):
    if pressed:
        button_color = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
    else:
        button_color = color
    pygame.draw.rect(window, button_color, rect, border_radius=15)
    draw_text(text, font, text_color, window, rect.x + 20, rect.y + 10)
    if icon:
        icon_width = 25
        icon_height = int(icon_width * (icon.get_height() / icon.get_width()))
        icon = pygame.transform.scale(icon, (icon_width, icon_height))
        window.blit(icon, (rect.x + rect.width - 35, rect.y + 7))

def draw_settings_button(surface, rect, text, font, color, text_color, pressed=False):
    if pressed:
        button_color = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))
    else:
        button_color = color
    pygame.draw.rect(surface, button_color, rect, border_radius=15)
    draw_text(text, font, text_color, surface, rect.x + 10, rect.y + (rect.height - font.get_height()) // 2)

def draw_icon_button(window, icon, x, y, target_width):
    icon_width = target_width
    icon_height = int(icon_width * (icon.get_height() / icon.get_width()))
    icon = pygame.transform.scale(icon, (icon_width, icon_height))
    icon_rect = pygame.Rect(x, y, icon_width, icon_height)
    window.blit(icon, (x, y))
    return icon_rect

def draw_status_message(window, status_message, error_message, profile_font, window_width, window_height):
    if error_message:
        status_text = profile_font.render(error_message, True, (255, 0, 0))
    else:
        status_text = profile_font.render(status_message, True, (75, 0, 130))
    text_rect = status_text.get_rect(center=(window_width // 2, window_height - 25))
    window.blit(status_text, text_rect)

def draw_input_field(surface, rect, text, active, label, input_font, light_purple, gray, white):
    color = light_purple if active else gray
    pygame.draw.rect(surface, color, rect, border_radius=10)
    draw_text(text, input_font, (75, 0, 130), surface, rect.x + 5, rect.y + (rect.height - input_font.get_height()) // 2)
    draw_text(label, input_font, white, surface, rect.x, rect.y - 20)

def draw_ram_slider(surface, rect, value, min_val, max_val, dragging, input_font, gray, light_purple, white):
    pygame.draw.rect(surface, gray, rect, border_radius=5)
    slider_width = rect.width / (max_val - min_val)
    slider_pos = rect.x + (value - min_val) * slider_width
    slider_rect = pygame.Rect(slider_pos - 5, rect.y - 2, 10, rect.height + 4)
    pygame.draw.rect(surface, light_purple if dragging else white, slider_rect, border_radius=5)
    ram_text = f"RAM: {value} GB"
    draw_text(ram_text, input_font, white, surface, rect.x + rect.width + 10, rect.y - 2)