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
pagina = int(args.getvalue('pagina'))


viajes_por_pag = 5

sql = f'''
        Select * FROM viaje LIMIT {(pagina-1)*viajes_por_pag}, {pagina*viajes_por_pag}
        '''
db.cursor.execute(sql)
viajes = db.cursor.fetchall()
paises = db.get_pais_o_ciudad(1)
ciudades = db.get_pais_o_ciudad(2)
kilos = db.get_kilos_encargo()
espacio = db.get_espacio_encargo()
###################
v = []
for viaje in viajes:
    orig = dbs.selectCityById(viaje[1], ciudades, paises)
    dest = dbs.selectCityById(viaje[2], ciudades, paises)
    fecha_ida = viaje[3]
    fecha_vuelta = viaje[4]
    kilos_disponible = dbs.selectByID(viaje[5], kilos)[1]
    espacio_disponible = dbs.selectByID(viaje[6], espacio)[1]
    mail = viaje[7]
    cel = viaje[8]
    v += [[viaje[0], orig, dest, fecha_ida, fecha_vuelta, kilos_disponible, espacio_disponible, mail, cel]]


###################

sql2 = "SELECT COUNT(*) FROM viaje"
db.cursor.execute(sql2)
total_viajes = db.cursor.fetchall()[0][0]
total_paginas = math.ceil( total_viajes/viajes_por_pag )

listado = """
<div class="table-responsive-sm">
        <table id="listado" class="table">
            <thead class="thead-dark">
            <tr>
                <th scope="col">ID</th>
            <th scope="col">Origen</th>
                <th scope="col">Destino</th>
            <th scope="col">Fecha ida</th>
            <th scope="col">Fecha llegada</th>
            <th scope="col">Kilos</th>
            <th scope="col">Espacio</th>
            <th scope="col">Email</th>
            <th scope="col">Celular</th>
            </tr>
            </thead>
        <tbody>"""
for celda in v:

    listado +=           f""" <tr class="cell" id="{celda[0]}" onclick="window.location='informacion_viaje.py?id={celda[0]}'">
                 <th scope="row" onclick="window.location='informacion_viaje.py?id={celda[0]}'">{celda[0]}</th>
                    <td>{celda[1]}</td>
                    <td>{celda[2]}</td>
                    <td>{celda[3]}</td>
                    <td>{celda[4]}</td>
                    <td>{celda[5]}</td>
                    <td>{celda[6]}</td>
                    <td>{celda[7]}</td>
                    <td>{celda[8]}</td>
                </tr>
                """
fin_listado = """        </tbody>
    </table>
    <nav aria-label="Page navigation example">
  <ul class="pagination justify-content-center">"""
if pagina == 1:
    previous =    f"""<li class="page-item disabled">
          <a class="page-link" href="ver_viajes.py?pagina={pagina}" >Previous</a>
            </li>"""
else:
    previous = f"""<li class="page-item">
              <a class="page-link" href="ver_viajes.py?pagina={pagina-1}" >Previous</a>
                </li>"""


pages =""
for i in range(total_paginas):
    pages += f"""<li class="page-item"><a class="page-link" href="ver_viajes.py?pagina={i+1}" onclick=" ">{i+1}</a></li>"""

if pagina == total_paginas:
    next = f"""
        <li class="page-item disabled">
            <a class="page-link" href="ver_viajes.py?pagina={pagina}">Next</a>
         </li>"""
else:
    next = f"""
            <li class="page-item">
                <a class="page-link" href="ver_viajes.py?pagina={pagina+1}">Next</a>
             </li>"""

last =  """</ul>
</nav>

    </div>
    <div class="wrapper">
        <div class="sliding-background"></div>
    </div>"""


with open('../agregar.html', 'r', encoding="utf-8") as ver:
    file = ver.read()
    print(file.format('Ver viajes', listado + fin_listado + previous + pages + next + last))