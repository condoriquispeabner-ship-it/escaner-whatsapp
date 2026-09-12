import streamlit as st
import re
import urllib.parse
from PIL import Image
import pytesseract

# Configuración de la página
st.set_page_config(page_title="Escanear Número", page_icon="📸", layout="centered")

st.title("📸 Escáner de Teléfonos")
st.markdown("Extrae números de imágenes o usando la cámara para chatear al instante.")

# Pestañas para elegir el método (Cámara o Galería)
tab1, tab2 = st.tabs(["📷 Usar Cámara", "📂 Subir de Galería"])

imagen = None

with tab1:
    imagen_camara = st.camera_input("Captura el recibo o número")
    if imagen_camara:
        imagen = Image.open(imagen_camara)

with tab2:
    imagen_subida = st.file_uploader("Sube una foto o captura", type=["png", "jpg", "jpeg"])
    if imagen_subida:
        imagen = Image.open(imagen_subida)

# Procesamiento de la imagen
if imagen:
    st.image(imagen, caption="Imagen lista", use_column_width=True)
    st.info("🔍 Analizando la imagen con Inteligencia Artificial...")
    
    try:
        # Extraer texto de la imagen (OCR)
        texto_detectado = pytesseract.image_to_string(imagen)
        
        # Buscar patrón de celular de Perú (9 dígitos, con o sin espacios)
        numeros = re.findall(r'\b9\d{2}[\s\-]?\d{3}[\s\-]?\d{3}\b', texto_detectado)
        
        numero_sugerido = ""
        if numeros:
            # Limpiar el número encontrado (quitar espacios)
            numero_sugerido = re.sub(r'\D', '', numeros[0])
            st.success("¡Número detectado automáticamente!")
        else:
            st.warning("No se detectó el número. Puedes digitarlo manualmente abajo.")
            
        # Campo para que el usuario confirme o corrija el número
        numero_final = st.text_input("Confirma el número (9 dígitos):", value=numero_sugerido, max_chars=9)
        
        if numero_final and len(numero_final) == 9:
            num_completo = "51" + numero_final
            mensaje = "Hola, te escribimos de parte de nuestra agencia para coordinar la entrega de tu pedido de Temu."
            mensaje_codificado = urllib.parse.quote(mensaje)
            link_whatsapp = f"https://wa.me/{num_completo}?text={mensaje_codificado}"
            
            # Botón verde estilo WhatsApp
            st.markdown(f"""
            <a href="{link_whatsapp}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-size: 18px; font-weight: bold; margin-top: 20px;">
                📲 Abrir Chat de WhatsApp
            </a>
            """, unsafe_allow_html=True)
        elif numero_final:
            st.error("El número debe tener exactamente 9 dígitos.")
            
    except Exception as e:
        st.error("Ocurrió un error leyendo la imagen. Revisa las instrucciones de instalación.")
