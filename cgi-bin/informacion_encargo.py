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
        Select * FROM encargo WHERE id = {id}
        '''
db.cursor.execute(sql)
encargo = db.cursor.fetchall()[0]


paises = db.get_pais_o_ciudad(1)
ciudades = db.get_pais_o_ciudad(2)
kilos = db.get_kilos_encargo()
espacio = db.get_espacio_encargo()
###################
descripcion = encargo[1]
kilos_disponible = dbs.selectByID(encargo[3], kilos)[1]
espacio_disponible = dbs.selectByID(encargo[2], espacio)[1]
orig = dbs.selectCityById(encargo[4], ciudades, paises)
dest = dbs.selectCityById(encargo[5], ciudades, paises)
mail = encargo[6]
cel = encargo[7]
sql_foto = f'SELECT id, ruta_archivo, nombre_archivo FROM foto WHERE encargo_id={encargo[0]}'
db.cursor.execute(sql_foto)
total_fotos = db.cursor.fetchall()
v = [encargo[0], descripcion, espacio_disponible, kilos_disponible, orig, dest,  mail, cel, total_fotos]


contenido = f"""
        <div class="card">
            <div class="card-body">
            <div class="col-sm-4"></div>
            <div class="col-sm-4">
            <h5 class="card-title inline"><u>Datos:</u></h5>
            <ul class="list-group" >
                <li id="Descripcion" class="list-group-item">Descripcion: {v[1]}</li>
                <li id="kilos-disponible" class="list-group-item">Kilos disponibles: {v[2]}</li>
                <li id="espacio-disponible" class="list-group-item">Espacio disponible: {v[3]}</li>
                <li id="origen" class="list-group-item">Origen: {v[4]}</li>
                <li id="destino" class="list-group-item">Destino: {v[5]}</li>
                <li id="Email" class="list-group-item">Email: {v[6]}</li>
                <li id="Celular" class="list-group-item">Celular: {v[7]}</li>
                <li class ="list-group-item">Imágenes encargos: </li>
            </ul> <div>"""
n_foto = 1

for foto in v[8]:
        contenido += f"""<div id="img{n_foto}" class="imagenes" >
                        <img id='alo{n_foto}' class="card-img-bottom" src="../media/{foto[1]}" width='640' height='480' alt="{foto[2]}"  onclick='relocate(this)'/>
                    </div><br>"""

        n_foto+=1


end =         """</div>
        </div>
            <div class="col-sm-4"></div>
            </div>
        </div>  
        </div></div>
        <style>
                .imagenes {
	            padding: 0px;
	            border: 0px;
	            object-fit: fill;
	            max-width: 640px;
                }

                .bigImagenes {
	            padding: 0px;
	            border: 0px;
	            object-fit: fill;
	            max-width: 1280px;
                }
        </style>
        
        <script> 
        function relocate(element) {
                img = document.getElementById(element.id);
                if (img.height == "1024" && img.width == "1280") {
                    img.className = "imagenes";
                    img.height = "480";
                    img.width = "640";
                } else {
                    img.className = "bigImagenes";
                    img.height = "1024";
                    img.width = "1280";
                }
                console.log(img.width);
                console.log(img.height);
            }


        </script>
          
"""


with open('../agregar.html', 'r', encoding="utf-8") as ver:
    file = ver.read()
    print(file.format('Información encargo', contenido+end))