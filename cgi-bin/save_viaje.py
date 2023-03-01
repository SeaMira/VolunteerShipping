#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import os
import sys
#import filetype
import db as dbs
from fun_validaciones import *

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')

db = dbs.DB('localhost', 'cc500236_u', 'quISsemper', 'cc500236_db')
form = cgi.FieldStorage()

paises = db.get_pais_o_ciudad(1)
ciudades = db.get_pais_o_ciudad(2)
kilos = db.get_kilos_encargo()
espacio = db.get_espacio_encargo()


pais_origen = int(form.getvalue('país-origen'))
ciudad_origen = int(form.getvalue('ciudad-origen'))
pais_destino = int(form.getvalue('país-destino'))
ciudad_destino = int(form.getvalue('ciudad-destino'))
fecha_ida = form.getvalue('fecha-ida')
fecha_regreso = form.getvalue('fecha-regreso')
espacio_disponible = int(form.getvalue('espacio-disponible'))
kilos_disponible = int(form.getvalue('kilos-disponibles'))
email_viajero = form.getvalue('email')
numero_celular_viajero = form.getvalue('celular')


# validaciones
errores = '''<div class="d-flex align-items-center">
                <div class="container p-3 my-3 border bg-light text-center">'''
valido = True
#pais de ida o regreso correctos
if (pais_origen == -1 or pais_origen != ciudad_origen or ciudad_origen==-1):
    errores += '<p>No se ha seleccionado país o ciudad de origen.</p>'
    valido = False
# ciudad de ida o regreso correctos
if (pais_destino == -1 or pais_destino != ciudad_destino or ciudad_destino==-1):
    errores += '<p>No se ha seleccionado país o ciudad de destino.</p>'
    valido = False
#fechas correctas
if (not valida_diff_fechas(fecha_ida, fecha_regreso)):
    errores += '<p>La fecha de ida o de regreso no está bien colocada, o la fecha de regreso es anterior a la de ida.</p>'
    valido = False
#espacio de encargo elegido correctamente
if (espacio_disponible == -1):
    errores += '<p>No se ha seleccionado un volumen determinado.</p>'
    valido = False
#kilos de encargo correctamente elegidos
if (kilos_disponible == -1):
    errores += '<p>No se ha seleccionado un peso apropiado.</p>'
    valido = False
#email que calce con regex
if (not valida_mail(email_viajero) or len(email_viajero) > 30):
    errores += '<p>La dirección de correo electrónico ingresada es incorrecta.</p>'

    valido = False
#email que calce con regex
if (not valida_tel(numero_celular_viajero) or len(numero_celular_viajero) > 15):
    errores += '<p>El número de teléfono ingresado es incorrecto.</p>'
    valido = False
#print( str(pais_origen) + str(pais_destino) + fecha_ida + fecha_regreso + str(kilos_disponible) + str(espacio_disponible) + email_viajero + numero_celular_viajero)


if (valido):
    id_origen = dbs.selectByID(pais_origen, ciudades)[2]
    id_destino = dbs.selectByID(pais_destino, ciudades)[2]
    data = (id_origen, id_destino, fecha_ida, fecha_regreso, kilos_disponible, espacio_disponible, email_viajero, numero_celular_viajero)
    db.save_viaje(data)
    mensaje =  '''
            <div class="d-flex align-items-center">
                <div class="container p-3 my-3 border bg-light text-center">
                    !Su viaje se ha agregado correctamente¡
                </div>
            </div>
    '''
    with open('../inicio_template.html','r', encoding="utf-8") as template:
        file = template.read()
        print(file.format(mensaje))
else:
    errores += '''</div>
            </div>'''
    with open('../inicio_template.html','r', encoding="utf-8") as template:
        file = template.read()
        print(file.format(errores))