## AnalisisPreliminar de Calidad de Datos

Datos Analizados

Los datos fueron obtenidos de organismos gubernamentales como del del Departamento de Energia de los EEUU, la Comisión de Taxis y Limusinas de Nueva York (TLC), Kaggle plataforma en línea que brinda data de conjuntos de datos públicos y de otros Organismos.

Variables Clave a tener en cuenta son caracteristicas de los autos (Tipo de auto, Tipo de Combustible, Costo Combustible, Recorrido, Emisiones CO2), Uso delos mismos (Horarios, Ubicaciones de recogida y destino, tiempos de viaje, tiempos de espera y eficiencia)

Durante el proceso de ETL, pudimos identificar varios problemas clave relacionados con la calidad y consistencia de los datos. Primero, la calidad de los datos se ve afectada por mucha presencia de valores nulos en columnas críticas, como el número de pasajeros y las distancias de los viajes. Esto impide obtener conclusiones confiables y genera inconsistencias en el análisis.

Además, se observó falta de granularidad en algunos campos, como las fechas de recogida y entrega, lo que podría complicar la identificación de patrones precisos. Otro aspecto es la presencia de datos duplicados, lo cual impacta directamente en los resultados del análisis, ya que distorsiona métricas clave, como promedios y totales.

El problema de la granularidad y la inconsistencia también afecta la interpretación de los datos. Por ejemplo, si la columna de distancias presenta valores nulos en registros importantes, esto podría inducir a suposiciones no válidas sobre el comportamiento de los viajes. Además, las advertencias de funciones deprecated (en desuso) como swapaxes, sugieren que el código está utilizando métodos que ya no se recomiendan, lo que puede comprometer la eficiencia y la mantenibilidad a largo plazo del proceso.

Varios campos importantes como el número de pasajeros, distancias de los viajes y tarifas contienen valores nulos o faltantes. Estos vacíos pueden sesgar el análisis y limitar la capacidad para obtener conclusiones precisas. La falta de granularidad en algunos campos, como la fecha y hora, también afecta la precisión de los resultados. En conjunto, esta falta de información reduce la calidad de los datos y podría llevar a interpretaciones erróneas.

Faltan datasets sobre el tráfico, el clima durante el periodo de los viajes, o datos socioeconómicos de las áreas involucradas (ubicación de recogida y destino) pueden proporcionar un contexto valioso. La ausencia de estos elementos puede limitar la interpretación de patrones y reducir la capacidad de hacer inferencias sólidas sobre los factores que afectan las tarifas o el comportamiento del cliente.


Resumen
Datos Analizados
Los datos fueron obtenidos de organismos gubernamentales, plataformas en línea y de otros Organismos.

Variables Clave a tener en cuenta son caracteristicas de los autos y Uso delos mismos.

Confiabilidad Alta Problemas detectados presencia de valores nulos y duplicados
