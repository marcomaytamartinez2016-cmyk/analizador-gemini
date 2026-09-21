import streamlit as st
import google.genai as genai
from PIL import Image

# Configuración de la página web
st.set_page_config(page_title="Analizador de Estado de Ánimo", page_icon="🎭")

st.title("🎭 Analizador de Estado de Ánimo con Gemini")
st.write("Sube una imagen para analizar las emociones y detalles visuales de la persona.")

# Clave de API de Gemini
API_KEY = "AQ.Ab8RN6I3GEsmdsUe9QI8VfTJ-yt5nC3W6gleWNLw5v8AdDq5oQ"
client = genai.Client(api_key=API_KEY)

# Componente para subir archivos en la web
archivo_subido = st.file_uploader("Elige una foto...", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    # Mostrar la imagen subida por el usuario
    imagen = Image.open(archivo_subido)
    st.image(imagen, caption="Imagen cargada", use_column_width=True)
    
    if st.button("Analizar Estado de Ánimo"):
        with st.spinner("Gemini está analizando la imagen..."):
            try:
                # Llamada a la API
                respuesta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[
                        "Analiza detalladamente el estado de ánimo de la persona en la imagen, "
                        "menciona las emociones detectadas y describe las expresiones faciales.", 
                        imagen
                    ]
                )
                st.success("¡Análisis completado!")
                st.subheader("Resultado del Análisis:")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al analizar la imagen: {e}")
