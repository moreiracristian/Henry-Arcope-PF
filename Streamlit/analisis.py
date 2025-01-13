import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
import acercaDe  # Importar la página 'home.py'
import dashboard  # Importar la página 'dashboard.py'
import modelos  # Importar la página 'modelos_ml.py'
import inicio # Importar la página 'inicio.py'
import base64

# Definir función principal para manejar pestañas
def analisis_page():
    
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
         'Análisis de Costos Operacionales de Vehículos')
    )

    # Cargar los datasets utilizando rutas relativas
    try:
        df_car_resale = pd.read_csv('./Data/car_resale_prices_clean.csv')
        df_yellow_taxi = pd.read_parquet('./Data/yellow_tripdata.parquet')
        df_vehicle_costs = pd.read_csv('./Data/costo_operacional_vehiculos_clean.csv')
    except Exception as e:
        st.error(f"Error al cargar los datasets: {e}")

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
        col1, col2 = st.columns([2, 2])

        with col1:
            st.subheader("Distribución de Precios de Reventa por Año de Registro")
            fig = px.box(df_car_resale, x='Registered_Year', y='Resale_Price', title="Distribución de Precios de Reventa por Año de Registro")
            fig.update_xaxes(title_text="Año de Registro")
            fig.update_yaxes(title_text="Precio de Reventa (USD)")
            # Ajustar el tamaño del gráfico
            fig.update_layout(width=700, height=400)  # Puedes ajustar estos valores
            
            st.plotly_chart(fig)

        with col2:
            st.subheader("Filtrar autos por presupuesto")
            presupuesto_cliente = st.number_input("Ingresa tu presupuesto (USD)", min_value=0, value=5000, step=1000)
            autos_recomendados = df_car_resale[df_car_resale['Resale_Price'] <= presupuesto_cliente].sort_values(by='Resale_Price', ascending=False).head(5)
            
            if not autos_recomendados.empty:
                st.markdown(f"### Autos recomendados dentro del presupuesto de ${presupuesto_cliente}:")
                st.dataframe(autos_recomendados[['Full_Name', 'Registered_Year', 'Resale_Price']])
            else:
                st.text(f"No se encontraron autos dentro del presupuesto de ${presupuesto_cliente}.")


    # Sección 2: Análisis de Costos Operacionales de Vehículos
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
