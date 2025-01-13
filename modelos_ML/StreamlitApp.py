import streamlit as st
import pandas as pd
import joblib

# Cargar el modelo entrenado
model = joblib.load('./Modelos_ML/random_forest_regressor.joblib')

# Cargar el dataset principal
df_costos = pd.read_csv('./Data/car_resale_prices_clean.csv')

# Asegurarnos de que resale_price sea numérico
df_costos['Resale_Price'] = pd.to_numeric(df_costos['Resale_Price'], errors='coerce')

# Verificar si hay valores nulos o incorrectos en resale_price
df_costos = df_costos.dropna(subset=['Resale_Price'])

# Cargar el dataset de costos operacionales
df = pd.read_csv('./Data/costo_operacional_vehiculos_clean.csv', sep=',')

# Calcular umbrales de costos para clasificación
low_cost_threshold = df_costos['Resale_Price'].quantile(0.33)
high_cost_threshold = df_costos['Resale_Price'].quantile(0.66)

# Revisa la función de categorización de vehículos
def categorize_vehicle(row):
    if row['Fuel_Type'] in ['Diesel', 'Petrol', 'Petrol/LPG']:
        return 'Convencional'
    elif row['Fuel_Type'] in ['Electricity', 'Electric']:
        return 'Eléctrico'
    else:
        return 'Híbrido'

# Aplicar la función al dataframe
df_costos['Vehicle_Type'] = df_costos.apply(categorize_vehicle, axis=1)

# Streamlit App
st.title('Evaluación de Autos')

# Entrada del presupuesto por parte del cliente
presupuesto_cliente = st.number_input('Ingresa tu presupuesto (en dólares):', min_value=0)

# Mostrar autos recomendados dentro del presupuesto
if presupuesto_cliente > 0:
    st.write(f'Autos recomendados dentro de tu presupuesto de ${presupuesto_cliente}:')
    
    # Filtrar los autos dentro del presupuesto
    autos_recomendados = df_costos[df_costos['Resale_Price'] <= presupuesto_cliente].sort_values(by='Resale_Price', ascending=False).head(5)
    
    # Si hay autos que cumplen el criterio
    if not autos_recomendados.empty:
        st.write(autos_recomendados[['Full_Name', 'Registered_Year', 'Fuel_Type', 'Resale_Price', 'Vehicle_Type']].rename(
            columns={
                'Full_Name': 'Nombre Completo',
                'Registered_Year': 'Año',
                'Fuel_Type': 'Tipo de Combustible',
                'Resale_Price': 'Precio en Dólares',
                'Vehicle_Type': 'Clasificación de Combustible'
            }
        ).round({'Precio en Dólares': 2}))
    else:
        st.write('No se encontraron autos dentro de tu presupuesto.')

# Mostrar detalles del auto seleccionado
st.write('Detalles del auto seleccionado:')
autos_list = df_costos['Full_Name'].unique()
selected_auto = st.selectbox('Selecciona un auto:', autos_list)

if selected_auto:
    auto_data = df_costos[df_costos['Full_Name'] == selected_auto]
    st.write(auto_data[['Full_Name', 'Registered_Year', 'Fuel_Type', 'Resale_Price', 'Vehicle_Type']].rename(
        columns={
            'Full_Name': 'Nombre Completo',
            'Registered_Year': 'Año',
            'Fuel_Type': 'Tipo de Combustible',
            'Resale_Price': 'Precio en Dólares',
            'Vehicle_Type': 'Clasificación de Combustible'
        }
    ).round({'Precio en Dólares': 2}))
