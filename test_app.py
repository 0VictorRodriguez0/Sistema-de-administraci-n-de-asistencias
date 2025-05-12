# File: test_app.py
import pytest
from unittest.mock import patch, MagicMock
from datetime import date, time, datetime
import pandas as pd
from streamlit.testing.v1 import AppTest

# Mock de datos para pruebas
MOCK_EMPLEADOS = [
    (1, "Juan", "Perez", "juan@test.com", "1234567890", "Developer", "IT",
     "RFC123", date(1990, 1, 1), time(9, 0), time(17, 0), 5, 1234)
]

MOCK_ASISTENCIAS = pd.DataFrame({
    "fecha": [date(2023, 1, 1), date(2023, 1, 2)],
    "total_asistencias": [10, 15]
})

MOCK_SALARIOS = pd.DataFrame({
    "fecha": [date(2023, 1, 1), date(2023, 2, 1)],
    "ingreso_mes": [50000, 55000],
    "nombre": ["Juan", "Maria"],
    "departamento": ["IT", "HR"]
})

# Fixture para la aplicación
@pytest.fixture
def app():
    return AppTest.from_file("app.py")

# Pruebas de Login
def test_login_exitoso(app):
    """Prueba el flujo de login exitoso"""
    with patch("funciones.verificar_login", return_value=True):
        app.run() # Run first to render login widgets
        app.text_input("Usuario").input("admin")
        app.text_input("Contraseña", type="password").input("admin")
        app.button("Iniciar sesión").click()
        app.run() # Run again to process interactions

        assert app.session_state["logged_in"] is True
        assert "Login exitoso" in app.success[0].value

def test_login_fallido(app):
    """Prueba el flujo de login fallido"""
    with patch("funciones.verificar_login", return_value=False):
        app.run() # Run first to render login widgets
        app.text_input("Usuario").input("wrong")
        app.text_input("Contraseña", type="password").input("wrong")
        app.button("Iniciar sesión").click()
        app.run() # Run again to process interactions

        assert app.session_state.get("logged_in", False) is False
        assert "incorrectos" in app.error[0].value.lower()

# Pruebas de Gestión de Empleados
def test_agregar_empleado(app):
    """Prueba el flujo completo de agregar empleado"""
    with patch("funciones.agregar_empleado", return_value=True), \
         patch("random.randint", return_value=1234):

        # Simular login
        app.session_state["logged_in"] = True
        app.run() # Render the main app with sidebar

        # Navegar a la sección (use app.sidebar.radio)
        app.sidebar.radio("### ☰ Menú de navegación").set_value("👷Agregar Empleado")
        app.run() # Process menu selection and render "Agregar Empleado" section

        # Llenar formulario
        app.text_input("Nombre").input("Juan")
        app.text_input("Apellido").input("Perez")
        app.text_input("Correo").input("juan@test.com")
        app.number_input("Número telefónico", format="%d", step=1).input(1234567890)
        app.text_input("Puesto").input("Developer")
        app.text_input("departamento").input("IT")
        app.text_input("RFC").input("RFC123")
        app.date_input("Fecha de Nacimiento").set_value(date(1990, 1, 1))
        app.time_input("Hora de Inicio").set_value(time(9, 0))
        app.time_input("Hora de Fin").set_value(time(17, 0))
        app.number_input("Días Laborables").set_value(5)

        # Enviar formulario
        app.button("Guardar").click()
        app.run() # Process form submission

        # Verificaciones
        assert "agregado con éxito" in app.success[0].value.lower()

def test_lista_empleados(app):
    """Prueba la visualización y búsqueda de empleados"""
    with patch("funciones.obtener_empleados", return_value=MOCK_EMPLEADOS):
        # Simular login
        app.session_state["logged_in"] = True
        app.run() # Render the main app with sidebar

        # Navegar a la sección (use app.sidebar.radio)
        app.sidebar.radio("### ☰ Menú de navegación").set_value("🧑‍🏭Ver Empleados")
        app.run() # Process menu selection and render "Ver Empleados" section

        # Verify that employees are displayed (expander labels are dynamic)
        # Need to run again after rendering the list
        app.run() # Run again to ensure expanders are rendered
        assert app.expander[0].label == "Juan Perez" # Check the label directly

        # Test search
        app.text_input("Buscar por nombre o apellido").input("Juan")
        app.run() # Process search input and re-render list
        assert len(app.expander) == 1  # Should show only 1 result
        assert app.expander[0].label == "Juan Perez" # Ensure the correct one is shown

# Pruebas de Dashboards
def test_dashboard_asistencia(app):
    """Prueba el dashboard de asistencia"""
    with patch("funciones.obtener_totales_asistencia_por_fecha", return_value=MOCK_ASISTENCIAS), \
         patch("funciones.obtener_promedio_horas_por_fecha", return_value=pd.DataFrame()):

        # Simular login
        app.session_state["logged_in"] = True
        app.run() # Render the main app with sidebar

        # Navegar a la sección (use app.sidebar.radio)
        app.sidebar.radio("### ☰ Menú de navegación").set_value("🕒Dashboard Asistencia")
        app.run() # Process menu selection and render dashboard

        # Verificar que se muestran los gráficos
        assert len(app.plotly_chart) >= 1

def test_dashboard_salarios(app):
    """Prueba el dashboard de salarios"""
    with patch("funciones.obtener_pago_por_mes", return_value=MOCK_SALARIOS):
        # Simular login
        app.session_state["logged_in"] = True
        app.run() # Render the main app with sidebar

        # Navegar a la sección (use app.sidebar.radio)
        app.sidebar.radio("### ☰ Menú de navegación").set_value("🧾Dashboard Salarios")
        app.run() # Process menu selection and render dashboard

        # Verificar que se muestran los gráficos
        assert len(app.plotly_chart) >= 2

# Pruebas de Reportes
def test_reporte_general(app):
    """Prueba la generación de reportes"""
    with patch("funciones.obtener_reporte_general", return_value=pd.DataFrame({
            "nombre": ["Juan"], "asistencias": [20], "horas_trabajadas": [160]
        })):

        # Simular login
        app.session_state["logged_in"] = True
        app.run() # Render the main app with sidebar

        # Navegar a la sección (use app.sidebar.radio)
        app.sidebar.radio("### ☰ Menú de navegación").set_value("🔔Reporte")
        app.run() # Process menu selection and render report section

        # Verificar que se muestra el reporte
        assert len(app.dataframe) >= 1
        assert "Descargar Reporte CSV" in app.button[0].label

# Prueba de Cierre de Sesión
def test_logout(app):
    """Prueba el cierre de sesión"""
    # Simular login first
    app.session_state["logged_in"] = True
    app.run() # Render the main app with sidebar

    # Hacer logout (use app.sidebar.button)
    app.sidebar.button("Cerrar sesión").click()
    app.run() # Process logout click

    # Verificaciones
    assert app.session_state["logged_in"] is False
    assert "cerrado sesión" in app.success[0].value.lower()
