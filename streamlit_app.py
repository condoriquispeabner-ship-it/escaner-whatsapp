import streamlit as st
import urllib.parse
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Entregas Temu Juliaca", page_icon="📦", layout="centered")

st.title("📦 Generador de Avisos (Temu)")
st.markdown("Escribe el número del cliente para crear el enlace y guardarlo en el registro.")

# Nombre del archivo donde se guardará el historial
ARCHIVO_REGISTRO = "registros_enviados.txt"

# Pestañas para separar el envío y el historial
tab1, tab2 = st.tabs(["📲 Generar Mensaje", "📋 Ver Registros Guardados"])

with tab1:
    numero_final = st.text_input("Número de celular (9 dígitos):", max_chars=9)

    if numero_final:
        if len(numero_final) == 9 and numero_final.isdigit():
            num_completo = "51" + numero_final
            
            mensaje = (
                "Hola! 👋 Te avisamos que tu pedido de Temu ya llegó a la ciudad de Juliaca "
                "y está por ser entregado. 📦\n\n"
                "🚨 *AVISO URGENTE*: Para la correcta entrega de tu pedido, debes responder este cuestionario de manera urgente:\n"
                "👉 https://docs.google.com/forms/d/e/1FAIpQLSdj8oVFPZkRmb71tv8ZI2f9DHjZmlSZCoHDO7pTqZFwJ27tQA/viewform?usp=header\n\n"
                "⚠️ *Nota importante*: Caso contrario de no responder en un lapso de 12 horas, tu pedido será devuelto a China.\n\n"
                "🏢 En caso de no poder o querer responder la encuesta, para tu control puedes acercarte a nuestra dirección "
                "con tu respectivo DNI:\n"
                "📍 https://maps.app.goo.gl/zyx2dPASQSi9HYjy6\n"
                "🕒 Horario de atención: De lunes a domingo entre la 1:00 PM y 10:00 PM."
            )
            
            mensaje_codificado = urllib.parse.quote(mensaje)
            link_whatsapp = f"https://wa.me/{num_completo}?text={mensaje_codificado}"
            
            # Botón para registrar y abrir WhatsApp
            if st.button("💾 Guardar número y generar enlace"):
                # Obtener la fecha y hora actual
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                registro_nuevo = f"Fecha: {fecha_hora} | Número: +51 {numero_final}\n"
                
                # Guardar en el archivo local de la app
                try:
                    with open(ARCHIVO_REGISTRO, "a", encoding="utf-8") as f:
                        f.write(registro_nuevo)
                    st.success("¡Número guardado en el registro exitosamente!")
                except Exception as e:
                    st.warning(f"Se generó el enlace pero hubo un detalle al guardar en el archivo: {e}")
            
            st.markdown(f"""
            <a href="{link_whatsapp}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-size: 18px; font-weight: bold; margin-top: 20px;">
                📲 Abrir Chat de WhatsApp al {numero_final}
            </a>
            """, unsafe_allow_html=True)
        else:
            st.error("⚠️ El número debe tener exactamente 9 números.")

with tab2:
    st.subheader("📁 Historial de números atendidos")
    st.markdown("Aquí puedes ver los números guardados y en qué archivo se encuentran.")
    
    st.info(f"📂 El archivo de respaldo se almacena en tu repositorio con el nombre: **`{ARCHIVO_REGISTRO}`**")
    
    # Leer y mostrar el contenido del archivo si existe
    try:
        with open(ARCHIVO_REGISTRO, "r", encoding="utf-8") as f:
            contenido = f.read()
            if contenido:
                st.text_area("Contenido del archivo de registros:", value=contenido, height=300)
                
                # Botón de descarga directa del archivo de texto
                st.download_button(
                    label="📥 Descargar archivo de registros (.txt)",
                    data=contenido,
                    file_name=ARCHIVO_REGISTRO,
                    mime="text/plain"
                )
            else:
                st.warning("El archivo de registro está vacío por ahora.")
    except FileNotFoundError:
        st.warning("Aún no se ha creado ningún registro. Guarda un número desde la pestaña anterior para generar el archivo.")
