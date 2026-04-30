# control
App de seguimiento de obra desarrollada con Python y Streamlit, que permite registrar tareas, estados de avance y trabajadores, generando automáticamente reportes en Excel para la gestión y control del proyecto.
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📋 Seguimiento de Obra")

# Logo (opcional)
st.image("logo.png", width=200)

# Lista de tareas
tareas = [
    "Trazado y marcado",
    "Ejecución rozas",
    "Montaje de soportes",
    "Colocación de tubos",
    "Tendido de cables",
    "Identificación",
    "Conexionado",
    "Instalación mecanismos",
    "Cuadro eléctrico",
    "Domótica",
    "Pruebas"
]

# Estados
estado = [
    "25%",
    "50%",
    "75%",
    "Finalizado OK",
    "Finalizado con errores",
    "Corregido"
]

# Inputs
tarea = st.selectbox("Selecciona tarea", tareas)
avance = st.selectbox("Estado", estado)
trabajador = st.text_input("Nombre del trabajador")
fecha = st.date_input("Fecha")

# Botón guardar
if st.button("Guardar registro"):
    nuevo_dato = {
        "Tarea": tarea,
        "Estado": avance,
        "Trabajador": trabajador,
        "Fecha": fecha
    }

    try:
        df = pd.read_excel("datos.xlsx")
    except:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
    df.to_excel("datos.xlsx", index=False)

    st.success("Datos guardados correctamente")

# Descargar Excel
if st.button("Descargar Excel"):
    df = pd.read_excel("datos.xlsx")
    st.download_button("Descargar", df.to_csv(), "datos.csv")
