import streamlit as st
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Entregas Temu Juliaca", page_icon="📦", layout="centered")

st.title("📦 Generador de Avisos (Temu)")
st.markdown("Escribe el número del cliente para crear el enlace directo a WhatsApp.")

# Recuadro para ingresar el número manualmente
numero_final = st.text_input("Número de celular (9 dígitos):", max_chars=9)

# Validar que se haya ingresado algo y que tenga 9 dígitos
if numero_final:
    if len(numero_final) == 9 and numero_final.isdigit():
        # Agregar el código de Perú (51)
        num_completo = "51" + numero_final
        
        # El mensaje actualizado con el aviso urgente de 12 horas y devolución a China
        mensaje = (
            "Hola! 👋 Te avisamos que tu pedido de Temu ya llegó a la ciudad de Juliaca "
            "y está por ser entregado. 📦\n\n"
            "🚨 *AVISO URGENTE*: Para la correcta entrega de tu pedido, debes responder este cuestionario de manera urgente:\n"
            "👉 https://docs.google.com/forms/d/e/1FAIpQLSdj8oVFPZkRmb71tv8ZI2f9DHjZmlSZCoHDO7pTqZFwJ27tQA/viewform?usp=header\n\n"
            "⚠️ *Nota importante*: Caso contrario de no responder en un lapso de 12 horas, tu pedido será devuelto a China."
        )
        
        # Convertir el texto para que funcione en un enlace web
        mensaje_codificado = urllib.parse.quote(mensaje)
        link_whatsapp = f"https://wa.me/{num_completo}?text={mensaje_codificado}"
        
        # Crear el botón verde para WhatsApp
        st.markdown(f"""
        <a href="{link_whatsapp}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-size: 18px; font-weight: bold; margin-top: 20px;">
            📲 Enviar WhatsApp al {numero_final}
        </a>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ El número debe tener exactamente 9 números.")
