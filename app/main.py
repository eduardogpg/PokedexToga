import toga
import requests

from consts import *
from toga.colors import *
from toga.style.pack import *

class Pokemon():
    def __init__(self, name):
        self.name = name
        self.sprite = ''

        self.moves = list()
        self.abilities = list()

    def create_by_dict(self, response):
        self.sprite_by_dict(response)
        self.abilities_by_dict(response)

    def sprite_by_dict(self, response):
        sprites = response.get('sprites', {})
        self.sprite = sprites.get('front_default', '')

    def abilities_by_dict(self, response):
        for item in response.get('abilities', []):
            ability = item.get('ability', {})
            name = ability.get('name', '')

            if name:
                self.abilities.append(name)

        print(len(self.abilities))

    @property
    def description(self):
        desc = 'Abilities :\n'
        for ability in self.abilities:
            desc += ability + "\n"

        return desc

class Pokedex(toga.App):
    def __init__(self, name, app_id):
        toga.App.__init__(self, name, app_id)

        self.name = name
        self.size = (WIDHT, HEIGHT)

        self.offset = 0
        self.limit = 20

        self.pokemon = list()
        self.pokemon_loaded = dict()
        self.current_pokemon = None

        self.headings = ['Name']
        self.current_pokemon = None

        self.load_data()
        self.create_components()

    def load_data(self):
        path = "{}?offset={}&limit={}".format(POKE_API, self.offset, self.limit)

        response = requests.get(path)
        if response:
            result = response.json()

            for element in result['results']:
                self.pokemon.append(element['name'])

    def load_element(self, id):
        pokemon = self.pokemon_loaded.get(id)
        if pokemon:
            self.current_pokemon = pokemon
        else:
            path = "{}{}".format(POKEMON_API, id)

            response = requests.get(path)
            if response:
                result = response.json()

                pokemon = Pokemon(id)
                pokemon.create_by_dict(result)

                self.current_pokemon = pokemon
                self.pokemon_loaded[id] = pokemon
                

        self.update_information_area()

    def create_components(self):
        self.create_table()
        self.create_next_command()
        self.create_previous_command()
        self.create_image_view(DEFAULT_IMAGE)
        self.create_description_content(TITLE, TEXT)

    def create_table(self):
        self.table = toga.Table(self.headings,
                                on_select=self.select_element,
                                data=self.pokemon)

    def create_next_command(self):
        self.next_command = toga.Command(self.next, label='Next',
                                            icon=BULBASAUR_ICON)

    def create_previous_command(self):
        self.previous_command = toga.Command(self.previous, label='Previous',
                                            icon=METAPOD_ICON)

    def create_image_view(self, url, width=200, height=200):
        image = toga.Image(url)
        style = Pack(width=width, height=height)

        self.image_view = toga.ImageView(image, style=style)

    def create_description_content(self, title, text):
        style = Pack(font_family=FANTASY, text_align=CENTER)

        self.title = toga.Label(title, style=style)
        self.description = toga.Label(text, style=style)

        self.title.style.font_size = 20
        self.description.style.font_size = 18

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)

        information_area = toga.Box(
            children=[self.image_view, self.title, self.description],
            style=Pack(
                direction=COLUMN,
                alignment=CENTER
            )
        )
        split = toga.SplitContainer()

        split.content = [self.table,  information_area]

        self.main_window.content = split

        self.main_window.toolbar.add(self.next_command, self.previous_command)

        self.main_window.show()

    def update_information_area(self):
        if self.current_pokemon:
            self.image_view.image = toga.Image(self.current_pokemon.sprite)
            self.description.text = self.current_pokemon.description

    #CALLBACKS
    def select_element(self, widget, row):
        self.load_element(row.name)
        self.title.text = self.title_formart(row.name)

    def title_formart(self, name):
        return name[0].upper() + name[1:]

    def next(self, widget):
        pass

    def previous(self, widget):
        pass

if __name__ == '__main__':
    app = Pokedex('Pokedex', 'com.codigofacilito.Pokedex')
    app.main_loop()
