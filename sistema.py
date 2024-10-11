#!/usr/bin/env python3

import mysql.connector

# Conectar a la base de datos principal para manejar las sucursales
def obtener_conexion_distribucion():
    return mysql.connector.connect(
        host='localhost',
        database='distribucion_db',
        user='usuario',
        password='contraseña'
    )

# Obtener la configuración de una sucursal por su nombre
def obtener_configuracion_sucursal(nombre_sucursal):
    conn = obtener_conexion_distribucion()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM sucursales WHERE nombre_sucursal = %s"
    cursor.execute(query, (nombre_sucursal,))
    sucursal = cursor.fetchone()

    cursor.close()
    conn.close()

    if sucursal:
        return {
            'host': sucursal['host'],
            'database': nombre_sucursal.lower() + '_db',  # Ejemplo: morelia_db
            'user': sucursal['usuario'],
            'password': sucursal['password']
        }
    else:
        raise ValueError(f"No se encontró la sucursal: {nombre_sucursal}")

# Conectar a la base de datos de la sucursal dinámica
def conectar_db(sucursal):
    config = obtener_configuracion_sucursal(sucursal)
    return mysql.connector.connect(**config)

# Función para agregar una nueva sucursal en la tabla
def agregar_sucursal(nombre_sucursal, host, usuario, password):
    try:
        conn = obtener_conexion_distribucion()
        cursor = conn.cursor()

        query = "INSERT INTO sucursales (nombre_sucursal, host, usuario, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre_sucursal, host, usuario, password))
        conn.commit()
        print(f"Sucursal {nombre_sucursal} agregada correctamente.")

    except mysql.connector.Error as err:
        print(f"Error al agregar sucursal: {err}")
    finally:
        cursor.close()
        conn.close()

# Función de menú con opción para agregar una nueva sucursal
def menu():
    while True:
        print("\nMenú Principal:")
        print("1. Insertar nuevo cliente")
        print("2. Actualizar cliente")
        print("3. Buscar cliente")
        print("4. Listar todos los clientes")
        print("5. Agregar nueva sucursal")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            sucursal = input("Seleccione la sucursal: ")
            # Resto del código para insertar cliente
        elif opcion == '5':
            nombre_sucursal = input("Nombre de la nueva sucursal: ")
            host = input("Host: ")
            usuario = input("Usuario de la base de datos: ")
            password = input("Contraseña: ")

            agregar_sucursal(nombre_sucursal, host, usuario, password)

        elif opcion == '6':
            print("Saliendo del sistema.")
            break
