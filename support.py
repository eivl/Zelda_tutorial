from csv import reader
from pathlib import Path
import pygame

def import_csv_layout(path):
    with open(path) as file:
        return [row for row in reader(file, delimiter=',')]

def import_folder(path):
    return [pygame.image.load(file).convert_alpha() for file in Path(path).glob('*')]
