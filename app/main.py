import os
import toga
import requests

# TODO: Size for Main window, No re size, Get 20 first elements, draw pokemon image
# TODO: Set new Icon!

from toga.style.pack import *

base_dir = os.path.dirname(os.path.abspath(__file__))
icon_dir = os.path.join(base_dir, 'icons')

class Pokedex(toga.App):
    def __init__(self, name, app_id):
        toga.App.__init__(self, name, app_id)

        self.size = (600, 500)

        self.pokemons = []
        self.headings = ['Pokemon name']

        self.offset = 0
        self.limit = 20

        self.table = self.create_table()
        self.next_command, self.previous_command = self.create_tools()
        self.content = self.create_content()

        self.load_pokemon()

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)
        self.main_window.toolbar.add(self.next_command, self.previous_command)

        split = toga.SplitContainer()
        split.content = [self.table, self.content]

        self.main_window.content = split
        self.main_window.show()

    def select_element(self, widget, row):
        print("Elemento seleccionado!")

    def create_table(self):
        table = toga.Table(headings=self.headings,
                            on_select=self.select_element)

        return table

    def create_content(self):
        content = toga.Box(style=Pack(direction=COLUMN, padding_top=10))

        description = toga.ScrollContainer(horizontal=False)
        description.content = content

        return description

    def create_tools(self):
        next = toga.Command(self.next, label='Siguiente',
            icon=os.path.join(icon_dir, 'bulbasaur.png')
        )
        
        previous = toga.Command(self.previous, label='Anterior',
            icon=os.path.join(icon_dir, 'metapod.png')
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
