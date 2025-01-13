import streamlit as st
import acercaDe  # Importar la página 'home.py'
import dashboard  # Importar la página 'dashboard.py'
import modelos  # Importar la página 'modelos_ml.py'
import inicio # Importar la página 'inicio.py'
import base64
from PIL import Image

# Función para cargar imágenes en base64
def get_image_b64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

def acercaDe_page():
    # Cambiar el fondo de la página
    st.markdown(
        """
        <style>
        .stApp {
            background-color: whitesmoke;
        }
        h1 { color: #F25A38; }
        h2 { color: #F25041; }
        h3 { color: #000000; }
        h4 { color: #000000; }
        h5 { color: #000000; }
        h6 { color: #000000; }
        .card {
            background-color: #56B5BF;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .social-logo {
            background-color: #F2F2F2;
            border-radius: 50%;
            padding: 5px;
            transform: scale(1.1); /* Aumentar el tamaño al pasar el mouse */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


    # Aquí va el contenido que ya tienes en la página de home.
    img1 = Image.open('./Streamlit/images/arcope-logo.jpeg') 
    st.markdown(
        f"<div style='text-align: center;'><img src='data:image/jpeg;base64,{get_image_b64('./Streamlit/images/arcope-logo.jpeg')}' width='300'/></div>",
        unsafe_allow_html=True
    )
    
    # Título del proyecto centrado
    st.markdown("""
    <h1 style="text-align: center; "><b>ARCOPE - PROYECTO FINAL</b></h1>
    """, unsafe_allow_html=True)

    # Divisor arcoíris
    st.markdown("""
    <hr style="border: none; height: 4px; 
    background: linear-gradient(to right, #F25A38, #F2A649, #56B5BF, #F25041, #F2F2F2);">
    """, unsafe_allow_html=True)
    
    # Descripción del proyecto
    st.markdown("""
    # Proyecto: Data Product orientado a la sostenibilidad y rentabilidad para Uber en la ciudad de New York.
    
    ## Objetivo Principal:
    #### Transformar el negocio de Uber en un referente de sostenibilidad y rentabilidad a largo plazo mediante la optimización operativa, la inversión en tecnología sustentable y la mejora de la imagen corporativa, para atraer tanto a clientes conscientes del medio ambiente como a inversores interesados en sostenibilidad.
    
    ## Cliente Objetivo:
    #### Empresa de Ride-Hailing, 'Uber', que conecta pasajeros con conductores de vehículos de alquiler a través de aplicaciones móviles y sitios web.
    
    ## Estrategia de Negocio:
    #### Uber busca herramientas para mejorar su imagen corporativa, incrementar la rentabilidad y maximizar la eficiencia operativa, con el objetivo de alinear su negocio hacia un enfoque más sustentable y atractivo para los inversores.
    
    ## Alcance:
    #### Proponemos un MVP centrado en analizar y procesar datos proporcionados por Uber y organismos gubernamentales, ofreciendo soluciones que permitan la toma de decisiones estratégicas basadas en sostenibilidad y rentabilidad.
    
    ## Contexto:
    #### Ciudad de Nueva York, EEUU.
    
    ## Justificación:
    #### El mercado está en plena transición hacia modelos sostenibles. Las empresas que adoptan prácticas sostenibles no solo mejoran su imagen pública, sino que también aseguran su rentabilidad a largo plazo al alinearse con normativas futuras. Este proyecto posicionará a Uber como líder en sostenibilidad en el sector Ride-Hailing, atrayendo a clientes conscientes del medio ambiente y ofreciendo nuevas oportunidades de negocio e incentivos fiscales.
    
    """)
    st.markdown("""<hr style="border: none; height: 4px; 
    background: linear-gradient(to right, #F25A38, #F2A649, #56B5BF, #F25041, #F2F2F2);">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    # Objetivos Particulares:
    
    ### 1. Mejorar la Imagen Corporativa a través de la Sostenibilidad
    - **KPI**: Reducción de CO2 y mejora de la calidad del aire.
    - **Medir**: Comparar las emisiones de CO2 de la flota actual con una nueva flota de vehículos híbridos y eléctricos. También se medirá la calidad del aire en áreas con alta concentración de operaciones.
    - **Impacto**: Posicionamiento como líder en sostenibilidad, atracción de un segmento de mercado más consciente del medio ambiente, y mejora de la percepción pública.
    
    ### 2. Incrementar la Rentabilidad a Largo Plazo mediante Inversión en Vehículos Eléctricos/Híbridos
    - **KPI**: Costos y beneficios por vehículo eléctrico en relación a la distancia recorrida.
    - **Medir**: Comparar los costos operativos y beneficios de los vehículos eléctricos frente a los de combustión interna.
    - **Impacto**: Reducción de costos operativos, acceso a incentivos fiscales, y mejora en la rentabilidad a largo plazo.
    
    ### 3. Maximizar la Eficiencia Operativa y la Rentabilidad del Servicio
    ####  - **KPI 3a**: Ingresos por milla recorrida. 
    ####  - **Medir**: (Total_amount - Tolls_amount - Congestion_Surcharge - Airport_fee) / Trip_distance.
    ####  - **Impacto**: Optimización de rutas, asignación de vehículos y tarifas para maximizar ingresos.
      
    ####  - **KPI 3b**: Tasa de utilización de vehículos.
    ####  - **Medir**: Total de viajes / Número total de horas disponibles.
    ####  - **Impacto**: Incremento de la rentabilidad al mejorar la utilización de la flota.
    
    ####  - **KPI 3c**: Promedio de pasajeros por viaje.
    ####  - **Medir**: Promedio(Passenger_count) por zona, tipo de servicio y hora del día.
    ####  - **Impacto**: Fomento del uso compartido de vehículos para incrementar la rentabilidad y reducir la cantidad de vehículos necesarios.
    """)
                
    st.markdown("""<hr style="border: none; height: 4px; 
    background: linear-gradient(to right, #F25A38, #F2A649, #56B5BF, #F25041, #F2F2F2);">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    # Análisis de Impacto:
    ### Implementar estos KPIs proporcionará una visión clara del desempeño de Uber en términos de sostenibilidad y rentabilidad. Basándose en estos análisis, se podrán tomar decisiones estratégicas como expandir la flota de vehículos eléctricos, optimizar rutas para reducir emisiones y costos, y rediseñar campañas de marketing centradas en el compromiso ambiental.
    
    #### Este proyecto ayudará a Uber no solo a cumplir con sus objetivos de sostenibilidad, sino también a mejorar su imagen pública y garantizar su rentabilidad a largo plazo, consolidándose como un líder en innovación dentro del sector de Ride-Hailing.
    
    ---
    ## **Propuesta y Stack Tecnológico**
    
    ---
    
    ### **1. Ingesta de Datos y ETL (Extract, Transform, Load)**
    
    ## **Herramientas y Tecnologías:**
    
    ####  - **Lenguaje de Programación: Python**
    ####  - **Descripción:** Lenguaje versátil y ampliamente utilizado en ciencia de datos y machine learning.
      
    ####  - **Bibliotecas de Python:**
    ####  - **Pandas:** Para la manipulación y limpieza de datos provenientes de archivos CSV o Parquet.
    ####  - **PyArrow:** Para leer y escribir archivos Parquet de manera eficiente.
      
    ####  - **Data Lake: MinIO**
    ####  - **Descripción:** MinIO es un sistema de almacenamiento de objetos. Se utiliza para almacenar datos en bruto y transformados, facilitando su acceso durante las etapas de ETL.
      
    ####  - **Gestión de Entornos:**
    ####  - **Visual Studio Code:** Facilita la gestión de paquetes y entornos virtuales, asegurando que todas las dependencias estén correctamente instaladas.
    
    ## **Justificación:**
    ####  - **Python**, junto con **Pandas** y **PyArrow**, proporciona una solución robusta y flexible para la ingesta y transformación de datos, permitiendo manejar diferentes formatos de archivo de manera eficiente.
    ####  - **MinIO** actúa como un Data Lake, proporcionando almacenamiento centralizado y escalable para grandes volúmenes de datos en diferentes formatos, facilitando el acceso rápido y eficiente para las siguientes fases del pipeline.
    
    ---
    ## **2. Ingreso en la Base de Datos (Data Warehouse)**
    
    ### **Herramientas y Tecnologías:**
    
    ####  - **Sistema de Gestión de Bases de Datos: MySQL**
    ####  - **Descripción**: Base de datos relacional ampliamente utilizada, adecuada para almacenar datos transformados y modelos entrenados.
    
    ####  - **Interfaz de Administración: phpMyAdmin**
    ####  - **Descripción**: Herramienta web para gestionar MySQL de manera visual y sencilla, facilitando la administración y consulta de la base de datos.
    
    ####  - **Conexión y ORM: SQLAlchemy**
    ####  - **Descripción**: Biblioteca de Python para interactuar con bases de datos SQL de manera eficiente y segura.
    
    ### **Justificación:**
    #### MySQL es una opción sólida para almacenar datos estructurados, y phpMyAdmin ofrece una interfaz amigable para la administración. SQLAlchemy simplifica las interacciones entre Python y la base de datos, permitiendo una integración fluida en el pipeline.
    
    ---
    ## **3. Entrenamiento del Modelo de Machine Learning**
    
    ### **Herramientas y Tecnologías:**
    
    ####  - **Bibliotecas de Machine Learning:**
    ####  - **Scikit-learn**: Ideal para modelos de machine learning básicos y medianamente complejos, como regresión y clasificación.
    
    ####  - **Serialización de Modelos:**
    ####  - **Pickle**: Para guardar y cargar modelos entrenados de manera sencilla.
    
    ####  - **Entorno de Desarrollo:**
    ####  - **Jupyter Notebook**: Para desarrollar, entrenar y documentar modelos de manera interactiva.
    
    ### **Justificación:**
    #### Scikit-learn es perfecto para comenzar con machine learning gracias a su simplicidad y eficacia. Jupyter Notebook facilita la experimentación y documentación del proceso de entrenamiento.
    
    ---
    ## **4. Creación de Dashboards e Informes**
    
    ### **Herramientas y Tecnologías:**
    
    ####  - **Visualización de Datos:**
    ####  - **Matplotlib y Seaborn**: Para crear gráficos estáticos y visualizaciones detalladas.
    ####  - **Plotly** (opcional): Para visualizaciones interactivas si se requiere mayor dinamismo en los dashboards.
    
    ####  - **Generación de Informes:**
    ####  - **Jupyter Notebook**: Para crear informes interactivos que combinan código, visualizaciones y texto descriptivo.
    ####  - **ReportLab** (opcional): Para generar informes en formato PDF si se necesita distribuir documentos estáticos.
    
    ####  - **Desarrollo de Dashboards Interactivos:**
    ####  - **Streamlit** o **Dash**: Frameworks de Python para crear aplicaciones web interactivas y dashboards de manera rápida y sencilla.
    
    ### **Justificación:**
    #### Matplotlib y Seaborn ofrecen una base sólida para la visualización de datos, mientras que herramientas como Streamlit permiten transformar estos gráficos en dashboards interactivos. Jupyter Notebook combina análisis y visualización en un solo entorno, facilitando la creación de informes comprensibles y detallados.
    
    ---
    # **Infraestructura y Seguridad**
    
    ### **Herramientas y Tecnologías:**
    
    ####  - **Servidor Local:**
    #####  - **Descripción**: Un servidor donde se alojarán MySQL y phpMyAdmin, accesible desde internet para permitir conexiones remotas.
    
    ####  - **Seguridad de la Base de Datos:**
    #####  - **Configuración de MySQL para Acceso Remoto**: Asegurar que MySQL esté configurado para aceptar conexiones remotas de manera segura.
    #####  - **Autenticación y Autorización**: Gestionar permisos de usuarios para controlar el acceso a diferentes partes de la base de datos.
    #####  - **Uso de SSH o VPN**: Para cifrar las conexiones y proteger los datos en tránsito.
    
    ####  - **Orquestador:**
    #####  - **Apache Airflow**: Para gestionar y orquestar los flujos de trabajo de ETL y entrenamiento de modelos.
    
    ### **Justificación:**
    #### Garantizar la seguridad es crucial cuando se permite el acceso remoto a la base de datos. Configurar MySQL correctamente y utilizar métodos de cifrado como SSH o VPN protege los datos y asegura que solo usuarios autorizados puedan acceder al sistema. Apache Airflow facilita la automatización y programación de tareas complejas en el flujo de trabajo.
    
    ---
    """)

    # Tabla con estilo CSS
    st.markdown("""
    <style>
    .table-container {
        background-color: black;
        color: white;
        padding: 10px;
        border-radius: 5px;
    }
    .table-container table {
        width: 100%;
        border-collapse: collapse;
    }
    .table-container th, .table-container td {
        padding: 10px;
        border: 1px solid white;
    }
    .table-container th {
        background-color: #333;
    }
    </style>

    <div class="table-container">
        <table>
            <tr>
                <th style="text-align: center";> Fase </th>
                <th style="text-align: center";> Herramientas y Tecnologías </th>
            </tr>
            <tr>
                <td>1. Ingesta de Datos y ETL</td>
                <td>Python, Pandas, PyArrow, MinIO</td>
            </tr>
            <tr>
                <td>2. Ingreso en la Base de Datos</td>
                <td>MySQL, phpMyAdmin, SQLAlchemy</td>
            </tr>
            <tr>
                <td>3. Entrenamiento de Machine Learning</td>
                <td>Scikit-learn, Pickle, Jupyter Notebook</td>
            </tr>
            <tr>
                <td>4. Creación de Dashboards e Informes</td>
                <td>Matplotlib, Seaborn, Plotly, Jupyter Notebook, Streamlit/Dash</td>
            </tr>
            <tr>
                <td>5. Orquestador</td>
                <td>Apache Airflow</td>
            </tr>
            <tr>
                <td>Infraestructura y Seguridad</td>
                <td>Servidor Local, Configuración de MySQL para Acceso Remoto, SSH/VPN</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    ### **Ejemplo de Diagrama:**
    
    #### 1. **Ingesta de Datos y ETL**
    ####    - MinIO → Python → Pandas/PyArrow → Transformaciones → Python
    
    #### 2. **Ingreso en la Base de Datos**
    ####    - Python/SQLAlchemy → MySQL → phpMyAdmin
    
    #### 3. **Entrenamiento de ML**
    ####    - MySQL → Python/Scikit-learn → Modelo Entrenado → MySQL
    
    #### 4. **Creación de Dashboards e Informes**
    ####    - MySQL → Python/Matplotlib/Seaborn → Jupyter Notebook/Streamlit → Dashboards/Informes
    
    #### 5. **Orquestación**
    ####    - Apache Airflow → Ingesta de Datos y ETL → Entrenamiento de ML → Creación de Dashboards e Informes
    """)
    
    st.divider()
    
    # Información del equipo
    st.header("Desarrollado por ⚙️")
    # Divisor arcoíris
    st.markdown("""
    <hr style="border: none; height: 4px; 
    background: linear-gradient(to right, #F25A38, #F2A649, #56B5BF, #F25041, #F2F2F2);">
    """, unsafe_allow_html=True)
    
    personas = [
        {
            "nombre": "Cristian Moreira",
            "profesion": "Project Manager",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen_link": "./Streamlit/images/cristian.jpeg"
        },
        {
            "nombre": "Andres Aguirre",
            "profesion": "Technical Project Manager & Data Analytics",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen_link": "./Streamlit/images/andres.jpeg"
        },
        {
            "nombre": "Jeison Zapata",
            "profesion": "Data Scientist & Data Analyst",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen_link": "./Streamlit/images/jeison.jpeg"
        },
        {
            "nombre": "Libardo Alarcon",
            "profesion": "Data Scientist",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen_link": "./Streamlit/images/libardo.jpeg"
        },
        {
            "nombre": "Manuel Carruitero",
            "profesion": "Data Engineer",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen_link": "./Streamlit/images/manuel.jpeg"
        },
        {
            "nombre": "Lucas Carranza",
            "profesion": "Data Engineer",
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "imagen_link": "./Streamlit/images/lucas.jpeg"
        }
    ]
    
    # Mejora en la disposición del equipo
    columns = st.columns(len(personas))
    for idx, persona in enumerate(personas):
        with columns[idx]:
            # Nombre y profesión centrados
            st.markdown(f'<h2 style="text-align: center; margin-bottom: 10px;">{persona["nombre"]}</h2>', unsafe_allow_html=True)  # Aumentar el margen
            st.markdown(f'<h4 style="text-align: center; color: gray; margin-bottom: 40px;">{persona["profesion"]}</h4>', unsafe_allow_html=True)  # Aumentar el margen
            
            # Imagen del equipo
            persona_image = get_image_b64(persona["imagen_link"])
            if persona_image:
                st.markdown(f'<div style="display: flex; justify-content: center; margin-bottom: 40px;"><img src="data:image/png;base64,{persona_image}" style="border-radius: 50%;" width="150"/></div>', unsafe_allow_html=True)  # Añadir margen abajo
            
            # Logos de redes sociales
            linkedin_logo = get_image_b64("./Streamlit/images/LI-In-Bug.png")
            github_logo = get_image_b64("./Streamlit/images/github-mark-white.png")
            st.markdown(
                f'''
                <div style="display: flex; justify-content: center; margin-top: 10px;">
                    <a href="{persona["linkedin"]}"><img src="data:image/png;base64,{linkedin_logo}" alt="LinkedIn" width="30" style="margin-right: 10px;"/></a>
                    <a href="{persona["github"]}"><img src="data:image/png;base64,{github_logo}" alt="GitHub" width="30"/></a>
                </div>
                ''', 
                unsafe_allow_html=True
            )
