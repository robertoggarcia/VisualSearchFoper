__author__ = 'sepulvedaavila'

from configGral import Config
from MotorImage import MotorIm
from cajas import CincoCajas
from formularioConfigCajas import FormularioConfigCajas
from formularioConfigMotoras import FormularioConfigMotoras
from formularioConfigVisual import FormularioConfigVisual
from formularioSujeto import FormularioSujeto
from visualSearch import VisualSearch
import sys
import config
from kivy.properties import NumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

# Window.fullscreen = True

Builder.load_file("Format.kv")
prueba_seleccionada = NumericProperty(0)


class MainMenu(Screen):
    description = config.MENU_DESCRIPCION
    title = config.MENU_TITULO
    pass


class MenuPruebas(Screen):
    descripcion_pruebas = "Estos son los tres tipos de pruebas que se pueden realizar.\n" \
                          "Selecciona la prueba que quieres ejecutar:"

    def prueba_seleccionada(self, numero_prueba):
        config.prueba_seleccionada = str(numero_prueba)
        print config.prueba_seleccionada + "-prueba_seleccionada-MenuPruebas"
    pass


class Descrip(Screen):
    full_descrip = config.DESCRIPCION_SISTEMA
    pass


class Quit(Screen):
    def salir(self):
        sys.exit(0)
    pass


config.manager.add_widget(MainMenu(name='mainmenu_screen'))
config.manager.add_widget(FormularioSujeto(name='formsujeto_screen'))
config.manager.add_widget(MenuPruebas(name='menupruebas_screen'))
config.manager.add_widget(Descrip(name='descrip_screen'))
config.manager.add_widget(Quit(name='quit_screen'))

config.manager.add_widget(MotorIm(name='motorIm_screen'))
config.manager.add_widget(VisualSearch(name='visualSearch_screen'))
config.manager.add_widget(CincoCajas(name='box_screen'))

config.manager.add_widget(Config(name='config_screen'))
config.manager.add_widget(FormularioConfigVisual(name='formConfigVisual_screen'))
config.manager.add_widget(FormularioConfigMotoras(name='formConfigMotor_screen'))
config.manager.add_widget(FormularioConfigCajas(name='formConfigBox_screen'))


class Foper(App):
    def build(self):
        return config.manager


if __name__ == '__main__':
    Foper().run()