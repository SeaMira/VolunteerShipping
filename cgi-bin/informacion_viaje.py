#!/usr/bin/python3
# -*- coding: utf-8 -*-

import cgi
import os
import mysql.connector
import sys
import math
#import filetype
import db as dbs

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')

db = dbs.DB('localhost', 'cc500236_u', 'quISsemper', 'cc500236_db')
args = cgi.FieldStorage()
id = args.getvalue('id')
#print(id)


sql = f'''
        Select * FROM viaje WHERE id = {id}
        '''
db.cursor.execute(sql)
viaje = db.cursor.fetchall()[0]

#print(viaje)
paises = db.get_pais_o_ciudad(1)
ciudades = db.get_pais_o_ciudad(2)
kilos = db.get_kilos_encargo()
espacio = db.get_espacio_encargo()
###################

orig = dbs.selectCityById(viaje[1], ciudades, paises)
dest = dbs.selectCityById(viaje[2], ciudades, paises)
fecha_ida = viaje[3]
fecha_vuelta = viaje[4]
kilos_disponible = dbs.selectByID(viaje[5], kilos)[1]
espacio_disponible = dbs.selectByID(viaje[6], espacio)[1]
mail = viaje[7]
cel = viaje[8]
v = [viaje[0], orig, dest, fecha_ida, fecha_vuelta, kilos_disponible, espacio_disponible, mail, cel]

contenido = f"""
        <div class="card">
            <div class="card-body">
            <div class="col-sm-4"></div>
            <div class="col-sm-4">
            <h5 class="card-title inline"><u>Datos:</u></h5>
            <ul class="list-group" >
                <li id="pais_origen" class="list-group-item">Pais origen: {v[1]}</li>
                <li id="destino" class="list-group-item">Destino: {v[2]}</li>
                <li id="fechaIda" class="list-group-item">Fecha ida: {v[3]}</li>
                <li id="fechaLlegada" class="list-group-item">Fecha llegada: {v[4]}</li>
                <li id="Espacio" class="list-group-item">Espacio: {v[5]}</li>
                <li id="Kilos" class="list-group-item">Kilos: {v[6]}</li>
                <li id="Email" class="list-group-item">Email: {v[7]}</li>
                <li id="Celular" class="list-group-item">Celular: {v[8]}</li>
            </ul>
            </div>
            <div class="col-sm-4"></div>
            </div>
        </div>  
    </div>      
"""

with open('../agregar.html', 'r', encoding="utf-8") as ver:
    file = ver.read()
    print(file.format('Información viaje', contenido))