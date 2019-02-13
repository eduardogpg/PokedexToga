import os
import toga
import requests

from .consts import *
from toga.style.pack import *

class Pokedex(toga.App):
    def __init__(self, name, app_id):
        toga.App.__init__(self, name, app_id)

        self.size = (WIDHT, HEIGHT)

        self.pokemons = []
        self.headings = ['Name']

        self.offset = OFFSET
        self.limit = LIMIT

        self.load_pokemon()
        self.create_components()

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)
        self.main_window.toolbar.add(self.next_command, self.previous_command)

        split = toga.SplitContainer()

        label = toga.Label('Hola Mundo!')
        button = toga.Button('Boton')

        self.content.add(label)

        split.content = [self.table, self.content]

        self.main_window.content = split
        self.main_window.show()

    def select_element(self, widget, row):
        image_url = self.get_pokemon(1)

        image_from_url = toga.Image(image_url)
        imageview_from_url = toga.ImageView(image_from_url)

        self.content.add(imageview_from_url)

    def create_table(self):
        table = toga.Table(headings=self.headings,
                            on_select=self.select_element)

        return table

    def create_content(self):
        content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))

        #description = toga.ScrollContainer(horizontal=False)
        #description.content = content

        return content

    def create_tools(self):
        next = toga.Command(self.next, label='Siguiente',
            icon=os.path.join(ICON_DIR, 'bulbasaur.png')
        )

        previous = toga.Command(self.previous, label='Anterior',
            icon=os.path.join(ICON_DIR, 'metapod.png')
        )

        return next, previous

    def next(self, widget):
        self.offset += 1
        self.load_pokemon()

    def previous(self, widget):
        self.offset -= 1
        self.load_pokemon()

    def validate_next_command(self):
        self.previous_command.enabled = not self.offset == 0

    def get_pokemon_url(self):
        return 'https://pokeapi.co/api/v2/pokemon-form?offset={}&limit={}'.format(self.offset, self.limit)

    def get_pokemon(self, id):
        response = requests.get('https://pokeapi.co/api/v2/pokemon-form/1/')
        if response:
            result = response.json()
            sprites = result.get('sprites', {})
            url_image = sprites.get('front_default', '')

            return url_image

    def load_pokemon(self):
        self.pokemons.clear()

        response = requests.get(self.get_pokemon_url())
        if response:
            results = response.json()
            pokemons = results.get('results', [])

            for pokemon in pokemons:
                name = pokemon.get('name', '')
                self.pokemons.append(name)

        self.table.data = self.pokemons
        self.validate_next_command()

if __name__ == '__main__':
    app = Pokedex('Podedex', 'com.codigofacilito.Podedex')
    app.main_loop()
