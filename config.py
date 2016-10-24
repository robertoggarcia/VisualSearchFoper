# -*- coding: utf-8 -*-
import os
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
import re
from kivy.uix.textinput import TextInput

# Configuration del proyecto, cadenas de los menus, y funciones genericas


"""======== Constantes Menu ========"""

MENU_DESCRIPCION = \
    "Instrucciones durante las distintas pruebas:\n\n" \
    "- Mantén la vista directamente en el centro de la pantalla.\n" \
    "- Trata de parpadear lo menos posible.\n" \
    "- No hables ni muevas la lengua o movimientos con el rostro.\n"

MENU_TITULO = "SISTEMA DE ADQUISICIÓN DE DATOS PARA INTERFACES CEREBRALES"

"""================== Constantes Prueba Motora ========"""

RUTA_IMAGENES_MI = "MotorImage"
TEXTO_INFORMACION_PRUEBA_MOTORIMAGE = \
    "Se mostrará en la pantalla una figura central en la cual el \n" \
    "sujeto de prueba se concentrará, para después observar las imágenes \n" \
    "que aparecerén a los lados de la figura central. Las figuras que " \
    "aparecerán, \n representan las manos, abiertas y cerradas. Cuando " \
    "aparezca la mano izquierda abierta, \n el sujeto de prueba deberá " \
    "pensar (sin mover ninguna extremidad) en la mano izquierda abierta, \n" \
    "a su vez, cuando aparezca la mano derecha abierta, el sujeto deberá " \
    "pensar en la mano derecha abierta, \n también aparecerán imágenes " \
    "de las manos cerradas, de la misma manera el sujeto deberá \n pensar " \
    "en las manos cerradas sin mover ninguna extremidad."

# Constantes Numericos
NUMERO_IMAGENES_MI = 7
TIEMPO_POR_IMAGEN_MI = 5
MOTOR_TIEMPO_ESTABILIZACION = 5

"""=========================== Constantes VEP =================="""
# Constantes Textuales
RUTA_IMAGENES = "VisualSearchImagenes"
TEXTO_INFORMACION_PRUEBA_VISUAL_SEARCH = \
    "Observa las imágenes que se muestran en la pantalla,\n\n" \
    " y busca el círculo amarillo que aparece en la imagen  \n\n" \
    "un momento después."

# Constantes Numericos
visual_porcentaje_estimulo = 0.04
visual_numero_imagenes = 5
visual_rango_estimulo_menor = 8
visual_rango_estimulo_mayour = 16
visual_tiempo_espera = 3
visual_espera_estimulo = 1
tiempo_estabilizacion = 5

""" ===============CONSTANTES PRUEBA DISCRIMINACION================"""

# Constantes Textuales
CAJAS_TITULO = "Prueba de 5 Cajas"
CAJAS_DESCRIPCION = \
    "Durante esta prueba, aparecerán 5 cajas vacías en la pantalla.\n" \
    "4 de las cajas serán azules y una sera verde. Diferentes estímulos\n" \
    "aparecerán y desaparecerán rápidamente dentro de las cajas. Para esta\n" \
    "prueba, usted SÓLO SE DEBE DE ENFOCAR EN LOS EVENTOS DENTRO DE LA CAJA\n" \
    "VERDE. A iniciar la prueba, habrá un tiempo de espera antes de inicar."

CAJAS_DESCRIPCIONES_PRUEBAS = [
    'En esta prueba los estímulos son CÍRCULOS ROJOS.',
    'En esta prueba los estímulos son CAJAS RELLENAS.',
    'Esta prueba es una combinación de los dos estímulos anteriores. Los\n'
    'estímulos son SÓLO LOS CÍRCULOS ROJOS.'
]
CAJAS_BTN_CIRCULOS_TEXT = "Prueba A"
CAJAS_BTN_RELLENO_TEXT = "Prueba B"
CAJAS_BTN_AMBAS_TEXT = "Prueba C"
CAJAS_BTN_INSTRUCCIONES = "Iniciar Prueba"

CAJAS_ATENDIDAS = [True, False, False, False, False]

# Constantes Numericos
cajas_eventos_totales = 100
cajas_eventos_rango = [.25, .5, .75, 1]
cajas_atendidas = [True, False, False, False, False]


"""==================== Constantes Generales ========"""

DESCRIPCION_SISTEMA = "Sistema desarrollado bajo el lenguaje " \
                      "\nPython 2.7.8 y el framework Kivy 1.8.0.: \n" \
                      "\n\nDesarrolladores:\n" \
                      " - Roberto de Jesús García García\n" \
                      " - Carlos Sepúlveda Avila\n" \
                      " - Miguel Angel Madera Madera\n" \
                      "\n" \
                      "\nMás información:\nrobertojesusgarcia@gmail.com\nmiguelmadera50@gmail.com\ncnsa1606@gmail.com"

manager = ScreenManager(transition =NoTransition())

grupo = 'A'
BASE_WIDGET_HEIGHT = (1, 1/float(12))

"""===================== Variable Temporales ========"""

prueba_seleccionada = ""

""" ===============VARIABLES DE DATOS================"""
# SELECT
sujetos_previos = ["1", "2"]

# INSERT
sujeto = None
datos_prueba = None


""" ===============FUNCIONES================"""


def export_to_file(data, group, subject, test, test_type=''):
    """
    Exportacion de datos de prueba a archivo

    :param data: Datos de la cada prueba
    :param group: grupo de estudio (caracter)
    :param subject: numero especifico del sujeto
    :param test: identificador de la prueba
    :param test_type: solo se utiliza en caso de la prueba de discriminacion
    :return: nombre del archivo que se escribio
    """

    name_string = group + str(subject).zfill(3) + \
                  'E' + str(test) + str(test_type)
    i = 1
    file_exists = True
    while file_exists:
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'datos_pruebas',
            name_string + '_' + str(i) + '.txt'
        )
        i += 1
        if not os.path.isfile(filename):
            file_exists = False

    with open(filename, 'w') as data_file:
        data_file.write('\n'.join(data))
    return name_string + '_' + str(i)


def save_data_suject(data):
    """
    Almacena datos de cada sujeto

    :param datos de sujeto
    :return None
    """
    suject_data = open('datos_pruebas/datos_sujetos.txt', 'a')
    data = [str(i) + ' ' for i in data]
    data[-1] = data[-1].replace(' ', '')
    data.append('\n')
    suject_data.writelines(data)


def save_data_test(data):
    """
    Almacena datos de cada prueba

    :param datos de cada prueba
    :return None
    """
    suject_data = open('datos_pruebas/datos_pruebas.txt', 'a')
    data = [str(i) + ' ' for i in data]
    data[-1] = data[-1].replace(' ', '')
    data.append('\n')
    suject_data.writelines(data)


def read_data():
    """
    Funcion general para la lectura de datos

    :param datos de sujeto
    :return filestream
    """
    suject_data = open('datos_pruebas/datos_sujetos.txt', 'r')
    return suject_data.readlines()


def last_data():
    """
    Obtiene el ultimo dat0
    """
    for i in read_data():
        ultimo = i
    return ultimo.split(' ')[0]


def nested_tuple_str_cast(nested_tuple):
    return tuple([tuple([str(j) for j in i]) for i in nested_tuple])


# Funciones (python recipes)
def accumulador(elem, lista=[0]):
    lista[0] += elem
    return lista[0]


def frange(inicio, fin=None, step=None):
    """
    Funcion range de python adaptada para funcionamiento con decimales.
    """

    if fin is None:
        fin = inicio + 0.0
        inicio = 0.0

    if step is None:
        step = 1.0

    range_list = []
    while True:
        siguiente = inicio + len(range_list) * step
        if step > 0 and siguiente >= fin:
            break
        elif step < 0 and siguiente <= fin:
            break

        # En nuestro caso no es necesario tener precision alta,
        # no importan los errores de puntos flotantes
        range_list.append(round(siguiente, 4))

    return range_list


# Clase Global
class FloatInput(TextInput):
    """
    Override de metodo insert_text para permitir
    solo caracteres numericos. Se utiliza regex para
    hacer la distincion.
    """
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s)
                          for s in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)