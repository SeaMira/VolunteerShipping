#!/usr/bin/python3
# -*- coding: utf-8 -*-


import cgi
import cgitb
from codecs import utf_8_decode
from encodings import utf_8;
import sys
import db
cgitb.enable()

print("Content-type: text/html; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')

db = db.DB('localhost', 'cc500236_u', 'quISsemper', 'cc500236_db')

formulario = """
    <form action="save_viaje.py" method="POST" enctype="multipart/form-data">

            <!-- Pais y ciudad de origen-->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-2">
                    <!-- Pais origen -->
                    <label for="paisOrigen">País origen:</label>
                        <select class="form-control" name="país-origen" id="paisOrigen">
                            <option selected value="-1">Escoja país de origen</option>"""



part1_form= """              </select><br>
                </div>
                <div class="col-sm-2">
                    <!-- Ciudad origen -->
                    <label for="ciudadOrigen">Ciudad origen</label>
                        <select class="form-control" name="ciudad-origen" id="ciudadOrigen" >
                            <option selected value="-1">Escoja ciudad de origen              </option>"""

part2_form ="""                        </select> <br>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <!-- Pais y ciudad de llegada-->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-2">
                    <!-- Pais llegada -->
                    <label for="paisLlegada">País llegada:</label>
                        <select class="form-control" name="país-destino" id="paisLlegada">
                            <option selected value="-1">Escoja país de llegada</option>"""

paises = db.get_pais_o_ciudad(1)
for p in paises:
    formulario += f"""
        <option value='{p[0]}'>{p[1]}</option> """
    part2_form += f"""
        <option value='{p[0]}'>{p[1]}</option> """
mid_form = """
        </select><br>
                </div>
                <div class="col-sm-2">
                    <!-- Ciudad llegada -->
                    <label for="ciudadLlegada">Ciudad llegada:</label>
                        <select class="form-control" name="ciudad-destino" id="ciudadLlegada" >
                            <option value="-1">Escoja ciudad de llegada  </option>"""

ciudades = db.get_pais_o_ciudad(2)
for c in ciudades:
    part1_form += f"""<option value="{c[0]}">{c[1]}</option>"""
    mid_form += f"""<option value="{c[0]}">{c[1]}</option>"""
final_form = """
       </select> <br>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <!-- fecha de ida y de regreso-->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-2">

                    <!-- Fecha ida -->
                    <label for="fechaIda">Fecha de ida</label>
                        <input type="tel" name="fecha-ida" class="form-control" id="fechaIda" placeholder="2001-01-01" "><br>
                </div>
                <div class="col-sm-2">
                    <!-- Fecha regreso -->
                    <label for="fechaRegreso">Fecha de regreso</label>
                        <input type="tel" name="fecha-regreso" class="form-control" id="fechaRegreso" placeholder="2002-01-01"><br>
                </div>
                <div class="col-sm-4"></div>
            </div>

            <!-- Espacio y kilo disponible-->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-2">

                    <!-- Espacio disponible -->
                    <label for="espacioDisponible">Espacio disponible:</label>
                        <select class="form-control" name="espacio-disponible" id="espacioDisponible" >
                            <option  value="-1">Escoja volumen...  </option>"""


esp = db.get_espacio_encargo()
for es in esp:
    final_form += f"""<option value="{es[0]}">{es[1]}</option>"""


final_form2=                       """</select>
                </div>
                <div class="col-sm-2">
                    <!-- Kilos disponible -->
                    <label for="kilosDisponibles">Kilos disponibles:</label>
                        <select class="form-control" name="kilos-disponibles" id="kilosDisponibles" >
                            <option  value="-1">Escoja peso...  </option>"""

kg = db.get_kilos_encargo()
for k in kg:
    final_form2 += f"""<option value="{k[0]}">{k[1]}</option>"""

final_form3 =                      """ </select>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <br>
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-4">
                    <label for="emailViajero"> Email viajero:</label>
                    <input type="tel" name="email" class="form-control" id="emailViajero" placeholder="ej: ****@gmail.com"><br>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-4">
                    <label for="telefonoViajero"> Numero de teléfono del viajero:</label>
                    <input type="tel" name="celular" class="form-control" id="telefonoViajero" placeholder="ej: +569 123 456 78"><br>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <br>
            <button type="submit" >Agregar viaje</button>
        </form>
    </div>"""




###alo

with open('../agregar.html', 'r', encoding="utf-8") as agregar:
    file = agregar.read()
    print(file.format('Agregar viaje', formulario + part1_form + part2_form + mid_form + final_form + final_form2 + final_form3))





















