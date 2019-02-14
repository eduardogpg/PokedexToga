import toga
import requests

from consts import *
from toga.style.pack import *

class Pokedex(toga.App):
    def __init__(self, name, app_id):
        toga.App.__init__(self, name, app_id)

        self.name = name
        self.size = (WIDHT, HEIGHT)

        self.offset = 0
        self.limit = 20

        self.pokemon = []
        self.headings = ['Name']
        self.current_pokemon = None

        self.load_pokemon()
        self.create_components()

    def create_components(self):

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
        self.table = toga.Table(self.headings, on_select=self.select_element, data=self.pokemon)

    def create_image_area(self, url, width=150, height=150):
        image = toga.Image(url)
        style = Pack(width=width, height=height)

        self.image_view = toga.ImageView(image, style=style)

    def create_description_area(self, text):
        self.title = toga.Label('Description', style=Pack(font_family=FANTASY, font_size=20))
        self.description = toga.Label(text, style=Pack(font_family=FANTASY, font_size=15))

        box = toga.Box(
            children=[self.title, self.description],
            style=Pack(
                direction=COLUMN,
            )
        )

        return box

    def create_information_area(self):
        self.create_image_area('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/1.png')
        description = self.create_description_area('Simple description')

        self.information_area = toga.Box(
            children=[self.image_view, description],
            style=Pack(
                flex=1,
                direction=COLUMN,
                alignment=CENTER
            )
        )

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
        self.pokemon.clear()

        path = "{}?offset={}&limit={}".format(POKE_API, self.offset, self.limit)

        response = requests.get(path)
        if response.status_code == 200:
            result = response.json()

            for pokemon in result.get('results', []):
                name = pokemon.get('name')
                self.pokemon.append(name)

        self.table.data = self.pokemon

if __name__ == '__main__':
    app = Pokedex('Pokedex', 'com.codigofacilito.Podedex')
    app.main_loop()
