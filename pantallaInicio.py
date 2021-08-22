from tkinter.font import BOLD
from camara import CamaraEscritorio

import pymysql
import os
import subprocess 
import tkinter as tk
import tkinter.messagebox
import traceback


ventana = tk.Tk()
ventana.title ("Registro de personas")
ventana.geometry ("1800x850+0+0")

tk.Label(ventana, font=30, text = "Registro Vehicular").place(x=60,y=40)
#Datos de personas
user = tk.StringVar(ventana)
tk.Label(ventana, text = "Nombre:").place(x=60,y=100)
caja1 = tk.Entry(ventana, width=100, textvariable=user).place(x=60,y=120)


direccion = tk.StringVar(ventana)
tk.Label(ventana, text = "Direccion").place(x=60,y=180)
caja2 = tk.Entry(ventana, width=100, textvariable=direccion).place(x=60,y=200)


mail = tk.StringVar(ventana)
tk.Label(ventana, text = "Correo:").place(x=60,y=260)
caja3 = tk.Entry(ventana,width=100, textvariable=mail).place(x=60,y=280)


#Registro de carros
descripcion = tk.StringVar(ventana)
tk.Label(ventana,font=25, text = "Datos de auto").place(x=60,y=340)
tk.Label(ventana, text = "Descripcion").place(x=60,y=390)
caja2 = tk.Entry(ventana, width=100, textvariable=descripcion).place(x=60,y=410)

#placas
placa = tk.StringVar(ventana)
tk.Label(ventana, font=25, text = "Datos de placa").place(x=60,y=450)
tk.Label(ventana, text = "Descripcion").place(x=60,y=500)
caja2 = tk.Entry(ventana, width=100, textvariable=placa).place(x=60,y=520)


def check_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute(""" CREATE TABLE IF NOT EXISTS personas (
                                        codigo integer PRIMARY KEY,
                                        nombre text NOT NULL,
                                        direccion text NOT NULL,
                                        descripcion_auto text NOT NULL,
                                        placa text NOT NULL,
                                        correo text
                                    ); """
                       )
      
        conn.commit()  

    except:
        traceback.print_exc()
        return False

    return True


def get_data():
    codigo=0;
    usuario = user.get()
    direc = direccion.get()
    plac = placa.get()
    desc = descripcion.get()
    correo = mail.get()

    valid = True
    if not usuario:
        
        valid = False
    if not direc:
       
        valid = False
    if not plac:
       
        valid = False
    if not desc:
        valid = False
    if not correo:
      
        valid = False

    if valid:
        return codigo,usuario,direc, correo,desc, plac
    return None


def InsertPersona(conn, data):
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO personas (codigo, nombre, direccion, correo,descripcion_auto,placa) VALUES(%s, %s, %s, %s, %s, %s)',(data))
        conn.commit()

    except:
        traceback.print_exc()
        return False
    return True


def login():
    
    try:
        db= pymysql.connect(
            host="localhost", port=3306, user="root",
            passwd="", db="dbdatos"
            )
       
    except:
        traceback.print_exc()
        tk.messagebox.showinfo(title="Configuración incorrecta",
                               message="NO HA SIDO POSIBLE CONECTARSE CON LA BD"
                               )
        return 

    if check_table(db):
        data = get_data()
        if data is not None:
            ins = InsertPersona(db, data)
            if ins:
                tk.messagebox.showinfo(title="Configuración correcta",
                                    message="DATOS ALMACENADOS CORRECTAMENTE"
                                    )
            else:
                tk.messagebox.showinfo(title="Configuración incorrecta",
                                    message="LOS DATOS NO HAN PODIDO SER ALMACENADOS"
                                    )
        else:
            tk.messagebox.showerror(title="Entrada inválida",
                                   message="TODOS LOS CAMPOS SON OBLIGATORIOS"
                                  )
    else:
        tk.messagebox.showerror(title="Configuración incorrecta",
                               message="NO HA SIDO POSIBLE ACCEDER NI CREAR LA TABLA 'usuarios'"
                              )

    db.rollback()
    db.close()

def SubirFotos():
    cmd = 'python subirImagen.py' 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)



def GuardarDatos():
    login()
def DetectorPlacas():
    cmd = 'python ocr_license_plate.py --input license_plates/group1' 
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True) 
    
tk.Button (text = "Guardar", width=40, command = GuardarDatos).place(x=60,y=560)
tk.Button (text = "Selecciona desde tu PC", width=40, command = SubirFotos).place(x=900,y=120)
tk.Button (text = " Camara", width=40, command = DetectorPlacas).place(x=900,y=160)
ventana.mainloop()