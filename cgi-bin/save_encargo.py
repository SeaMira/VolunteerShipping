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


pais_origen = int(form.getvalue('pais-origen'))
ciudad_origen = int(form.getvalue('ciudad-origen'))
pais_destino = int(form.getvalue('pais-destino'))
ciudad_destino = int(form.getvalue('ciudad-destino'))
descripcion = form.getvalue('descripcion')
espacio_solicitado = int(form.getvalue('espacio-solicitado'))
kilos_solicitados = int(form.getvalue('kilos-solicitados'))
email = form.getvalue('email')
celular = form.getvalue('celular')

img1 = form['foto-encargo-1']
img2 = form['foto-encargo-2']
img3 = form['foto-encargo-3']
MAX_FILE_SIZE= 100000000
tipos_soportados = ['image/jpeg', 'image/jpg', 'image/png']


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
if (len(descripcion) > 250 or len(descripcion) == 0):
    errores += '<p>La descripción dada excede el máximo de caracteres (250) o no se ha dado una descripción.</p>'
    valido = False
#espacio de encargo elegido correctamente
if (espacio_solicitado == -1):
    errores += '<p>No se ha seleccionado un volumen determinado.</p>'
    valido = False
#kilos de encargo correctamente elegidos
if (kilos_solicitados == -1):
    errores += '<p>No se ha seleccionado un peso apropiado.</p>'
    valido = False
#email que calce con regex
if (not valida_mail(email) or len(email) > 30):
    errores += '<p>La dirección de correo electrónico ingresada es incorrecta.</p>'

    valido = False
#email que calce con regex
if (not valida_tel(celular) or len(celular) > 15):
    errores += '<p>El número de teléfono ingresado es incorrecto.</p>'
    valido = False
#print( str(pais_origen) + str(pais_destino) + fecha_ida + fecha_regreso + str(kilos_disponible) + str(espacio_disponible) + email_viajero + numero_celular_viajero)

max_file_size = 100000000
supported_types = ['image/jpeg', 'image/jpg', 'image/png']

v_img1 = valida_img(img1, max_file_size, supported_types)
v_img2 = valida_img(img2, max_file_size, supported_types)
v_img3 = valida_img(img3, max_file_size, supported_types)

if not v_img1 and not v_img2 and not v_img3:
    errores += '<p>No se han subido imágenes o los archivos del encargo no pueden ser procesados.</p>'
    valido = False
imagenes = [img1, img2, img3]
for img in imagenes:
    if not valida_img(img, max_file_size, supported_types):
        imagenes.remove(img)


if (valido):
    id_origen = dbs.selectByID(pais_origen, ciudades)[2]
    id_destino = dbs.selectByID(pais_destino, ciudades)[2]
    data = (descripcion, espacio_solicitado, kilos_solicitados, id_origen, id_destino, email, celular)
    db.save_encargo(data, imagenes)
    mensaje =  '''
            <div class="d-flex align-items-center">
                <div class="container p-3 my-3 border bg-light text-center">
                    !Su encargo se ha agregado correctamente¡
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
