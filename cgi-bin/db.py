#!/usr/bin/python3
# -*- coding: utf-8 -*-

import mysql.connector
import hashlib
import sys

class DB:
    def __init__(self, host, user, password, database):
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.db.cursor()

    def save_viaje(self, data):

        try:
            sql = '''
                INSERT INTO viaje (origen,	destino,	fecha_ida,	fecha_regreso,	kilos_disponible,	espacio_disponible,	email_viajero,	celular_viajero) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                '''
            self.cursor.execute(sql, data)  # ejecuto la consulta
            self.db.commit()  # modifico la base de datos

        except:
            print("ERROR AL GUARDAR EN LA BASE DE DATOS")
            sys.exit()

    def save_encargo(self, data, imagenes):

        try:
            sql = '''
                INSERT INTO encargo (descripcion, espacio, kilos, origen, destino, email_encargador, celular_encargador) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                '''
            self.cursor.execute(sql, data)  # ejecuto la consulta
            self.db.commit()  # modifico la base de datos

        except:
            print("ERROR AL GUARDAR ENCARGO EN LA BASE DE DATOS")
            sys.exit()
        id_encargo = self.cursor.getlastrowid()

        try:
            for img in imagenes:
                filename = img.filename

                sql = "SELECT COUNT(id) FROM foto"  # Cuenta los archivos que hay en la base de datos
                self.cursor.execute(sql)
                total = self.cursor.fetchall()[0][0] + 1
                filename_hash = hashlib.sha256(filename.encode()).hexdigest()[0:30]  # aplica función de hash
                filename_hash += f"_{total}"
                tupla = (filename_hash, filename, id_encargo)

                open(f"../media/{filename_hash}", "wb").write(img.file.read())

                sql = '''
                    INSERT INTO foto (ruta_archivo, nombre_archivo, encargo_id)
                    VALUES (%s, %s, %s)
                                '''
                self.cursor.execute(sql, tupla)  # ejecuto la consulta
                self.db.commit()  # modifico la base de datos

        except:
            print("ERROR AL GUARDAR FOTO EN LA BASE DE DATOS")
            sys.exit()

    def get_data(self):
        
        sql = '''
            SELECT p.nombre, p.email, p.comentarios, c.path FROM pedidos p
            LEFT JOIN foto c
            ON p.foto = c.id
            '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_pais_o_ciudad(self, valor):
        if valor == 1:
            sql = '''
                        SELECT p.id, p.nombre FROM pais p
                        '''
        elif valor == 2:
            sql = '''
                                    SELECT c.pais, c.nombre, c.id FROM ciudad c
                                    '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_kilos_encargo(self):
        sql ='''
        SELECT k.id, k.valor FROM kilos_encargo k

        '''
        self.cursor.execute(sql)
        return  self.cursor.fetchall()

    def get_espacio_encargo(self):
        sql ='''
        SELECT e.id, e.valor FROM espacio_encargo e

        '''
        self.cursor.execute(sql)
        return  self.cursor.fetchall()

    def get_viajes_conteok(self):
        sql = f'''
                        SELECT kilos_disponible, COUNT(*) AS conteo FROM viaje GROUP BY kilos_disponible 
                        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()
        # v = []
        # for viaje in viajes:
        #     v += [[viaje[0], viaje[1], viaje[2], str(viaje[3]).split()[0], str(viaje[4]).split()[0], viaje[5], viaje[6], viaje[7], viaje[8]]]
        # return v

    def get_encargos_conteok(self):
        sql = f'''
                        SELECT kilos, COUNT(*) AS conteo FROM encargo GROUP BY kilos 
                        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_viajes_conteoe(self):
        sql = f'''
                        SELECT espacio_disponible, COUNT(*) AS conteo FROM viaje GROUP BY espacio_disponible 
                        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_encargos_conteoe(self):
        sql = f'''
                        SELECT espacio, COUNT(*) AS conteo FROM encargo GROUP BY espacio 
                        '''
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_encargos(self):
        sql = f'''
                        SELECT * FROM encargo 
                        '''
        self.cursor.execute(sql)
        viajes = self.cursor.fetchall()
        for viaje in viajes:
            viaje[3] = str(viaje[3]).split()[0]
            viaje[4] = str(viaje[4]).split()[0]
        return viajes



    def get_last5_viajes(self):
        sql = f'''
                Select * FROM viaje ORDER BY id DESC LIMIT 5
                '''
        self.cursor.execute(sql)
        viajes = self.cursor.fetchall()

        paises = self.get_pais_o_ciudad(1)
        ciudades = self.get_pais_o_ciudad(2)
        kilos = self.get_kilos_encargo()
        espacio = self.get_espacio_encargo()

        ret = []
        for viaje in viajes:
            orig = selectCityById(viaje[1], ciudades, paises).split(', ')
            dest = selectCityById(viaje[2], ciudades, paises).split(', ')
            fecha_ida = viaje[3]
            fecha_vuelta = viaje[4]
            kilos_disponible = selectByID(viaje[5], kilos)[1]
            espacio_disponible = selectByID(viaje[6], espacio)[1]
            mail = viaje[7]
            cel = viaje[8]
            ret += [[orig, dest, str(fecha_ida).split()[0], str(fecha_vuelta).split()[0], kilos_disponible, espacio_disponible, mail, cel]]
        return ret

    def get_last5_encargos(self):
        sql = f'''
                Select * FROM encargo ORDER BY id DESC LIMIT 5
                '''
        self.cursor.execute(sql)
        encargos = self.cursor.fetchall()

        paises = self.get_pais_o_ciudad(1)
        ciudades = self.get_pais_o_ciudad(2)
        kilos = self.get_kilos_encargo()
        espacio = self.get_espacio_encargo()

        ret = []
        for encargo in encargos:
            descripcion = encargo[1]
            kilos_disponible = selectByID(encargo[3], kilos)[1]
            espacio_disponible = selectByID(encargo[2], espacio)[1]
            orig = selectCityById(encargo[4], ciudades, paises).split(', ')
            dest = selectCityById(encargo[5], ciudades, paises).split(', ')
            mail = encargo[6]
            cel = encargo[7]
            ret += [[descripcion, espacio_disponible, kilos_disponible, orig, dest,  mail, cel]]
        return ret


    ################### obteniendo las tuplas de cada viaje ############################



def selectByID(id, table):
    for t in table:
        if (id ==t[0]):
            return t
    return None

def selectCityById(id, city, countries):
    for i in city:
        if i[2] == id:
            ciudad = i[1]
            id_pais = i[0]
            break
    for j in countries:
        if j[0] == id_pais:
            return j[1]   + ", "+ ciudad
