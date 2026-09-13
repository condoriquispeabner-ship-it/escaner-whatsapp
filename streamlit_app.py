import streamlit as st
import re
import urllib.parse
from PIL import Image
import pytesseract

# Configuración de la página
st.set_page_config(page_title="Entregas Temu Juliaca", page_icon="📦", layout="centered")

st.title("📦 Escáner de Entregas (Temu)")
st.markdown("Extrae el número de la etiqueta para enviar el formulario de entrega al instante.")

tab1, tab2 = st.tabs(["📷 Usar Cámara", "📂 Subir de Galería"])

imagen = None

with tab1:
    imagen_camara = st.camera_input("Captura la etiqueta (enfoca el Teléfono)")
    if imagen_camara:
        imagen = Image.open(imagen_camara)

with tab2:
    imagen_subida = st.file_uploader("Sube una foto de la etiqueta", type=["png", "jpg", "jpeg"])
    if imagen_subida:
        imagen = Image.open(imagen_subida)

if imagen:
    st.image(imagen, caption="Etiqueta cargada", use_container_width=True)
    st.info("🔍 Analizando la imagen en busca del número...")
    
    try:
        # Convertir a escala de grises para que Tesseract lea mejor el texto negro sobre blanco
        imagen_gris = imagen.convert('L')
        texto_detectado = pytesseract.image_to_string(imagen_gris)
        
        # Busca un número de 9 dígitos que empiece por 9 (ignora guiones o espacios)
        numeros = re.findall(r'9\d{8}', re.sub(r'[\s\-]', '', texto_detectado))
        
        numero_sugerido = ""
        if numeros:
            numero_sugerido = numeros[0]
            st.success("¡Número del cliente detectado con éxito!")
        else:
            st.warning("No se detectó el número automáticamente. Por favor, escríbelo abajo.")
            
        numero_final = st.text_input("Confirma el número (9 dígitos):", value=numero_sugerido, max_chars=9)
        
        if numero_final and len(numero_final) == 9:
            num_completo = "51" + numero_final
            
            # MENSAJE ACTUALIZADO Y FORMATEADO PARA WHATSAPP
            mensaje = (
                "Hola! 👋 Te avisamos que tu pedido de Temu ya llegó a la ciudad de Juliaca "
                "y está por ser entregado. 📦\n\n"
                "Para el correcto envío de tu paquete, por favor ayúdanos respondiendo este breve cuestionario:\n"
                "👉 https://docs.google.com/forms/d/e/1FAIpQLSdj8oVFPZkRmb71tv8ZI2f9DHjZmlSZCoHDO7pTqZFwJ27tQA/viewform?usp=header"
            )
            
            # Preparamos el mensaje para que sea un enlace web válido
            mensaje_codificado = urllib.parse.quote(mensaje)
            link_whatsapp = f"https://wa.me/{num_completo}?text={mensaje_codificado}"
            
            # Botón verde de WhatsApp
            st.markdown(f"""
            <a href="{link_whatsapp}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-size: 18px; font-weight: bold; margin-top: 20px;">
                📲 Enviar aviso al {numero_final}
            </a>
            """, unsafe_allow_html=True)
        elif numero_final:
            st.error("El número debe tener exactamente 9 dígitos.")
            
    except Exception as e:
        st.error(f"Error al procesar la imagen: {e}")
