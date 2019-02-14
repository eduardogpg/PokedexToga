import os

WIDHT = 600
HEIGHT = 500

IMAGE_WIDHT = 200
IMAGE_HEIGHT = 200

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, 'icons')

METAPOD_ICON = os.path.join(ICON_DIR, 'metapod.png')
BULBASAUR_ICON = os.path.join(ICON_DIR, 'bulbasaur.png')

POKE_API = 'https://pokeapi.co/api/v2/pokemon-form'
POKEMON_API = 'https://pokeapi.co/api/v2/pokemon/'
