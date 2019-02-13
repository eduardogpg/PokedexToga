import toga
import requests

from consts import *
from toga.style.pack import Pack, CENTER

class Pokedex(toga.App):
    def __init__(self, name, app_id):
        toga.App.__init__(self, name, app_id)

        self.name = name
        self.size = (WIDHT, HEIGHT)

        self.offset = 0
        self.limit = 20
        self.loading = False

        self.headings = ['Name']
        self.pokemon_list = []

        self.create_table()
        self.create_toolbar()
        self.create_information_area()

        self.load_pokemon()

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)

        split = toga.SplitContainer()
        split.content = [self.table, self.information_area]

        self.main_window.content = split
        self.main_window.toolbar.add(self.next_command, self.previous_command)

        self.main_window.show()

    def create_table(self):
        self.table = toga.Table(self.headings, on_select=self.select_element,
                                data=self.pokemon_list)

    def create_information_area(self):
        self.information_area = toga.Box()

    def create_toolbar(self):
        self.create_next_command()
        self.create_previous_command()

        self.enable_previous_command()

    def create_next_command(self):
        self.next_command = toga.Command(self.next, label='Siguiente',
                                            icon=BULBASAUR_ICON)

    def create_previous_command(self):
        self.previous_command = toga.Command(self.previous, label='Anterior',
                                            icon=METAPOD_ICON)

    def select_element(self, widget, row):
        pass

    def next(self, widget):
        self.offset += 1
        self.command_handler(widget)

    def previous(self, widget):
        self.offset -= 1
        self.command_handler(widget)

    def command_handler(self, widget):
        widget.enabled = False
        self.load_pokemon()
        widget.enabled = True

        self.enable_previous_command()

    def enable_previous_command(self):
        self.previous_command.enabled = not self.offset == 0

    def load_pokemon(self):
        self.pokemon_list.clear()

        path = "{}?offset={}&limit={}".format(POKE_API, self.offset, self.limit)

        response = requests.get(path)
        if response.status_code == 200:
            result = response.json()

            for pokemon in result.get('results', []):
                name = pokemon.get('name')
                self.pokemon_list.append(name)

        self.table.data = self.pokemon_list

    def get_pokemon(self, id):
        path = "{}/{}".format(POKE_API, id)

if __name__ == '__main__':
    app = Pokedex('Pokedex', 'com.codigofacilito.Podedex')
    app.main_loop()
