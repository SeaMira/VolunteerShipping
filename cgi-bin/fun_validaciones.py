#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
from datetime import datetime


def valida_tel(telefono ):
    if (len(telefono) == 0 ):
        return True
    patron = "^\\+?\d{7,15}$"
    return re.match(patron, telefono)


def valida_mail(email):
    emailRegex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    return re.fullmatch(emailRegex, email)


def valida_fecha(fecha):
    if (len(fecha) > 10):
        return False
    regexfecha = re.compile(r'\d{4}-\d{2}-\d{2}')
    return re.match(regexfecha, fecha)

def valida_diff_fechas(fecha_ida, fecha_vuelta):
    if (not valida_fecha(fecha_ida) or not valida_fecha(fecha_vuelta)):
        return False

    # convert string to date object
    d1 = datetime.strptime(fecha_ida, "%Y-%m-%d")
    d2 = datetime.strptime(fecha_vuelta, "%Y-%m-%d")

    # difference between dates in timedelta
    delta = d2 - d1
    return delta.days >= 1

def valida_pais(pais):
    return (pais != -1)

def valida_ciudad(ciudad):
    return ciudad != -1

def valida_img(archivo, file_size, supported_types):
    if archivo.filename:
        tipo = archivo.type
        size = os.fstat(archivo.file.fileno()).st_size
        if tipo not in supported_types:
            return False
        if size > file_size:
            return False
        return True
    else:
        return False