# -*- coding: utf-8 -*-
__author__ = 'roberto'

from functools import partial
from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


import kivy
kivy.require('1.0.6')
import config


class FormularioConfigVisual(Screen):

    def build(self):
        """
        Creacion de la interfaz
        """
        layout = self.ids.layout_screen_config_visual
        layout.clear_widgets()
        lyt_top = BoxLayout(orientation='horizontal')
        lyt_labels = BoxLayout(orientation='vertical')
        lyt_inputs = BoxLayout(orientation='vertical')
        lyt_bottom = BoxLayout(orientation='horizontal',
                               size_hint=config.BASE_WIDGET_HEIGHT)

        # Labels
        lbl_titulo = Label(text='Configuracion de prueba: Visual',
                           size_hint=config.BASE_WIDGET_HEIGHT)
        lbl_imagenes = Label(text='Numero de Imagenes')
        lbl_porcentaje = Label(text='Porcentaje del tamaño del estimulo')
        lbl_max = Label(text='Rango Maximo de tiempo entre estimulos')
        lbl_min = Label(text='Rango Minimo de tiempo entre estimulos')
        lbl_espera = Label(text='Tiempo de Espera entre los estimulos')
        lbl_estabilizacion = Label(text='Tiempo de Estabilizacion Inicial')

        # Inputs
        txt_imagenes = config.FloatInput()
        txt_porcentaje = config.FloatInput()
        txt_max = config.FloatInput()
        txt_min = config.FloatInput()
        txt_espera = config.FloatInput()
        txt_estabilizacion = config.FloatInput()

        # Botones
        btn_cancel = Button(text='Cancelar')
        btn_new_config = Button(text='Guardar')

        # Inputs
        inputs = dict()
        inputs['imagenes'] = txt_imagenes
        inputs['porcentaje'] = txt_porcentaje
        inputs['max'] = txt_max
        inputs['min'] = txt_min
        inputs['espera'] = txt_espera
        inputs['estabilizacion'] = txt_estabilizacion

        inputs['imagenes'].text = str(config.visual_numero_imagenes)
        inputs['porcentaje'].text = str(config.visual_porcentaje_estimulo)
        inputs['max'].text = str(config.visual_rango_estimulo_mayour)
        inputs['min'].text = str(config.visual_rango_estimulo_menor)
        inputs['espera'].text = str(config.visual_tiempo_espera)
        inputs['estabilizacion'].text = str(config.tiempo_estabilizacion)

        # Bindings
        btn_cancel.bind(on_press=partial(self.menu))
        btn_new_config.bind(on_press=partial(
            self.new_config, inputs))

        # Creacion de Interfaz
        lyt_labels.add_widget(lbl_imagenes)
        lyt_labels.add_widget(lbl_porcentaje)
        lyt_labels.add_widget(lbl_max)
        lyt_labels.add_widget(lbl_min)
        lyt_labels.add_widget(lbl_espera)
        lyt_labels.add_widget(lbl_estabilizacion)
        lyt_labels.add_widget(Label(size_hint=(1, 5)))

        lyt_inputs.add_widget(txt_imagenes)
        lyt_inputs.add_widget(txt_porcentaje)
        lyt_inputs.add_widget(txt_max)
        lyt_inputs.add_widget(txt_min)
        lyt_inputs.add_widget(txt_espera)
        lyt_inputs.add_widget(txt_estabilizacion)
        lyt_inputs.add_widget(Label(size_hint=(1, 5)))

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
        config.config_visual = [
            inputs['imagenes'].text,
            inputs['porcentaje'].text,
            inputs['min'].text,
            inputs['max'].text,
            inputs['espera'].text,
            inputs['estabilizacion'].text,
            # inputs['name'].text
        ]

        form_complete = True
        for elem in config.config_visual:
            if type(elem) == str and elem == '':
                form_complete = False

        if form_complete:
            config.visual_porcentaje_estimulo = float(inputs['porcentaje'].text)
            config.visual_numero_imagenes = int(inputs['imagenes'].text)
            config.visual_rango_estimulo_menor = float(inputs['min'].text)
            config.visual_rango_estimulo_mayour = float(inputs['max'].text)
            config.visual_tiempo_espera = float(inputs['espera'].text)
            config.tiempo_estabilizacion = float(inputs['estabilizacion'].text)
            self.menu()

    def menu(self, *largs):
        self.manager.current= 'config_screen'
        self.manager.transition.direction= 'right'