import streamlit as st
import google.genai as genai
from PIL import Image

# Configuración de la página web
st.set_page_config(page_title="Analizador Psicológico de Dibujos", page_icon="🎨")

st.title("🎨 Analizador de Estado de Ánimo según Dibujos")
st.write("Sube la foto de un dibujo hecho a mano para analizar el estado emocional a través del arte y los trazos.")

# Clave de API de Gemini
API_KEY = "AQ.Ab8RN6I3GEsmdsUe9QI8VfTJ-yt5nC3W6gleWNLw5v8AdDq5oQ"
client = genai.Client(api_key=API_KEY)

# Componente para subir archivos en la web
archivo_subido = st.file_uploader("Sube el dibujo aquí...", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    # Mostrar el dibujo subido por el usuario
    imagen = Image.open(archivo_subido)
    st.image(imagen, caption="Dibujo cargado", use_container_width=True)
    
    if st.button("Analizar Estado Emocional del Dibujo"):
        with st.spinner("Analizando la expresión artística y los trazos..."):
            try:
                # Prompt especializado en la interpretación psicológica y artística de dibujos
                prompt_analisis = (
                    "Actúa como un experto en análisis de la expresión artística y emociones a través del dibujo. "
                    "Analiza la imagen adjunta interpretando: "
                    "1. El estado de ánimo o emociones que transmite la obra. "
                    "2. El uso de trazos, líneas, colores (o sombras) y distribución del espacio. "
                    "3. Una breve conclusión comprensiva sobre lo que expresa la persona al realizar este dibujo."
                )
                
                # Llamada a la API de Gemini
                respuesta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt_analisis, imagen]
                )
                st.success("¡Análisis del dibujo completado!")
                st.subheader("Interpretación Emocional del Arte:")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al analizar el dibujo: {e}")
