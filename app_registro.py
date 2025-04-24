import streamlit as st
from datetime import datetime, date
from funciones_registro import existe_usuario, obtener_id_empleado, asistencia_existente, registrar_asistencia, registrar_salida,asistencia_completa

st.set_page_config(page_title="Registro de Asistencia", layout="centered")
st.title("Registro de Asistencia de Empleados")

id_usuario = st.text_input("ID de Usuario")
pin = st.text_input("PIN (4 dígitos)", type="password")

if st.button("Registrar Asistencia"):
    if id_usuario and pin:
        if existe_usuario(id_usuario, pin):
            id_empleado = obtener_id_empleado(id_usuario)
            hoy = date.today()

            if asistencia_completa(id_empleado, hoy):
                st.info("✅ Ya registraste tu entrada y salida del día de hoy.")
            elif asistencia_existente(id_empleado, hoy):
                registrar_salida(id_empleado, hoy)
                st.success("⏺ Hora de salida registrada correctamente.")
            else:
                registrar_asistencia(id_empleado, hoy)
                st.success("🟢 Hora de entrada registrada correctamente.")
        else:
            st.error("ID o PIN incorrectos.")
    else:
        st.warning("Por favor ingresa el ID y el PIN.")
