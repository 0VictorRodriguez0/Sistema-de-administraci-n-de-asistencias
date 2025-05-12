import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import datetime
from datetime import date, time

# Mock de la conexión a la base de datos y cursor
@pytest.fixture
def mock_db():
    with patch('mysql.connector.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_connect, mock_conn, mock_cursor

# Mock para streamlit (ya que muchas funciones usan st.error, st.success)
@pytest.fixture
def mock_st():
    with patch('streamlit.error') as mock_error, \
         patch('streamlit.success') as mock_success:
        yield mock_error, mock_success

def test_get_connection(mock_db):
    mock_connect, _, _ = mock_db
    from app import get_connection
    conn = get_connection()
    mock_connect.assert_called_once_with(
        host="localhost",
        user="root",
        password="",
        database="empleados"
    )
    assert conn is not None

def test_agregar_empleado_exitoso(mock_db, mock_st):
    mock_connect, mock_conn, mock_cursor = mock_db
    mock_error, mock_success = mock_st
    
    from funciones import agregar_empleado
    
    # Configurar el mock para lastrowid
    mock_cursor.lastrowid = 123
    
    # Datos de prueba
    nombre = "Juan"
    apellido = "Pérez"
    correo = "juan@example.com"
    telefono = 1234567890
    puesto = "Desarrollador"
    departamento = "TI"
    rfc = "ABC123456XYZ"
    fecha_nac = date(1990, 1, 1)
    hora_inicio = time(9, 0)
    hora_fin = time(18, 0)
    dias_laborables = "Lunes a Viernes"
    pin = 1234
    
    # Llamar a la función
    agregar_empleado(nombre, apellido, correo, telefono, puesto, departamento, 
                     rfc, fecha_nac, hora_inicio, hora_fin, dias_laborables, pin)
    
    # Verificar que se llamó a execute con los parámetros correctos
    assert mock_cursor.execute.call_count == 3
    
    # Verificar que se llamó a commit
    mock_conn.commit.assert_called_once()
    
    # Verificar que se mostró el mensaje de éxito
    mock_success.assert_called_once_with("Empleado agregado exitosamente con ID: 123 y PIN: 1234")

def test_agregar_empleado_error(mock_db, mock_st):
    mock_connect, mock_conn, mock_cursor = mock_db
    mock_error, mock_success = mock_st
    
    from funciones import agregar_empleado
    
    # Configurar el mock para que falle
    mock_cursor.execute.side_effect = Exception("Error de base de datos")
    
    # Datos de prueba
    nombre = "Juan"
    apellido = "Pérez"
    # ... otros parámetros
    
    # Llamar a la función
    agregar_empleado(nombre, apellido, "correo", 123, "puesto", "depto", 
                     "rfc", date.today(), time(9), time(18), "dias", 1234)
    
    # Verificar que se mostró el mensaje de error
    mock_error.assert_called_once_with("Error al agregar empleado: Error de base de datos")

def test_obtener_empleados(mock_db):
    mock_connect, mock_conn, mock_cursor = mock_db
    
    from funciones import obtener_empleados
    
    # Configurar datos de prueba que devolverá el cursor
    mock_data = [
        (1, "Juan", "Pérez", "juan@example.com", "1234567890", 
         "Desarrollador", "TI", "ABC123456XYZ", date(1990, 1, 1), 
         time(9, 0), time(18, 0), "Lunes a Viernes")
    ]
    mock_cursor.fetchall.return_value = mock_data
    
    # Llamar a la función
    empleados = obtener_empleados()
    
    # Verificar que se ejecutó la consulta correcta
    mock_cursor.execute.assert_called_once_with("""
        SELECT e.id_empleado, e.nombre, e.apellido, e.correo, e.telefono, e.puesto, e.departamento, e.rfc, e.fecha_nac, 
               h.hora_inicio, h.hora_fin, h.dias_laborables 
        FROM empleado e
        JOIN horario h ON e.id_empleado = h.id_empleado
    """)
    
    # Verificar que se devolvieron los datos correctos
    assert empleados == mock_data

def test_eliminar_empleado_exitoso(mock_db, mock_st):
    mock_connect, mock_conn, mock_cursor = mock_db
    mock_error, mock_success = mock_st
    
    from funciones import eliminar_empleado
    
    # Llamar a la función
    eliminar_empleado(123)
    
    # Verificar que se llamó a execute 3 veces (para las 3 tablas)
    assert mock_cursor.execute.call_count == 3
    
    # Verificar que se llamó a commit
    mock_conn.commit.assert_called_once()
    
    # Verificar que se mostró el mensaje de éxito
    mock_success.assert_called_once_with("Empleado  eliminado correctamente.")

def test_actualizar_empleado_exitoso(mock_db, mock_st):
    mock_connect, mock_conn, mock_cursor = mock_db
    mock_error, mock_success = mock_st
    
    from funciones import actualizar_empleado
    
    # Datos de prueba
    id_empleado = 123
    nombre = "Juan"
    apellido = "Pérez"
    # ... otros parámetros
    
    # Llamar a la función
    actualizar_empleado(id_empleado, nombre, apellido, "correo", 123, "puesto", 
                        "depto", "rfc", date.today(), time(9), time(18), "dias")
    
    # Verificar que se llamó a execute 2 veces (empleado y horario)
    assert mock_cursor.execute.call_count == 2
    
    # Verificar que se llamó a commit
    mock_conn.commit.assert_called_once()
    
    # Verificar que se mostró el mensaje de éxito
    mock_success.assert_called_once_with("Datos del empleado y su horario actualizados correctamente.")

def test_verificar_login(mock_db):
    mock_connect, mock_conn, mock_cursor = mock_db
    
    from funciones import verificar_login
    
    # Caso 1: Login exitoso
    mock_cursor.fetchone.return_value = (1,)  # Simula que encontró un registro
    
    result = verificar_login("admin", "password123")
    assert result is True
    
    # Caso 2: Login fallido
    mock_cursor.fetchone.return_value = None  # Simula que no encontró registros
    
    result = verificar_login("admin", "wrongpass")
    assert result is False

@patch('pandas.read_sql')
def test_obtener_totales_asistencia_por_fecha(mock_read_sql, mock_db):
    mock_connect, mock_conn, _ = mock_db
    
    from funciones import obtener_totales_asistencia_por_fecha
    
    # Configurar datos de prueba
    test_df = pd.DataFrame({
        'fecha': ['2023-01-01', '2023-01-02'],
        'total_asistencias': [10, 15]
    })
    mock_read_sql.return_value = test_df
    
    # Llamar a la función
    result = obtener_totales_asistencia_por_fecha()
    
    # Verificar que se llamó a read_sql con la consulta correcta
    expected_query = """
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
    mock_read_sql.assert_called_once_with(expected_query, mock_conn)
    
    # Verificar que se devolvieron los datos correctos
    pd.testing.assert_frame_equal(result, test_df)

def test_puestos():
    from funciones import puestos
    
    # Llamar a la función
    result = puestos()
    
    # Verificar que es un DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Verificar las columnas
    assert set(result.columns) == {'puesto', 'departamento', 'pago_hora'}
    
    # Verificar algunos valores
    assert result.loc[0, 'puesto'] == "Maestro Repostero"
    assert result.loc[0, 'pago_hora'] == 80

@patch('app.obtener_asistencias')
def test_obtener_pago_por_semana(mock_obtener_asistencias):
    from funciones import obtener_pago_por_semana
    
    # Configurar datos de prueba
    test_asistencias = [
        (1, date(2023, 1, 1), time(9), time(17), "Juan", "Pérez", "Vendedor Mostrador", "Ventas"),
        (2, date(2023, 1, 2), time(9), time(17), "Juan", "Pérez", "Vendedor Mostrador", "Ventas"),
    ]
    mock_obtener_asistencias.return_value = test_asistencias
    
    # Llamar a la función
    result = obtener_pago_por_semana()
    
    # Verificar que es un DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Verificar que contiene las columnas esperadas
    expected_columns = ['nombre', 'apellido', 'puesto', 'fecha', 'horas_trabajadas', 
                       'departamento', 'pago_hora', 'ingreso_semana']
    assert all(col in result.columns for col in expected_columns)

@patch('app.obtener_asistencias')
def test_obtener_pago_por_quincena(mock_obtener_asistencias):
    from funciones import obtener_pago_por_quincena
    
    # Configurar datos de prueba
    test_asistencias = [
        (1, date(2023, 1, 1), time(9), time(17), "Juan", "Pérez", "Vendedor Mostrador", "Ventas"),
        (2, date(2023, 1, 16), time(9), time(17), "Juan", "Pérez", "Vendedor Mostrador", "Ventas"),
    ]
    mock_obtener_asistencias.return_value = test_asistencias
    
    # Llamar a la función
    result = obtener_pago_por_quincena()
    
    # Verificar que es un DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Verificar que contiene las columnas esperadas
    expected_columns = ['nombre', 'apellido', 'puesto', 'quincena', 'horas_trabajadas', 
                       'departamento', 'pago_hora', 'ingreso_quincena']
    assert all(col in result.columns for col in expected_columns)

@patch('app.obtener_asistencias')
def test_obtener_pago_por_mes(mock_obtener_asistencias):
    from funciones import obtener_pago_por_mes
    
    # Configurar datos de prueba
    test_asistencias = [
        (1, date(2023, 1, 1), time(9), time(17), "Juan", "Pérez", "Vendedor Mostrador", "Ventas"),
        (2, date(2023, 1, 15), time(9), time(17), "Juan", "Pérez", "Vendedor Mostrador", "Ventas"),
    ]
    mock_obtener_asistencias.return_value = test_asistencias
    
    # Llamar a la función
    result = obtener_pago_por_mes()
    
    # Verificar que es un DataFrame
    assert isinstance(result, pd.DataFrame)
    
    # Verificar que contiene las columnas esperadas
    expected_columns = ['nombre', 'apellido', 'puesto', 'fecha', 'horas_trabajadas', 
                       'departamento', 'pago_hora', 'ingreso_mes']
    assert all(col in result.columns for col in expected_columns)