_author__ = 'sepulvedaavila'

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
import time
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from functools import partial
import config


class MotorIm(Screen):
    imPo = 0
    motor_image_widget = Image(source=config.RUTA_IMAGENES_MI + '/im_.png')
    descripcion = Label(text=config.TEXTO_INFORMACION_PRUEBA_MOTORIMAGE, font_size = '20sp', valign = 'middle', halign = 'center')
    tiempo_inicial = None
    tiempos_eventos = []
    tiempo_final = None
    imPo = 0

    def mostrarDescripcion(self, *largs):
        layout = self.ids.layout_screen_Motor
        # layout.clear_widgets()
        Clock.schedule_once(partial(self.change_image), config.TIEMPO_POR_IMAGEN_MI)

    def change_image(self, dt):
        layout = self.ids.layout_screen_Motor
        if self.imPo == 7:
            self.tiempo_final ="{0:.3f}".format(time.time() - self.tiempo_inicial)
            print 'tiempo final', str(self.tiempo_final)
            self.salir()
        else:
            layout.clear_widgets()
            print 'path', config.RUTA_IMAGENES_MI, type(config.RUTA_IMAGENES_MI)
            self.motor_image_widget.source = config.RUTA_IMAGENES_MI+"/im_"+str(self.imPo)+".png"
            layout.add_widget(self.motor_image_widget)
            tiempo_actual = "{0:.3f}".format(time.time()-self.tiempo_inicial)
            self.tiempos_eventos.append(tiempo_actual)
            print "Tiempo evento: "+str(tiempo_actual)
            self.imPo += 1
            Clock.schedule_once(partial(self.mostrarDescripcion))

    def start(self, *largs):
        layout = self.ids.layout_screen_Motor
        layout.clear_widgets()
        self.tiempo_inicial = time.time()
        Clock.schedule_once(partial(self.mostrarDescripcion), 3)

    def salir(self):
        subject_folio = None
        if type(config.sujeto) == str:
            subject_folio = config.sujeto
        else:
            subject_folio = config.last_data()

        filename = config.export_to_file(
            [str(i) for i in self.tiempos_eventos],
            config.grupo,
            subject_folio,
            'M'
        )

        config.datos_prueba = [
            subject_folio,
            filename[:-1] + str(int(filename[-1])-1),
            str(self.tiempo_final),
            str([i for i in self.tiempos_eventos])[1:-1],
            ]
        config.save_data_test(config.datos_prueba)
        self.manager.current = 'quit_screen'

    def build(self):
        layout = self.ids.layout_screen_Motor
        """
        This is the main screen waiting to start the test
        """
        label_titulo = Label(font_size='20sp', text='-- Motor --')
        label_informacion = Label(font_size='20sp', text=config.TEXTO_INFORMACION_PRUEBA_MOTORIMAGE)

        lyt_botton = BoxLayout(orientation='horizontal')
        btn_menu = Button(text='Menu', size_hint=(.5, .3))
        btn_menu.bind(on_press=partial(self.menu))
        boton = Button(text='Iniciar', size_hint=(.5, .3))
        boton.bind(on_press=partial(self.start))
        lyt_botton.add_widget(btn_menu)
        lyt_botton.add_widget(boton)

        layout.add_widget(label_titulo)
        layout.add_widget(label_informacion)
        layout.add_widget(lyt_botton)
        numero_imagen = 0

    def menu(self, *largs):
        self.manager.current= 'mainmenu_screen'
        self.manager.transition.direction= 'right'