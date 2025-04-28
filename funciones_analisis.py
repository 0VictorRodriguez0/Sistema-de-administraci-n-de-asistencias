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

def obtener_asistencias():
    conn = get_connection()
    cursor = conn.cursor()
    # Unir las tablas empleado y horario por id_empleado
    # cursor.execute("""
    #     SELECT e.id_empleado, e.nombre, e.apellido, e.correo, e.telefono, e.puesto, e.rfc, e.fecha_nac, 
    #            h.hora_inicio, h.hora_fin, h.dias_laborables 
    #     FROM empleado e
    #     JOIN horario h ON e.id_empleado = h.id_empleado
    # """)
    cursor.execute("""
        SELECT a.id_asistencia, a.fecha, a.hora_entrada, a.hora_salida, e.nombre, e.apellido, e.puesto, e.departamento
        FROM empleado e 
        JOIN  asistencia a ON e.id_empleado = a.id_empleado
    """)
    asistencias = cursor.fetchall()
    conn.close()
    return asistencias
