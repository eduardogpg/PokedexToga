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

        self.table = self.create_table()
        self.tools = self.create_tools()
        self.content = self.create_content()

        self.load_pokemons()

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)

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
        pass

    def get_pokemon_url(self):
        return 'https://pokeapi.co/api/v2/pokemon-form?offset=0&limit=20'

    def load_pokemons(self):
        response = requests.get(self.get_pokemon_url())
        if response:
            results = response.json()
            pokemons = results.get('results', [])

            for pokemon in pokemons:
                name = pokemon.get('name', '')
                self.pokemons.append(name)

        self.table.data = self.pokemons

if __name__ == '__main__':
    app = Pokedex('Podedex', 'com.codigofacilito.Podedex')
    app.main_loop()
