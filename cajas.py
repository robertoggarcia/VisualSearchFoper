__author__ = 'miguel'

import kivy
import time
from kivy.uix.screenmanager import Screen
kivy.require('1.0.6')
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from functools import partial
from kivy.clock import Clock
import random
import config


class CincoCajas(Screen):
    """
    3 Pruebas de discriminacion y atencion basadas en eventos veloces
    con el fin de evocar la onda P300.

    Nota: La separacion en funciones en algunos casos
    existe solo para legilibilidad del codigo.
    """
    tiempo_inicial = None
    tiempos_eventos = []
    tiempos_reaccion = []
    tiempos_atendidos = []
    tipo = 1

    def build(self):
        """
        Se limpia la pantalla al crear el objeto e inicializa las
        variables de la prueba/

        :param layout: layout incial recibido desde el menu
        :return: None
        """
        layout = self.ids.layout_screen_Box
        layout.clear_widgets()
        self.iniciar_menu_5_cajas()

    def iniciar_menu_5_cajas(self):
        """
        Creacion de Menu Simple para Seleccion de Pruebas
        """
        layout = self.ids.layout_screen_Box
        # Layouts
        lyt_main = BoxLayout(orientation='vertical')
        lyt_buttons = BoxLayout(orientation='horizontal',
                                size_hint=config.BASE_WIDGET_HEIGHT)

        # Labels
        lbl_cajas_titulo = Label(font_size='20sp',
                                 text=config.CAJAS_TITULO,
                                 size_hint=config.BASE_WIDGET_HEIGHT)
        lbl_cajas_descripcion = Label(font_size='20sp',
                                      text=config.CAJAS_DESCRIPCION)

        # Botones
        btn_prueba1 = Button(text=config.CAJAS_BTN_CIRCULOS_TEXT)
        btn_prueba2 = Button(text=config.CAJAS_BTN_RELLENO_TEXT)
        btn_prueba3 = Button(text=config.CAJAS_BTN_AMBAS_TEXT)

        # Creacion de Interfaz
        lyt_buttons.add_widget(btn_prueba1)
        lyt_buttons.add_widget(btn_prueba2)
        lyt_buttons.add_widget(btn_prueba3)
        lyt_main.add_widget(lbl_cajas_titulo)
        lyt_main.add_widget(lbl_cajas_descripcion)
        lyt_main.add_widget(lyt_buttons)
        layout.add_widget(lyt_main)

        # Bindings
        btn_prueba1.bind(
            on_press=partial(self.instrucciones_pruebas, 1))
        btn_prueba2.bind(
            on_press=partial(self.instrucciones_pruebas, 2))
        btn_prueba3.bind(
            on_press=partial(self.instrucciones_pruebas, 3))

    def instrucciones_pruebas(self, tipo, *largs):
        """
        Instrucciones para cada prueba en esta interfaz

        :param tipo: variante de la prueba de discriminacion
        :param largs: Argumentos de Kivy
        :return: layout de las instrucciones
        """
        layout = self.ids.layout_screen_Box
        self.tipo = tipo
        layout.clear_widgets()

        # Widgets
        lyt_botones = BoxLayout(orientation='horizontal')
        btn_menu = Button(text='Menu', size_hint=(1, 0.3))
        btn_instrucciones = Button(
            text=config.CAJAS_BTN_INSTRUCCIONES, size_hint=(1, .3))
        lyt_botones.add_widget(btn_menu)
        lyt_botones.add_widget(btn_instrucciones)


        lbl_cajas_titulo = Label(font_size='20sp',
                                 text=config.CAJAS_TITULO,
                                 size_hint=config.BASE_WIDGET_HEIGHT)
        lbl_pruebas_descripcion = Label(
            text=config.CAJAS_DESCRIPCIONES_PRUEBAS[tipo - 1],
            font_size='20sp'
        )


        # Creacion de Interfaz
        layout.add_widget(lbl_cajas_titulo)
        layout.add_widget(lbl_pruebas_descripcion)
        layout.add_widget(lyt_botones)

        # Bindings de Botones
        btn_instrucciones.bind(
            on_press=partial(self.iniciar_prueba, tipo))
        btn_menu.bind(on_press=partial(self.menu))

    def iniciar_prueba(self, *largs):
        """
        Antes de iniciar la prueba es necesario generar todas las variables
        necesarias, ya que demasiadas llamadas a funciones y ciclos pueden
        aumentan la tolerancia de errores.

        NOTA: todos los componentes de interfaz deben de ser relativos al
        tamano de la pantalla
        """
        layout = self.ids.layout_screen_Box
        # Tiempos entre cada evento
        tiempos = []
        for i in xrange(config.cajas_eventos_totales):
            tiempos.append(random.choice(config.cajas_eventos_rango))
        self.tiempos_eventos = map(config.accumulador, tiempos)

        # El cuadro atendido es seleccionado aleatoriamente
        random.shuffle(config.CAJAS_ATENDIDAS)

        # Rectangulo Exterior
        rect_ext = dict()
        rect_ext['y'] = layout.height * .5
        rect_ext['ancho'] = layout.width * .1
        rect_ext['alto'] = rect_ext['ancho']
        rect_ext['ext'] = True
        pos_ext = [layout.width * (float(x) / 100)
                   for x in range(5, 105, 20)]

        # Rectangulo Interior
        rect_int = dict()
        rect_int['red'] = 0
        rect_int['green'] = 0
        rect_int['blue'] = 0
        rect_int['y'] = layout.height * .53
        rect_int['ancho'] = layout.width * .05
        rect_int['alto'] = rect_int['ancho']
        pos_int = [layout.width * (float(x) + 2.5) / 100
                   for x in range(5, 100, 20)]

        # Creacion de widgets de interfaz, no genera interfaz
        exterior = []
        interior = []
        for i in xrange(len(pos_ext)):

            # Es necesario agregar los colores aqui
            # debido a que se sobreescriben
            rect_ext['red'] = 0
            rect_ext['green'] = 0
            rect_ext['blue'] = 1
            exterior.append(self.generar_cuadro(pos_ext[i], rect_ext,
                                                config.CAJAS_ATENDIDAS[i]))
        for i in xrange(len(pos_int)):
            interior.append(self.generar_cuadro(pos_int[i], rect_int))
        figuras = [exterior, interior, iter(self.generar_estimulos())]

        # Clock.schedule maneja los hilos y asegura que alla menos
        # de 1 milisegundo de error en cada evento
        layout.clear_widgets()
        Clock.schedule_once(
            partial(self.iniciar_interfaz, figuras),
            config.tiempo_estabilizacion)

    def generar_estimulos(self):
        """
        Aqui se definen los eventos dependiendo en el tipo
        de prueba seleccionada
        """
        layout = self.ids.layout_screen_Box

        # Posicion y tamano de los eventos
        evento = dict()
        evento['ancho'] = layout.width * .05
        evento['alto'] = evento['ancho']
        evento['y'] = layout.height * .53

        # Posiciones aleatorias
        eventos_posibles = [layout.width * (float(x) + 2.5)/100
                            for x in range(5, 105, 20)]
        eventos_posiciones = eventos_posibles * (
            config.cajas_eventos_totales / 5)
        random.shuffle(eventos_posiciones)

        # Registro de tiempos atendidos (para medir tiempos de reaccion)
        pos_atendidos = [config.CAJAS_ATENDIDAS[(eventos_posibles.index(i))]
                         for i in eventos_posiciones]

        # Uso de List Comprehension para comparar datos de dos listas
        # Es posible que esta linea no conforma al estilo "pythonic"
        # del lenguaje, puede ser mas legible pero no mas reducida.
        [self.tiempos_atendidos.append(b) if a else None
         for a, b in zip(pos_atendidos, self.tiempos_eventos)]

        # La posicion y tipo de los eventos depende del tipo de prueba
        widgets = []
        if self.tipo == 1:
            for ev in eventos_posiciones:
                widgets.append(self.generar_circulo(ev, evento))
        else:
            evento['red'] = 0

            if self.tipo == 2:
                for ev in eventos_posiciones:

                    evento['green'] = 0
                    evento['blue'] = 1

                    # Decide el color de los cuadros
                    atendido = \
                        config.CAJAS_ATENDIDAS[(eventos_posibles.index(ev))]
                    widgets.append(self.generar_cuadro(ev, evento, atendido))
            else:
                for ev in eventos_posiciones:
                    if random.getrandbits(1):
                        widgets.append(self.generar_circulo(ev, evento))
                    else:
                        evento['green'] = 0
                        evento['blue'] = 1

                        # Decide el color de los cuadros
                        atendido = \
                            config.CAJAS_ATENDIDAS[(eventos_posibles.index(ev))]
                        widgets.append(
                            self.generar_cuadro(ev, evento, atendido)
                        )
        return widgets

    def generar_circulo(self, pos, evento, *largs):
        """
        Genera un widget circular dado la posicion y el tamano.
        (No genera el evento en pantalla, solo el widget)

        :param pos: posicion del evento (relativa a la pantalla)
        :param evento: diccionario con datos de tamano
        :return: el widget que se agrego a la pantallas
        """

        widget = Widget()
        with widget.canvas:
            Color(1, 0, 0)
            Ellipse(pos=(pos,
                         evento['y']),
                    size=(evento['ancho'],
                          evento['alto']))
        return widget

    def generar_cuadro(self, pos, figura, atendido=False, *largs):
        """
        Genera un widget rectangular (cuadrado) dado la posicion y el tamano
        :param pos: posicion del evento (relativa a la pantalla)
        :param figura: diccionario con datos de tamano
        :param atendido: diccionario con datos de tamano
        :param largs: Argumentos de Kivy
        :return: el widget que se agrego a la pantallas
        """

        # Si es rectangulo atendido, cabiear color a verde
        if atendido:
            figura['green'] = 1
            figura['blue'] = 0

        widget = Widget()
        with widget.canvas:
            Color(figura['red'],
                  figura['green'],
                  figura['blue'])
            Rectangle(pos=(pos,
                           figura['y']),
                      size=(figura['ancho'],
                            figura['alto']))
        return widget

    def iniciar_interfaz(self, figuras, *largs):
        """
        Se genera la interfaz de pruebas e inicia la prueba y
        se inica la funcion que agrega cade uno de los eventos
        a la pantalla dependiendo en los tiempos dados.

        :param figuras: diccionario con datos de tamano
        :param largs: Argumentos de Kivy
        """
        layout = self.ids.layout_screen_Box
        layout.clear_widgets()

        for widget in figuras[0]:
            layout.add_widget(widget)
        for widget in figuras[1]:
            layout.add_widget(widget)

        # Inicia los eventos en diferentes hilos (Clock.schedule)
        self.tiempo_inicial = time.time()
        map(lambda x: Clock.schedule_once(partial(
            self.lanzar_estimulo, figuras[2].next()), x), self.tiempos_eventos)
        Clock.schedule_once(partial(self.salir), max(self.tiempos_eventos) + 3)

    def lanzar_estimulo(self, widget, *largs):
        """
        En esta funcion se generan los estimulos en la pantalla usando hilos
        Se determina el tiempo de eliminacion del widget.
        """
        layout = self.ids.layout_screen_Box
        layout.add_widget(widget)
        Clock.schedule_once(partial(self.eliminar_widget, widget), .25)

    def eliminar_widget(self, widget, *largs):
        """
        Elimina un widget de la pantalla

        :param widget: Objeto del widget
        :param largs: Argumentos de Kivy
        """
        layout = self.ids.layout_screen_Box
        layout.remove_widget(widget)

    def menu(self, *largs):
        self.manager.current = 'menupruebas_screen'
        self.manager.transition.direction = 'right'

    def salir(self, *largs):
        """
        Establece el tipo de prueba en el archvo de configuracion y
        termina la prueba.
        :param largs: Argumentos de Kivy
        :return: None
        """

        if self.tipo == 1:
            config.prueba = 2
        elif self.tipo == 2:
            config.prueba = 4
        else:
            config.prueba = 5

        subject_folio = None
        if type(config.sujeto) == str:
            subject_folio = config.sujeto
        else:
            subject_folio = config.last_data()

        datos = [str(round(i, 3)-2.000) + ' ' + str(round(j, 3)-2.000) for i, j in zip(self.tiempos_eventos, self.tiempos_atendidos)]
        # TODO send datos to export file, miguel test
        filename = config.export_to_file(
            [str(i) for i in self.tiempos_atendidos],
            config.grupo,
            subject_folio,
            'B',
            str(self.tipo)
        )

        config.datos_prueba = [
            subject_folio,
            filename[:-1] + str(int(filename[-1])-1),
            str(self.tiempos_atendidos[-1]),
            str([round(i, 3) for i in self.tiempos_eventos])[1:-1],
            str([round(i, 3) for i in self.tiempos_atendidos])[1:-1],
        ]
        config.save_data_test(config.datos_prueba)
        self.manager.current = 'quit_screen'