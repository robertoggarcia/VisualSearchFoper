__author__ = 'roberto'

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial


class Config(Screen):

    def build(self):
        layout = self.ids.layout_screen_Configuracion
        layout.clear_widgets()
        lyt_vertical = BoxLayout(orientation='vertical')
        lbl_empty1 = Label(size_hint=(.1, .1))
        lbl_empty2 = Label(size_hint=(.1, .1))

        lbl_Config = Label(text='Configuraciones generales')

        lyt_botones_pruebas = BoxLayout(orientation='horizontal')

        btn_config_visual = Button(text='Configurar prueba visual', size_hint=(1, 0.3))
        btn_config_visual.bind(on_press=partial(self.configVisualScreen))

        btn_config_motor = Button(text='Configurar prueba Motora', size_hint=(1, 0.3))
        btn_config_motor.bind(on_press=partial(self.configMotorScreen))

        btn_config_box = Button(text='Configurar prueba Box', size_hint=(1, 0.3))
        btn_config_box.bind(on_press=partial(self.configBoxScreen))

        lyt_botones_pruebas.add_widget(btn_config_visual)
        lyt_botones_pruebas.add_widget(btn_config_motor)
        lyt_botones_pruebas.add_widget(btn_config_box)

        lyt_botones = BoxLayout(orientation='horizontal')
        btn_menu = Button(text='Menu', size_hint=(1, 0.3))
        btn_menu.bind(on_press=partial(self.menu))
        btn_salir = Button(text='Salir', size_hint=(1, .3))
        btn_salir.bind(on_press=partial(self.salir))
        lyt_botones.add_widget(btn_menu)
        lyt_botones.add_widget(btn_salir)
        lbl_empty3 = Label()

        lyt_vertical.add_widget(lbl_Config)
        lyt_vertical.add_widget(lyt_botones_pruebas)
        lyt_vertical.add_widget(lbl_empty3)
        lyt_vertical.add_widget(lyt_botones)

        layout.add_widget(lbl_empty1)
        layout.add_widget(lyt_vertical)
        layout.add_widget(lbl_empty2)

    def menu(self, *largs):
        self.manager.current= 'mainmenu_screen'
        self.manager.transition.direction= 'right'

    def salir(self, *largs):
        self.manager.current = 'quit_screen'
        self.manager.transition.direction= 'right'

    def configVisualScreen(self, *largs):
        self.manager.current = 'formConfigVisual_screen'
        self.manager.get_screen('formConfigVisual_screen').build()

    def configMotorScreen(self, *largs):
        self.manager.current = 'formConfigMotor_screen'
        self.manager.get_screen('formConfigMotor_screen').build()

    def configBoxScreen(self, *largs):
        self.manager.current = 'formConfigBox_screen'
        self.manager.get_screen('formConfigBox_screen').build()