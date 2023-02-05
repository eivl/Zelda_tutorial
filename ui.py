import pygame
from settings import *


class UI:
    def __init__(self):
        # General
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # Bar setup
        self.health_bar = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

    def show_bar(self, current, maximum, bar, color):
        # Calculate bar width
        bar_width = int(bar.width * current / maximum)

        # Draw background
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bar)

        # Draw bar
        pygame.draw.rect(self.display_surface, color, (bar.x, bar.y, bar_width, bar.height))

        # Draw border
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bar, 4)

    def show_xp(self, xp):
        text_surface = self.font.render(f'XP: {xp}', False, TEXT_COLOR)
        text_rect = text_surface.get_rect(bottomright=(WIDTH-20, HEIGHT-20))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(10, 10))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(10, 10), 3)

    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)


    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar, ENERGY_COLOR)
        self.show_xp(player.xp)
        self.selection_box(10, HEIGHT-ITEM_BOX_SIZE-20)  # Weapon
        self.selection_box(80, HEIGHT-ITEM_BOX_SIZE-15)  # Magic
