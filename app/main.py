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

        self.load_pokemon()

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)

        self.table = self.create_table()
        self.information_area = self.create_information_area()

        split = toga.SplitContainer()
        split.content = [self.table, self.information_area]

        next_command = self.create_next_command()
        previous_command = self.create_previous_command()

        self.main_window.content = split
        self.main_window.toolbar.add(next_command, previous_command)

        self.main_window.show()

    def create_table(self):
        table = toga.Table(self.headings, on_select=self.select_element)

        return table

    def create_information_area(self):
        information = toga.Box()

        return information

    def select_element(self, widget, row):
        print("Elemento seleccionado!")

    def next(self, widget):
        self.offset += 1

    def previous(self, widget):
        self.offset -= 1

    def validate_commands(self):
        pass

    def create_next_command(self):
        return toga.Command(self.next, label='Siguiente', icon=BULBASAUR_ICON)

    def create_previous_command(self):
        return toga.Command(self.previous, label='Anterior', icon=METAPOD_ICON)

    def load_pokemon(self):
        self.pokemon_list.clear()

        path = "{}?offset={}&limit={}".format(POKE_API, self.offset, self.limit)

        response = requests.get(path)
        if response.status_code == 200:
            result = response.json()

            for pokemon in result.get('results', []):
                name = pokemon.get('name')
                self.pokemon_list.append(name)

    def get_pokemon(self, id):
        path = "{}/{}".format(POKE_API, id)

if __name__ == '__main__':
    app = Pokedex('Pokedex', 'com.codigofacilito.Podedex')
    app.main_loop()
