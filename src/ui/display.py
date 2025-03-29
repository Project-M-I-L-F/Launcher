import pygame

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(topleft=(x, y))
    surface.blit(textobj, textrect)

def draw_button(window, rect, text, font, color, text_color, icon=None, pressed=False):
    button_color = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0)) if pressed else color
    pygame.draw.rect(window, button_color, rect, border_radius=15)
    draw_text(text, font, text_color, window, rect.x + 20, rect.y + 10)
    if icon:
        icon = pygame.transform.scale(icon, (25, int(25 * icon.get_height() / icon.get_width())))
        window.blit(icon, (rect.x + rect.width - 35, rect.y + 7))

def draw_settings_button(surface, rect, text, font, color, text_color, pressed=False):
    button_color = (max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0)) if pressed else color
    text_surface = font.render(text, True, text_color)
    rect.width = text_surface.get_width() + 20
    rect.height = text_surface.get_height() + 10
    pygame.draw.rect(surface, button_color, rect, border_radius=15)
    draw_text(text, font, text_color, surface, rect.x + 10, rect.y + 5)

def draw_icon_button(window, icon, x, y, target_width):
    icon = pygame.transform.scale(icon, (target_width, int(target_width * icon.get_height() / icon.get_width())))
    icon_rect = pygame.Rect(x, y, icon.get_width(), icon.get_height())
    window.blit(icon, (x, y))
    return icon_rect

def draw_status_message(window, status_message, error_message, profile_font, window_width, window_height):
    text = profile_font.render(error_message if error_message else status_message, True, (255, 0, 0) if error_message else (75, 0, 130))
    window.blit(text, text.get_rect(center=(window_width // 2, window_height - 25)))

def draw_input_field(surface, rect, text, active, label, input_font, light_purple, gray, white):
    pygame.draw.rect(surface, light_purple if active else gray, rect, border_radius=10)
    draw_text(text, input_font, (75, 0, 130), surface, rect.x + 5, rect.y + (rect.height - input_font.get_height()) // 2)
    draw_text(label, input_font, white, surface, rect.x, rect.y - 20)

def draw_ram_slider(surface, rect, value, min_val, max_val, dragging, input_font, gray, light_purple, white):
    pygame.draw.rect(surface, gray, rect, border_radius=5)
    slider_pos = rect.x + (value - min_val) * rect.width / (max_val - min_val)
    slider_rect = pygame.Rect(slider_pos - 5, rect.y - 2, 10, rect.height + 4)
    pygame.draw.rect(surface, light_purple if dragging else white, slider_rect, border_radius=5)
    draw_text(f"RAM: {value} GB", input_font, white, surface, rect.x + rect.width + 10, rect.y - 2)