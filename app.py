import streamlit as st
import google.genai as genai

# Configuración de la página web
st.set_page_config(page_title="Asesor Inteligente de Vehículos", page_icon="🚗", layout="wide")

st.title("🚗 Asesor Inteligente de Vehículos")
st.write("Responde al cuestionario para recibir una recomendación personalizada del vehículo ideal para ti (SUV, Sedán o Pickup).")

# Clave de API de Gemini
API_KEY = "AQ.Ab8RN6JsTnQjteHz2oFWOMqTSYTCTrfiuVCddI4e5Kgz2YU8Gw"
client = genai.Client(api_key=API_KEY)

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

# Botón para procesar la recomendación
if st.button("🔍 Analizar y Recomendar Vehículo Ideal"):
    with st.spinner("Gemini está evaluando tu perfil y seleccionando las mejores opciones..."):
        try:
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

            respuesta = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt]
            )

            st.success("¡Análisis completado!")
            st.markdown("---")
            st.write(respuesta.text)

        except Exception as e:
            st.error(f"Error al procesar la solicitud: {e}")
