# contiene funciones solo utilizadas en app_registro.py
import mysql.connector
from datetime import datetime

# Conexión
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="empleados"
    )

# Verifica si usuario existe
def existe_usuario(id_usuario, pin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE id_usuario = %s AND pin = %s", (id_usuario, pin))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Obtener id_empleado a partir del id_usuario
def obtener_id_empleado(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_empleado FROM usuario WHERE id_usuario = %s", (id_usuario,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# Verifica si ya tiene una asistencia hoy con hora_entrada
def asistencia_existente(id_empleado, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM asistencia 
        WHERE id_empleado = %s AND fecha = %s AND hora_entrada IS NOT NULL
    """, (id_empleado, fecha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# Registrar hora_entrada (nueva asistencia)
def registrar_asistencia(id_empleado, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    hora_actual = datetime.now().time()
    cursor.execute("""
        INSERT INTO asistencia (fecha, hora_entrada, hora_salida, id_empleado)
        VALUES (%s, %s, NULL, %s)
    """, (fecha, hora_actual, id_empleado))
    conn.commit()
    conn.close()

# Registrar hora_salida si ya había entrada
def registrar_salida(id_empleado, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    hora_actual = datetime.now().time()
    cursor.execute("""
        UPDATE asistencia 
        SET hora_salida = %s 
        WHERE id_empleado = %s AND fecha = %s AND hora_salida IS NULL
    """, (hora_actual, id_empleado, fecha))
    conn.commit()
    conn.close()

# Verifica si ya registró entrada y salida hoy
def asistencia_completa(id_empleado, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM asistencia 
        WHERE id_empleado = %s AND fecha = %s 
        AND hora_entrada IS NOT NULL AND hora_salida IS NOT NULL
    """, (id_empleado, fecha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

