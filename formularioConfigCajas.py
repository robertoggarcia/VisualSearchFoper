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


class FormularioConfigCajas(Screen):

    def build(self):
        """
        Creacion de la interfaz
        """
        layout = self.ids.layout_screen_config_box
        layout.clear_widgets()

        lyt_top = BoxLayout(orientation='horizontal')
        lyt_labels = BoxLayout(orientation='vertical')
        lyt_inputs = BoxLayout(orientation='vertical')
        lyt_bottom = BoxLayout(orientation='horizontal',
                               size_hint=config.BASE_WIDGET_HEIGHT)

        # Labels
        lbl_titulo = Label(text='Configuracion de prueba: 5 Cajas',
                           size_hint=config.BASE_WIDGET_HEIGHT)
        lbl_max = Label(text='Rango Maximo de tiempo entre estimulos')
        lbl_min = Label(text='Rango Minimo de tiempo entre estimulos')
        lbl_intervalo = Label(text='Intervalo entre los dos rangos')
        lbl_cantidad_eventos = Label(text='Cantidad de Eventos')
        lbl_tiempo = Label(text='Tiempo de Estabilizacion Inicial')

        # Inputs
        txt_max = config.FloatInput()
        txt_min = config.FloatInput()
        txt_intervalo = config.FloatInput()
        txt_cantidad_eventos = config.FloatInput()
        txt_tiempo = config.FloatInput()

        # Botones
        btn_cancel = Button(text='Cancelar')
        btn_new_config = Button(text='Guardar')

        # Inputs
        inputs = dict()
        inputs['max'] = txt_max
        inputs['min'] = txt_min
        inputs['intervalo'] = txt_intervalo
        inputs['eventos'] = txt_cantidad_eventos
        inputs['tiempo'] = txt_tiempo

        # TODO Miguel Settings
        """
        # Configuraciones anteriores
        inputs['max'].text = str(config.)
        inputs['min'].text = str(config.)
        inputs['intervalo'].text = str(config.)
        inputs['eventos'].text = str(config.)
        inputs['tiempo'].text = str(config.)
        """

        # Bindings
        btn_cancel.bind(on_press=partial(self.menu))
        btn_new_config.bind(on_press=partial(
            self.new_config, inputs))

        # Creacion de Interfaz
        lyt_labels.add_widget(lbl_max)
        lyt_labels.add_widget(lbl_min)
        lyt_labels.add_widget(lbl_intervalo)
        lyt_labels.add_widget(lbl_cantidad_eventos)
        lyt_labels.add_widget(lbl_tiempo)
        lyt_labels.add_widget(Label(size_hint=(1, 5)))

        lyt_inputs.add_widget(txt_max)
        lyt_inputs.add_widget(txt_min)
        lyt_inputs.add_widget(txt_intervalo)
        lyt_inputs.add_widget(txt_cantidad_eventos)
        lyt_inputs.add_widget(txt_tiempo)
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
        config.config_cajas = [
            inputs['eventos'].text,
            inputs['intervalo'].text,
            inputs['min'].text,
            inputs['max'].text,
            inputs['tiempo'].text,
        ]

        form_complete = True
        for elem in config.config_cajas:
            if type(elem) == str and elem == '':
                form_complete = False

        if form_complete:
            config.cajas_eventos_totales = int(inputs['eventos'].text)
            config.cajas_eventos_rango = \
                config.frange(float(inputs['min'].text),
                              float(inputs['max'].text),
                              float(inputs['intervalo'].text))
            config.tiempo_estabilizacion = float(inputs['tiempo'].text)
            self.menu()

    def menu(self, *largs):
        self.manager.current = 'config_screen'
        self.manager.transition.direction= 'right'