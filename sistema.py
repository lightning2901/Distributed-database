#!/usr/bin/env python3
import uuid
import mysql.connector
import os 

# IMPORTANTE
# primer push a la rama main, el anterior estable se encuentra en master.
#Si ves algún error Dani, ponmelo por mensaje jsjs


# Configuraciones a la base de datos!!!
# Antes de ejecutar este archivo debe ejecutarse get_data.sh y otorgarle permisos de ejecución para cargar en ~/.bashrc las variables de entorno de mariadb

configuraciones = {
    'Morelia': {
        'host': os.getenv('MORELIA_DB_HOST'),
        'database': os.getenv('MORELIA_DB_NAME'),
        'user': os.getenv('MORELIA_DB_USER'),
        'password': os.getenv('MORELIA_DB_PASSWORD')
    },
    'Pátzcuaro': {
        'host': os.getenv('PATZCUARO_DB_HOST'),
        'database': os.getenv('PATZCUARO_DB_NAME'),
        'user': os.getenv('PATZCUARO_DB_USER'),
        'password': os.getenv('PATZCUARO_DB_PASSWORD')
    }
}





# Función para conectar con la base de datos de una sucursal
def conectar_db(sucursal):
    config = configuraciones.get(sucursal)
    if config:
        return mysql.connector.connect(**config)
    else:
        raise ValueError(f"No se encontró la sucursal: {sucursal}")

# Función para insertar un nuevo cliente y su dirección
def insertar_cliente(sucursal, nombre, apellido_paterno, apellido_materno, rfc, calle, numero, colonia, estado, cp):
    # Generar un UUID único para el cliente
    id_cliente = str(uuid.uuid4())

    # Conectar a la base de datos de la sucursal seleccionada
    conn = conectar_db(sucursal)
    cursor = conn.cursor()

    try:
        # Query para insertar en la tabla cliente
        query_cliente = """
        INSERT INTO cliente (id_cliente, nombre, apellidoPaterno, apellidoMaterno, rfc)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query_cliente, (id_cliente, nombre, apellido_paterno, apellido_materno, rfc))

        # Query para insertar en la tabla direccion
        query_direccion = """
        INSERT INTO direccion (calle, numero, colonia, estado, cp, id_clienteD)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query_direccion, (calle, numero, colonia, estado, cp, id_cliente))

        # Hacer commit para guardar los cambios en la base de datos
        conn.commit()
        print(f"Cliente '{nombre} {apellido_paterno}' insertado exitosamente en la sucursal {sucursal}.")

    except mysql.connector.Error as err:
        # Si hay un error, revertir los cambios
        print(f"Error: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

# Función de prueba
def prueba_insertar_cliente():
    # Datos de ejemplo para insertar un cliente en la sucursal de Morelia
    insertar_cliente(
        'Morelia',
        nombre='Juan',
        apellido_paterno='Pérez',
        apellido_materno='López',
        rfc='JPL930923HDF',
        calle='Calle Falsa',
        numero='123',
        colonia='Centro',
        estado='Michoacán',
        cp='58000'
    )

# Llamar a la función de prueba para insertar un cliente
# No estoy seguro de que funcione, poner a prueba
prueba_insertar_cliente()
