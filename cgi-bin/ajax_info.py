#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import cgi
import json
import logging
from db import DB

print('Access-Control-Allow-Origin: *')
print("Content-type:  application/json; charset=UTF-8")
print()
sys.stdout.reconfigure(encoding='utf-8')

db = DB('localhost', 'cc500236_u', 'quISsemper', 'cc500236_db')

form = cgi.FieldStorage()
info = form.getvalue('info')


if info == 'viajes':
    results = db.get_last5_viajes()
    print(json.dumps(results))

if info == 'encargos':
    results = db.get_last5_encargos()
    print(json.dumps(results))

if info == 'lista_viajesk':
    results = db.get_viajes_conteok()
    print(json.dumps(results))

if info == 'lista_viajese':
    results = db.get_viajes_conteoe()
    print(json.dumps(results))

if info == 'lista_encargosk':
    results = db.get_encargos_conteok()
    print(json.dumps(results))

if info == 'lista_encargose':
    results = db.get_encargos_conteoe()
    print(json.dumps(results))

if info == 'kilos':
    results = db.get_kilos_encargo()
    print(json.dumps(results))

if info == 'espacio':
    results = db.get_espacio_encargo()
    print(json.dumps(results))