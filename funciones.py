# contiene funciones solo utilizadas en app.py
from datetime import datetime
import mysql.connector
import streamlit as st
import pandas as pd

# Configurar conexión
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="crud_empleados"
    )

# Funciones CRUD
# Función para agregar empleado y luego su horario
def agregar_empleado(nombre, apellido, correo, telefono, puesto, departamento, rfc, fecha_nac, hora_inicio, hora_fin, dias_laborables,pin):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Formatear valores
        telefono_str = str(telefono)
        fecha_nac_str = fecha_nac.strftime('%Y-%m-%d')
        hora_inicio_str = hora_inicio.strftime('%H:%M:%S')
        hora_fin_str = hora_fin.strftime('%H:%M:%S')

        # Insertar empleado
        cursor.execute("""
            INSERT INTO empleado (nombre, apellido, correo, telefono, puesto, departamento, rfc, fecha_nac)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, correo, telefono_str, puesto, departamento, rfc, fecha_nac_str))

        # Obtener el id del nuevo empleado
        id_empleado = cursor.lastrowid

        # Insertar en la tabla horario
        cursor.execute("""
            INSERT INTO horario (hora_inicio, hora_fin, dias_laborables, id_empleado)
            VALUES (%s, %s, %s, %s)
        """, (hora_inicio_str, hora_fin_str, dias_laborables, id_empleado))

        cursor.execute("""
            INSERT INTO usuario (pin, id_empleado)
            VALUES (%s, %s)
        """, (pin, id_empleado))

        id_usuario = cursor.lastrowid

        conn.commit()
        st.success(f"Empleado agregado exitosamente con ID: {id_usuario} y PIN: {pin}")

    except Exception as e:
        st.error(f"Error al agregar empleado: {e}")

    finally:
        conn.close()

def obtener_empleados():
    conn = get_connection()
    cursor = conn.cursor()
    # Unir las tablas empleado y horario por id_empleado
    cursor.execute("""
        SELECT e.id_empleado, e.nombre, e.apellido, e.correo, e.telefono, e.puesto, e.departamento, e.rfc, e.fecha_nac, 
               h.hora_inicio, h.hora_fin, h.dias_laborables 
        FROM empleado e
        JOIN horario h ON e.id_empleado = h.id_empleado
    """)
    empleados = cursor.fetchall()
    conn.close()
    return empleados



def eliminar_empleado(id_empleado):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Eliminar primero el horario asociado al empleado
        cursor.execute("DELETE FROM horario WHERE id_empleado = %s", (id_empleado,))

        # Eliminar el usuario asociado al empleado
        cursor.execute("DELETE FROM usuario WHERE id_empleado = %s", (id_empleado,))

        # Luego eliminar al empleado
        cursor.execute("DELETE FROM empleado WHERE id_empleado = %s", (id_empleado,))
        
        conn.commit()
        st.success("Empleado  eliminado correctamente.")
    except Exception as e:
        st.error(f"Error al eliminar empleado: {e}")
    finally:
        conn.close()


def actualizar_empleado(id_empleado, nombre, apellido, correo, telefono, puesto, departamento, rfc, fecha_nac, hora_inicio, hora_fin, dias_laborables):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Actualizar los datos del empleado
        cursor.execute("""
            UPDATE empleado 
            SET nombre = %s, apellido = %s, correo = %s, telefono = %s, puesto = %s, departamento = %s, rfc = %s, fecha_nac = %s 
            WHERE id_empleado = %s
        """, (nombre, apellido, correo, telefono, puesto, departamento, rfc, fecha_nac, id_empleado))

        # Actualizar el horario del empleado
        cursor.execute("""
            UPDATE horario
            SET hora_inicio = %s, hora_fin = %s, dias_laborables = %s
            WHERE id_empleado = %s
        """, (hora_inicio, hora_fin, dias_laborables, id_empleado))

        conn.commit()
        st.success("Datos del empleado y su horario actualizados correctamente.")
    except Exception as e:
        st.error(f"Error al actualizar empleado: {e}")
    finally:
        conn.close()



# Función de verificación de login
def verificar_login(usuario, contraseña):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM administrador WHERE usuario = %s AND contraseña = %s", (usuario, contraseña))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# cantidad de asistencias por fecha
def obtener_totales_asistencia_por_fecha():
    conn = get_connection()
    query = """
        SELECT 
            fecha,
            COUNT(*) AS total_asistencias
        FROM 
            asistencia
        GROUP BY 
            fecha
        ORDER BY 
            fecha;
    """
    df = pd.read_sql(query, conn) 
    conn.close()
    return df

# horas promedio trabajadas por fecha
def obtener_promedio_horas_por_fecha():
    conn = get_connection()
    query = """
        SELECT 
            fecha,
            ROUND(AVG(TIMESTAMPDIFF(SECOND, hora_entrada, hora_salida) / 3600), 2) AS horas_promedio
        FROM 
            asistencia
        WHERE 
            hora_entrada IS NOT NULL AND hora_salida IS NOT NULL
        GROUP BY 
            fecha
        ORDER BY 
            fecha;
    """
    df = pd.read_sql(query, conn) 
    conn.close()
    return df

# Obtener lista de meses disponibles con registros en nómina
def obtener_meses_nomina():
    conn = get_connection()
    query = """
        SELECT DISTINCT DATE_FORMAT(fecha, '%Y-%m') AS mes 
        FROM nomina 
        ORDER BY mes DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df["mes"].tolist()

# Obtener pagos totales por empleado en un mes
def obtener_total_pagado_mes(mes):
    conn = get_connection()
    query = """
        SELECT 
            e.id_empleado,
            %s AS mes,
            COALESCE(SUM(n.total_pago), 0) AS total_pagado
        FROM 
            empleado e
        LEFT JOIN 
            nomina n ON e.id_empleado = n.id_empleado 
            AND DATE_FORMAT(n.fecha, '%Y-%m') = %s
        GROUP BY 
            e.id_empleado
        ORDER BY 
            total_pagado DESC;
    """
    df = pd.read_sql(query, conn, params=(mes, mes))
    conn.close()
    return df

# Obtener pagos totales por quincena en un mes
def obtener_total_pagado_quincena(mes, dia_inicio, dia_fin, quincena_nombre):
    conn = get_connection()
    query = f"""
        SELECT 
            e.id_empleado,
            '{quincena_nombre}' AS quincena,
            COALESCE(SUM(n.total_pago), 0) AS total_pagado
        FROM 
            empleado e
        LEFT JOIN 
            nomina n ON e.id_empleado = n.id_empleado
            AND DATE_FORMAT(n.fecha, '%Y-%m') = %s
            AND DAY(n.fecha) BETWEEN %s AND %s
        GROUP BY 
            e.id_empleado
        ORDER BY 
            total_pagado DESC;
    """
    df = pd.read_sql(query, conn, params=(mes, dia_inicio, dia_fin))
    conn.close()
    return df

# Reporte general: asistencia detallada con horas trabajadas
def obtener_reporte_general():
    conn = get_connection()
    query = """
        SELECT 
            e.nombre,
            e.apellido,
            e.correo,
            e.telefono,
            e.puesto,
            e.departamento,
            e.rfc,
            e.fecha_nac,
            a.fecha,
            a.hora_entrada,
            a.hora_salida,
            TIMESTAMPDIFF(MINUTE, a.hora_entrada, a.hora_salida)/60 AS horas_trabajadas
        FROM 
            empleado e
        JOIN 
            asistencia a ON e.id_empleado = a.id_empleado
        ORDER BY 
            a.fecha;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Meses disponibles en asistencia
def obtener_meses_asistencia():
    conn = get_connection()
    query = """
        SELECT DISTINCT DATE_FORMAT(fecha, '%Y-%m') AS mes 
        FROM asistencia 
        ORDER BY mes DESC;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df["mes"].tolist()

# Reporte mensual resumido por empleado
def obtener_reporte_mensual(mes):
    conn = get_connection()
    query = """
        SELECT 
            e.id_empleado,
            CONCAT(e.nombre, ' ', e.apellido) AS nombre_completo,
            COUNT(DISTINCT a.fecha) AS dias_asistidos,
            ROUND(SUM(
                CASE 
                    WHEN a.hora_entrada IS NOT NULL AND a.hora_salida IS NOT NULL 
                    THEN TIMESTAMPDIFF(MINUTE, a.hora_entrada, a.hora_salida) 
                    ELSE 0 
                END
            ) / 60, 2) AS horas_totales,
            ROUND(AVG(
                CASE 
                    WHEN a.hora_entrada IS NOT NULL AND a.hora_salida IS NOT NULL 
                    THEN TIMESTAMPDIFF(MINUTE, a.hora_entrada, a.hora_salida) 
                    ELSE NULL
                END
            ) / 60, 2) AS horas_promedio_dia
        FROM 
            empleado e
        LEFT JOIN 
            asistencia a ON e.id_empleado = a.id_empleado
            AND DATE_FORMAT(a.fecha, '%Y-%m') = %s
        GROUP BY 
            e.id_empleado
        ORDER BY 
            nombre_completo;
    """
    df = pd.read_sql(query, conn, params=(mes,))
    conn.close()
    df.fillna(0, inplace=True)
    return df

def obtener_total_pagado_por_departamento(mes):
    conn = get_connection()
    query = """
        SELECT 
            e.departamento,
            COALESCE(SUM(n.total_pago), 0) AS total_pagado
        FROM 
            empleado e
        LEFT JOIN 
            nomina n ON e.id_empleado = n.id_empleado 
            AND DATE_FORMAT(n.fecha, '%Y-%m') = %s
        GROUP BY 
            e.departamento
        ORDER BY 
            total_pagado DESC;
    """
    df = pd.read_sql(query, conn, params=(mes,))
    conn.close()
    return df

