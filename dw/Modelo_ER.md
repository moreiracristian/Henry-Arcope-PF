## **Modelo de Entidad-Relación (ER)**

### **1. air_quality_measurement**

| Atributo          | Tipo de dato   | Descripción                                          | Clave       |
|-------------------|----------------|------------------------------------------------------|-------------|
| `indicator_id`    | Integer        | Identificador único del indicador                    | PK          |
| `name`            | Object         | Nombre del indicador                                 |             |
| `measure`         | Object         | Medida del indicador                                 |             |
| `geo_join_id`     | Integer        | Identificador del área geográfica                    |             |
| `geo_place_name`  | Object         | Nombre del barrio                                    |             |
| `data_value`      | Float          | Valor real del indicador                             |             |
| `time_period`     | Object         | Período de tiempo al que aplican los datos           |             |
| `year`            | Integer        | Año en el que se tomaron los datos                   |             |
| `unique_air`      | Integer        | Identificador unico de la tabla                      |             |

**Relaciones:**
- Sin relación con otra entidad


### **2. vehicles**

| Atributo          | Tipo de dato   | Descripción                                           | Clave       |
|-------------------|----------------|-------------------------------------------------------|-------------|
| `manuf`           | Object         | Fabricante del vehículo                               |             |
| `model`           | Object         | Modelo del vehículo                                   | PK          |
| `fuel_type`       | Object         | Tipo de combustible                                   |             |
| `fuel_cost`       | Float          | Costo anual del combustible (en GBP)                  |             |
| `electric_cost`   | Float          | Costo anual eléctrico (en GBP)                        |             |
| `total_cost`      | Float          | Costo total anual (en GBP)                            |             |
| `noise_level`     | Float          | Nivel de ruido del vehículo (en dB)                   |             |
| `unique_vehicles` | Integer        | Identificador único de la tabla                       |             |

**Relaciones:**
- `model` → **Trips** (`model`) - Relación con la entidad **Trips** mediante el vehículo usado en el viaje


### **3. trips (Yellow, Green, FHV)**

| Atributo              | Tipo de dato   | Descripción                                         | Clave       |
|-----------------------|----------------|-----------------------------------------------------|-------------|
| `vendor_id`           | Integer        | Identificación del proveedor                        |             |
| `type`                | Object         | Tipo de vehículo                                    |             |
| `pickup_datetime`     | Datetime       | Fecha y hora de recogida                            |             |
| `dropoff_datetime`    | Datetime       | Fecha y hora de entrega                             |             |
| `passenger_count`     | Float          | Número de pasajeros                                 |             |
| `trip_distance`       | Float          | Distancia total del viaje                           |             |
| `total_amount`        | Float          | Importe total del viaje                             |             |
| `PULocationID`        | Integer        | ID de la ubicación de recogida                      | FK          |
| `DOLocationID`        | Integer        | ID de la ubicación de entrega                       | FK          |
| `payment_type`        | Integer        | Método de pago utilizado                            |             |
| `congestion_surcharge`| Float          | Recargo por congestión                              |             |
| `unique_trips`        | Integer        | Identificador único de la tabla                     |             |

**Relaciones:**
- `PULocationID` → **Geographic Data** (`geo_join_id`) - Relación con la ubicación geográfica de recogida
- `DOLocationID` → **Geographic Data** (`geo_join_id`) - Relación con la ubicación geográfica de entrega
- `pickup_datetime` → **Meteorological Data** (`time`) - Relación con el clima durante el viaje


### **4. geographic_data**

| Atributo              | Tipo de dato   | Descripción                                          | Clave       |
|-----------------------|----------------|------------------------------------------------------|-------------|
| `geo_join_id`         | Integer        | Identificador geográfico                             | PK          |
| `latitude`            | Float          | Latitud                                              |             |
| `longitude`           | Float          | Longitud                                             |             |
| `unique_geographic`   | Integer        | Identificador único de la tabla                      |             |

**Relaciones:**
- `geo_join_id` → **Trips** (`PULocationID`, `DOLocationID`) - Relación con viajes realizados en la ubicación


### **5. meteorological_data**

| Atributo                | Tipo de dato   | Descripción                                          | Clave       |
|-------------------------|----------------|------------------------------------------------------|-------------|
| `time`                  | Datetime       | Hora                                                 | PK          |
| `temperature_2m`        | Float          | Temperatura a 2m de altura                           |             |
| `rain`                  | Float          | Lluvia en mm                                         |             |
| `is_day`                | Object         | Indica si es de día                                  |             |
| `unique_meteorological` | Integer        | Identificador único de la tabla                      |             |

**Relaciones:**
- `time` → **Trips** (`pickup_datetime`) - Relación con viajes en función del clima durante el trayecto	


### **6. fuel_stations**

| Atributo             | Tipo de dato   | Descripción                                          | Clave       |
|----------------------|----------------|------------------------------------------------------|-------------|
| `station_id`         | Object         | ID de la estación                                    |             |
| `station_name`       | Object         | Nombre de la estación                                |             |
| `street_address`     | Object         | Dirección                                            |             |
| `city`               | Object         | Ciudad                                               |             |
| `state`              | Object         | Estado                                               |             |
| `fuel_type_code`     | Object         | Código de tipo de combustible                        | PK          |
| `unique_stations`    | Integer        | Identificador único de la tabla                      |             |

**Relaciones:**
- `fuel_type_code` → **Vehicles** (`fuel_type`) - Relación con el tipo de combustible de los vehículos


### **7. fuel_economy_data**

| Atributo              | Tipo de dato   | Descripción                                         | Clave       |
|-----------------------|----------------|-----------------------------------------------------|-------------|
| `manufacturer`        | Object         | Productor del vehículo                              |             |
| `model`               | Object         | Modelo del vehículo                                 | PK          |
| `miles_per_gallon`    | Float          | Millas por galón                                    |             |
| `co2_per_mile`        | Float          | Emisiones de CO2 por milla                          |             |
| `fuel_cost`           | Float          | Costo de combustible anual                          |             |
| `unique_economy_data` | Integer        | Identificador único de la tabla                     |             |

**Relaciones:**
- `model` → **Vehicles** (`model`) - Relación con datos de vehículos


### **8. car_resale_prices**

| Atributo              | Tipo de dato   | Descripción                                         | Clave       |
|-----------------------|----------------|-----------------------------------------------------|-------------|
| `full_name`           | Object         | Nombre completo (marca y modelo)                    | FK          |
| `registred_year`      | Object         | Año registrado                                      |             |
| `transmission_type`   | Float          | Tipo de transmisión (Manual o Automático)           |             |
| `fuel_type`           | Float          | Tipo de combustible                                 |             |
| `max_power`           | Float          | Potencia máxima del motor	                       |             |
| `resale_price`        | Float          | Precio de reventa en USD      	                   |             |
| `unique_resale_price` | Integer        | Identificador único de la tabla                     |             |

**Relaciones:**
- `full_name` → **Vehicles** (`model`) - ¿Indicaría que el precio de reventa está asociado a un vehículo específico?

---

## **Relaciones entre Entidades**


### Relación 1: **Vehicles** y **Trips**
- **Descripción:** Muchos viajes pueden estar asociados con un único modelo de vehículo.
- **Tipo de Relación:** Muchos a Uno (N:1)
- **Cardinalidad:** Muchos viajes pueden ser realizados con un solo modelo de vehículo.
- **Explicación:** Un modelo de vehículo puede estar involucrado en múltiples viajes, pero cada viaje está asociado con un modelo específico.


### Relación 2: **Air Quality Measurement** y **Trips**
- **Descripción:** Cada viaje tiene asociada una medición de calidad del aire para el tiempo y lugar del viaje.
- **Tipo de Relación:** Uno a Uno (1:1)
- **Cardinalidad:** Cada viaje está vinculado a una única medición de calidad del aire correspondiente.
- **Explicación:** Se vinculan las condiciones del aire al momento específico del viaje.


### Relación 3: **Trips** y **Geographic Data**
- **Descripción:** Cada viaje tiene una ubicación de recogida y una de entrega que están definidas en **Geographic Data**.
- **Tipo de Relación:** Uno a Muchos (1:N)
- **Cardinalidad:** Cada viaje tiene una ubicación de recogida y entrega, y cada ubicación puede tener múltiples viajes.
- **Explicación:** Una ubicación geográfica puede estar asociada con varios viajes como punto de recogida o entrega.


### Relación 4: **Trips** y **Meteorological Data**
- **Descripción:** Los viajes están influenciados por las condiciones climáticas al momento del trayecto.
- **Tipo de Relación:** Uno a Uno (1:1)
- **Cardinalidad:** Cada viaje tiene un momento específico asociado a un registro meteorológico.
- **Explicación:** Cada registro meteorológico se relaciona con un viaje basado en el tiempo de recogida del viaje.


### Relación 5: **Vehicles** y **Fuel Economy Data**
- **Descripción:** Cada modelo de vehículo tiene datos específicos sobre su economía de combustible.
- **Tipo de Relación:** Uno a Uno (1:1)
- **Cardinalidad:** Cada modelo de vehículo tiene un conjunto único de datos de economía de combustible.
- **Explicación:** Los datos de economía de combustible están disponibles para cada modelo de vehículo, proporcionando información sobre su eficiencia.


### Relación 6: **Fuel Stations** y **Vehicles**
- **Descripción:** Las estaciones de combustible suministran el tipo de combustible utilizado por los vehículos.
- **Tipo de Relación:** Muchos a Uno (N:1)
- **Cardinalidad:** Varias estaciones pueden suministrar el mismo tipo de combustible.
- **Explicación:** Un tipo de combustible puede estar disponible en múltiples estaciones, y cada vehículo usa un tipo específico de combustible.


### Relación 7: **Car Resale Prices** y **Vehicles**
- **Descripción:** La tabla Car Resale Prices almacena información sobre los precios de reventa de distintos modelos de automóviles, junto con detalles como el tipo de transmisión, el tipo de combustible y la potencia máxima del vehículo. La tabla Vehicles contiene información técnica y de costos de los automóviles, como su tipo de combustible y sus costos operativos.
- **Tipo de Relación:** Muchos a Uno
- **Cardinalidad:** Un modelo de automóvil de la tabla Vehicles puede aparecer varias veces en la tabla Car Resale Prices con distintos años de registro o precios de reventa.
- **Explicación:** Permite almacenar información histórica o específica sobre los precios de reventa de vehículos. Esto asegura que cualquier precio de reventa esté vinculado a un modelo de vehículo existente en la base de datos.

---