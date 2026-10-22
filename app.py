import streamlit as st
from google import genai
from google.genai import types

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Asistente AI - Sistemas Inteligentes",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Asistente Virtual 'Astra'")
st.caption(
    "UAdeO • Materia: Sistemas Inteligentes • Dra. Aiblis Susej Herrera Palafox"
)

# ==============================================================================
# API KEY (Protegida para GitHub usando Streamlit Secrets)
# ==============================================================================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ Falta configurar la GEMINI_API_KEY en los secretos de Streamlit Cloud.")
    st.stop()

# ==============================================================================
# CONFIGURACIÓN DEL BOT
# ==============================================================================
CONFIG_INSTRUCCIONES = types.GenerateContentConfig(
    system_instruction=(
        "Eres Astra, un asistente académico inteligente, formal y estructurado "
        "para la materia Sistemas Inteligentes de la UAdeO. "
        "Tu objetivo es explicar conceptos de Inteligencia Artificial, "
        "Agentes y Redes Neuronales de forma clara y accesible. "
        "Si preguntan por entregas o fechas, indica amablemente que deben "
        "consultar a la Dra. Aiblis Susej Herrera Palafox."
    ),
    temperature=0.7
)

# ==============================================================================
# CLIENTE GEMINI
# ==============================================================================
if (
    "client" not in st.session_state
    or st.session_state.get("current_api_key") != api_key
):
    st.session_state.client = genai.Client(api_key=api_key)
    st.session_state.current_api_key = api_key
    st.session_state.chat_session = (
        st.session_state.client.chats.create(
            model="gemini-2.5-flash",  # Actualizado al modelo estándar estable
            config=CONFIG_INSTRUCCIONES
        )
    )

# ==============================================================================
# HISTORIAL
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 ¡Hola! Soy Astra. ¿En qué tema de Sistemas Inteligentes te puedo ayudar hoy?"
        }
    ]

# ==============================================================================
# SIDEBAR
# ==============================================================================
with st.sidebar:
    st.header("⚙️ Opciones del Agente")
    st.markdown("Modelo backend: **Gemini 2.5 Flash**")

    if st.button("🧹 Limpiar Conversación"):
        st.session_state.chat_session = (
            st.session_state.client.chats.create(
                model="gemini-2.5-flash",
                config=CONFIG_INSTRUCCIONES
            )
        )
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "🧹 La sesión ha sido reiniciada. ¿Qué otra duda tienes?"
            }
        ]
        st.rerun()

# ==============================================================================
# MOSTRAR MENSAJES
# ==============================================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==============================================================================
# CHAT
# ==============================================================================
if user_input := st.chat_input("Escribe tu pregunta o duda aquí..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Pensando respuesta..."):
            try:
                response = st.session_state.chat_session.send_message(
                    user_input
                )
                st.markdown(response.text)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response.text
                    }
                )
            except Exception as e:
                st.error(f"❌ Error al consultar la API: {e}")