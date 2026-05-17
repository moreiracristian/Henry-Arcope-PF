import streamlit as st
import base64


def get_image_b64(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return None


def acercaDe_page():
    st.markdown("""
        <style>
        .stApp { background-color: whitesmoke; }
        h1 { color: #F25A38; }
        h2 { color: #F25041; }
        h3 { color: #000000; }
        .rainbow-hr {
            border: none; height: 4px;
            background: linear-gradient(to right, #F25A38, #F2A649, #56B5BF, #F25041);
            margin: 24px 0;
        }
        .team-card {
            background: white;
            border-radius: 12px;
            padding: 20px 10px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── Logo + Título ──────────────────────────────────────────────────────────
    logo = get_image_b64('./Streamlit/images/arcope-logo.jpeg')
    if logo:
        st.markdown(
            f"<div style='text-align:center; padding: 10px 0 4px;'>"
            f"<img src='data:image/jpeg;base64,{logo}' width='160' style='border-radius:12px;'/></div>",
            unsafe_allow_html=True
        )

    st.markdown("<h1 style='text-align:center;'>ARCOPE — Proyecto Final Henry</h1>", unsafe_allow_html=True)
    st.markdown("<div class='rainbow-hr'></div>", unsafe_allow_html=True)

    # ── Problema y Solución ────────────────────────────────────────────────────
    col_prob, col_sol = st.columns(2, gap="large")

    with col_prob:
        st.markdown("### El Problema")
        st.write(
            "Uber opera miles de vehículos en NYC con una flota mayoritariamente de combustión interna: "
            "altos costos operativos, emisiones crecientes y presión regulatoria en ascenso. "
            "Sin datos claros, es difícil justificar ante accionistas la transición a vehículos eléctricos."
        )

    with col_sol:
        st.markdown("### La Solución")
        st.write(
            "Un **Data Product end-to-end** que procesa datos reales de viajes TLC, calidad del aire "
            "y costos operacionales para responder: ¿cuánto CO₂ ahorramos?, ¿es rentable la transición?, "
            "¿cómo maximizar la flota actual?"
        )

    st.markdown("<div class='rainbow-hr'></div>", unsafe_allow_html=True)

    # ── KPIs ──────────────────────────────────────────────────────────────────
    st.markdown("### KPIs del Proyecto")

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown("**KPI 1 — Sostenibilidad**")
        st.markdown("Reducción de CO₂ comparando flota actual vs eléctrica/híbrida por zona y período.")
        st.code("CO₂_actual vs CO₂_flota_eléctrica\n(g/milla × millas_totales)")
    with k2:
        st.markdown("**KPI 2 — Rentabilidad**")
        st.markdown("Ingresos netos por milla para identificar zonas y horarios más rentables.")
        st.code("(Total - Peajes - Cargos) / Trip_distance")
    with k3:
        st.markdown("**KPI 3 — Eficiencia Operativa**")
        st.markdown("Tasa de utilización de vehículos y promedio de pasajeros por viaje.")
        st.code("Viajes / Horas_disponibles\nAvg(Passengers) por zona y hora")

    st.markdown("<div class='rainbow-hr'></div>", unsafe_allow_html=True)

    # ── Stack Tecnológico ──────────────────────────────────────────────────────
    st.markdown("### Stack Tecnológico")

    st.markdown("""
    <style>
    .stack-table table { width: 100%; border-collapse: collapse; }
    .stack-table th { background-color: #111; color: white; padding: 10px; text-align: left; }
    .stack-table td { padding: 10px; border-bottom: 1px solid #ddd; }
    .stack-table tr:nth-child(even) { background-color: #f5f5f5; }
    </style>
    <div class="stack-table">
    <table>
        <tr><th>Fase</th><th>Herramientas</th></tr>
        <tr><td>Ingesta & ETL</td><td>Python · Pandas · PyArrow · MinIO</td></tr>
        <tr><td>Data Warehouse</td><td>MySQL · SQLAlchemy · phpMyAdmin</td></tr>
        <tr><td>Machine Learning</td><td>scikit-learn · Random Forest · Joblib</td></tr>
        <tr><td>Visualización</td><td>Plotly · Matplotlib · Seaborn · Streamlit</td></tr>
        <tr><td>IA Conversacional</td><td>Groq API (LLaMA 3.1 70B)</td></tr>
        <tr><td>Orquestación</td><td>Apache Airflow</td></tr>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='rainbow-hr'></div>", unsafe_allow_html=True)

    # ── Equipo ─────────────────────────────────────────────────────────────────
    st.markdown("<h2 style='text-align:center;'>Equipo</h2>", unsafe_allow_html=True)

    personas = [
        {
            "nombre": "Cristian Moreira",
            "rol": "Project Manager",
            "github": "https://github.com/moreiracristian",
            "linkedin": "https://www.linkedin.com/in/moreiracristian/",
            "imagen": "./Streamlit/images/cristian.jpeg",
        },
        {
            "nombre": "Andrés Aguirre",
            "rol": "TPM & Data Analytics",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen": "./Streamlit/images/andres.jpeg",
        },
        {
            "nombre": "Jeison Zapata",
            "rol": "Data Scientist & Analyst",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen": "./Streamlit/images/jeison.jpeg",
        },
        {
            "nombre": "Libardo Alarcon",
            "rol": "Data Scientist",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen": "./Streamlit/images/libardo.jpeg",
        },
        {
            "nombre": "Manuel Carruitero",
            "rol": "Data Engineer",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen": "./Streamlit/images/manuel.jpeg",
        },
        {
            "nombre": "Lucas Carranza",
            "rol": "Data Engineer",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen": "./Streamlit/images/lucas.jpeg",
        },
    ]

    linkedin_logo = get_image_b64("./Streamlit/images/LI-In-Bug.png")
    github_logo = get_image_b64("./Streamlit/images/github-mark-white.png")

    cols = st.columns(3)
    for i, persona in enumerate(personas):
        with cols[i % 3]:
            foto = get_image_b64(persona["imagen"])
            foto_html = (
                f"<img src='data:image/jpeg;base64,{foto}' width='100' "
                f"style='border-radius:50%; margin-bottom:10px;'/>"
                if foto else "<div style='height:100px;'></div>"
            )
            li_html = (
                f"<a href='{persona['linkedin']}' target='_blank'>"
                f"<img src='data:image/png;base64,{linkedin_logo}' width='26' style='margin-right:8px;'/></a>"
                if linkedin_logo else ""
            )
            gh_html = (
                f"<a href='{persona['github']}' target='_blank'>"
                f"<img src='data:image/png;base64,{github_logo}' width='26'/></a>"
                if github_logo else ""
            )
            st.markdown(f"""
                <div class='team-card'>
                    {foto_html}
                    <p style='font-weight:bold; font-size:16px; margin:4px 0;'>{persona['nombre']}</p>
                    <p style='color:gray; font-size:13px; margin:0 0 12px;'>{persona['rol']}</p>
                    <div>{li_html}{gh_html}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='rainbow-hr'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center; color:gray; font-size:13px;'>"
        "Proyecto Final · Henry Data Science Bootcamp · 2024</p>",
        unsafe_allow_html=True
    )
