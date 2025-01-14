import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Cache de datos para mejorar el rendimiento
@st.cache_data
def get_data(dataset: str):
    if dataset == 'trips':
        # Cargar los datos de trips
        trips = pd.read_parquet('etl_minio/trips.parquet')
        # Asegurarse de que la columna de fecha está en formato datetime
        trips['pickup_datetime'] = pd.to_datetime(trips['pickup_datetime'])
        # Crear la columna 'day_of_week' basada en la fecha del viaje
        trips['day_of_week'] = trips['pickup_datetime'].dt.day_name()
        return trips

    elif dataset == 'vehicles':
        # Cargar los datos de vehicles
        vehicles = pd.read_parquet('etl_minio/vehicles.parquet')
        return vehicles
    elif dataset == 'air':
        air= pd.read_parquet('etl_minio/air_quality_measurement.parquet')
        return air
    elif dataset == 'fuel' :
        fuel =pd.read_parquet('etl_minio/fuel_economy_data.parquet')
        return fuel
    else:
        raise ValueError("El parámetro dataset debe ser 'trips' o 'vehicles'")

# Función para categorizar los vehículos en función de su tipo de combustible
def categorize_vehicle(co2_value):
    if co2_value <= 0:
        return 'electrico'
    elif co2_value <= 200:
        return 'hibrido'
    else:
        return 'convencional'

# Función para calcular el KPI de emisiones evitadas
def calculate_kpi_emisiones(fuel, manufacturer_filter, millas_min, millas_max):
    
        # Valores fijos de emisiones por milla de electricidad (en g/milla)
    emisiones_electricas = 120  # promedio de 120 g CO2/milla para eléctricos
    emisiones_hibrido = 200  # promedio de 200 g CO2/milla para híbridos
    
    # Aplicar la categorización al dataset
    fuel['tipo_vehiculo'] = fuel['co2_per_mile'].apply(categorize_vehicle)

    # Filtrar por manufacturer y millas recorridas
    fuel_filtered = fuel[(fuel['manufacturer'] == manufacturer_filter) & 
                         (fuel['miles_per_gallon'] >= millas_min) & 
                         (fuel['miles_per_gallon'] <= millas_max)]

    # Sumar las millas recorridas por cada tipo de vehículo
    millas_convencional = fuel_filtered.loc[fuel_filtered['tipo_vehiculo'] == 'convencional', 'miles_per_gallon'].sum()
    millas_electrico = fuel_filtered.loc[fuel_filtered['tipo_vehiculo'] == 'electrico', 'miles_per_gallon'].sum()
    millas_hibrido = fuel_filtered.loc[fuel_filtered['tipo_vehiculo'] == 'hibrido', 'miles_per_gallon'].sum()
    millas_totales = millas_convencional + millas_electrico + millas_hibrido

    if millas_totales == 0:
        return 0  # Evitar divisiones por 0

    # Emisiones evitadas (por milla) al utilizar eléctricos o híbridos
    reduccion_co2_electrico = fuel_filtered.loc[fuel_filtered['tipo_vehiculo'] == 'electrico', 'co2_per_mile'].apply(lambda x: (fuel['co2_per_mile'].max() - (x + emisiones_electricas)) / fuel['co2_per_mile'].max())
    reduccion_co2_hibrido = fuel_filtered.loc[fuel_filtered['tipo_vehiculo'] == 'hibrido', 'co2_per_mile'].apply(lambda x: (fuel['co2_per_mile'].max() - (x + emisiones_hibrido)) / fuel['co2_per_mile'].max())

    # Cálculo del KPI ajustado
    kpi_value1 = ((reduccion_co2_electrico.sum() * millas_electrico + reduccion_co2_hibrido.sum() * millas_hibrido) / millas_totales) * 100 
    return kpi_value1 # KPI en porcentaje

# Función para calcular el KPI
def calculate_kpi(trips_data):
    total_amount_sum = trips_data['total_amount'].sum()
    trip_distance_sum = trips_data['trip_distance'].sum()

    if trip_distance_sum == 0:
        return 0  # Evitar divisiones por 0

    kpi_value = (total_amount_sum / trip_distance_sum) * 100
    return kpi_value

# Función para mostrar cada KPI con su estructura
def show_kpi(title, value, objective, gauge_max, gauge_value, trend_data=None, trend_goal=None):
    # Valores predeterminados si no se dan valores de tendencia
    if trend_data is None:
        trend_data = {
            'x': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'y': [0.03, 0.04, 0.02, 0.05, 0.05, 0.03, 0.02]
        }
    if trend_goal is None:
        trend_goal = {
            'x': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'y': [0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
        }

    # Gráfico de medidor
    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, gauge_max]},
               'bar': {'color': "green"}},
    ))

    # Gráfico de líneas
    line_fig = go.Figure()
    line_fig.add_trace(go.Scatter(x=trend_data['x'], y=trend_data['y'], mode='lines+markers', name='Rentabilidad Operativa'))
    line_fig.add_trace(go.Scatter(x=trend_goal['x'], y=trend_goal['y'], mode='lines', name='Meta', line=dict(dash='dash')))
    
    return gauge_fig, line_fig

# Gráfico de líneas con las emisiones evitadas por tipo de vehículo
def line_chart_emisiones(fuel_filtered):
    # Resumir por tipo de vehículo y calcular las emisiones evitadas
    fuel_filtered['tipo_vehiculo'] = fuel_filtered['co2_per_mile'].apply(categorize_vehicle)
    resumen = fuel_filtered.groupby('tipo_vehiculo').agg({
        'co2_per_mile': 'mean',
        'miles_per_gallon': 'sum'
    }).reset_index()

    # Crear el gráfico de líneas
    line_fig = go.Figure()

    # Agregar datos al gráfico de líneas para cada tipo de vehículo
    line_fig.add_trace(go.Scatter(x=resumen['tipo_vehiculo'], 
                                  y=resumen['co2_per_mile'], 
                                  mode='lines+markers', 
                                  name='CO2 por Milla'))

    line_fig.update_layout(title="Emisiones CO2 Promedio por Tipo de Vehículo",
                           xaxis_title="Tipo de Vehículo",
                           yaxis_title="CO2 por Milla (g)",
                           template="plotly_dark")
    
    return line_fig

# Función principal para ejecutar el dashboard
def main():
    # Obtener los datos
    trips = get_data('trips')
    vehicles = get_data('vehicles')
    air = get_data('air')
    fuel= get_data('fuel')

    

    # Crear la estructura de KPIs
    st.title("Dashboard de KPIs")

    # Crear las columnas donde se van a mostrar los KPIs
    col1, _, col2, _, col3 = st.columns([1, 0.1, 1, 0.1, 1])

     # KPI 1: Emisiones evitadas por vehículos eléctricos e híbridos
    with col1:
        st.subheader("Emisiones Evitadas Vehículos Eléctricos e Híbridos")
        
        # Filtro de manufacturer usando valores únicos de la columna manufacturer
        tiposf = fuel['manufacturer'].unique()
        manufacturer_filter = st.selectbox("Selecciona el fabricante", tiposf)
        
        # Filtro para el rango de millas recorridas
        millas_min, millas_max = st.slider("Rango de millas recorridas", 
                                           min_value=int(fuel['miles_per_gallon'].min()), 
                                           max_value=int(fuel['miles_per_gallon'].max()), 
                                           value=(0, 10000))  # valores por defecto

        # Calcular el KPI de emisiones evitadas con los filtros aplicados
        kpi_emisiones = calculate_kpi_emisiones(fuel, manufacturer_filter, millas_min, millas_max)
        
        st.metric(label="", value=f"{kpi_emisiones:.2f}%", delta="Objetivo: 1000.00%", label_visibility="collapsed")
        gauge_fig, line_fig = show_kpi("Emisiones Evitadas", kpi_emisiones,'objetivo', 1000, kpi_emisiones)
        st.plotly_chart(gauge_fig)

        # Filtrar los datos para el gráfico de líneas
        fuel_filtered = fuel[(fuel['manufacturer'] == manufacturer_filter) & 
                                 (fuel['miles_per_gallon'] >= millas_min) & 
                                 (fuel['miles_per_gallon'] <= millas_max)]

        # Gráfico de líneas con las emisiones evitadas por tipo de vehículo
        line_figg = line_chart_emisiones(fuel_filtered)
        st.plotly_chart(line_figg)

    # Calcular el KPI de ahorro porcentual en la columna 2
    with col2:
        st.subheader("Ahorro Porcentual de Costos Vehiculares")

        # Filtro de fabricante usando valores únicos de la columna manufacturer
        fabricantes = vehicles['manuf'].unique()
        fabricante_selec = st.selectbox("Selecciona el fabricante", fabricantes)

        # Filtro de tipo de costo (combustible vs electricidad)
        tipo_costo = st.radio('Selecciona el tipo de costo a visualizar', ('Combustible', 'Electricidad'))

        # Filtrar los datos según los filtros aplicados
        df_filtrado = vehicles
        if fabricante_selec:
            df_filtrado = df_filtrado[df_filtrado['manuf'] == fabricante_selec]
        if tipo_costo == 'Combustible':
            df_filtrado = df_filtrado[df_filtrado['fuel_cost'] > 0]
        elif tipo_costo == 'Electricidad':
            df_filtrado = df_filtrado[df_filtrado['electric_cost'] > 0]

        # Calcular el ahorro porcentual
        costo_promedio_convencional = df_filtrado[df_filtrado['fuel_type'] == 'Petrol']['total_cost'].mean()
        costo_promedio_electrico = df_filtrado[df_filtrado['fuel_type'] == 'Electricity']['total_cost'].mean()

        if costo_promedio_convencional > 0 and costo_promedio_electrico > 0:
            ahorro_porcentual = (costo_promedio_convencional - costo_promedio_electrico) / costo_promedio_convencional * 100
        else:
            ahorro_porcentual = 0

        # Mostrar el medidor con el valor del ahorro porcentual
        gauge_fig, line_fig = show_kpi("Ahorro Porcentual", ahorro_porcentual, "Objetivo: 20%", 100, ahorro_porcentual)
        st.plotly_chart(gauge_fig)

        # Crear un gráfico de barras comparando costos entre tipos de vehículos
        bar_fig = go.Figure()
        bar_fig.add_trace(go.Bar(
            x=['Convencional', 'Eléctrico'],
            y=[costo_promedio_convencional, costo_promedio_electrico],
            marker_color=['orange', 'green']
        ))
        bar_fig.update_layout(title="Comparación de Costos Promedio", xaxis_title="Tipo de Vehículo", yaxis_title="Costo Promedio")
        st.plotly_chart(bar_fig)


    # KPI 3: Rentabilidad Operativa por Días de la Semana (Aplicar filtro)
    with col3:
        st.subheader("Rentabilidad Operativa por Tipo de Viaje (Días de la Semana)")
        # Filtro por fecha

        min_date = trips['pickup_datetime'].min()
        max_date = trips['pickup_datetime'].max()
        
        st.subheader("Filtros de Fecha")
        start_date = st.date_input("Fecha de inicio", value=min_date, min_value=min_date, max_value=max_date)
        end_date = st.date_input("Fecha de fin", value=max_date, min_value=min_date, max_value=max_date)
        
        trips_filtered = trips[(trips['pickup_datetime'] >= pd.to_datetime(start_date)) & 
                            (trips['pickup_datetime'] <= pd.to_datetime(end_date))]
        
        tipos = trips['type'].unique()
        tipo_seleccionado = st.selectbox("Selecciona el tipo de viaje", tipos)
        
        trips_filtrados_kpi3 = trips_filtered[trips_filtered['type'] == tipo_seleccionado]
        
        kpi_value = calculate_kpi(trips_filtrados_kpi3)
        st.metric(label=f"Tipo de viaje: {tipo_seleccionado}", value=f"{kpi_value:.2f}", delta="Objetivo: 1500")

        trend_data = trips_filtrados_kpi3.groupby('day_of_week').agg({'total_amount': 'sum', 'trip_distance': 'sum'})
        trend_data['kpi'] = (trend_data['total_amount'] / trend_data['trip_distance']) * 100
        trend_data = trend_data.reset_index()

        trend_chart_data = {
            'x': trend_data['day_of_week'],  
            'y': trend_data['kpi']
        }

        trend_goal = {
            'x': trend_data['day_of_week'],
            'y': [kpi_value] * len(trend_data['day_of_week'])  
        }

        gauge_fig, line_fig = show_kpi("KPI 3", kpi_value, "Objetivo", 1500, kpi_value, trend_data=trend_chart_data, trend_goal=trend_goal)
        st.plotly_chart(gauge_fig)
        st.plotly_chart(line_fig)

    # Indicadores adicionales
    st.subheader("Indicadores adicionales")

    col_financiero, col_ambiental = st.columns(2)

    with col_financiero:
        st.subheader("Financiero")
        # Aquí agregarás más KPIs financieros que me proporcionarás
        # Título de la aplicación
        st.title("Ingreso Medio por Pasajero")

        # Filtros en la página, justo arriba de la gráfica
        date_filter = st.date_input("Seleccione el rango de fechas:", [trips['pickup_datetime'].min(), trips['pickup_datetime'].max()])

        # Filtrar los datos según el rango de fechas seleccionado
        filtered_data = trips[(trips['pickup_datetime'] >= pd.to_datetime(date_filter[0])) & (trips['pickup_datetime'] <= pd.to_datetime(date_filter[1]))]

        
        # Agrupar por el número de pasajeros
        df_grouped = filtered_data.groupby('passenger_count').agg(
            avg_income_per_passenger=('total_amount', 'mean'),
            total_trips=('total_amount', 'count')
        ).reset_index()

        # Crear gráfico interactivo
        fig = px.bar(
            df_grouped,
            x='passenger_count',
            y='avg_income_per_passenger',
            title='Ingreso Medio por Pasajero',
            labels={'passenger_count': 'Número de Pasajeros', 'avg_income_per_passenger': 'Ingreso Medio por Pasajero'},
            hover_data=['total_trips'],
            color='total_trips',
            color_discrete_sequence=px.colors.qualitative.Bold  # Paleta de colores brillantes
        )

        # Actualizar la apariencia
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            title_font_size=20
        )

        # Mostrar gráfico en Streamlit
        st.plotly_chart(fig)

        # Título de la aplicación
        st.title("Costo Promedio por Tipo de Vehículo")

        # Filtros en la página, justo arriba de la gráfica
        fuel_type_filter = st.multiselect("Seleccione el tipo de combustible:", vehicles['fuel_type'].unique(), default=vehicles['fuel_type'].unique(),  label_visibility='hidden')

        # Filtrar los datos según los filtros seleccionados
        filtered_data = vehicles[(vehicles['fuel_type'].isin(fuel_type_filter))]

        # Agrupar y calcular el costo promedio por tipo de vehículo
        grouped_data = filtered_data.groupby(['fuel_type']).agg(
            avg_cost=('total_cost', 'mean')).reset_index()

        
            # Gráfico interactivo
        fig = px.bar(grouped_data,
                    x='fuel_type', 
                    y='avg_cost', 
                    color='fuel_type',
                    barmode='group',
                    labels={'avg_cost': 'Costo Promedio'},
                    title='Costo Promedio por Tipo de Vehículo',
                    color_discrete_sequence=px.colors.qualitative.Bold  # Paleta de colores brillantes
                    )


        # Actualizar la apariencia
        fig.update_layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            font_color='white',
            title_font_size=20
        )

        # Mostrar gráfico en Streamlit
        st.plotly_chart(fig)

    with col_ambiental:
        st.subheader("Ambiental")
        # Aquí agregarás más KPIs ambientales que me proporcionarás
        # Título de la aplicación
        st.title("Mapa de Concentración de Partículas Finas (PM 2.5)")

        # Filtros de selección para el usuario
        años = st.selectbox("Selecciona el Año", air['year'].unique())
        regiones = st.multiselect("Selecciona las Regiones", air['geo_place_name'].unique(), default=air['geo_place_name'].unique())

        # Filtrar el DataFrame según los valores seleccionados
        df_filtered = air[(air['year'] == años) & (air['geo_place_name'].isin(regiones))]

        # Crear el mapa interactivo
        fig = px.scatter_mapbox(
            df_filtered,
            lat="latitude",
            lon="longitude",
            size="data_value",
            color="data_value",
            hover_name="geo_place_name",
            hover_data={"data_value": ':.2f'},  # Mostrar el valor de partículas con 2 decimales
            labels={"data_value": "PM 2.5 (µg/m³)"},  # Etiqueta clara para el valor
            color_continuous_scale=px.colors.sequential.Plasma,
            size_max=20,  # Tamaño máximo para mejor visualización
            zoom=4,  # Ajuste del nivel de zoom
            mapbox_style="carto-positron",  # Un estilo de mapa más limpio y claro
            title=f"Concentración Promedio de Partículas Finas (PM 2.5) en {años} por Región"
        )

        # Ajustar el layout para mejorar legibilidad
        fig.update_layout(
            margin={"r":0,"t":50,"l":0,"b":0},  # Menos márgenes
            coloraxis_colorbar={
                'title': 'PM 2.5 (µg/m³)',  # Título del color bar
                'ticksuffix': ' µg/m³',  # Sufijo para mayor claridad
            }
        )

        # Mostrar el mapa en la aplicación de Streamlit
        st.plotly_chart(fig)
# Ejecutar la aplicación
if __name__ == "__main__":
    main()
