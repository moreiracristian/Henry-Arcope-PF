import os
import streamlit as st
from groq import Groq


def _get_client():
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass
    if not api_key:
        return None
    return Groq(api_key=api_key)


def _get_ai_response(client, messages):
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=messages,
        temperature=0.5,
        max_tokens=512,
    )
    try:
        return completion.choices[0].message.content
    except AttributeError:
        return "Error al procesar la respuesta."


def _build_system_prompt(user_type):
    return (
        f"Sos un asistente virtual para {user_type}s de Uber en Nueva York. "
        "El proyecto ARCOPE analiza datos de viajes, calidad del aire y costos operacionales "
        "para ayudar a Uber a migrar hacia una flota más sustentable (vehículos eléctricos e híbridos). "
        "Respondé siempre en español, de forma concisa y útil. "
        "Si no tenés datos reales disponibles, ofrecé una respuesta coherente basada en el contexto del proyecto."
    )


PREGUNTAS = {
    "Pasajero": [
        "¿Cuál es el impacto ambiental de mis viajes en Uber?",
        "¿Hay vehículos eléctricos disponibles en mi zona?",
        "¿Cómo puedo reducir mi huella de carbono usando Uber?",
    ],
    "Conductor": [
        "¿Cuánto podría ahorrar si reemplazo mi auto por un híbrido?",
        "¿Cuál es la mejor zona para trabajar hoy con un auto eléctrico?",
        "¿Qué incentivos existen para conductores con vehículos eléctricos?",
    ],
    "Inversores / Ejecutivos": [
        "¿Cuál es el ROI estimado de migrar la flota a eléctricos?",
        "¿Qué zonas de NYC muestran mayor rentabilidad por milla?",
        "¿Cómo afecta la calidad del aire a la imagen de Uber en NYC?",
    ],
}


def chatbot_page():
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; }
        .chat-bubble-user {
            background: #f0f0f0; border-radius: 12px 12px 2px 12px;
            padding: 10px 14px; margin: 6px 0; max-width: 80%;
            margin-left: auto; text-align: right;
        }
        .chat-bubble-bot {
            background: #000000; color: #ffffff;
            border-radius: 12px 12px 12px 2px;
            padding: 10px 14px; margin: 6px 0; max-width: 80%;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Asistente Virtual ARCOPE")
    st.caption("Consultá sobre sostenibilidad, eficiencia de flota y rentabilidad de Uber en NYC.")

    client = _get_client()
    if client is None:
        st.warning(
            "**GROQ_API_KEY no configurada.**\n\n"
            "Para activar el chatbot, creá el archivo `.streamlit/secrets.toml` con:\n"
            "```toml\nGROQ_API_KEY = 'tu_api_key'\n```\n"
            "O definí la variable de entorno `GROQ_API_KEY` antes de iniciar la app.\n\n"
            "Podés obtener una clave gratuita en [console.groq.com](https://console.groq.com/keys)."
        )
        return

    # Inicializar estado
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    if "chatbot_role" not in st.session_state:
        st.session_state.chatbot_role = "Pasajero"

    # Selector de rol
    role = st.selectbox(
        "Tu rol:",
        list(PREGUNTAS.keys()),
        index=list(PREGUNTAS.keys()).index(st.session_state.chatbot_role),
    )
    if role != st.session_state.chatbot_role:
        st.session_state.chatbot_role = role
        st.session_state.chatbot_messages = []
        st.rerun()

    # Historial de conversación
    if st.session_state.chatbot_messages:
        st.markdown("---")
        for msg in st.session_state.chatbot_messages:
            st.markdown(
                f"<div class='chat-bubble-user'>👤 {msg['user']}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='chat-bubble-bot'>🤖 {msg['response']}</div>",
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Preguntas sugeridas
    pregunta_sugerida = st.selectbox(
        "Preguntas frecuentes:",
        ["— Escribí tu propia pregunta abajo —"] + PREGUNTAS[role],
    )

    pregunta_custom = st.text_input("O escribí tu pregunta:", placeholder="Ej: ¿Qué zonas tienen mayor demanda de noche?")

    col_send, col_clear = st.columns([3, 1])
    with col_send:
        enviar = st.button("Enviar", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Limpiar", use_container_width=True):
            st.session_state.chatbot_messages = []
            st.rerun()

    if enviar:
        pregunta = pregunta_custom.strip() if pregunta_custom.strip() else (
            pregunta_sugerida if pregunta_sugerida != "— Escribí tu propia pregunta abajo —" else ""
        )
        if not pregunta:
            st.warning("Escribí o seleccioná una pregunta antes de enviar.")
            return

        # Construir contexto para la API
        messages = [{"role": "system", "content": _build_system_prompt(role)}]
        for msg in st.session_state.chatbot_messages[-6:]:  # últimos 3 turnos
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["response"]})
        messages.append({"role": "user", "content": pregunta})

        with st.spinner("Pensando..."):
            respuesta = _get_ai_response(client, messages)

        st.session_state.chatbot_messages.append({"user": pregunta, "response": respuesta})
        st.rerun()
