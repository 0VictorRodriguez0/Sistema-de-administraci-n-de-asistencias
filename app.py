import streamlit as st
import unicodedata
import datetime
import random
import pandas as pd
import plotly.express as px
from funciones import agregar_empleado, obtener_empleados, eliminar_empleado, actualizar_empleado, verificar_login, get_connection

# Streamlit
st.set_page_config(page_title="CRUD Empleados", layout="centered")
st.title("Sistema de Gestión de Empleados")

# Verificar si el usuario está logueado
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Panel de login
if not st.session_state["logged_in"]:
    st.subheader("Iniciar Sesión")
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Iniciar sesión"):
        if usuario and contraseña:
            if verificar_login(usuario, contraseña):
                st.session_state["logged_in"] = True
                st.success("Login exitoso.")
                st.rerun()
                # No se utiliza st.experimental_rerun(), se mantiene la página actual
            else:
                st.error("Usuario o contraseña incorrectos.")
        else:
            st.warning("Por favor ingresa usuario y contraseña.")
else:
    # Si el usuario está logueado, muestra el menú de operaciones
    menu = st.sidebar.radio("Menú", ["Agregar Empleado", "Ver Empleados", "Dashboard Asistencia", "Dashboard Salarios", "Reporte"])

    # Cerrar sesión en la sidebar
    if st.sidebar.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.success("Has cerrado sesión correctamente.")
        st.rerun()
        # No es necesario recargar la página, el flujo se actualiza correctamente sin eso

    # Agregar empleado
    if menu == "Agregar Empleado":
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre")
        with col2:
            apellido = st.text_input("Apellido")

        col3, col4 = st.columns(2)
        with col3:
            correo = st.text_input("Correo")
        with col4:
            telefono = st.number_input("Número telefónico", format="%d", step=1)

        col5, col6 = st.columns(2)
        with col5:
            puesto = st.text_input("Puesto")
        with col6:
            departamento = st.text_input("departamento")

        col7, col8 = st.columns(2)
        with col7:
            rfc = st.text_input("RFC")
        with col8:
            fecha_nac = st.date_input("Fecha de Nacimiento",min_value=datetime.date(1950, 1, 1),max_value=datetime.date.today())

        st.markdown("---")  # Línea divisoria opcional

        col9, col10 = st.columns(2)
        with col9:
            hora_inicio = st.time_input("Hora de Inicio")
        with col10:
            hora_fin = st.time_input("Hora de Fin")

        dias_laborables = st.number_input("Días Laborables", min_value=1, max_value=7, value=5)

        pin = random.randint(1000, 9999)
        if st.button("Guardar"):
            if nombre and apellido and correo and telefono and puesto and departamento and rfc and fecha_nac and hora_inicio and hora_fin and dias_laborables:
                agregar_empleado(nombre, apellido, correo,telefono,puesto,departamento,rfc,fecha_nac,hora_inicio,hora_fin,dias_laborables,pin)
                st.success("Empleado agregado con éxito.")
            else:
                st.warning("Completa todos los campos.")

    # Ver empleados
    elif menu == "Ver Empleados":
        st.subheader("Lista de Empleados")
        # Barra de búsqueda
        search_term = st.text_input("Buscar por nombre o apellido", "")
        # Normalizar y convertir a minúsculas el término de búsqueda
        search_term_normalized = unicodedata.normalize('NFD', search_term).encode('ascii', 'ignore').decode('utf-8').lower()
        #Cargar empleados
        empleados = obtener_empleados()

        # Filtrar empleados que coincidan con el término de búsqueda
        if search_term:
            empleados = [emp for emp in empleados if 
                     search_term_normalized in unicodedata.normalize('NFD', (emp[1] + " " + emp[2])).encode('ascii', 'ignore').decode('utf-8').lower()]

        #mostrar los empleados filtrados
        for index, emp in enumerate(empleados):
            id_emp, nombre, apellido, correo, telefono, puesto, departamento, rfc, fecha_nac, hora_inicio, hora_fin, dias_laborables = emp
            with st.expander(f"{nombre} {apellido}"):

                st.write(f"ID: {id_emp}")
                st.write(f"Correo: {correo}")
                st.write(f"Teléfono: {telefono}")
                st.write(f"Puesto: {puesto}")
                st.write(f"Puesto: {departamento}")
                st.write(f"RFC: {rfc}")
                st.write(f"Fecha de Nacimiento: {fecha_nac}")

                # Formulario para actualizar datos del empleado
                nuevo_nombre = st.text_input("Nuevo Nombre", nombre, key=f"nombre_{id_emp}_{index}")
                nuevo_apellido = st.text_input("Nuevo Apellido", apellido, key=f"apellido_{id_emp}_{index}")
                nuevo_correo = st.text_input("Nuevo Correo", correo, key=f"correo_{id_emp}_{index}")
                nuevo_telefono = st.text_input("Nuevo Teléfono", telefono, key=f"telefono_{id_emp}_{index}")
                nuevo_puesto = st.text_input("Nuevo Puesto", puesto, key=f"puesto_{id_emp}_{index}")
                nuevo_departamento = st.text_input("Nuevo Departamento", departamento, key=f"departamento_{id_emp}_{index}")
                nuevo_rfc = st.text_input("Nuevo RFC", rfc, key=f"rfc_{id_emp}_{index}")
                nuevo_fecha_nac = st.date_input("Nueva Fecha de Nacimiento", fecha_nac, key=f"fecha_nac_{id_emp}_{index}")

                # Formulario para actualizar horario
                # Corregir la obtención de la hora de inicio y la hora de fin
                if isinstance(hora_inicio, datetime.timedelta):
                    hora_inicio = (datetime.datetime.min + hora_inicio).time()

                if isinstance(hora_fin, datetime.timedelta):
                    hora_fin = (datetime.datetime.min + hora_fin).time()

                # Ahora, puedes usar hora_inicio y hora_fin directamente en time_input
                nuevo_hora_inicio = st.time_input("Nuevo Hora de Inicio", hora_inicio, key=f"hora_inicio_{id_emp}_{index}")
                nuevo_hora_fin = st.time_input("Nuevo Hora de Fin", hora_fin, key=f"hora_fin_{id_emp}_{index}")
                nuevo_dias_laborables = st.number_input("Nuevo Días Laborables", min_value=1, max_value=7, value=dias_laborables, key=f"dias_laborables_{id_emp}_{index}")

                colguardar, coleliminar = st.columns(2)

                with colguardar:
                    if st.button("Guardar Cambios", key=f"guardar_{id_emp}_{index}"):  # Añadir el índice para que sea único
                        # Actualizar empleado y horario
                        actualizar_empleado(id_emp, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, nuevo_puesto, nuevo_departamento, nuevo_rfc, nuevo_fecha_nac, nuevo_hora_inicio, nuevo_hora_fin, nuevo_dias_laborables)
                        st.rerun()  # Actualizar la página para reflejar los cambios

                with coleliminar:
                    if st.button("Eliminar", key=f"eliminar_{id_emp}_{index}"):  # Añadir el índice para que sea único
                        eliminar_empleado(id_emp)
                        st.warning("Empleado y su horario eliminados.")
                        st.rerun()  # Actualizar la página para reflejar los cambios

    # Dashboard de asistencia
    elif menu == "Dashboard Asistencia":
        st.subheader("Asistencia")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT 
                fecha AS fecha,
                COUNT(*) AS total_asistencias
            FROM 
                asistencia
            GROUP BY 
                fecha
            ORDER BY 
                fecha;
            """)
            datos_asistencia = cursor.fetchall()

            if datos_asistencia:
                
                df_asistencia = pd.DataFrame(datos_asistencia, columns=["Fecha", "Registros"])
            
                fig1 = px.line(df_asistencia, x="Fecha", y="Registros",
                           title="Registros de Asistencia por Fecha", markers=True)
                
                st.plotly_chart(fig1)

            else:
                st.info("No hay datos de asistencia registrados.")
        
            cursor.execute("""
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
            """)

            datos_horas = cursor.fetchall()

            if datos_horas:
                df_horas = pd.DataFrame(datos_horas, columns=["Fecha", "Horas promedio"])
                fig2 = px.line(df_horas, x="Fecha", y="Horas promedio",
                            title=" Horas Promedio Trabajadas por Día", markers=True)
                st.plotly_chart(fig2)
            else:
                st.info("No hay datos suficientes para calcular horas promedio.")

        except Exception as e:
            st.error(f" Error al obtener datos del dashboard de asistencia: {e}")

        finally:
            cursor.close()
            conn.close()

        # Dashboard Salarios
    elif menu == "Dashboard Salarios":
        st.subheader("Dashboard de Salarios")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                SELECT 
                    e.id_empleado,
                    CONCAT(e.nombre, ' ', e.apellido) AS nombre_completo,
                    DATE_FORMAT(n.fecha, '%Y-%m') AS mes,
                    SUM(n.total_pago) AS total_pagado
                FROM 
                    nomina n
                JOIN 
                    empleado e ON e.id_empleado = n.id_empleado
                GROUP BY 
                    e.id_empleado, mes
                ORDER BY 
                    mes, nombre_completo;
            """)

            resultados = cursor.fetchall()

            if resultados:
                df_salarios = pd.DataFrame(resultados, columns=["ID Empleado", "Nombre", "Mes", "Total Pagado"])
                st.dataframe(df_salarios)

                fig = px.bar(df_salarios, 
                             x="Mes", 
                             y="Total Pagado", 
                             color="Nombre", 
                             barmode="group", 
                             title="Total Pagado por Empleado y Mes")
                st.plotly_chart(fig)
            else:
                st.info("No hay registros de salarios disponibles.")

        except Exception as e:
            st.error(f"Error al cargar el dashboard de salarios: {e}")

        finally:
            cursor.close()
            conn.close()
    
        # Reporte
    elif menu == "Reporte":
        st.subheader("Reporte General")

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
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
            """)
            reporte = cursor.fetchall()

            if reporte:
                df_reporte = pd.DataFrame(reporte, columns=[
                    "Nombre", "Apellido", "Correo", "Teléfono", "Puesto", "Departamento",
                    "RFC", "Fecha Nacimiento", "Fecha", "Hora Entrada", "Hora Salida", "Horas Trabajadas"
                ])
                st.dataframe(df_reporte)

                csv = df_reporte.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Descargar Reporte CSV",
                    data=csv,
                    file_name="reporte_general.csv",
                    mime="text/csv"
                )
            else:
                st.info("No hay registros disponibles para el reporte.")

        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")
        finally:
            cursor.close()
            conn.close()
