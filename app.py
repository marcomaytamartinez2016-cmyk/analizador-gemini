import streamlit as st
import requests
from google import genai

# 1. Configuración de la interfaz Streamlit
st.set_page_config(
    page_title="Asesor Inteligente de Vehículos", 
    page_icon="🚗", 
    layout="wide"
)

st.title("🚗 Asesor Inteligente de Vehículos")
st.write("Responde al cuestionario para recibir una recomendación personalizada del vehículo ideal para ti (SUV, Sedán o Pickup).")

# 2. Recuperación prioritaria de la API Key (Secrets > Fallback directo)
API_KEY = None
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    API_KEY = "AQ.Ab8RN6J2V4zNvQVCoZdsPCUg5_2AYYwqqvo_gGgQB1lFilJVcQ"

st.subheader("📋 Cuestionario de Necesidades")

col1, col2 = st.columns(2)

with col1:
    uso_principal = st.selectbox(
        "¿Cuál será el uso principal del vehículo?",
        [
            "Ciudad y trayectos diarios al trabajo",
            "Viajes familiares y comodidad en carretera",
            "Trabajo pesado, carga y transporte de materiales",
            "Aventura todoterreno (Off-road) y terrenos difíciles",
            "Uso mixto (Ciudad, viajes el fin de semana y algo de carga)"
        ]
    )
    
    pasajeros = st.radio(
        "¿Cuántas personas viajarán frecuentemente?",
        ["1 a 2 personas", "3 a 5 personas", "6 a 8 personas (Familia numerosa)"]
    )

    prioridad_confort = st.multiselect(
        "¿Qué características de CONFORT y TECNOLOGÍA valoras más?",
        [
            "Asientos de cuero y ergonomía superior",
            "Pantalla multimedia grande y conectividad (Apple CarPlay / Android Auto)",
            "Aislamiento acústico (cabina silenciosa)",
            "Suspensión suave para baches y mal camino",
            "Climatizador bizona o trizona",
            "Asistencias de conducción (frenado autónomo, control crucero adaptativo)"
        ]
    )

with col2:
    necesidad_carga = st.selectbox(
        "¿Qué nivel de capacidad de carga o maletero necesitas?",
        [
            "Maletero estándar para compras y equipaje ligero",
            "Maletero amplio para varias maletas y coche de bebé",
            "Tolva/Caja abierta para materiales, herramientas o equipos grandes",
            "Capacidad de remolque de carga pesada"
        ]
    )

    terreno = st.select_slider(
        "¿Por qué tipo de terreno circularás habitualmente?",
        options=["Pista / Asfalto urbano", "Carretera y trocha ligera", "Caminos afirmados / Calaminita", "Todoterreno extremo (Barro, rocas, arena)"]
    )

    prioridad_general = st.multiselect(
        "¿Qué aspectos son INDISPENSABLES para ti?",
        [
            "Economía de combustible / Bajo consumo",
            "Facilidad para estacionar en la ciudad",
            "Potencia y respuesta del motor",
            "Tracción 4x4 o AWD",
            "Durabilidad y bajo costo de mantenimiento",
            "Diseño elegante / Estatus social"
        ]
    )

presupuesto = st.text_input("Presupuesto aproximado (opcional, ej. $20,000 - $35,000 USD):", "")
comentarios_extra = st.text_area("¿Algún otro detalle o marca de tu preferencia?", "")

# Función de ejecución optimizada con doble canal
def generar_recomendacion(prompt_text, key):
    # Intento 1: Uso del SDK oficial 'google-genai'
    try:
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt_text
        )
        if response and hasattr(response, 'text') and response.text:
            return response.text
    except Exception:
        pass

    # Intento 2: Petición HTTP directa pasando la clave por consulta (REST Fallback)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}

    res = requests.post(url, json=payload, headers=headers)
    res_data = res.json()

    if res.status_code == 200 and 'candidates' in res_data:
        return res_data['candidates'][0]['content']['parts'][0]['text']
    else:
        error_msg = res_data.get('error', {}).get('message', 'Error de autenticación desconocido.')
        raise Exception(f"Código {res.status_code}: {error_msg}")

# Botón para procesar la recomendación
if st.button("🔍 Analizar y Recomendar Vehículo Ideal"):
    with st.spinner("Evaluando tu perfil y conectando con el modelo Gemini..."):
        prompt = f"""
        Actúa como un experto consultor automotriz. Analiza las siguientes necesidades de un comprador y genera un informe detallado con la recomendación ideal.

        **Perfil del Cliente:**
        - **Uso principal:** {uso_principal}
        - **Pasajeros:** {pasajeros}
        - **Preferencias de Confort:** {', '.join(prioridad_confort) if prioridad_confort else 'No especificó'}
        - **Capacidad de carga:** {necesidad_carga}
        - **Terreno habitual:** {terreno}
        - **Prioridades indispensables:** {', '.join(prioridad_general) if prioridad_general else 'No especificó'}
        - **Presupuesto:** {presupuesto if presupuesto else 'No especificado'}
        - **Comentarios adicionales:** {comentarios_extra if comentarios_extra else 'Ninguno'}

        **Estructura de la Respuesta:**
        1. **Categoría Recomendada:** Determina con claridad si le conviene un SEDÁN, un SUV o una PICKUP (o un crossover) y explica brevemente POR QUÉ.
        2. **Modelos Específicos Recomendados (Dar al menos 3 opciones principales de distintas marcas):**
           - Menciona Marca y Modelo.
           - Puntos fuertes según su perfil (destacando el confort, espacio o tracción según eligió).
        3. **Análisis de Confort y Desempeño:** Cómo cada opción satisface sus preferencias de confort y terreno.
        4. **Pros y Contras de la Categoría Seleccionada:** Para que el usuario tome una decisión informada.
        """

        try:
            resultado = generar_recomendacion(prompt, API_KEY)
            st.success("¡Análisis completado!")
            st.markdown("---")
            st.write(resultado)
        except Exception as e:
            st.error(f"Error al procesar la recomendación: {e}")
