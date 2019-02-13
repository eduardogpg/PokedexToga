import toga

class Pokedex(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)

        box = toga.Box()

        self.main_window.content = box
        self.main_window.show()

if __name__ == '__main__':
    app = Pokedex('Podedex', 'com.codigofacilito.Podedex')
    app.main_loop()
