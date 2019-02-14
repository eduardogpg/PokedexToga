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

    def startup(self):
        self.main_window = toga.MainWindow('main', title=self.name, size=self.size)

        self.main_window.content = toga.Box()

        self.main_window.show()

if __name__ == '__main__':
    app = Pokedex('Pokedex', 'com.codigofacilito.Pokedex')
    app.main_loop()
