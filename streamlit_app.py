import streamlit as st
import urllib.parse
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(page_title="Entregas Temu Juliaca", page_icon="📦", layout="centered")

# --- LÓGICA DE CARPETAS Y ARCHIVOS ---
CARPETA_REGISTROS = "registros_temu"

# Crear la carpeta si no existe
if not os.path.exists(CARPETA_REGISTROS):
    os.makedirs(CARPETA_REGISTROS)

def obtener_archivos():
    """Obtiene la lista de archivos .txt creados en la carpeta de registros."""
    archivos = [f for f in os.listdir(CARPETA_REGISTROS) if f.endswith('.txt')]
    return sorted(archivos)

# --- BARRA LATERAL (CREAR ARCHIVOS) ---
with st.sidebar:
    st.header("📁 Gestor de Archivos")
    st.markdown("Crea listas para organizar tus envíos (ej. 'Lunes_12', 'Zona_Centro').")
    
    nuevo_nombre = st.text_input("Nombre del nuevo archivo:")
    if st.button("Crear Archivo"):
        if nuevo_nombre:
            # Asegurar que termine en .txt
            nombre_archivo = f"{nuevo_nombre}.txt" if not nuevo_nombre.endswith('.txt') else nuevo_nombre
            ruta = os.path.join(CARPETA_REGISTROS, nombre_archivo)
            
            if not os.path.exists(ruta):
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(f"--- Registro: {nombre_archivo} ---\n")
                st.success(f"¡Archivo '{nombre_archivo}' creado!")
                st.rerun() # Recarga la app para que aparezca en las listas
            else:
                st.warning("Ese archivo ya existe.")
        else:
            st.error("Escribe un nombre válido.")

# --- TÍTULO PRINCIPAL ---
st.title("📦 Generador de Avisos (Temu)")
st.markdown("Escribe el número, añade información extra, elige dónde guardarlo y crea el enlace.")

# --- PESTAÑAS ---
tab1, tab2 = st.tabs(["📲 Generar Mensaje y Guardar", "📋 Ver Historiales"])

archivos_disponibles = obtener_archivos()

with tab1:
    if not archivos_disponibles:
        st.warning("⚠️ No tienes ningún archivo creado. Ve al menú de la izquierda para crear tu primer archivo.")
    else:
        # Elegir archivo
        archivo_seleccionado = st.selectbox("📂 Selecciona el archivo donde se guardará:", archivos_disponibles)
        
        st.markdown("---")
        
        # Datos del cliente
        numero_final = st.text_input("Número de celular (9 dígitos):", max_chars=9)
        info_adicional = st.text_area("Información del cliente (Nombre, zona, notas, etc.):", placeholder="Ej: Juan Pérez - Entregar por la tarde...")

        if numero_final:
            if len(numero_final) == 9 and numero_final.isdigit():
                num_completo = "51" + numero_final
                
                # Mensaje de Whatsapp
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
                
                # Botón para registrar
                if st.button(f"💾 Guardar número en '{archivo_seleccionado}' y generar enlace"):
                    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Limpiamos saltos de línea de la info adicional para que ocupe una sola línea en el txt
                    info_limpia = info_adicional.replace('\n', ' | ') if info_adicional else "Sin información extra"
                    
                    registro_nuevo = f"Fecha: {fecha_hora} | Número: +51 {numero_final} | Info: {info_limpia}\n"
                    
                    ruta_archivo = os.path.join(CARPETA_REGISTROS, archivo_seleccionado)
                    try:
                        with open(ruta_archivo, "a", encoding="utf-8") as f:
                            f.write(registro_nuevo)
                        st.success(f"¡Datos guardados exitosamente en {archivo_seleccionado}!")
                    except Exception as e:
                        st.error(f"Hubo un error al guardar: {e}")
                
                # Botón visual para abrir WhatsApp
                st.markdown(f"""
                <a href="{link_whatsapp}" target="_blank" style="display: block; width: 100%; text-align: center; background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-decoration: none; font-size: 18px; font-weight: bold; margin-top: 20px;">
                    📲 Abrir Chat de WhatsApp al {numero_final}
                </a>
                """, unsafe_allow_html=True)
            else:
                st.error("⚠️ El número debe tener exactamente 9 dígitos numéricos.")


with tab2:
    st.subheader("📁 Visor de Archivos y Registros")
    
    if not archivos_disponibles:
        st.info("Aún no hay archivos de registro. Créalos en la barra lateral.")
    else:
        # Selector de archivo a visualizar
        archivo_a_ver = st.selectbox("Selecciona el archivo que deseas visualizar o descargar:", archivos_disponibles, key="ver_archivo")
        ruta_ver = os.path.join(CARPETA_REGISTROS, archivo_a_ver)
        
        try:
            with open(ruta_ver, "r", encoding="utf-8") as f:
                contenido = f.read()
                
            st.text_area(f"Contenido de {archivo_a_ver}:", value=contenido, height=300)
            
            # Botón de descarga directa
            st.download_button(
                label=f"📥 Descargar {archivo_a_ver}",
                data=contenido,
                file_name=archivo_a_ver,
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"No se pudo leer el archivo: {e}")
                
