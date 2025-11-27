import streamlit as st
import google.generativeai as genai
import os

# ------------------------------------
# CONFIGURACIÓN DE LA APP
# ------------------------------------
st.set_page_config(page_title="EcoGuía Pro", page_icon="♻️", layout="centered")

# Pega tu API Key aquí (He mantenido la variable lista para que funcione)
CLAVE_GOOGLE = os.getenv("CLAVE_GOOGLE")
genai.configure(api_key=CLAVE_GOOGLE)

# ------------------------------------
# ESTILOS CSS (DISEÑO VISUAL)
# ------------------------------------
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: #f8f9f; }
    
    /* Títulos */
    h1 { color: #2e7d32; text-align: center; font-family: 'Helvetica', sans-serif; font-weight: 800; }
    h3 { margin-bottom: 0; }
    
    /* Input de texto */
    .stTextInput>div>div>input {
        border-radius: 12px; border: 1px solid #ced4da; padding: 12px;
    }
    
    /* Botón Principal */
    .stButton>button {
        background-color: #2e7d32; color: white; border-radius: 12px;
        height: 50px; width: 100%; font-size: 18px; font-weight: bold; border: none;
        transition: 0.3s box-shadow;
    }
    .stButton>button:hover {
        background-color: #1b5e20; box-shadow: 0 4px 12px rgba(46, 125, 50, 0.4);
    }
    
    /* Caja de Resultado (La respuesta de la IA) */
    .resultado-card {
        padding: 30px; border-radius: 20px; text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1); margin-top: 20px;
        animation: fadeIn 0.8s;
    }
    
    /* Tarjetas de la Guía (Abajo) */
    .guia-card {
        padding: 15px; border-radius: 10px; text-align: center;
        height: 180px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .guia-card:hover { transform: translateY(-5px); }
    .guia-titulo { font-weight: bold; font-size: 16px; margin-top: 10px; color: #333; }
    .guia-desc { font-size: 12px; color: #666; margin-top: 5px; line-height: 1.2; }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------
# LÓGICA INTELIGENTE
# ------------------------------------
def clasificar_residuo(residuo):
    prompt = f"""
    Eres un experto en reciclaje (Norma Técnica Colombiana y Estándar Global). 
    Clasifica el residuo: "{residuo}".
    
    Responde ÚNICAMENTE con este formato exacto:
    CATEGORIA|COLOR|EXPLICACIÓN CORTA|EMOJI
    
    Las opciones posibles son:
    - Orgánicos|Verde|Restos de comida y desechos agrícolas.|🍏
    - Papel y Cartón|Azul|Limpio, seco y sin grasa.|📘
    - Plástico/Vidrio/Metal|Blanco|Materiales reciclables limpios.|🧴
    - No Reciclables|Negro|Papel sucio, servilletas, cartón engrasado.|⬛
    - Peligrosos|Rojo|Riesgo biológico, químicos o baterías.|⚠️

     Luego da una explicación corta, utiliza esta tipografia de letra font-size: 18px, Negra; .
    """

    try:
        # Usamos 1.5-flash porque es más rápido y estable para cuentas gratis
        modelo = genai.GenerativeModel("gemini-2.5-flash")
        respuesta = modelo.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        return f"ERROR: {str(e)}"

# ------------------------------------
# INTERFAZ DE USUARIO
# ------------------------------------

# Encabezado
st.title("🌱 EcoGuía Inteligente")
st.markdown("<p style='text-align: center; color: #555; font-size: 18px;'>Tu asistente virtual para el reciclaje correcto.</p>", unsafe_allow_html=True)
st.write("") # Espacio

# Zona de Interacción
col_input, col_btn = st.columns([3, 1])

with col_input:
    residuo = st.text_input("Ingresa el residuo aquí:", placeholder="Ej: Caja de pizza, pila, cáscara de huevo...", label_visibility="collapsed")

with col_btn:
    boton = st.button("🔍 CLASIFICAR")

# Lógica del Botón
if boton:
    if not residuo:
        st.warning("⚠️ Por favor escribe un residuo primero.")
    else:
        with st.spinner("🧠 La IA está analizando el material..."):
            resultado_raw = clasificar_residuo(residuo)

            if "ERROR" in resultado_raw:
                st.error("Hubo un problema de conexión. Intenta de nuevo.")
            else:
                # Procesamos la respuesta (separamos por las barritas |)
                try:
                    partes = resultado_raw.split('|')
                    categoria = partes[0]
                    color_nombre = partes[1]
                    explicacion = partes[2]
                    emoji = partes[3]

                    # Mapeo de colores hexadecimales para el diseño
                    mapa_colores = {
                        "Verde": "#d1e7dd", "Azul": "#cff4fc", 
                        "Blanco": "#ffffff", "Negro": "#e2e3e5", 
                        "Rojo": "#f8d7da"
                    }
                    bg_color = mapa_colores.get(color_nombre, "#eee")
                    
                    # Mostrar Tarjeta de Resultado Grande
                    st.markdown(f"""
                    <div class="resultado-card" style="background-color: {bg_color}; border: 2px solid rgba(0,0,0,0.1);">
                        <div style="font-size: 60px; margin-bottom: 10px;">{emoji}</div>
                        <h2 style="color: #333; margin: 0;">{categoria}</h2>
                        <h4 style="color: #555; text-transform: uppercase; letter-spacing: 1px; font-size: 14px; margin-top: 5px;">Caneca {color_nombre}</h4>
                        <hr style="border-top: 1px solid rgba(0,0,0,0.1); margin: 15px 0;">
                        <p style="font-size: 18px; color: #444;">{explicacion}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                except:
                    # Si la IA no respeta el formato, mostramos el texto plano
                    st.info(resultado_raw)

# ------------------------------------
# GUÍA VISUAL DE COLORES (Lo que pediste)
# ------------------------------------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.subheader("📚 Guía Rápida de Colores")
st.markdown("---")

c1, c2, c3, c4, c5 = st.columns(5)

# Definimos las tarjetas de la guía
def crear_tarjeta_guia(emoji, titulo, desc, color_fondo):
    return f"""
    <div class="guia-card" style="background-color: {color_fondo};">
        <div style="font-size: 30px;">{emoji}</div>
        <div class="guia-titulo">{titulo}</div>
        <div class="guia-desc">{desc}</div>
    </div>
    """

with c1: st.markdown(crear_tarjeta_guia("🍏", "Orgánicos", "Restos de comida, cáscaras.", "#d1e7dd"), unsafe_allow_html=True)
with c2: st.markdown(crear_tarjeta_guia("📘", "Papel/Cartón", "Limpio, seco, revistas.", "#cff4fc"), unsafe_allow_html=True)
with c3: st.markdown(crear_tarjeta_guia("🧴", "Blanco", "Plástico, vidrio, metal limpio.", "#ffffff"), unsafe_allow_html=True)
with c4: st.markdown(crear_tarjeta_guia("⬛", "No Reciclable", "Servilletas, cartón sucio.", "#e2e3e5"), unsafe_allow_html=True)
with c5: st.markdown(crear_tarjeta_guia("⚠️", "Peligrosos", "Baterías, aceites, químicos.", "#f8d7da"), unsafe_allow_html=True)

st.markdown("<br><p style='text-align: center; color: #ccc; font-size: 12px;'>Powered by Google Gemini 1.5</p>", unsafe_allow_html=True)