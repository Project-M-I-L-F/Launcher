import os
import sys
import pygame

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def update_status(message, status_message):
    status_message[0] = message
    print(f"Status: {message}")
    pygame.display.flip()