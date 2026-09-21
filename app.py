import streamlit as st
import google.genai as genai
from PIL import Image
import numpy as np
from streamlit_drawable_canvas import st_canvas

# Configuración de la página web
st.set_page_config(page_title="Pizarra de Análisis Emocional", page_icon="🎨")

st.title("🎨 Dibuja y Analiza tu Estado de Ánimo")
st.write("Dibuja lo que sientas en el lienzo de abajo (un paisaje, una persona, garabatos, etc.) para analizar tu estado emocional.")

# Clave de API de Gemini
API_KEY = "AQ.Ab8RN6I3GEsmdsUe9QI8VfTJ-yt5nC3W6gleWNLw5v8AdDq5oQ"
client = genai.Client(api_key=API_KEY)

# Opciones de personalización del pincel en la barra lateral
st.sidebar.header("Opciones de Dibujo")
stroke_width = st.sidebar.slider("Grosor del pincel: ", 1, 25, 3)
stroke_color = st.sidebar.color_picker("Color del pincel: ", "#000000")
bg_color = st.sidebar.color_picker("Color de fondo: ", "#ffffff")

st.subheader("Lienzo Interactivo:")
# Crear el lienzo interactivo
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Color de relleno predeterminado
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=400,
    width=600,
    drawing_mode="freedraw",
    key="canvas",
)

# Botón para iniciar el análisis
if st.button("Analizar Dibujo"):
    if canvas_result.image_data is not None:
        # Convertir los datos de la imagen del lienzo a formato PIL
        img_array = canvas_result.image_data.astype(np.uint8)
        imagen = Image.fromarray(img_array)
        
        # Verificar si el usuario ha dibujado algo
        if np.all(img_array[:, :, :3] == 255) or np.all(img_array[:, :, 3] == 0):
            st.warning("Por favor, realiza un dibujo antes de presionar el botón.")
        else:
            with st.spinner("Gemini está analizando tu trazo y composición..."):
                try:
                    prompt_analisis = (
                        "Actúa como un experto en psicología del arte y expresión gráfica. "
                        "Analiza el dibujo creado por el usuario en este lienzo digital e interpreta: "
                        "1. Estado emocional sugerido por la composición, trazos e intensidad. "
                        "2. Significado del uso de los colores, formas y distribución del espacio. "
                        "3. Una conclusión reflexiva y empática sobre lo que expresa el usuario."
                    )
                    
                    # Llamada a la API de Gemini
                    respuesta = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[prompt_analisis, imagen]
                    )
                    st.success("¡Análisis completado!")
                    st.subheader("Resultado de la Interpretación:")
                    st.write(respuesta.text)
                except Exception as e:
                    st.error(f"Error al analizar el lienzo: {e}")
    else:
        st.warning("Por favor, dibuja algo en el lienzo.")
