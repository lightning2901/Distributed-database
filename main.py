#!/usr/bin/env python3
'''
import mysql.connector
import os
from configparser import ConfigParser
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env (si está presente)
load_dotenv()

class BaseDatosSucursal:
    def __init__(self, sucursal):
        self.sucursal = sucursal
        self.conexion = None
        self.config = self.cargar_configuracion()

    def cargar_configuracion(self):
        """Carga la configuración de la base de datos desde variables de entorno o config.ini."""
        host = os.getenv(f'{self.sucursal.upper()}_HOST')
        user = os.getenv(f'{self.sucursal.upper()}_USER')
        password = os.getenv(f'{self.sucursal.upper()}_PASSWORD')
        database = os.getenv(f'{self.sucursal.upper()}_DATABASE')

        if not all([host, user, password, database]):
            config = ConfigParser()
            config.read('config.ini')
            if self.sucursal in config:
                host = config[self.sucursal]['host']
                user = config[self.sucursal]['user']
                password = config[self.sucursal]['password']
                database = config[self.sucursal]['database']
            else:
                raise ValueError(f"No se encontró configuración para {self.sucursal} en config.ini ni en variables de entorno.")

        return {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }

    def conectar(self):
        """Conecta a la base de datos de la sucursal especificada."""
        try:
            self.conexion = mysql.connector.connect(**self.config)
            print(f"Conexión a {self.sucursal} exitosa.")
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos."""
        if self.conexion:
            self.conexion.close()

    def insertar_cliente(self, nombre, apellido_paterno, apellido_materno, rfc):
        """Inserta un nuevo cliente en la base de datos."""
        cursor = self.conexion.cursor()
        query = "INSERT INTO Clientes (Nombre, ApellidoPaterno, ApellidoMaterno, RFC) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, apellido_paterno, apellido_materno, rfc))
        self.conexion.commit()
        cursor.close()
        print("Cliente insertado correctamente.")

    def insertar_direccion(self, calle, numero, colonia, estado, cp, id_cliente):
        """Inserta una nueva dirección para un cliente en la base de datos."""
        cursor = self.conexion.cursor()
        query = "INSERT INTO Direcciones (Calle, Numero, Colonia, Estado, CP, idCliente) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (calle, numero, colonia, estado, cp, id_cliente))
        self.conexion.commit()
        cursor.close()
        print("Dirección insertada correctamente.")

    def actualizar_cliente(self, cliente_id, **datos_actualizados):
        """Actualiza los datos de un cliente."""
        cursor = self.conexion.cursor()
        updates = ", ".join(f"{columna} = %s" for columna in datos_actualizados.keys())
        query = f"UPDATE Clientes SET {updates} WHERE Id = %s"
        values = list(datos_actualizados.values()) + [cliente_id]
        cursor.execute(query, values)
        self.conexion.commit()
        cursor.close()
        print("Cliente actualizado correctamente.")

    def buscar_cliente(self, criterio, valor):
        """Busca clientes según el criterio especificado (nombre, RFC o domicilio)."""
        cursor = self.conexion.cursor(dictionary=True)
        query = f"SELECT * FROM Clientes WHERE {criterio} LIKE %s"
        cursor.execute(query, (f"%{valor}%",))
        resultados = cursor.fetchall()
        cursor.close()
        return resultados

    def listar_clientes(self):
        """Lista todos los clientes en la base de datos."""
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Clientes")
        clientes = cursor.fetchall()
        cursor.close()
        return clientes

    def crear_tablas(self):
        """Crea tablas adicionales con fragmentación horizontal."""
        cursor = self.conexion.cursor()
        # Ejemplo de fragmentación horizontal: crea una nueva tabla para un rango específico de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clientes_Extra (
                Id INT PRIMARY KEY AUTO_INCREMENT,
                Nombre VARCHAR(255),
                ApellidoPaterno VARCHAR(255),
                ApellidoMaterno VARCHAR(255),
                RFC VARCHAR(13) UNIQUE
            )
        """)
        self.conexion.commit()
        cursor.close()
        print("Tablas distribuidas creadas correctamente.")

    def agregar_nodo(self, host, user, password, database):
        """Permite agregar un nuevo nodo al sistema distribuido."""
        # Aquí se definiría la lógica para registrar un nuevo nodo en la base de datos distribuida
        print(f"Nodo agregado: {host}")

# Ejemplo de uso
if __name__ == "__main__":
    sucursal_bd = BaseDatosSucursal('sucursal_1')
    sucursal_bd.conectar()

    # Inserciones de ejemplo
    sucursal_bd.insertar_cliente("Juan", "Pérez", "Gómez", "JPG123456789")
    sucursal_bd.insertar_direccion("Calle 123", "456", "Colonia Centro", "Estado", "12345", 1)

    # Buscar y listar clientes
    print(sucursal_bd.buscar_cliente("Nombre", "Juan"))
    print(sucursal_bd.listar_clientes())

    # Crear tablas adicionales y agregar un nodo
    sucursal_bd.crear_tablas()
    sucursal_bd.agregar_nodo("IP_nodo", "user_nodo", "pass_nodo", "database_nodo")

    # Cerrar conexión
    sucursal_bd.cerrar_conexion()

'''
import mysql.connector
import configparser
import threading

# Cargar la configuración desde el archivo config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# Función para conectar a la base de datos usando la configuración de config.ini
def conectar_bd(sucursal):
    sucursal_mapping = {
        '1': 'sucursal_1',
        '2': 'sucursal_2'
    }

    sucursal_seleccionada = sucursal_mapping.get(sucursal)
    
    if not sucursal_seleccionada:
        print("Sucursal no válida.")
        return None

    try:
        conexion = mysql.connector.connect(
            host=config[sucursal_seleccionada]['host'],
            user=config[sucursal_seleccionada]['user'],
            password=config[sucursal_seleccionada]['password'],
            database=config[sucursal_seleccionada]['database']
        )
        return conexion
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

# Función para buscar en la tabla Clientes
def buscar_en_clientes(sucursal, busqueda):
    conexion = conectar_bd(sucursal)
    if conexion:
        cursor = conexion.cursor()
        query_cliente = "SELECT * FROM Clientes WHERE Nombre LIKE %s OR RFC LIKE %s"
        cursor.execute(query_cliente, ('%' + busqueda + '%', '%' + busqueda + '%'))
        resultados_clientes = cursor.fetchall()
        cursor.close()
        return resultados_clientes
    return []

# Función para buscar en la tabla Direcciones
def buscar_en_direcciones(sucursal, busqueda):
    conexion = conectar_bd(sucursal)
    if conexion:
        cursor = conexion.cursor()
        query_direccion = "SELECT * FROM Direcciones WHERE CONCAT(Calle, ' ', Numero, ' ', Colonia, ' ', Estado, ' ', CP) LIKE %s"
        cursor.execute(query_direccion, ('%' + busqueda + '%',))
        resultados_direcciones = cursor.fetchall()
        cursor.close()
        return resultados_direcciones
    return []

# Función para mostrar los resultados combinados de la búsqueda
def mostrar_resultados(sucursal, clientes, direcciones):
    if clientes or direcciones:
        print(f"\nResultados en Sucursal {sucursal}:")
    if clientes:
        for cliente in clientes:
            print(f"Sucursal {sucursal} - ID: {cliente[0]}, Nombre: {cliente[1]}, ApellidoPaterno: {cliente[2]}, ApellidoMaterno: {cliente[3]}, RFC: {cliente[4]}")
    if direcciones:
        for direccion in direcciones:
            print(f"Sucursal {sucursal} - Calle: {direccion[1]}, Número: {direccion[2]}, Colonia: {direccion[3]}, Estado: {direccion[4]}, CP: {direccion[5]}")
    if not clientes and not direcciones:
        print(f"Sucursal {sucursal} - No se encontraron resultados.")

# Función para ejecutar la búsqueda en paralelo
def buscar_cliente():
    busqueda = input("Ingrese el nombre, RFC o domicilio para buscar: ")

    # Crear hilos para buscar en ambas sucursales
    resultados_sucursal_1_clientes = []
    resultados_sucursal_1_direcciones = []
    resultados_sucursal_2_clientes = []
    resultados_sucursal_2_direcciones = []

    # Hilos para buscar en Sucursal 1
    def buscar_sucursal_1():
        resultados_sucursal_1_clientes.extend(buscar_en_clientes('1', busqueda))
        resultados_sucursal_1_direcciones.extend(buscar_en_direcciones('1', busqueda))

    # Hilos para buscar en Sucursal 2
    def buscar_sucursal_2():
        resultados_sucursal_2_clientes.extend(buscar_en_clientes('2', busqueda))
        resultados_sucursal_2_direcciones.extend(buscar_en_direcciones('2', busqueda))

    # Iniciar los hilos
    hilo_sucursal_1 = threading.Thread(target=buscar_sucursal_1)
    hilo_sucursal_2 = threading.Thread(target=buscar_sucursal_2)

    hilo_sucursal_1.start()
    hilo_sucursal_2.start()

    # Esperar a que terminen los hilos
    hilo_sucursal_1.join()
    hilo_sucursal_2.join()

    # Mostrar los resultados de la búsqueda
    mostrar_resultados('1', resultados_sucursal_1_clientes, resultados_sucursal_1_direcciones)
    mostrar_resultados('2', resultados_sucursal_2_clientes, resultados_sucursal_2_direcciones)

# Función para insertar cliente solo en la Sucursal Local (Sucursal 1)
def insertar_cliente(sucursal, nombre, apellido_paterno, apellido_materno, rfc, calle, numero, colonia, estado, cp):
    # Aseguramos que la inserción es solo en la sucursal local (Sucursal 1)
    if sucursal != '1':
        print("Solo se pueden insertar clientes en la Sucursal 1 (local).")
        return

    conexion = conectar_bd(sucursal)
    if conexion:
        cursor = conexion.cursor()

        # Insertar cliente
        query_cliente = "INSERT INTO Clientes (Nombre, ApellidoPaterno, ApellidoMaterno, RFC) VALUES (%s, %s, %s, %s)"
        cursor.execute(query_cliente, (nombre, apellido_paterno, apellido_materno, rfc))
        conexion.commit()

        # Obtener el ID del cliente insertado
        id_cliente = cursor.lastrowid

        # Insertar dirección
        query_direccion = "INSERT INTO Direcciones (Calle, Numero, Colonia, Estado, CP, idCliente) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query_direccion, (calle, numero, colonia, estado, cp, id_cliente))
        conexion.commit()

        print(f"Sucursal {sucursal} - Cliente y dirección insertados con éxito.")
        cursor.close()
        conexion.close()

# Función para actualizar cliente y dirección distribuido
def actualizar_cliente_distribuido():
    try:
        # Solicitar datos del cliente a actualizar
        id_cliente = int(input("Ingrese el ID del cliente que desea actualizar: "))
        nombre = input("Nuevo nombre del cliente: ")
        apellido_paterno = input("Nuevo apellido paterno: ")
        apellido_materno = input("Nuevo apellido materno: ")
        rfc = input("Nuevo RFC: ")
        calle = input("Nueva calle: ")
        numero = input("Nuevo número: ")
        colonia = input("Nueva colonia: ")
        estado = input("Nuevo estado: ")
        cp = input("Nuevo código postal: ")

        # Conectar a la Sucursal 1
        conexion_1 = conectar_bd('1')
        if conexion_1:
            cursor = conexion_1.cursor()

            # Actualizar cliente en Sucursal 1
            query_cliente_1 = "UPDATE Clientes SET Nombre = %s, ApellidoPaterno = %s, ApellidoMaterno = %s, RFC = %s WHERE Id = %s"
            cursor.execute(query_cliente_1, (nombre, apellido_paterno, apellido_materno, rfc, id_cliente))
            conexion_1.commit()

            # Actualizar dirección en Sucursal 1
            query_direccion_1 = "UPDATE Direcciones SET Calle = %s, Numero = %s, Colonia = %s, Estado = %s, CP = %s WHERE idCliente = %s"
            cursor.execute(query_direccion_1, (calle, numero, colonia, estado, cp, id_cliente))
            conexion_1.commit()

            cursor.close()
            conexion_1.close()

        # Conectar a la Sucursal 2
        conexion_2 = conectar_bd('2')
        if conexion_2:
            cursor = conexion_2.cursor()

            # Actualizar cliente en Sucursal 2
            query_cliente_2 = "UPDATE Clientes SET Nombre = %s, ApellidoPaterno = %s, ApellidoMaterno = %s, RFC = %s WHERE Id = %s"
            cursor.execute(query_cliente_2, (nombre, apellido_paterno, apellido_materno, rfc, id_cliente))
            conexion_2.commit()

            # Actualizar dirección en Sucursal 2
            query_direccion_2 = "UPDATE Direcciones SET Calle = %s, Numero = %s, Colonia = %s, Estado = %s, CP = %s WHERE idCliente = %s"
            cursor.execute(query_direccion_2, (calle, numero, colonia, estado, cp, id_cliente))
            conexion_2.commit()

            cursor.close()
            conexion_2.close()

        print(f"Cliente con ID {id_cliente} actualizado correctamente en Sucursal 1 y Sucursal 2.")
    except ValueError:
        print("Error: El ID debe ser un número.")

# Función para agregar nuevos nodos al sistema
def agregar_nuevo_nodo(sucursal, host, user, password, database):
    if sucursal not in ['1', '2']:
        print("Sucursal no válida. Solo se pueden agregar nodos a Sucursal 1 o Sucursal 2.")
        return

    config[sucursal]['host'] = host
    config[sucursal]['user'] = user
    config[sucursal]['password'] = password
    config[sucursal]['database'] = database

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

    print(f"Nuevo nodo agregado para la {sucursal}.")

# Función de menú
def mostrar_menu():
    print("\n--- Menú de Opciones ---")
    print("1. Insertar Cliente")
    print("2. Buscar Cliente")
    print("3. Agregar Nuevo Nodo")
    print("4. Actualizar Cliente y Dirección Distribuidos")
    print("5. Salir")

def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre del cliente: ")
            apellido_paterno = input("Apellido paterno: ")
            apellido_materno = input("Apellido materno: ")
            rfc = input("RFC: ")
            calle = input("Calle: ")
            numero = input("Número: ")
            colonia = input("Colonia: ")
            estado = input("Estado: ")
            cp = input("Código Postal: ")

            # Insertar cliente solo en la Sucursal 1 (local)
            insertar_cliente('1', nombre, apellido_paterno, apellido_materno, rfc, calle, numero, colonia, estado, cp)

        elif opcion == "2":
            # Buscar Cliente
            buscar_cliente()

        elif opcion == "3":
            # Agregar un nuevo nodo
            sucursal = input("Ingrese la sucursal (1 o 2): ")
            host = input("Host del nuevo nodo: ")
            user = input("Usuario del nuevo nodo: ")
            password = input("Contraseña del nuevo nodo: ")
            database = input("Base de datos del nuevo nodo: ")

            agregar_nuevo_nodo(sucursal, host, user, password, database)

        elif opcion == "4":
            # Actualizar Cliente y Dirección Distribuidos
            actualizar_cliente_distribuido()

        elif opcion == "5":
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()
