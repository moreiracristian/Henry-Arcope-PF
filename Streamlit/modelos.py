import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler


@st.cache_resource
def cargar_clasificador():
    return joblib.load('./Modelos_ML/modelo_rf.joblib')


@st.cache_resource
def cargar_modelo_eficiencia():
    return joblib.load('./Modelos_ML/Modelo_ML1.joblib')


@st.cache_data
def cargar_vehiculos():
    df = pd.read_parquet('./Data/Df_vfed.parquet')
    df = df[(df['Year'] > 2010) & (df['CO2 (p/mile)'] >= 0)].copy()

    def categorizar(row):
        if row['Alternative Fuel'] == 'Electricity':
            return 'Híbrido'
        elif row['Fuel'] == 'Electricity':
            return 'Eléctrico'
        elif row['Alternative Fuel'] in ['E85', 'No'] and row['Fuel'] != 'Natural Gas' and row['CO2 (p/mile)'] > 0:
            return 'Convencional'
        return 'Gas'

    df['Categoria'] = df.apply(categorizar, axis=1)
    df['Vehículo_unico'] = df['Manufacturer'] + ' ' + df['Model'] + ' ' + df['Year'].astype(str)
    return df


def _predecir_y_mostrar(df_filtrado, modelo):
    if df_filtrado.empty:
        st.warning('No se encontraron vehículos que cumplan ese criterio.')
        return
    X = df_filtrado[['Year', 'Miles per gallon (mpg)', 'CO2 (p/mile)', 'FuelCost']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    resultado = df_filtrado.copy()
    resultado['Eficiencia'] = modelo.predict(X_scaled)
    recomendados = resultado.sort_values('Eficiencia', ascending=False).head(5)
    st.session_state['dataset'] = recomendados
    st.success('Top 5 vehículos más eficientes energéticamente:')
    st.dataframe(
        recomendados[['Year', 'Vehículo_unico', 'Miles per gallon (mpg)', 'CO2 (p/mile)', 'FuelCost', 'Categoria']],
        use_container_width=True,
    )


def modelos_page():
    if 'page' not in st.session_state:
        st.session_state.page = 'Portada'

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Portada'):
            st.session_state.page = 'Portada'
    with col2:
        if st.button('Eficiencia Energética'):
            st.session_state.page = 'Eficiencia_E'

    st.markdown("""
        <style>
        .stButton>button {
            background-color: #333333;
            color: white;
            border: none;
            padding: 10px 24px;
            font-size: 18px;
            cursor: pointer;
            transition-duration: 0.3s;
            border-radius: 12px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: white;
            color: black;
            border: 2px solid #333333;
        }
        </style>
    """, unsafe_allow_html=True)

    # ── PORTADA ────────────────────────────────────────────────────────────────
    if st.session_state.page == 'Portada':
        st.markdown("""
        <div style="font-size:44px; color:#FFFFFF; font-weight:bold; text-align:center;
                    padding:20px; background-color:#000000; border-radius:10px;
                    box-shadow:2px 2px 12px rgba(0,0,0,0.2); margin-bottom:20px;">
            Plataforma de Vehículos Eficientes
        </div>
        """, unsafe_allow_html=True)

        st.write("""
            Esta plataforma usa modelos de machine learning entrenados sobre datos reales
            para recomendar vehículos eficientes y calcular ahorros operativos concretos.
        """)

        # ── Métricas del modelo ───────────────────────────────────────────────
        st.markdown("---")
        st.markdown("#### Métricas del Clasificador de Tipo de Vehículo")
        st.caption("RandomForestClassifier · `costo_operacional_vehiculos_clean.csv` · test_size=0.30 · random_state=42")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Accuracy", "90%")
        c2.metric("Registros totales", "3,813")
        c3.metric("Split de prueba", "30%")
        c4.metric("Clases", "3")

        st.markdown("---")

        # ── Feature importance ────────────────────────────────────────────────
        try:
            clf = cargar_clasificador()
            features = ['Fuel_Cost', 'Electric_Cost', 'Noise_Level']
            importances = clf.feature_importances_.tolist()
            fig = px.bar(
                x=importances,
                y=features,
                orientation='h',
                labels={'x': 'Importancia relativa', 'y': 'Variable'},
                title='Importancia de Variables — Clasificador de Tipo de Vehículo',
                color=importances,
                color_continuous_scale='Greens',
            )
            fig.update_layout(
                showlegend=False,
                coloraxis_showscale=False,
                height=260,
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.info("Gráfico de importancia no disponible (modelo no encontrado).")

        # ── Distribución del dataset ──────────────────────────────────────────
        st.markdown("---")
        dist_data = {
            'Tipo': ['Convencional', 'Híbrido', 'Eléctrico'],
            'Registros': [2710, 884, 219],
        }
        fig2 = px.pie(
            dist_data,
            names='Tipo',
            values='Registros',
            title='Distribución de vehículos en el dataset de entrenamiento',
            color_discrete_sequence=['#636EFA', '#00CC96', '#EF553B'],
            hole=0.4,
        )
        fig2.update_layout(height=300, margin=dict(t=40, b=10))
        st.plotly_chart(fig2, use_container_width=True)

        # ── Descripción de cada modelo ────────────────────────────────────────
        st.markdown("---")
        st.markdown("<h3 style='text-align:center;'>Modelos disponibles</h3>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Eficiencia Energética**")
            st.write(
                "Recomienda los 5 vehículos más eficientes filtrados por fabricante y año, "
                "priorizando bajo consumo, menor costo operativo y mínimas emisiones de CO₂."
            )
        with col_b:
            st.markdown("**Maximización Operativa** *(próximamente)*")
            st.write(
                "Identifica vehículos con menores costos operativos totales y predice "
                "su valor de reventa para decisiones de costo-beneficio a largo plazo."
            )

    # ── EFICIENCIA ENERGÉTICA ─────────────────────────────────────────────────
    elif st.session_state.page == 'Eficiencia_E':
        st.title("Recomendador de Vehículos Eficientes")
        st.write("Filtrá por año y fabricante para ver los 5 vehículos con mejor eficiencia energética.")

        try:
            modelo = cargar_modelo_eficiencia()
            df_vehiculos = cargar_vehiculos()
        except Exception as e:
            st.error(f"No se pudo cargar el modelo o los datos: {e}")
            return

        marcas = ['Todos'] + sorted(df_vehiculos['Manufacturer'].unique().tolist())
        anios = ['Todos'] + list(range(2023, 2010, -1))

        col1, col2 = st.columns(2)
        with col1:
            año = st.selectbox('Año del vehículo', anios)
        with col2:
            fabricante = st.selectbox('Marca del vehículo', marcas)

        if st.button('Obtener recomendación', type='primary'):
            filtro = df_vehiculos.copy()
            if año != 'Todos':
                filtro = filtro[filtro['Year'] == año]
            if fabricante != 'Todos':
                filtro = filtro[filtro['Manufacturer'] == fabricante]
            _predecir_y_mostrar(filtro, modelo)

        # ── Simulador de consumo ──────────────────────────────────────────────
        st.markdown("---")
        st.subheader('Simulador de consumo por kilómetros')

        if 'dataset' in st.session_state and not st.session_state['dataset'].empty:
            dataset = st.session_state['dataset']
            opciones = ['— Seleccioná un vehículo —'] + dataset['Vehículo_unico'].tolist()
            seleccion = st.selectbox('Vehículo:', opciones)

            if seleccion != '— Seleccioná un vehículo —':
                v = dataset[dataset['Vehículo_unico'] == seleccion].iloc[0]

                m1, m2, m3 = st.columns(3)
                m1.metric("Costo combustible/galón", f"${v['FuelCost']:.2f} US")
                m2.metric("CO₂ por milla", f"{v['CO2 (p/mile)']:.1f} g")
                m3.metric("Millas por galón", f"{v['Miles per gallon (mpg)']:.1f} mpg")
                st.caption(f"Categoría: **{v['Categoria']}** · Año: **{int(v['Year'])}**")

                km = st.number_input('Kilómetros a recorrer', min_value=0, max_value=1_000_000, step=100)
                if km > 0:
                    km_por_litro = v['Miles per gallon (mpg)'] * 0.425144
                    litros = km / km_por_litro
                    costo = litros * v['FuelCost']
                    co2 = km * (v['CO2 (p/mile)'] / 1.60934)

                    r1, r2, r3 = st.columns(3)
                    r1.metric("Combustible usado", f"{litros:.1f} L")
                    r2.metric("Costo total", f"${costo:.2f} US")
                    r3.metric("CO₂ emitido", f"{co2:,.0f} g")
        else:
            st.info("Generá una recomendación primero para usar el simulador.")
