import streamlit as st
import pandas as pd
import io
from datetime import date

# Título y Logo (Requisito: Logo de la empresa)
st.title("📋 Seguimiento de Obra - Fundación Masaveu")
try:
    st.image("logo.png", width=200)
except:
    st.info("Sube 'logo.png' a GitHub para visualizar el logo oficial.")

# Listas de tareas y estados según el PDF
tareas = [
    "Trazado y marcado de cajas, tubos y cuadros", "Ejecución rozas en paredes y techos",
    "Montaje de soportes", "Colocación tubos y conductos", "Tendido de cables",
    "Identificación y etiquetado", "Conexionado de cables en bornes o regletas",
    "Instalación y conexionado de mecanismos", "Fijación de carril DIN y mecanismos en cuadro eléctrico",
    "Cableado interno del cuadro eléctrico", "Configuración de equipos domóticos",
    "Pruebas de continuidad", "Pruebas de funcionamiento"
]

estados = [
    "Avance de la tarea en torno al 25% aprox.", "Avance de la tarea en torno al 50% aprox.",
    "Avance de la tarea en torno al 75% aprox.", "OK, finalizado sin errores",
    "Finalizado, pero con errores pendientes de corregir", "Finalizado y corregidos los errores"
]

# Formulario (Requisito: Nombre del trabajador y Fecha)
trabajador = st.text_input("Nombre del trabajador")
fecha = st.date_input("Fecha de envío", value=date.today())
tarea_sel = st.selectbox("Selecciona tarea", tareas)
avance_sel = st.selectbox("Estado", estados)

# GENERACIÓN Y DESCARGA EN EXCEL (.xlsx)
if st.button("Preparar Informe Excel"):
    if trabajador:
        # 1. Crear el DataFrame con los datos actuales
        nuevo_dato = {
            "Trabajador": [trabajador],
            "Fecha": [fecha.strftime("%d/%m/%Y")],
            "Tarea": [tarea_sel],
            "Estado": [avance_sel]
        }
        df = pd.DataFrame(nuevo_dato)

        # 2. Crear un buffer de memoria (esto evita errores en Streamlit Cloud)
        output = io.BytesIO()
        
        # 3. Escribir el Excel usando xlsxwriter (Motor para .xlsx real)
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Seguimiento')
        
        # 4. Botón de descarga final con el MIME Type correcto
        st.success("✅ Informe listo.")
        st.download_button(
            label="📥 Descargar archivo .xlsx",
            data=output.getvalue(),
            file_name=f"Informe_{trabajador}_{fecha}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Por favor, introduce el nombre del trabajador.")
