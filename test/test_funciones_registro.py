import pytest
from unittest.mock import MagicMock, patch, call
from datetime import datetime, date
import mysql.connector
from funciones_registro import *

# Fixture para mock de conexión
@pytest.fixture
def mock_db():
    with patch('funciones_registro.get_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        yield mock_get_conn, mock_conn, mock_cursor

# Pruebas para get_connection()
def test_get_connection():
    with patch('mysql.connector.connect') as mock_connect:
        mock_connect.return_value = "mock_connection"
        
        result = get_connection()
        
        mock_connect.assert_called_once_with(
            host="localhost",
            user="root",
            password="",
            database="empleados"
        )
        assert result == "mock_connection"

# Pruebas para existe_usuario()
def test_existe_usuario_true(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (1,)  # Usuario existe
    
    assert existe_usuario("user1", "1234") is True
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM usuario WHERE id_usuario = %s AND pin = %s", 
        ("user1", "1234")
    )
    mock_conn.close.assert_called_once()

def test_existe_usuario_false(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None  # Usuario no existe
    
    assert existe_usuario("user1", "wrong") is False

# Pruebas para obtener_id_empleado()
def test_obtener_id_empleado_existe(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (101,)
    
    assert obtener_id_empleado("user1") == 101
    mock_cursor.execute.assert_called_once_with(
        "SELECT id_empleado FROM usuario WHERE id_usuario = %s", 
        ("user1",)
    )

def test_obtener_id_empleado_no_existe(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None
    
    assert obtener_id_empleado("inexistente") is None

# Pruebas para asistencia_existente()
def test_asistencia_existente_true(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (1,)
    test_date = date(2023, 1, 1)
    
    assert asistencia_existente(101, test_date) is True
    
    # Verificar la llamada a execute con los parámetros correctos
    expected_query = """
        SELECT * FROM asistencia 
        WHERE id_empleado = %s AND fecha = %s AND hora_entrada IS NOT NULL
    """
    mock_cursor.execute.assert_called_once()
    actual_args, actual_kwargs = mock_cursor.execute.call_args
    assert actual_args[0].strip() == expected_query.strip()
    assert actual_args[1] == (101, test_date)

def test_asistencia_existente_false(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None
    
    assert asistencia_existente(101, date(2023, 1, 1)) is False

# Pruebas para registrar_asistencia()
@patch('funciones_registro.datetime')
def test_registrar_asistencia(mock_datetime, mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    test_time = datetime.strptime("08:30:00", "%H:%M:%S").time()
    mock_datetime.now.return_value.time.return_value = test_time
    test_date = date(2023, 1, 1)
    
    registrar_asistencia(101, test_date)
    
    # Verificar la llamada a execute
    expected_query = """
        INSERT INTO asistencia (fecha, hora_entrada, hora_salida, id_empleado)
        VALUES (%s, %s, NULL, %s)
    """
    mock_cursor.execute.assert_called_once()
    actual_args, actual_kwargs = mock_cursor.execute.call_args
    assert actual_args[0].strip() == expected_query.strip()
    assert actual_args[1] == (test_date, test_time, 101)
    mock_conn.commit.assert_called_once()

# Pruebas para registrar_salida()
@patch('funciones_registro.datetime')
def test_registrar_salida(mock_datetime, mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    test_time = datetime.strptime("17:45:00", "%H:%M:%S").time()
    mock_datetime.now.return_value.time.return_value = test_time
    test_date = date(2023, 1, 1)
    
    registrar_salida(101, test_date)
    
    # Verificar la llamada a execute
    expected_query = """
        UPDATE asistencia 
        SET hora_salida = %s 
        WHERE id_empleado = %s AND fecha = %s AND hora_salida IS NULL
    """
    mock_cursor.execute.assert_called_once()
    actual_args, actual_kwargs = mock_cursor.execute.call_args
    assert actual_args[0].strip() == expected_query.strip()
    assert actual_args[1] == (test_time, 101, test_date)
    mock_conn.commit.assert_called_once()

# Pruebas para asistencia_completa()
def test_asistencia_completa_true(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = (1,)
    test_date = date(2023, 1, 1)
    
    assert asistencia_completa(101, test_date) is True
    
    # Verificar la llamada a execute
    expected_query = """
        SELECT * FROM asistencia 
        WHERE id_empleado = %s AND fecha = %s 
        AND hora_entrada IS NOT NULL AND hora_salida IS NOT NULL
    """
    mock_cursor.execute.assert_called_once()
    actual_args, actual_kwargs = mock_cursor.execute.call_args
    assert actual_args[0].strip() == expected_query.strip()
    assert actual_args[1] == (101, test_date)

def test_asistencia_completa_false(mock_db):
    mock_get_conn, mock_conn, mock_cursor = mock_db
    mock_cursor.fetchone.return_value = None
    
    assert asistencia_completa(101, date(2023, 1, 1)) is False

# Prueba de integración básica
@patch('funciones_registro.get_connection')
def test_flujo_completo(mock_get_conn):
    # Configurar mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_conn.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    # Configurar respuestas para cada llamada
    mock_cursor.fetchone.side_effect = [
        (1,),                   # existe_usuario
        (101,),                 # obtener_id_empleado
        None,                   # asistencia_existente (antes de registrar)
        (1,),                   # asistencia_existente (después de registrar)
        None,                   # asistencia_completa (antes de registrar salida)
        (1,)                    # asistencia_completa (después de registrar salida)
    ]
    
    # Mock para datetime
    with patch('funciones_registro.datetime') as mock_datetime:
        mock_datetime.now.return_value.time.side_effect = [
            datetime.strptime("09:00:00", "%H:%M:%S").time(),  # hora_entrada
            datetime.strptime("18:00:00", "%H:%M:%S").time()   # hora_salida
        ]
        
        # Ejecutar flujo completo
        test_date = date(2023, 1, 1)
        
        # 1. Verificar usuario
        assert existe_usuario("emp1", "1234") is True
        
        # 2. Obtener ID empleado
        id_emp = obtener_id_empleado("emp1")
        assert id_emp == 101
        
        # 3. Verificar si ya tiene asistencia
        assert asistencia_existente(id_emp, test_date) is False
        
        # 4. Registrar entrada
        registrar_asistencia(id_emp, test_date)
        
        # 5. Verificar asistencia después de registrar entrada
        assert asistencia_existente(id_emp, test_date) is True
        
        # 6. Verificar si ya tiene asistencia completa (debería ser False)
        assert asistencia_completa(id_emp, test_date) is False
        
        # 7. Registrar salida
        registrar_salida(id_emp, test_date)
        
        # 8. Verificar asistencia completa
        assert asistencia_completa(id_emp, test_date) is True
    
    # Verificar que se cerró la conexión en cada llamada
    assert mock_conn.close.call_count == 8  # 8 llamadas que usan conexión