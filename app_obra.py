import streamlit as st
import pandas as pd
from datetime import datetime
import smtplib
from email.message import EmailMessage
import io

st.title("📋 Seguimiento de Obra")

# Logo (Requisito RA4CEb) [cite: 10]
try:
    st.image("logo.png", width=200)
except:
    st.write("Sube el logo.png a GitHub para cumplir con el formato.")

# Tareas completas del proyecto [cite: 11, 12, 13, 14, 15, 16, 29, 33]
tareas = [
    "Trazado y marcado de cajas, tubos y cuadros",
    "Ejecución rozas en paredes y techos",
    "Montaje de soportes",
    "Colocación tubos y conductos",
    "Tendido de cables",
    "Identificación y etiquetado",
    "Pruebas de continuidad",
    "Pruebas de funcionamiento"
]

# Estados del avance [cite: 34, 35, 36, 38, 39]
estados = [
    "Avance de la tarea en torno al 25% aprox.",
    "Avance de la tarea en torno al 50% aprox.",
    "Avance de la tarea en torno al 75% aprox.",
    "OK, finalizado sin errores",
    "Finalizado, pero con errores pendientes de corregir"
]

# Inputs [cite: 41, 42]
trabajador = st.text_input("Trabajador")
fecha = st.date_input("Fecha")
tarea = st.selectbox("Tarea", tareas)
estado = st.selectbox("Estado", estados)

# Crear el DataFrame con el registro actual
nuevo_registro = {
    "Tarea": [tarea],
    "Estado": [estado],
    "Trabajador": [trabajador],
    "Fecha": [fecha.strftime("%d/%m/%Y")]
}
df_actual = pd.DataFrame(nuevo_registro)

# --- SECCIÓN DE DESCARGA EXCEL (.xlsx) ---
st.subheader("💾 Descargar Informe")

# Usamos un buffer de memoria para generar el Excel real (RA3CEb) 
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_actual.to_excel(writer, index=False, sheet_name='Informe')

st.download_button(
    label="Descargar archivo .xlsx",
    data=buffer.getvalue(),
    file_name=f"Informe_{trabajador}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# --- SECCIÓN DE CORREO (RA4CEd) ---
st.subheader("📧 Enviar informe por correo")
correo_destino = st.text_input("Correo destino (Email de la profesora)", value="profesora@ejemplo.com")

if st.button("Enviar correo"):
    if trabajador and correo_destino:
        try:
            # Crear el mensaje
            msg = EmailMessage()
            msg["Subject"] = f"Informe de Obra - {trabajador}"
            msg["From"] = st.secrets["email_user"] # Usa Secrets para seguridad 
            msg["To"] = correo_destino
            msg.set_content(f"Se adjunta el reporte de obra de {trabajador} con fecha {fecha}.")

            # Adjuntar el Excel desde el buffer
            msg.add_attachment(
                buffer.getvalue(),
                maintype="application",
                subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                filename=f"Informe_{trabajador}.xlsx"
            )

            # Envío seguro (Requiere Secrets en Streamlit) [cite: 44, 46]
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(st.secrets["email_user"], st.secrets["email_password"])
                smtp.send_message(msg)
            st.success("✅ Correo enviado correctamente")
        except Exception as e:
            st.error(f"Error al enviar: Verifique los Secrets en Streamlit")
    else:
        st.warning("Complete el nombre y el correo de destino.")
