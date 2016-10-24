# -*- coding: utf-8 -*-
__author__ = 'roberto'

from kivy.uix.screenmanager import Screen
import kivy
kivy.require('1.0.6')
from functools import partial
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import config as config


class FormularioSujeto(Screen):

    def build(self):
        """
        Creacion de la interfaz
        """
        config.sujetos_previos = tuple(['Folio: ' + i.split(' ')[0] for i in
                                        config.read_data()])
        layout = self.ids.layout_screen_Formulario_Sujeto
        layout.clear_widgets()

        lyt_top = BoxLayout(orientation='horizontal')
        lyt_labels = BoxLayout(orientation='vertical')
        lyt_inputs = BoxLayout(orientation='vertical')
        lyt_genero = BoxLayout(orientation='horizontal')
        lyt_destreza = BoxLayout(orientation='horizontal')

        # Spinner
        spn_config = Spinner(
            text='Sujetos Previos',
            values=config.sujetos_previos,
            size_hint=config.BASE_WIDGET_HEIGHT
        )


        # Labels
        lbl_titulo = Label(text='Informacion del Sujeto',
                           size_hint=config.BASE_WIDGET_HEIGHT)
        lbl_tester = Label(text='IDs de los Testers')
        lbl_group = Label(text='Grupo')
        lbl_folio = Label(text='Folio del Sujeto')
        lbl_edad = Label(text='Edad')
        lbl_sueno = Label(text='Horas de Sueño')
        lbl_ayuna = Label(text='Horas de Ayuna')
        lbl_salud = Label(text='Comentarios de Salud')
        lbl_genero = Label(text='Genero')
        lbl_destreza = Label(text='Destreza')
        lbl_fuma = Label(text='Fuma?')
        lbl_lentes = Label(text='Usa Lentes?')

        lbl_fem = Label(text='Femenino')
        lbl_mas = Label(text='Masculino')
        lbl_diestro = Label(text='Diestro')
        lbl_ambidiestro = Label(text='Ambidiestro')
        lbl_zurdo = Label(text='Zurdo')

        # Inputs
        txt_tester = TextInput()
        txt_folio = config.FloatInput()
        txt_group = config.TextInput()
        txt_edad = config.FloatInput()
        txt_sueno = config.FloatInput()
        txt_ayuna = config.FloatInput()
        txt_salud = TextInput()

        # Botones y CheckBoxes
        chk_fuma = CheckBox()
        chk_lentes = CheckBox()
        chk_fem = CheckBox(group="genero")
        chk_mas = CheckBox(group="genero")
        chk_diestro = CheckBox(group="destreza")
        chk_ambidiestro = CheckBox(group="destreza")
        chk_zurdo = CheckBox(group="destreza")
        btn_menu = Button(text='Menu')
        btn_previous_subject = Button(text='Utilizar sujeto seleccionado')
        btn_new_subject = Button(text='Registrar nuevo sujeto')

        entradas = dict()
        entradas['tester'] = txt_tester
        entradas['folio'] = txt_folio
        entradas['group'] = txt_group
        entradas['edad'] = txt_edad
        entradas['sueno'] = txt_sueno
        entradas['ayuna'] = txt_ayuna
        entradas['salud'] = txt_salud
        entradas['fuma'] = chk_fuma
        entradas['lentes'] = chk_lentes
        entradas['fem'] = chk_fem
        entradas['mas'] = chk_mas
        entradas['diestro'] = chk_diestro
        entradas['ambidiestro'] = chk_ambidiestro
        entradas['zurdo'] = chk_zurdo

        # Bindings
        btn_previous_subject.bind(on_press=partial(
            self.selected_subject, spn_config))
        btn_new_subject.bind(on_press=partial(
            self.new_subject, entradas))
        btn_menu.bind(on_press=partial(self.menu))


        # Creacion de Interfaz
        lyt_genero.add_widget(lbl_fem)
        lyt_genero.add_widget(chk_fem)
        lyt_genero.add_widget(lbl_mas)
        lyt_genero.add_widget(chk_mas)

        lyt_destreza.add_widget(lbl_diestro)
        lyt_destreza.add_widget(chk_diestro)
        lyt_destreza.add_widget(lbl_ambidiestro)
        lyt_destreza.add_widget(chk_ambidiestro)
        lyt_destreza.add_widget(lbl_zurdo)
        lyt_destreza.add_widget(chk_zurdo)

        lyt_labels.add_widget(lbl_tester)
        lyt_labels.add_widget(lbl_folio)
        lyt_labels.add_widget(lbl_group)
        lyt_labels.add_widget(lbl_edad)
        lyt_labels.add_widget(lbl_sueno)
        lyt_labels.add_widget(lbl_ayuna)
        lyt_labels.add_widget(lbl_salud)
        lyt_labels.add_widget(lbl_genero)
        lyt_labels.add_widget(lbl_destreza)
        lyt_labels.add_widget(lbl_fuma)
        lyt_labels.add_widget(lbl_lentes)
        lyt_labels.add_widget(Label())
        lyt_labels.add_widget(btn_menu)

        lyt_inputs.add_widget(txt_tester)
        lyt_inputs.add_widget(txt_folio)
        lyt_inputs.add_widget(txt_group)
        lyt_inputs.add_widget(txt_edad)
        lyt_inputs.add_widget(txt_sueno)
        lyt_inputs.add_widget(txt_ayuna)
        lyt_inputs.add_widget(txt_salud)
        lyt_inputs.add_widget(lyt_genero)
        lyt_inputs.add_widget(lyt_destreza)
        lyt_inputs.add_widget(chk_fuma)
        lyt_inputs.add_widget(chk_lentes)
        lyt_inputs.add_widget(Label())
        lyt_inputs.add_widget(btn_previous_subject)
        lyt_inputs.add_widget(btn_new_subject)

        lyt_top.add_widget(lyt_labels)
        lyt_top.add_widget(lyt_inputs)
        layout.clear_widgets()
        layout.add_widget(lbl_titulo)
        layout.add_widget(spn_config)
        layout.add_widget(lyt_top)

    def selected_subject(self, spinner, *largs):
        """
        Asignacion de grupo en casos aplicables

        :param spinner: Objeto spinner de kivy
        :param largs: Argumento de kivy
        :return: None
        """
        if spinner.text != 'Sujetos Previos':
            config.sujeto = spinner.text.split(': ')[1]
            self.test_forms()

    def new_subject(self, entradas, *largs):
        """
        Almacena la informacion de cada sujeto
        :param entradas: diccionario con datos del formulario
        :param largs: Argumentos de Kivy
        :return: None
        """
        genero = None
        destreza = None

        # Representacion booleana en base de datos, mas = 1 fem = 0
        if entradas['fem'].active or entradas['mas'].active:
            genero = int(entradas['mas'].active)

        if entradas['diestro'].active or entradas['zurdo'].active or \
           entradas['ambidiestro'].active:
            if entradas['diestro'].active:
                destreza = 'diestro'
            elif entradas['ambidiestro'].active:
                destreza = 'ambidiestro'
            else:
                destreza = 'zurdo'

        config.sujeto = [
            entradas['folio'].text,
            entradas['group'].text,
            entradas['tester'].text,
            entradas['edad'].text,
            genero,
            destreza,
            entradas['sueno'].text,
            entradas['ayuna'].text,
            entradas['salud'].text,
            entradas['lentes'].active,
            entradas['fuma'].active,

        ]

        form_complete = True
        for elem in config.sujeto:
            if type(elem) == str and elem == '':
                form_complete = False

        if form_complete:
            config.grupo = entradas['group'].text
            self.test_forms()

    def test_forms(self):
        """
        Decide la interfaz de la prueba inicial
        """
        prueba_siguiente = config.prueba_seleccionada

        if type(config.sujeto) == list:
             config.save_data_suject(config.sujeto)

        if prueba_siguiente == "0":
            self.manager.current = 'visualSearch_screen'
            self.manager.get_screen('visualSearch_screen').build()
        elif prueba_siguiente == "1":
            self.manager.current = 'motorIm_screen'
            self.manager.get_screen('motorIm_screen').build()
        elif prueba_siguiente == "2":
            self.manager.current = 'box_screen'
            self.manager.get_screen('box_screen').build()
        else:
            print "Error: Archivo configuracion, número de prueba a " \
                  "inicializar no se ha encontrado."

    def menu(self, *largs):
        self.manager.current = 'mainmenu_screen'
        self.manager.transition.direction = 'right'