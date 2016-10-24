# -*- coding: utf-8 -*-
__author__ = 'roberto'

import random
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.screenmanager import Screen
import time
import config
import kivy
kivy.require('1.0.6')
from kivy.uix.boxlayout import BoxLayout


class VisualSearch(Screen):

    # Declaration of global variables
    global tiempo_final, tiempo_inicial, tiempo_eventos, tiempo_estimulos, \
        numero_imagen, ruta_imagen

    # Times are recorded here
    tiempo_inicial = None
    tiempo_eventos = []
    tiempo_estimulos = []
    tiempo_final = None

    # NumeroImagen variable specifies the control of the image being deployed
    # The number of images that must be displayed according to the
    # description of the test is 5
    numero_imagen = 0
    ruta_imagen = config.RUTA_IMAGENES

    def build(self):
        layout = self.ids.layout_screen_Visual
        """
        This is the main screen waiting to start the test
        """
        label_titulo = Label(font_size='20sp', text='-- Visual Search Test --')
        label_informacion = Label(
            font_size='20sp',
            text=config.TEXTO_INFORMACION_PRUEBA_VISUAL_SEARCH
        )

        lyt_botton = BoxLayout(orientation='horizontal')
        btn_menu = Button(text='Menu', size_hint=(.5, .3))
        btn_menu.bind(on_press=partial(self.menu))
        boton = Button(text='Iniciar', size_hint=(.5, .3))
        boton.bind(on_press=partial(self.iniciar))
        lyt_botton.add_widget(btn_menu)
        lyt_botton.add_widget(boton)

        layout.add_widget(label_titulo)
        layout.add_widget(label_informacion)
        layout.add_widget(lyt_botton)
        numero_imagen = 0

    def menu(self, *largs):
        self.manager.current= 'mainmenu_screen'
        self.manager.transition.direction= 'right'

    def iniciar(self, *largs):
        global tiempo_inicial
        tiempo_inicial = time.time()
        layout = self.ids.layout_screen_Visual
        layout.clear_widgets()
        Clock.schedule_once(self.pausa, 2)

    def pausa(self, *largs):
        """
        Layout needs to be cleaned later add the items as picture and button
         , Wait 3 seconds after the dark screen before displaying the image
        """
        layout = self.ids.layout_screen_Visual
        layout.clear_widgets()
        Clock.schedule_once(self.mostrar_imagen, config.visual_tiempo_espera)

    def mostrar_imagen(self, dt):
        """
        N image (numeroImagen) is displayed and a value is generated in a
        range of 8 to 16 seconds call stimulus. the variable "dt" is an
        implicit variable when used Clock, and its value It represents the
        real time when I was called to a function
        """
        global numero_imagen, tiempo_inicial, tiempo_eventos, tiempo_estimulo

        layout = self.ids.layout_screen_Visual
        numero_imagen = numero_imagen + 1
        if numero_imagen <= config.visual_numero_imagenes:
            # Add the record time for the event is 5
            tiempo_eventos.append(time.time() - tiempo_inicial)

            src = ruta_imagen + "/%d.jpg" % numero_imagen
            imagen = Image(source=src, pos=layout.pos, size=layout.size)
            layout.add_widget(imagen)
            tiempo_estimulo = random.randint(
                config.visual_rango_estimulo_menor,
                config.visual_rango_estimulo_mayour
            )
            Clock.schedule_once(partial(self.estimulo, imagen), tiempo_estimulo)
        else:
            # If all images were already completed, the test is terminated
            tiempo_final = time.time()
            layout.clear_widgets()
            label = Label(text='Prueba finalizada.')
            layout.add_widget(label)
            datos = [
                str(round(i, 3)-2.000) + ' ' +
                str(round(j, 3)-2.000) for i, j in
                zip(tiempo_eventos, tiempo_estimulos)
            ]

            subject_folio = None
            if type(config.sujeto) == str:
                subject_folio = config.sujeto
            else:
                subject_folio = config.last_data()

            filename = config.export_to_file(
                datos,
                config.grupo,
                subject_folio,
                'V',
            )

            config.datos_prueba = [
                subject_folio,
                filename[:-1] + str(int(filename[-1])-1),
                str(tiempo_final-tiempo_inicial),
                str([round(i, 3)-2.000 for i in tiempo_eventos])[1:-2],
                str([round(i, 3)-2.000 for i in tiempo_estimulos])[1:-2],

            ]
            config.save_data_test(config.datos_prueba)
            self.manager.current = 'quit_screen'

    def estimulo(self, imagen, dt):
        """
        The stimulus a circle that is added to the image in a random position
        is created, in this case within a defined range.
        """
        layout = self.ids.layout_screen_Visual
        # Time registration is added to the stimulus
        tiempo_estimulos.append(time.time() - tiempo_inicial)

        widget = Widget()
        centro_x = random.randint(1, int(imagen.width))

        # The start variable is the range within axis from where the
        # stimulus is displayed.
        inicio = int(.001 * int(imagen.height))
        centro_y = random.randint(inicio, int(imagen.height))
        diametro_estimulo = int(int(layout.height) *
                                config.visual_porcentaje_estimulo)
        with widget.canvas:
            Color(1, 1, 0)
            Ellipse(pos=(centro_x, centro_y), size=(
                diametro_estimulo, diametro_estimulo
            ))
        imagen.add_widget(widget)
        Clock.schedule_once(self.pausa, config.visual_espera_estimulo)
