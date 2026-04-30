import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage

st.title("📋 Seguimiento de Obra")

# Logo
try:
    st.image("logo.png", width=200)
except:
    st.write("")

# Tareas
tareas = [
    "Trazado y marcado de cajas, tubos y cuadros",
    "Ejecución rozas en paredes y techos",
    "Montaje de soportes",
    "Colocación tubos y conductos",
    "Tendido de cables",
    "Identificación y etiquetado",
    "Conexionado de cables",
    "Instalación de mecanismos",
    "Cuadro eléctrico",
    "Domótica",
    "Pruebas"
]

# Estados
estados = [
    "25%",
    "50%",
    "75%",
    "Finalizado OK",
    "Finalizado con errores",
    "Corregido"
]

# Inputs
tarea = st.selectbox("Tarea", tareas)
estado = st.selectbox("Estado", estados)
trabajador = st.text_input("Trabajador")
fecha = st.date_input("Fecha")

# Guardar datos
if st.button("Guardar"):
    nuevo = {
        "Tarea": tarea,
        "Estado": estado,
        "Trabajador": trabajador,
        "Fecha": fecha
    }

    try:
        df = pd.read_excel("datos.xlsx")
    except:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_excel("datos.xlsx", index=False)

    st.success("Registro guardado")

# Descargar
import io

# ... (resto de tu código anterior)

if st.button("Generar Registro"):
    # Creamos el diccionario con los datos actuales
    datos = {
        "Trabajador": [nombre],
        "Fecha": [fecha_envio.strftime("%d/%m/%Y")],
        "Tarea": [tarea],
        "Estado": [estado]
    }
    df = pd.DataFrame(datos)
    
    # Creamos un buffer en memoria para el archivo Excel
    buffer = io.BytesIO()
    
    # Usamos el motor xlsxwriter para crear el Excel
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Seguimiento')
    
    # Botón de descarga real
    st.download_button(
        label="Descargar Informe en Excel",
        data=buffer.getvalue(),
        file_name=f"seguimiento_{nombre}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Enviar por correo
st.subheader("📧 Enviar informe")

correo = st.text_input("Correo destino")

if st.button("Enviar correo"):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Informe de obra"
        msg["From"] = "TUEMAIL@gmail.com"
        msg["To"] = correo
        msg.set_content("Adjunto informe de obra")

        with open("datos.xlsx", "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename="datos.xlsx")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("TUEMAIL@gmail.com", "CONTRASEÑA_APP")
            smtp.send_message(msg)

        st.success("Correo enviado correctamente")

    except:
        st.error("Error al enviar correo")
      
