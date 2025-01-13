import streamlit as st
import base64
from PIL import Image

# Function to convert an image to base64
def get_image_b64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Image not found at {image_path}")
        return None

# Function to set the background of the page with a slight transparency
def set_background(png_file):
    encoded_image = get_image_b64(png_file)
    if encoded_image:
        st.markdown(
            f"""
            <style>
            .stApp {{
                margin: auto;
                background-image: url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: scroll;
                background-position: center;
                background-color: rgba(0,0,0,0.8);
                overflow: auto;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    # Get the logo image in base64
    logo_b64 = get_image_b64('./Streamlit/images/uber_logo1.png')

    # Get the Canva image in base64
    canva_b64 = get_image_b64('./Streamlit/images/canva.png')

    # Check if logo is loaded correctly
    if logo_b64:
        # Reduce vertical spacing with 'mt-1' class and set smaller logo size
        st.markdown(
            f"""
            <div class="container-fluid d-flex justify-content-center align-items-center" style="height: 30vh;">
                <div class="row text-center">
                    <div class="col">
                        <img src="data:image/png;base64,{logo_b64}" alt="Uber Logo" style="width: 180px; margin-top: 1rem; border-radius: 50%;">  
                        <p>&nbsp;</p>
                        <h1 class="mt-1" style="color: #ffffff; text-shadow: 6px 6px 9.5px #000000; font-size: 4.2rem; font-weight: bold;">Data Product by Arcope</h1>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Logo image not found!")

    # Check if Canva image is loaded correctly
    if canva_b64:
        # Display Canva image with link and hover effect
        st.markdown(
            f"""
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <p>&nbsp;</p>
            <div class="container-fluid d-flex justify-content-center align-items-center" style="height: 30vh;">
                <div class="row text-center">
                    <div class="col">
                        <a href="https://www.canva.com/design/DAGSRLCbQ_4/ElfqkaX_JbZqlid7SVm3pw/edit?utm_content=DAGSRLCbQ_4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton" target="_blank">
                            <img src="data:image/jpeg;base64,{canva_b64}" alt="Canva" class="hover-image" style="width: 560px; margin-top: 2rem; transition: transform 0.5s;">
                        </a>
                        <h2 class="mt-1" style="color: #ffffff; text-shadow: 6px 6px 9.5px #000000; font-size: 4.2rem; font-weight: bold;">Presentacion del proyecto</h2>
                    </div>
                </div>
            </div>
            <p>&nbsp;</p>
            <style>
            .hover-image:hover {{
                transform: scale(1.05);  /* Slight zoom on hover */
                transition: transform 0.3s ease-in-out;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Canva image not found!")




# Function to set the logo and reduce space between navbar and logo
def inicio_page():
    # Set the background with 80% opacity
    set_background('./Streamlit/images/wallpaper_uber.png')

    
