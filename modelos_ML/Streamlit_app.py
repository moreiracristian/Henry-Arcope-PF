import streamlit as st
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Cargar el modelo entrenado
model = joblib.load('./Modelos_ML/random_forest_regressor.joblib')

# Cargar el dataset principal
df_costos = pd.read_csv('./Data/car_resale_prices_clean.csv')

# Asegurarnos de que Resale_Price sea numérico
df_costos['Resale_Price'] = pd.to_numeric(df_costos['Resale_Price'], errors='coerce')

# Verificar si hay valores nulos o incorrectos en Resale_Price
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


#Segundo modelo de ML1 

# Cargamos el modelo guardado 
modelo_ML1 = joblib.load('./Modelos_ML/Modelo_ML1.joblib')
# Cargamos el dataset
df_Vehiculos = pd.read_parquet('./Data/Df_vfed.parquet')
df_Vehiculos_N = df_Vehiculos[df_Vehiculos['Year'] > 2010]
df_Vehiculos_F = df_Vehiculos_N[df_Vehiculos_N['CO2 (p/mile)'] >= 0]
# Realizamos una función para categorizar los vehículos
def categorizar_vehiculos(row):
    if row['Alternative Fuel'] == 'Electricity':
        return 'Híbrido'
    elif row['Fuel'] == 'Electricity':
        return 'Eléctrico'
    elif row['Alternative Fuel'] in ['E85', 'No'] and row['Fuel'] != 'Natural Gas' and row['CO2 (p/mile)'] > 0:
        return 'Comvencional'
    else:
        return 'Gas'
    
# Aplicamos la función 
df_Vehiculos_F['Categoria'] = df_Vehiculos_F.apply(categorizar_vehiculos, axis=1)
#Obtenemos las marcas de los vehículos 
Marcas = df_Vehiculos_F['Manufacturer'].unique()
Marcas.inset(0, 'Todos')
# Titulo 
st.title('Recomendación de vehículos con mayor eficiencia energetica')

# Entrada de usuario: año y fabricante
año = st.number_input('Ingrese el año', min_value=2011, max_value=2024)
fabricante = st.selectbox('Ingrese la marca', Marcas)

def eficiencia (Vehiculos):
    # Verificar si hay vehículos que cumplar con esta condición 
    if len(Vehiculos_filtrado) > 0:
        #Estandarizamos las caracteristicas
        X = Vehiculos_filtrado[['Year', 'Miles per gallon (mpg)', 'CO2 (p/mile)', 'FuelCost']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        # Hacemos las predicciones con el modelo 
        predicciones = modelo_ML1.predict(X_scaled)
        # Añadimos las predicciones al dataframe
        Vehiculos_filtrado['Eficiencia'] = predicciones
        # Ordenas por eficiencia de mayor a menor
        vehiculos_recomendados = Vehiculos_filtrado.sort_values(by='Eficiencia', ascending=False).head(5)
        # Mostrar los 5 vehículos recomendados 
        return st.write('Los 5 vehículos mas eficientes energeticamente son:')
        return st.dataframe(vehiculos_recomendados[['Year', 'Manufacturer', 'Miles per gallon (mpg)', 'CO2 (p/mile)', 'FuelCost', 'Fuel', 'Categoria']])
    else: 
        return st.write('No se encontraron vehículos que cumplan con ese citerio')

# Boton para ejecutar la predicción
if st.button('Obtener recomendaciones por año y marca'):
    if Marcas != 'Todos':
       # Filtrar vehiculos por año y fabricante
       Vehiculos_filtrado = df_Vehiculos_F[(df_Vehiculos_F['Year'] == año) & (df_Vehiculos_F['Manufacturer'] == fabricante)]
       eficiencia(Vehiculos_filtrado)
    else:
        Vehiculos_filtrado = df_Vehiculos_F
        eficiencia(Vehiculos_filtrado)


# Boton de recomandaciones por año

if st.button('Obtener recomendaciones por año'):
    # Filtrar vehiculos por año 
    Vehiculos_filtrado = df_Vehiculos_F[(df_Vehiculos_F['Year'] == año) ]

    # Verificar si hay vehículos que cumplar con esta condición 
    if len(Vehiculos_filtrado) > 0:
        #Estandarizamos las caracteristicas
        X = Vehiculos_filtrado[['Year', 'Miles per gallon (mpg)', 'CO2 (p/mile)', 'FuelCost']]
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        # Hacemos las predicciones con el modelo 
        predicciones = modelo_ML1.predict(X_scaled)
        # Añadimos las predicciones al dataframe
        Vehiculos_filtrado['Eficiencia'] = predicciones
        # Ordenas por eficiencia de mayor a menor
        vehiculos_recomendados = Vehiculos_filtrado.sort_values(by='Eficiencia', ascending=False).head(5)
        # Mostrar los 5 vehículos recomendados 
        st.write('Los 5 vehículos mas eficientes energeticamente son:')
        st.dataframe(vehiculos_recomendados[['Year', 'Manufacturer', 'Miles per gallon (mpg)', 'CO2 (p/mile)', 'FuelCost', 'Fuel', 'Categoria']])
    else: 
        st.write('No se encontraron vehículos que cumplan con ese citerio')
