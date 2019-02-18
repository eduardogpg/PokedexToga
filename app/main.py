import toga
import requests
import threading

from consts import *
from toga.colors import *
from toga.style.pack import *

class Pokemon():
    def __init__(self, name, response):
        self.name = name
        self.sprite = ''

        self.moves = list()
        self.abilities = list()
        self.create_by_dict(response)

        self.name = response['forms'][0]['name']

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

    @property
    def description(self):
        desc = 'Abilities :\n'
        for ability in self.abilities:
            desc += "> " + ability + "\n"

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

        self.create_components()
        self.load_data()

    def get_url_all_pokemon(self):
        return "{}?offset={}&limit={}".format(POKE_API, self.offset, self.limit)

    def get_url_pokemon(self, pokemon_id):
        return "{}{}".format(POKEMON_API, pokemon_id)

    def get_all_pokemon(self):
        self.pokemon.clear()

        response = requests.get(self.get_url_all_pokemon())
        if response:
            result = response.json()

            for element in result['results']:
                self.pokemon.append(element['name'])

        self.table.data = self.pokemon
        self.title.text = TITLE

    def get_pokemon(self, pokemon_id):
        response = requests.get(self.get_url_pokemon(pokemon_id))
        if response:
            result = response.json()
            pokemon = Pokemon(id, result)

            self.current_pokemon = pokemon
            self.update_information_area()

    def load_data(self):
        thread = threading.Thread(target=self.get_all_pokemon)
        thread.start()

    def load_element(self, pokemon_id):
        thread = threading.Thread(target=self.get_pokemon, args=[pokemon_id])
        thread.start()

    def create_components(self):
        self.create_table()
        self.create_next_command()
        self.create_previous_command()
        self.create_progress_bar()
        self.create_image_view(DEFAULT_IMAGE)
        self.create_description_content(TITLE, TEXT)

        self.validate_previous_command()

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
        style = Pack(font_family=MONOSPACE, text_align=CENTER)

        self.title = toga.Label(title, style=style)
        self.description = toga.Label(text, style=style)

        self.title.style.font_size = 20
        self.title.style.padding_bottom = 10
        self.description.style.font_size = 18

    def create_progress_bar(self):
        self.progress_bar = toga.ProgressBar(style=Pack(flex=1, visibility=VISIBLE), max=1, running=False, value=0)

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

        self.main_window.toolbar.add(self.previous_command, self.next_command)

        self.main_window.show()

    def update_information_area(self):
        self.image_view.image = toga.Image(self.current_pokemon.sprite)
        self.description.text = self.current_pokemon.description
        self.title.text = self.current_pokemon.name

    #CALLBACKS
    def select_element(self, widget, row):
        if row:
            self.reset_description_area()
            self.load_element(row.name)

    def reset_description_area(self):
        self.title.text = 'Loading ... '
        self.image_view.image = None
        self.description.text = ""

    def title_formart(self, name):
        return name[0].upper() + name[1:]

    def next(self, widget):
        self.offset += 10
        self.handler_command(widget)

    def previous(self, widget):
        self.offset -= 10
        self.handler_command(widget)

    def handler_command(self, widget):
        widget.enabled = False

        self.reset_description_area()
        self.load_data()

        widget.enabled = True

        self.table.data = self.pokemon
        self.validate_previous_command()

    def validate_previous_command(self):
        self.previous_command.enabled = not self.offset == 0

if __name__ == '__main__':
    app = Pokedex('Pokedex', 'com.codigofacilito.Pokedex')
    app.main_loop()
