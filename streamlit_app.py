import streamlit as st
import urllib.parse
import os

# Crear carpeta para guardar los registros
CARPETA_REGISTROS = "registros"
if not os.path.exists(CARPETA_REGISTROS):
    os.makedirs(CARPETA_REGISTROS)

def obtener_archivos():
    archivos = [f for f in os.listdir(CARPETA_REGISTROS) if f.endswith(".txt")]
    return archivos if archivos else []

st.set_page_config(page_title="Entregas Temu Juliaca", page_icon="📦", layout="centered")
st.title("📦 Generador de Avisos (Temu)")

st.markdown("**1. Selecciona o crea tu archivo**")
col1, col2 = st.columns(2)

with col1:
    archivos_disp = obtener_archivos()
    opciones_select = ["(Selecciona un archivo)"] + archivos_disp
    archivo_seleccionado = st.selectbox("Archivos existentes:", opciones_select)

with col2:
    nuevo_archivo = st.text_input("O crea uno nuevo (Escribe y presiona Enter):", placeholder="Ej: BOLSA 2")
    if nuevo_archivo:
        nombre_limpio = nuevo_archivo.strip()
        if not nombre_limpio.endswith(".txt"):
            nombre_limpio += ".txt"
        
        ruta_nuevo = os.path.join(CARPETA_REGISTROS, nombre_limpio)
        if not os.path.exists(ruta_nuevo):
            with open(ruta_nuevo, "w", encoding="utf-8") as f:
                f.write("") # Crea el archivo totalmente en blanco
            st.success(f"✅ Archivo '{nombre_limpio}' creado. Selecciónalo al lado.")
        else:
            st.info("Ese archivo ya existe.")

archivo_activo = archivo_seleccionado if archivo_seleccionado != "(Selecciona un archivo)" else None

st.markdown("---")

tab1, tab2 = st.tabs(["📲 2. Guardar y Enviar", "📋 3. Ver Registros"])

with tab1:
    st.markdown("**Ingresa el Número**")
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
            
            st.write("")
            
            if not archivo_activo:
                st.error("⚠️ SELECCIONA UN ARCHIVO ARRIBA PARA GUARDAR EL NÚMERO.")
            else:
                # Botón de acción principal
                if st.button("💾 GUARDAR NÚMERO Y CREAR ENLACE", type="primary", use_container_width=True):
                    # Guarda SOLO el número exacto y salta a la siguiente línea
                    ruta_completa = os.path.join(CARPETA_REGISTROS, archivo_activo)
                    with open(ruta_completa, "a", encoding="utf-8") as f:
                        f.write(f"{numero_final}\n")
                    
                    st.success("✅ Guardado correctamente.")
                    
                    # Genera el botón nativo de Streamlit para ir a WhatsApp
                    st.link_button(
                        f"📲 ABRIR WHATSAPP AL {numero_final}", 
                        link_whatsapp, 
                        use_container_width=True
                    )
        else:
            st.error("⚠️ El número debe tener exactamente 9 dígitos numéricos.")

with tab2:
    if not archivo_activo:
        st.info("👆 Selecciona un archivo en la parte superior.")
    else:
        st.markdown(f"**Lista de números guardados en {archivo_activo}**")
        ruta_ver = os.path.join(CARPETA_REGISTROS, archivo_activo)
        
        try:
            with open(ruta_ver, "r", encoding="utf-8") as f:
                contenido = f.read()
            
            st.text_area("Números:", value=contenido, height=350)
            
            st.download_button(
                label=f"📥 Descargar {archivo_activo}",
                data=contenido,
                file_name=archivo_activo,
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")
