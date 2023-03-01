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

formulario = '''
<form action="save_encargo.py" method="POST" enctype="multipart/form-data">
            <!-- Descripción de encargo -->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-4 text-left">
                    <label class="text-left" for="descripcion">Descripción del encargo:</label>
                    <textarea name="descripcion" class="form-control" id="descripcion" rows="3" placeholder="Escriba su descripción aquí (máximo 100 caracteres)"></textarea>
                </div>
            </div>

            <!-- Espacio y kilo disponible-->
            <div class="row">
    <div class="col-sm-4"></div>
                <div class="col-sm-2">

                    <!-- Espacio disponible -->
                    <label for="espacioDisponible">Espacio disponible:</label>
                        <select class="form-control" name="espacio-solicitado" id="espacioDisponible" >
                            <option value="-1">Escoja volumen...  </option>'''
esp = db.get_espacio_encargo()
for es in esp:
    formulario += f"""<option value="{es[0]}">{es[1]}</option>"""

form2 =                        '''</select>
                </div>
                <div class="col-sm-2">
                    <!-- Kilos disponible -->
                    <label for="kilosDisponibles">Kilos disponibles:</label>
                        <select class="form-control" name="kilos-solicitados" id="kilosDisponibles" >
                            <option value="-1">Escoja peso...  </option>'''
kg = db.get_kilos_encargo()
for k in kg:
    form2 += f"""<option value="{k[0]}">{k[1]}</option>"""

form3=                      ''' </select>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <br>

            <!-- Pais y ciudad de origen-->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-2">
                    <!-- Pais origen -->
                    <label for="paisOrigen">País origen:</label>
                        <select class="form-control" name="pais-origen" id="paisOrigen">
                            <option selected value="-1">Escoja país de origen</option>'''



part1_form= """           </select><br>
                </div>
                <div class="col-sm-2">
                    <!-- Ciudad origen -->
                    <label for="ciudadOrigen">Ciudad origen</label>
                        <select class="form-control" name="ciudad-origen" id="ciudadOrigen" >
                            <option selected value="-1">Escoja ciudad de origen              </option>"""

part2_form ="""          </select> <br>
                </div>
                <div class="col-sm-4"></div>
            </div>
            <!-- Pais y ciudad de llegada-->
            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-2">
                    <!-- Pais llegada -->
                    <label for="paisLlegada">País llegada:</label>
                        <select class="form-control" name="pais-destino" id="paisLlegada">
                            <option selected value="-1">Escoja país de llegada</option>"""

paises = db.get_pais_o_ciudad(1)
for p in paises:
    form3 += f"""
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
                            <option value="-1">Escoja ciudad de llegada  </option> """

ciudades = db.get_pais_o_ciudad(2)
for c in ciudades:
    part1_form += f"""<option value="{c[0]}">{c[1]}</option>"""
    mid_form += f"""<option value="{c[0]}">{c[1]}</option>"""
final_form = """
               </select> <br>
                </div>
                <div class="col-sm-4"></div>
            </div>

            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-4">
                    <label >Seleccione las imágenes de su encargo (mín. 1, máx. 3):</label>
                    <input type="file" id="myfile1" name="foto-encargo-1" accept="image/png, image/jgp, image/jpeg"><br>
                    <input type="file" id="myfile2" name="foto-encargo-2" accept="image/png, image/jgp, image/jpeg"><br>
                    <input type="file" id="myfile3" name="foto-encargo-3" accept="image/png, image/jgp, image/jpeg"><br>
                </div>
                <div class="col-sm-4"></div>
            </div>

            <div class="row">
                <div class="col-sm-4"></div>
                <div class="col-sm-4">
                    <label for="emailViajero"> Email viajero:</label>
                    <input  name="email" class="form-control" id="emailViajero" placeholder="ej: ****@gmail.com"><br>
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
            <button type="submit" >Agregar encargo</button>
        </form>
    </div>"""




###alo

with open('../agregar.html', 'r', encoding="utf-8") as agregar:
    file = agregar.read()
    print(file.format('Agregar encargo', formulario + form2 + form3 + part1_form + part2_form + mid_form + final_form))

