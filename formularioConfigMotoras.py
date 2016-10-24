# -*- coding: utf-8 -*-
__author__ = 'roberto'

from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import kivy
kivy.require('1.0.6')
import config


class FormularioConfigMotoras(Screen):

    def build(self):
        """
        Creacion de la interfaz
        """
        print "Build config motor"
        layout = self.ids.layout_screen_config_Motor
        layout.clear_widgets()
        lyt_top = BoxLayout(orientation='horizontal')
        lyt_labels = BoxLayout(orientation='vertical')
        lyt_inputs = BoxLayout(orientation='vertical')
        lyt_bottom = BoxLayout(orientation='horizontal',
                               size_hint=config.BASE_WIDGET_HEIGHT)

        # Labels
        lbl_titulo = Label(text='Configuracion de prueba: Imagenes Motoras',
                           size_hint=config.BASE_WIDGET_HEIGHT)
        lbl_estabilizacion = Label(text='Tiempo de Estabilizacion Inicial')

        # Inputs
        txt_estabilizacion = config.FloatInput()

        inputs = dict()
        inputs['estabilizacion'] = txt_estabilizacion

        inputs['estabilizacion'].text = str(config.MOTOR_TIEMPO_ESTABILIZACION)

        # Botones
        btn_cancel = Button(text='Cancelar')
        btn_new_config = Button(text='Guardar')

        # Bindings
        btn_cancel.bind(on_press=partial(self.menu))
        btn_new_config.bind(on_press=partial(
            self.new_config, inputs))

        # Creacion de Interfaz
        lyt_labels.add_widget(lbl_estabilizacion)
        lyt_labels.add_widget(Label(size_hint=(1, 10)))

        lyt_inputs.add_widget(txt_estabilizacion)
        lyt_inputs.add_widget(Label(size_hint=(1, 10)))

        lyt_top.add_widget(lyt_labels)
        lyt_top.add_widget(lyt_inputs)

        lyt_bottom.add_widget(btn_cancel)
        lyt_bottom.add_widget(btn_new_config)

        layout.add_widget(lbl_titulo)
        layout.add_widget(lyt_top)
        layout.add_widget(lyt_bottom)

    def new_config(self, inputs, *largs):
        """
        Almacenamiento de los valores capturados
        """
        config.config_motoras = [
            inputs['estabilizacion'].text,
        ]

        form_complete = True
        for elem in config.config_motoras:
            if type(elem) == str and elem == '':
                form_complete = False

        if form_complete:
            config.MOTOR_TIEMPO_ESTABILIZACION = float(inputs['estabilizacion'].text)
            self.menu()

    def menu(self, *largs):
        self.manager.current = 'config_screen'
        self.manager.transition.direction= 'right'