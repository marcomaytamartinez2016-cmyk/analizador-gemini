import streamlit as st
import google.genai as genai
from PIL import Image
import io
import base64

# Configuración de la página web
st.set_page_config(page_title="Pizarra de Análisis Emocional", page_icon="🎨")

st.title("🎨 Dibuja y Analiza tu Estado de Ánimo")
st.write("Dibuja lo que sientas en la pizarra de abajo para analizar tu estado emocional con Gemini.")

# Clave de API de Gemini
API_KEY = "AQ.Ab8RN6I3GEsmdsUe9QI8VfTJ-yt5nC3W6gleWNLw5v8AdDq5oQ"
client = genai.Client(api_key=API_KEY)

# Componente HTML para lienzo interactivo de dibujo
canvas_html = """
<div style="text-align: center;">
    <canvas id="canvas" width="500" height="350" style="border:2px solid #333; background-color:#ffffff; cursor:crosshair; border-radius:8px;"></canvas>
    <br><br>
    <button onclick="clearCanvas()" style="padding:8px 16px; background-color:#f44336; color:white; border:none; border-radius:4px; cursor:pointer;">Limpiar Lienzo</button>
</div>

<script>
    var canvas = document.getElementById('canvas');
    var ctx = canvas.getContext('2d');
    var drawing = false;

    canvas.addEventListener('mousedown', function(e) { drawing = true; draw(e); });
    canvas.addEventListener('mouseup', function() { drawing = false; ctx.beginPath(); });
    canvas.addEventListener('mousemove', draw);

    // Soporte para pantallas táctiles
    canvas.addEventListener('touchstart', function(e) { drawing = true; draw(e.touches[0]); e.preventDefault(); });
    canvas.addEventListener('touchend', function() { drawing = false; ctx.beginPath(); });
    canvas.addEventListener('touchmove', function(e) { draw(e.touches[0]); e.preventDefault(); });

    function draw(e) {
        if (!drawing) return;
        var rect = canvas.getBoundingClientRect();
        ctx.lineWidth = 4;
        ctx.lineCap = 'round';
        ctx.strokeStyle = '#000000';

        ctx.lineTo(e.clientX - rect.left, e.clientY - rect.top);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX - rect.left, e.clientY - rect.top);
    }

    function clearCanvas() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
</script>
"""

st.components.v1.html(canvas_html, height=430)

st.info("💡 Una vez que hagas tu dibujo en la pizarra, toma una captura de pantalla o dibújalo y sube la imagen abajo para el análisis:")

archivo_subido = st.file_uploader("O sube directamente el dibujo/captura:", type=["jpg", "jpeg", "png"])

if archivo_subido is not None:
    imagen = Image.open(archivo_subido)
    st.image(imagen, caption="Dibujo a analizar", use_container_width=True)
    
    if st.button("Analizar Estado de Ánimo del Dibujo"):
        with st.spinner("Gemini está analizando los trazos..."):
            try:
                prompt_analisis = (
                    "Actúa como un experto en psicología del arte y expresión gráfica. "
                    "Analiza el dibujo creado por el usuario e interpreta: "
                    "1. Estado emocional sugerido por los trazos, formas y composición. "
                    "2. Significado del uso del espacio y figuras. "
                    "3. Una conclusión reflexiva y empática sobre lo que expresa el usuario."
                )
                
                respuesta = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt_analisis, imagen]
                )
                st.success("¡Análisis completado!")
                st.subheader("Resultado de la Interpretación:")
                st.write(respuesta.text)
            except Exception as e:
                st.error(f"Error al analizar el dibujo: {e}")
