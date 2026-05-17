import streamlit as st
import pandas as pd
import plotly.express as px

# Definir función principal para manejar pestañas
def dashboard_page():
    
# Estilo CSS para ocultar la barra lateral
    

    # Encabezado principal con formato
    st.markdown("""
    # Presentación Interactiva de Análisis de Datos 📊
    Este dashboard interactivo presenta diferentes análisis relacionados con precios de reventa de autos, viajes en taxis amarillos, costos operacionales de vehículos y KPIs relacionados con eficiencia y costos.
    Navega por los diferentes análisis para explorar las gráficas y análisis asociados. Utiliza el menú lateral para seleccionar y visualizar cada uno.
    """, unsafe_allow_html=True)

    # Sidebar para la selección de análisis (pestañas)
    st.sidebar.header("Selecciona un Análisis:")
    analisis = st.sidebar.selectbox(
        'Selecciona el análisis',
        ('Análisis de Precios de Reventa de Autos',
         'Análisis de Viajes FHV (Uber)',
         'Análisis de Costos Operacionales de Vehículos',
         'KPIs de Eficiencia y Costos Operacionales')
    )

    try:
        df_car_resale = pd.read_csv('./Data/car_resale_prices_clean.csv')
        df_vehicle_costs = pd.read_csv('./Data/costo_operacional_vehiculos_clean.csv')
    except Exception as e:
        st.error(f"Error al cargar los datasets: {e}")
        return

    # Sección 1: Análisis de Precios de Reventa de Autos
    if analisis == 'Análisis de Precios de Reventa de Autos':
        st.header('📈 Análisis de Precios de Reventa de Autos')
        st.markdown("""
        Descripción: Este análisis muestra la distribución de los precios de reventa de autos por año de registro y permite filtrar autos según el presupuesto.
        """)

        # Crear una nueva columna para agrupar los años en rangos de 5 años
        df_car_resale['Year_Category'] = pd.cut(df_car_resale['Registered_Year'],
                                                bins=[1990, 1995, 2000, 2005, 2010, 2015, 2020],
                                                labels=['1990-1995', '1996-2000', '2001-2005', '2006-2010', '2011-2015', '2016-2020'])

        # Layout mejorado: Usamos columnas para mostrar gráficas y filtros
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Distribución de Precios de Reventa por Año de Registro")
            fig = px.box(df_car_resale, x='Registered_Year', y='Resale_Price', title="Distribución de Precios de Reventa por Año de Registro")
            fig.update_xaxes(title_text="Año de Registro")
            fig.update_yaxes(title_text="Precio de Reventa (USD)")
            st.plotly_chart(fig)

        with col2:
            st.subheader("Filtrar autos por presupuesto")
            presupuesto_cliente = st.number_input("Ingresa tu presupuesto (USD)", min_value=0, value=5000, step=1000)
            autos_recomendados = df_car_resale[df_car_resale['Resale_Price'] <= presupuesto_cliente].sort_values(by='Resale_Price').head(5)
            
            if not autos_recomendados.empty:
                st.markdown(f"### Autos recomendados dentro del presupuesto de ${presupuesto_cliente}:")
                st.dataframe(autos_recomendados[['Full_Name', 'Registered_Year', 'Resale_Price']])
            else:
                st.text(f"No se encontraron autos dentro del presupuesto de ${presupuesto_cliente}.")

    # Sección 2: Análisis de Viajes FHV (Uber)
    elif analisis == 'Análisis de Viajes FHV (Uber)':
        st.header('🚗 Análisis de Viajes FHV (For-Hire Vehicles — Uber)')
        st.markdown("Datos de viajes de vehículos de alquiler con chofer (FHV) en NYC, la categoría donde opera Uber.")

        try:
            df_fhv = pd.read_parquet('./Data/fhv_tripdata.parquet')
        except Exception as e:
            st.error(f"No se pudo cargar fhv_tripdata.parquet: {e}")
            df_fhv = None

        if df_fhv is not None:
            datetime_col = next((c for c in df_fhv.columns if 'pickup' in c.lower() and 'datetime' in c.lower()), None)
            if datetime_col:
                st.subheader("Cantidad de Viajes por Mes")
                df_fhv['pickup_month'] = pd.to_datetime(df_fhv[datetime_col], errors='coerce').dt.to_period('M').astype(str)
                fig = px.histogram(df_fhv, x='pickup_month', title="Cantidad de Viajes FHV por Mes")
                fig.update_xaxes(title_text="Mes")
                fig.update_yaxes(title_text="Número de Viajes")
                st.plotly_chart(fig)
            else:
                st.info("Columna de fecha no encontrada en el dataset FHV.")

    # Sección 3: Análisis de Costos Operacionales de Vehículos
    elif analisis == 'Análisis de Costos Operacionales de Vehículos':
        st.header('🚗 Análisis de Costos Operacionales de Vehículos')
        st.markdown("""
        Descripción: Este análisis muestra los costos operacionales de vehículos según su tipo de combustible.
        """)

        # Selección de la gráfica para mostrar
        grafico_costos = st.selectbox(
            'Selecciona la gráfica para Costos Operacionales',
            ('Costos Operacionales por Tipo de Combustible',)
        )

        if grafico_costos == 'Costos Operacionales por Tipo de Combustible':
            st.subheader("Costos Operacionales por Tipo de Combustible")
            fig = px.bar(df_vehicle_costs, x='Fuel_Type', y='Fuel_Cost', title="Costos Operacionales por Tipo de Combustible")
            fig.update_xaxes(title_text="Tipo de Combustible")
            fig.update_yaxes(title_text="Costo de Combustible (GBP)")
            st.plotly_chart(fig)

            # Comparación de tipos de combustible
            st.subheader("Comparación de Costos de Combustibles")
            fuel_comparison = df_vehicle_costs.groupby('Fuel_Type')['Fuel_Cost'].mean().reset_index()
            st.table(fuel_comparison)

    # Sección 4: KPIs de Eficiencia y Costos Operacionales
    elif analisis == 'KPIs de Eficiencia y Costos Operacionales':
        st.header('📊 KPIs de Eficiencia y Costos Operacionales')
        st.markdown("Emisiones de CO₂ por tipo de combustible a lo largo del tiempo y distribución de costos operativos.")

        try:
            df_vfed = pd.read_parquet('./Data/Df_vfed.parquet')
            df_co2 = df_vfed[df_vfed['CO2 (p/mile)'] > 0].copy()
        except Exception as e:
            st.error(f"No se pudo cargar el dataset de eficiencia vehicular: {e}")
            df_co2 = None

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("CO₂ promedio por milla según año y combustible")
            if df_co2 is not None:
                co2_por_anio = (
                    df_co2.groupby(['Year', 'Fuel'])['CO2 (p/mile)']
                    .mean()
                    .reset_index()
                )
                fuels_principales = ['Regular Gasoline', 'Premium Gasoline', 'Diesel', 'Electricity']
                co2_filtrado = co2_por_anio[co2_por_anio['Fuel'].isin(fuels_principales)]
                fig = px.line(
                    co2_filtrado, x='Year', y='CO2 (p/mile)', color='Fuel',
                    title='CO₂ promedio por milla (2009–2024)',
                    labels={'CO2 (p/mile)': 'CO₂ (g/milla)', 'Year': 'Año', 'Fuel': 'Combustible'},
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Distribución de costos operativos por tipo de vehículo")
            fig = px.histogram(
                df_vehicle_costs, x="Total_Cost", color="Fuel_Type",
                barmode="overlay", nbins=50,
                title="Costo operativo total por tipo de combustible",
                labels={"Total_Cost": "Costo Total", "Fuel_Type": "Combustible"},
            )
            st.plotly_chart(fig, use_container_width=True)

        # Métrica resumen
        if df_co2 is not None:
            st.markdown("---")
            co2_gas = df_co2[df_co2['Fuel'].str.contains('Gasoline', na=False)]['CO2 (p/mile)'].mean()
            co2_elec = df_vfed[df_vfed['Fuel'] == 'Electricity']['CO2 (p/mile)'].mean()
            costo_conv = df_vehicle_costs[df_vehicle_costs['Fuel_Type'].isin(['Petrol', 'Diesel'])]['Total_Cost'].mean()
            costo_elec = df_vehicle_costs[df_vehicle_costs['Fuel_Type'] == 'Electricity']['Total_Cost'].mean()

            m1, m2, m3, m4 = st.columns(4)
            co2_elec_val = 0.0 if (co2_elec != co2_elec or co2_elec == 0) else co2_elec
            m1.metric("CO₂ promedio — Gasolina", f"{co2_gas:.0f} g/milla")
            m2.metric("CO₂ promedio — Eléctrico", f"{co2_elec_val:.0f} g/milla",
                      delta=f"{co2_elec_val - co2_gas:.0f} g/milla", delta_color="inverse")
            m3.metric("Costo op. — Convencional", f"£{costo_conv:.0f}")
            m4.metric("Costo op. — Eléctrico", f"£{costo_elec:.0f}",
                      delta=f"£{costo_elec - costo_conv:.0f}", delta_color="inverse")
