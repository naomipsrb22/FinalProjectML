import json
import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import time
import random
from streamlit_option_menu import option_menu
import os
import traceback
import base64
from pathlib import Path
import gdown
from keras.models import load_model

# --------------------------
# Custom Font & Advanced Aesthetic CSS
# --------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --primary-light: #a5b4fc;
        --secondary: #8b5cf6;
        --accent: #ec4899;
        --accent-dark: #db2777;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --info: #3b82f6;
        --text: #1f2937;
        --light-text: #6b7280;
        --bg: #f9fafb;
        --card-bg: rgba(255, 255, 255, 0.98);
        --glass-bg: rgba(255, 255, 255, 0.25);
        --shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        --glow: 0 0 30px rgba(99, 102, 241, 0.2);
        --transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        --gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
        --gradient-secondary: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        --gradient-dark: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #db2777 100%);
        --gradient-success: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --gradient-warning: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        --border-radius: 20px;
        --border-radius-lg: 30px;
    }
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: var(--bg);
        color: var(--text);
        scroll-behavior: smooth;
        font-weight: 400;
        line-height: 1.6;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 0.75rem;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #f8f9fd 100%);
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Hero Section */
    .hero {
        text-align: center;
        padding: 6rem 1rem 4rem;
        position: relative;
        overflow: hidden;
        margin-bottom: 2rem;
        border-radius: 0 0 var(--border-radius-lg) var(--border-radius-lg);
        background: var(--gradient-dark);
        box-shadow: 0 15px 50px -10px rgba(79, 70, 229, 0.3);
    }
    
    .hero::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 100%;
        background: url('https://images.unsplash.com/photo-1517842645767-c639042777db?q=80&w=1470&auto=format&fit=crop') center/cover;
        z-index: -3;
        opacity: 0.1;
    }
    
    .title {
        font-size: 4.5rem;
        font-weight: 900;
        color: white;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        margin-bottom: 1.5rem;
        line-height: 1.1;
        animation: fadeIn 0.8s ease;
        letter-spacing: -1.5px;
        background: linear-gradient(90deg, #fff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        font-size: 1.5rem;
        font-weight: 400;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2.5rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        animation: fadeIn 1s ease;
    }
    
    /* Cards */
    .card {
        background: var(--card-bg);
        padding: 2.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: var(--transition);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .card::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: var(--gradient);
        opacity: 0.05;
        z-index: -1;
        transform: rotate(30deg);
    }
    
    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15), var(--glow);
    }
    
    .result-card {
        text-align: center;
        padding: 3rem 2rem;
        background: var(--gradient-dark);
        color: white;
        border: none;
        box-shadow: 0 20px 50px -10px rgba(79, 70, 229, 0.3);
    }
    
    .result-card h3 {
        color: white;
        font-size: 2rem;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    .predicted-letter {
        font-size: 12rem;
        font-weight: 900;
        color: white;
        margin: 1.5rem 0;
        text-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        animation: bounce 0.8s ease, pulse 2s infinite;
        line-height: 1;
        background: linear-gradient(135deg, #fff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .confidence-meter {
        height: 18px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
        margin: 2rem auto;
        max-width: 400px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .confidence-fill {
        height: 100%;
        background: var(--gradient-success);
        border-radius: 10px;
        transition: width 1s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
    }
    
    .confidence-text {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 1rem;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient);
        color: white;
        font-weight: 600;
        padding: 1.2rem 2.5rem;
        border-radius: var(--border-radius);
        border: none;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
        transition: var(--transition);
        width: 100%;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        font-size: 1rem;
        position: relative;
        overflow: hidden;
        font-family: 'Poppins', sans-serif;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.3);
        background: var(--gradient);
    }
    
    /* Upload Container */
    .upload-container {
        border: 2px dashed var(--primary-light);
        border-radius: var(--border-radius);
        padding: 4rem 2rem;
        text-align: center;
        transition: var(--transition);
        background: rgba(255, 255, 255, 0.4);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(5px);
    }
    
    .upload-container:hover {
        border-color: var(--primary);
        background: rgba(99, 102, 241, 0.1);
        transform: translateY(-5px);
        box-shadow: var(--glow);
    }
    
    /* Preview Image */
    .preview-image {
        border-radius: var(--border-radius);
        box-shadow: 0 15px 30px -10px rgba(0, 0, 0, 0.1);
        transition: var(--transition);
        object-fit: cover;
        border: 4px solid white;
        width: 100%;
    }
    
    .preview-image:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.15);
    }
    
    /* Animations */
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-25px); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    @keyframes floating {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1.2rem 2rem;
        border-radius: var(--border-radius);
        transition: var(--transition);
        background: rgba(255, 255, 255, 0.7);
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-family: 'Poppins', sans-serif;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: var(--primary) !important;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.15);
        transform: translateY(-3px);
    }
    
    /* Success Message */
    .success-message {
        display: flex;
        align-items: center;
        gap: 1rem;
        color: white;
        font-weight: 500;
        padding: 1.2rem 2rem;
        background: var(--gradient-success);
        border-radius: var(--border-radius);
        margin: 1.5rem 0;
        box-shadow: 0 10px 20px rgba(16, 185, 129, 0.2);
        animation: fadeIn 0.6s ease;
    }
    
    /* Info Box */
    .info-box {
        padding: 2rem;
        background: white;
        border-radius: var(--border-radius);
        border-left: 6px solid var(--primary);
        margin: 2rem 0;
        box-shadow: var(--shadow);
        transition: var(--transition);
    }
    
    .info-box:hover {
        transform: translateY(-5px);
    }
    
    .info-box h3 {
        color: var(--primary-dark);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        font-size: 1.4rem;
    }
    
    /* Feature Cards */
    .feature-card {
        padding: 2.5rem;
        background: white;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow);
        transition: var(--transition);
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .feature-icon {
        width: 80px;
        height: 80px;
        background: var(--gradient);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 2rem;
        color: white;
        font-size: 2rem;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
        animation: floating 4s ease-in-out infinite;
    }
    
    .feature-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 25px 50px -10px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card h3 {
        color: var(--primary-dark);
        margin-bottom: 1.2rem;
        font-size: 1.5rem;
    }
    
    .feature-card p {
        color: var(--light-text);
        font-size: 1.1rem;
        line-height: 1.7;
    }
    
    /* Alphabet Grid */
    .alphabet-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .alphabet-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 2rem 1rem;
        text-align: center;
        box-shadow: var(--shadow);
        transition: var(--transition);
        cursor: pointer;
    }
    
    .alphabet-card:hover {
        background: var(--primary);
        color: white;
        transform: translateY(-8px) scale(1.05);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.2);
    }
    
    .alphabet-char {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--primary);
        margin-bottom: 0.5rem;
        transition: var(--transition);
    }
    
    .alphabet-card:hover .alphabet-char {
        color: white;
    }
    
    .alphabet-label {
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Progress Steps */
    .progress-steps {
        display: flex;
        justify-content: space-between;
        position: relative;
        margin: 3rem 0 4rem;
        counter-reset: step;
    }
    
    .progress-steps::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 6px;
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-50%);
        z-index: -1;
        border-radius: 3px;
    }
    
    .progress-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 150px;
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        background: rgba(255, 255, 255, 0.2);
        border: 4px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        position: relative;
        transition: var(--transition);
        font-size: 1.5rem;
    }
    
    .progress-step.active .step-number {
        background: white;
        border-color: white;
        color: var(--primary);
        transform: scale(1.1);
        box-shadow: 0 10px 20px rgba(255, 255, 255, 0.2);
    }
    
    .step-label {
        font-size: 1rem;
        font-weight: 600;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
    }
    
    .progress-step.active .step-label {
        color: white;
        font-weight: 700;
    }
    
    /* Spinner */
    .spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .spinner-circle {
        width: 80px;
        height: 80px;
        border: 8px solid rgba(255, 255, 255, 0.2);
        border-top-color: white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        font-size: 1rem;
        color: var(--light-text);
        margin-top: 5rem;
        padding: 3rem 0 2rem;
        border-top: 1px solid rgba(0, 0, 0, 0.05);
    }
    
    .social-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--gradient);
        color: white;
        transition: var(--transition);
        margin: 0 0.75rem;
        box-shadow: 0 10px 20px rgba(99, 102, 241, 0.2);
    }
    
    .social-link:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.3);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .title {
            font-size: 3rem;
        }
        .subtitle {
            font-size: 1.2rem;
        }
        .predicted-letter {
            font-size: 8rem;
        }
        .feature-card {
            padding: 2rem;
        }
        .alphabet-grid {
            grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
            gap: 1rem;
        }
        .hero {
            padding: 4rem 1rem 3rem;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-light);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary);
    }
    
    /* Floating elements */
    .floating-element {
        animation: floating 5s ease-in-out infinite;
    }
    
    /* Gradient text */
    .gradient-text {
        background: var(--gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-fill-color: transparent;
    }
    
    /* Section headers */
    .section-header {
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .section-header h2 {
        font-size: 2.8rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, var(--primary) 0%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .section-header p {
        font-size: 1.2rem;
        color: var(--light-text);
        max-width: 700px;
        margin: 0 auto;
    }
    
    /* Sidebar styles */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary-dark) 0%, var(--primary) 100%);
    }

    [data-testid="stSidebarNavItems"] {
        padding-top: 2rem;
    }

    [data-testid="stSidebarNavLink"] {
        color: white !important;
        background: rgba(0, 0, 0, 0.2) !important;  /* buat kontras */
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 1.5rem !important;
        margin: 0.25rem 0 !important;
        border-radius: var(--border-radius) !important;
        transition: var(--transition) !important;
        text-shadow: 0 0 5px rgba(0,0,0,0.7); /* efek bayangan agar teks lebih terbaca */
    }

    [data-testid="stSidebarNavLink"]:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }

    [data-testid="stSidebarNavLink"].active {
        background: white !important;
        color: var(--primary) !important;
        font-weight: 600 !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
    }

    [data-testid="stSidebarNavLink"] svg {
        color: inherit !important;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------
# Load model & class indices
# --------------------------
@st.cache_resource
def load_ml_model():
    try:
        # ID Google Drive untuk model.h5
        model_id = "1fAafbt2aYgX-de9JqaP5Dpk5vDGePH-Z"
        model_file = "model.h5"

        # Path lokal untuk class_indices.json
        class_indices_path = "class_indices.json"

        # Unduh model jika belum ada
        if not os.path.exists(model_file):
            model_url = f"https://drive.google.com/uc?id={model_id}"
            gdown.download(model_url, model_file, quiet=False)

        # Cek apakah class_indices.json ada
        if not os.path.exists(class_indices_path):
            st.error("File class_indices.json tidak ditemukan di direktori lokal.")
            return None, None

        # Load model dan class indices
        model = load_model(model_file)
        with open(class_indices_path, "r") as f:
            class_indices = json.load(f)

        idx_to_label = {int(v): k for k, v in class_indices.items()}
        return model, idx_to_label

    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.error(traceback.format_exc())
        return None, None

# Panggil fungsi
model, idx_to_label = load_ml_model()

# --------------------------
# Particle Animation
# --------------------------
def create_particles():
    particle_html = ""
    colors = [
        (99, 102, 241),   
        (139, 92, 246),   
        (236, 72, 153)    
    ]
    
    for i in range(30):
        size = random.randint(5, 20)
        pos_x = random.randint(0, 100)
        delay = random.randint(0, 15)
        duration = random.randint(15, 40)
        color = random.choice(colors)
        alpha = random.uniform(0.3, 0.7)
        
        particle_html += f"""
        <div class="particle" style="
            width: {size}px;
            height: {size}px;
            left: {pos_x}%;
            top: 100%;
            animation: float {duration}s linear {delay}s infinite;
            animation-delay: {delay}s;
            background: rgba({color[0]}, {color[1]}, {color[2]}, {alpha});
        "></div>
        """
    return particle_html

# --------------------------
# Navigation Menu in Sidebar
# --------------------------
def sidebar_navigation():
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h2 style="color: white; margin-bottom: 0.5rem;">HandTalk</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Penerjemah Bahasa Isyarat</p>
        </div>
        """, unsafe_allow_html=True)
        
        selected = option_menu(
            menu_title=None,
            options=["Beranda", "Deteksi", "Panduan", "Tentang"],
            icons=["house", "camera", "book", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "transparent",
                },
                "nav-link": {
                    "font-family": "'Poppins', sans-serif",
                    "font-size": "1rem",
                    "font-weight": "400",
                    "text-align": "left",
                    "padding": "0.75rem 1.5rem",
                    "margin": "0.25rem 0",
                    "border-radius": "var(--border-radius)",
                    "color": "rgba(0, 0, 0, 0.7)", 
                    "background": "transparent",
                    "transition": "background-color 0.3s ease, color 0.3s ease",
                },
                "nav-link-selected": {
                    "background": "white",
                    "color": "var(--primary)",
                    "font-weight": "600",
                    "box-shadow": "0 5px 15px rgba(0,0,0,0.1)",
                },
                "nav-link:hover": {
                    "background": "rgba(0, 0, 0, 0.1)",  
                    "color": "black",  
                },
            }
        )
    
    return selected

# --------------------------
# Home Page
# --------------------------
def show_home():
    st.markdown("""
    <div class="section-header">
        <h2>HandTalk: Visual Sign Language Translator</h2>
        <p>Mengubah Gerakan Menjadi Makna, Terjemahkan Bahasa Isyarat dengan Mudah!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="font-size: 1.8rem; color: var(--primary-dark); margin-bottom: 1.5rem;">Apa itu HandTalk?</h3>
            <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.8; margin-bottom: 1.5rem;">
                HandTalk adalah solusi berbasis kecerdasan buatan yang dapat mengenali dan menerjemahkan 
                bahasa isyarat dari gambar tangan Anda. Dengan teknologi deep learning terkini, sistem kami 
                mampu mengenali berbagai bentuk tangan dengan akurasi tinggi.
            </p>
            <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.8;">
                Aplikasi ini dirancang untuk membantu komunikasi antara penyandang tunarungu dengan masyarakat 
                umum, serta sebagai alat pembelajaran bahasa isyarat yang interaktif.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h3><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16">
                <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
            </svg> Cara Menggunakan</h3>
            <ol style="padding-left: 1.5rem; color: var(--light-text); line-height: 1.8; font-size: 1.1rem;">
                <li>Pilih menu <strong>Deteksi</strong> di navigasi samping</li>
                <li>Unggah gambar tangan Anda atau ambil foto langsung</li>
                <li>Tunggu sistem menganalisis gambar</li>
                <li>Lihat hasil terjemahan bahasa isyarat</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="card">
            <h3 style="font-size: 1.8rem; color: var(--primary-dark); margin-bottom: 1.5rem;">Fitur Unggulan</h3>
            <div style="display: grid; grid-template-columns: 1fr; gap: 1.5rem;">
                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                    <div style="background: var(--gradient); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">🤖</div>
                    <div>
                        <h4 style="color: var(--primary-dark); margin-bottom: 0.5rem; font-size: 1.3rem;">Model CNN Canggih</h4>
                        <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.6;">Menggunakan arsitektur convolutional neural network yang telah dilatih dengan ribuan gambar</p>
                    </div>
                </div>
                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                    <div style="background: var(--gradient); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">⚡</div>
                    <div>
                        <h4 style="color: var(--primary-dark); margin-bottom: 0.5rem; font-size: 1.3rem;">Proses Cepat</h4>
                        <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.6;">Deteksi real-time dengan waktu pemrosesan kurang dari 3 detik</p>
                    </div>
                </div>
                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                    <div style="background: var(--gradient); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">🎯</div>
                    <div>
                        <h4 style="color: var(--primary-dark); margin-bottom: 0.5rem; font-size: 1.3rem;">Akurasi Tinggi</h4>
                        <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.6;">Tingkat akurasi mencapai 96% pada dataset uji</p>
                    </div>
                </div>
                <div style="display: flex; gap: 1rem; align-items: flex-start;">
                    <div style="background: var(--gradient); width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.5rem;">📱</div>
                    <div>
                        <h4 style="color: var(--primary-dark); margin-bottom: 0.5rem; font-size: 1.3rem;">Responsif</h4>
                        <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.6;">Desain yang optimal untuk semua perangkat, termasuk mobile</p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features Section
    st.markdown("""
    <div class="section-header">
        <h2> Keunggulan HandTalk </h2>
        <p>Teknologi mutakhir untuk pengalaman penerjemahan bahasa isyarat yang lebih baik</p>
    </div>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem; margin-top: 1rem;">
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>Model Deep Learning</h3>
            <p>Menggunakan arsitektur CNN canggih yang telah dilatih dengan ribuan gambar bahasa isyarat untuk mencapai akurasi hingga 97.84%</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <h3>Proses Real-time</h3>
            <p>Deteksi instan dalam hitungan detik dengan optimasi untuk performa tinggi, bahkan pada perangkat mobile</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h3>Presisi Tinggi</h3>
            <p>Mampu membedakan gerakan halus dan bentuk tangan yang mirip dengan algoritma khusus</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# Detection Page
# --------------------------
def show_detection():
    st.session_state.pop("prediction_result", None)

    st.markdown("""
    <div class="section-header">
        <h2>Deteksi Bahasa Isyarat</h2>
        <p>
            Unduh data testing terlebih dahulu pada link di bawah lalu unggah gambar tangan atau ambil foto langsung untuk menerjemahkan bahasa isyarat.
            <a href="https://its.id/m/DataTestingHandTalk" target="_blank">https://its.id/m/DataTestingHandTalk</a> 
        </p>
    </div>
    """, unsafe_allow_html=True)

    if model is None or idx_to_label is None:
        st.error("""
        **Model tidak tersedia!**

        Sistem tidak dapat melakukan deteksi. Kemungkinan penyebab:
        - File model tidak ditemukan di path yang ditentukan
        - Terjadi kesalahan saat memuat model
        - Format model tidak kompatibel

        Silakan periksa kembali path model atau hubungi administrator.
        """)
        return

    tab1, tab2 = st.tabs(["📤 Unggah Gambar", "📷 Ambil Foto Langsung"])

    with tab1:
        st.markdown("""
        <div class="card">
            <h3 style="font-size: 1.8rem; color: var(--primary-dark); margin-bottom: 1.5rem;">Unggah Gambar Tangan Anda</h3>
            <p style="color: var(--light-text); margin-bottom: 2rem; font-size: 1.1rem;">
                Pilih gambar yang menunjukkan huruf bahasa isyarat dengan jelas. Pastikan tangan berada di latar depan 
                dan memiliki kontras yang baik dengan latar belakang.
            </p>
            <div class="upload-container" id="upload-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" fill="var(--primary)" viewBox="0 0 16 16" style="margin-bottom: 1.5rem;">
                    <path d="M.05 3.555A2 2 0 0 1 2 2h12a2 2 0 0 1 1.95 1.555L8 8.414.05 3.555ZM0 4.697v7.104l5.803-3.558L0 4.697ZM6.761 8.83l-6.57 4.027A2 2 0 0 0 2 14h12a2 2 0 0 0 1.808-1.144l-6.57-4.027L8 9.586l-1.239-.757Zm3.436-.586L16 11.801V4.697l-5.803 3.546Z"/>
                </svg>
                <h4 style="color: var(--primary); margin-bottom: 0.5rem;">Seret & Lepas Gambar Disini</h4>
                <p style="color: var(--light-text); font-size: 0.9rem;">atau klik untuk memilih file</p>
                <p style="color: var(--light-text); font-size: 0.8rem; margin-top: 1rem;">Format yang didukung: JPG, PNG, JPEG</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png"], label_visibility="collapsed", key="file_uploader")
        
        if uploaded_file is not None:
            try:
                img = Image.open(uploaded_file)
                st.session_state.uploaded_image = img
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Gambar yang Diunggah")
                    st.image(img, caption="Gambar Asli", use_container_width=True)
                
                with col2:
                    st.markdown("### Preview Pemrosesan")
                    processed_img = img.copy()
                    processed_img = processed_img.resize((100, 100))
                    processed_img = processed_img.convert('RGB')
                    st.image(processed_img, caption="Gambar yang Diproses (100x100)", use_container_width=True)
                    
                    # Add button to detect
                    detect_button = st.button("Deteksi Bahasa Isyarat", use_container_width=True, type="primary", key="detect_upload")
                    
                    if detect_button:
                        with st.spinner('Menganalisis gambar...'):
                            # Simulate processing time
                            progress_bar = st.progress(0)
                            for percent_complete in range(100):
                                time.sleep(0.02)
                                progress_bar.progress(percent_complete + 1)
                            
                            # Prepare image for prediction
                            img_array = image.img_to_array(processed_img)
                            img_array = np.expand_dims(img_array, axis=0)
                            img_array = img_array / 255.0
                            
                            # Make prediction
                            predictions = model.predict(img_array)
                            predicted_class = np.argmax(predictions[0])
                            confidence = np.max(predictions[0])
                            
                            # Store results in session state
                            st.session_state.prediction_result = {
                                "letter": idx_to_label[predicted_class],
                                "confidence": float(confidence),
                                "time": time.strftime("%H:%M:%S")
                            }
                            
                        st.success("Analisis selesai!")
                
                if "prediction_result" in st.session_state:
                    show_prediction_results()

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {str(e)}")
                st.error(traceback.format_exc())
    
    with tab2:
        st.markdown("""
        <div class="card">
            <h3 style="font-size: 1.8rem; color: var(--primary-dark); margin-bottom: 1.5rem;">Ambil Foto Langsung</h3>
            <p style="color: var(--light-text); margin-bottom: 2rem; font-size: 1.1rem;">
                Gunakan kamera perangkat Anda untuk mengambil foto tangan Anda secara langsung. 
                Pastikan pencahayaan cukup dan tangan terlihat jelas.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        camera_img = st.camera_input("Ambil foto tangan Anda", label_visibility="collapsed", key="camera_input")
        
        if camera_img is not None:
            try:
                img = Image.open(camera_img)
                st.session_state.uploaded_image = img
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 📸 Foto yang Diambil")
                    st.image(img, caption="Foto Asli", use_container_width=True)
                
                with col2:
                    st.markdown("### 🔍 Preview Pemrosesan")
                    processed_img = img.copy()
                    processed_img = processed_img.resize((100, 100))
                    processed_img = processed_img.convert('RGB')
                    st.image(processed_img, caption="Gambar yang Diproses (100x100)", use_container_width=True)
                    
                    # Add button to detect
                    detect_button = st.button("Deteksi Bahasa Isyarat", use_container_width=True, type="primary", key="camera_detect")
                    
                    if detect_button:
                        with st.spinner('Menganalisis gambar...'):
                            # Simulate processing time
                            progress_bar = st.progress(0)
                            for percent_complete in range(100):
                                time.sleep(0.02)
                                progress_bar.progress(percent_complete + 1)
                            
                            # Prepare image for prediction
                            img_array = image.img_to_array(processed_img)
                            img_array = np.expand_dims(img_array, axis=0)
                            img_array = img_array / 255.0
                            
                            # Make prediction
                            predictions = model.predict(img_array)
                            predicted_class = np.argmax(predictions[0])
                            confidence = np.max(predictions[0])
                            
                            # Store results in session state
                            st.session_state.prediction_result = {
                                "letter": idx_to_label[predicted_class],
                                "confidence": float(confidence),
                                "time": time.strftime("%H:%M:%S")
                            }
                            
                            # Show success message
                        st.success("Analisis selesai!")
                
                if "prediction_result" in st.session_state:
                    show_prediction_results()

            except Exception as e:
                st.error(f"Terjadi kesalahan saat memproses gambar: {str(e)}")
                st.error(traceback.format_exc())

    # Jangan lagi panggil show_prediction_results() di sini tanpa pengecekan,
    # sudah diganti ke atas dan dilindungi dengan kondisi valid

# Function to display prediction results
def show_prediction_results():
    result = st.session_state.get("prediction_result")

    if not isinstance(result, dict) or "confidence" not in result or "letter" not in result:
        st.warning("Hasil analisis belum tersedia atau tidak valid.")
        return

    confidence_percent = result["confidence"] * 100

    st.markdown("---")
    st.markdown("## 📊 Hasil Analisis")

    st.markdown(f"""
    <div class="result-card">
        <h3>Huruf yang Terdeteksi</h3>
        <div class="predicted-letter">{result["letter"]}</div>
        <div class="confidence-meter">
            <div class="confidence-fill" style="width: {confidence_percent}%"></div>
        </div>
        <div class="confidence-text">
            Tingkat Kepercayaan: <strong>{confidence_percent:.2f}%</strong>
        </div>
        <p style="color: rgba(255,255,255,0.8); margin-top: 1.5rem;">Dianalisis pada: {result["time"]}</p>
    </div>
    """, unsafe_allow_html=True)

def show_guide():
    """Display a comprehensive guide for sign language with alphabet, numbers, and tips."""
    # CSS Styles with better organization and variables
    st.markdown("""
    <style>
    :root {
        --primary: #4a6bdf;
        --primary-dark: #3a56b2;
        --accent: #ff6b6b;
        --light-text: #6c757d;
        --card-bg: rgba(255, 255, 255, 0.05);
    }
    
    .section-header {
        margin-bottom: 2.5rem;
    }
    
    .section-title {
        font-size: 2rem;
        color: var(--primary-dark);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .section-subtitle {
        color: var(--light-text);
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    .card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .card-title {
        font-size: 1.5rem;
        color: var(--primary-dark);
        margin-bottom: 1.5rem;
        position: relative;
        padding-bottom: 0.5rem;
    }
    
    .card-title:after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 50px;
        height: 3px;
        background: var(--accent);
    }
    
    .card-description {
        color: var(--light-text);
        margin-bottom: 2rem;
        font-size: 1.05rem;
        line-height: 1.7;
    }
    
    .alphabet-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
        gap: 1.2rem;
        margin-top: 1.5rem;
    }
    
    .alphabet-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem 0.8rem;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .alphabet-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .alphabet-char {
        font-size: 2.2rem;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 0.6rem;
    }
    
    .alphabet-label {
        font-size: 0.85rem;
        color: var(--light-text);
        line-height: 1.4;
    }
    
    .tips-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.8rem;
        margin-top: 1.5rem;
    }
    
    .tip-item {
        background: var(--card-bg);
        border-radius: 10px;
        padding: 1.5rem;
        transition: all 0.3s ease;
        border-left: 4px solid var(--accent);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .tip-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .tip-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1rem;
    }
    
    .tip-header h4 {
        color: var(--primary);
        margin: 0;
        font-size: 1.15rem;
    }
    
    .tip-icon {
        min-width: 24px;
        color: var(--accent);
    }
    
    .tip-item p {
        color: var(--light-text);
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.7;
    }
    
    @media (max-width: 768px) {
        .alphabet-grid {
            grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
        }
        
        .tips-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Section 1: Header with better structure
    st.markdown("""
    <div class="section-header">
        <h1 class="section-title">📚 Panduan Bahasa Isyarat</h1>
        <p class="section-subtitle">Pelajari alfabet dan angka bahasa isyarat Indonesia (BISINDO) dengan panduan interaktif kami. 
        Gunakan panduan ini untuk memahami gerakan tangan yang benar.</p>
    </div>
    """, unsafe_allow_html=True)

    # Section 2: Alphabet and Number Guide with improved organization
    st.markdown("""
    <div class="card">
        <h2 class="card-title">Alfabet & Angka Bahasa Isyarat</h2>
        <p class="card-description">
            Sistem kami mendukung pengenalan seluruh huruf alfabet (A-Z) dan angka (0-9) dalam bahasa isyarat Indonesia. 
            Berikut adalah panduan visual dengan contoh gerakan tangan yang benar untuk setiap karakter.
        </p>
        <div class="alphabet-grid">
    """, unsafe_allow_html=True)

    # Data organization
    alphabet_guide = {
        "A": "Tangan dikepal rapat menghadap depan",
        "B": "Ibu jari menyentuh telapak tangan",
        "C": "Bentuk seperti huruf C dengan jari",
        "D": "Jari telunjuk mengarah ke atas",
        "E": "Tangan dikepal terbuka sedikit menghadap depan",
        "F": "Ibu jari dan telunjuk bersentuhan",
        "G": "Telunjuk menunjuk ke samping",
        "H": "Telunjuk dan jari tengah menunjuk ke samping",
        "I": "Kelingking terangkat, jari lain mengepal",
        "J": "Kelingking terangkat, jari lain mengepal dimiringkan",
        "K": "Telunjuk dan jari tengah mengarah atas, ibu jari di tengah kedua jari",
        "L": "Ibu jari dan telunjuk membentuk L",
        "M": "Tangan dikepal, ibu jari di sela jari kelingking dan jari manis",
        "N": "Tangan dikepal, ibu jari di sela jari manis dan jari tengah",
        "O": "Semua jari membentuk lingkaran",
        "P": "Telunjuk tegak lurus, ibu jari menyentuh jari tengah menghadap bawah",
        "Q": "Ibu jari dan jari telunjuk menghadap bawah",
        "R": "Jari tengah menyilang di atas telunjuk",
        "S": "Kepalan tangan tertutup sempurna",
        "T": "Tangan dikepal, ibu jari di sela jari tengah dan jari telunjuk",
        "U": "Telunjuk dan jari tengah rapat ke atas",
        "V": "Telunjuk dan jari tengah membentuk V",
        "W": "Telunjuk, tengah, dan manis membentuk W",
        "X": "Ibu jari digenggam jari tengah, manis, dan kelingking, telunjuk menekuk",
        "Y": "Ibu jari dan kelingking terentang",
        "Z": "Jari telunjuk diangkat ke atas dan miring"
    }

    number_guide = {
        "0": "Kepalan tangan terbuka sedikit",
        "1": "Jari telunjuk mengarah ke atas",
        "2": "Telunjuk dan jari tengah membentuk V",
        "3": "Ibu jari, telunjuk, dan jari tengah terangkat",
        "4": "Empat jari terentang (ibu jari terlipat)",
        "5": "Semua lima jari terentang lebar",
        "6": "Ibu jari menyentuh kelingking",
        "7": "Ibu jari menyentuh jari manis",
        "8": "Ibu jari menyentuh jari tengah",
        "9": "Ibu jari menyentuh jari telunjuk"
    }

    # Combine and display
    full_guide = {**alphabet_guide, **number_guide}
    guide_html = "".join(
        f"""
        <div class="alphabet-card">
            <div class="alphabet-char">{char}</div>
            <div class="alphabet-label">{desc}</div>
        </div>
        """ for char, desc in full_guide.items()
    )
    
    st.markdown(guide_html + "</div></div>", unsafe_allow_html=True)

    # Section 3: Image Capture Tips with better icons and structure
    st.markdown("""
    <div class="card">
        <h2 class="card-title">Tips Pengambilan Gambar</h2>
        <p class="card-description">
            Untuk mendapatkan hasil pengenalan yang optimal, ikuti panduan berikut saat mengambil gambar isyarat tangan:
        </p>
        <div class="tips-grid">
    """, unsafe_allow_html=True)

    tips = [
        ("💡 Pencahayaan", "Pastikan pencahayaan cukup dan merata. Hindari bayangan pada tangan dan latar belakang yang terlalu terang/gelap. Pencahayaan alami dari samping biasanya yang terbaik."),
        ("🌅 Latar Belakang", "Gunakan latar belakang polos dengan warna hitam. Hindari pola atau tekstur yang rumit."),
        ("✋ Posisi Tangan", "Pastikan seluruh tangan terlihat jelas dalam frame. Jari-jari harus terbuka dan tidak saling menutupi. Tunjukkan bagian depan tangan."),
        ("📏 Ukuran Tangan", "Tangan harus memenuhi 60-70% frame. Jarak ideal adalah sekitar 50-80 cm dari kamera. Hindari terlalu dekat atau terlalu jauh."),
        ("📷 Kamera Stabil", "Gunakan penyangga atau letakkan tangan di permukaan datar. Jika memotret sendiri, gunakan timer untuk menghindari guncangan."),
        ("🖐️ Isyarat Tunggal", "Pastikan hanya satu isyarat yang ditampilkan per gambar. Sistem bekerja optimal dengan satu tangan yang jelas terlihat."),
        ("👕 Lengan Terlihat", "Pastikan lengan bawah terlihat jelas. Gunakan lengan baju pendek atau gulung lengan baju panjang."),
        ("⏱️ Waktu Pengambilan", "Tahan posisi selama 1-2 detik sebelum mengambil gambar untuk memastikan pose stabil dan jelas.")
    ]

    tips_html = "".join(
        f"""
        <div class="tip-item">
            <div class="tip-header">
                <h4>{title}</h4>
            </div>
            <p>{desc}</p>
        </div>
        """ for title, desc in tips
    )
    
    st.markdown(tips_html + "</div></div>", unsafe_allow_html=True)

    # Additional section for best practices
    st.markdown("""
    <div class="card">
        <h2 class="card-title">Praktik Terbaik</h2>
        <p class="card-description">
            Beberapa saran tambahan untuk membantu Anda belajar bahasa isyarat dengan lebih efektif:
        </p>
        <div class="tips-grid">
            <div class="tip-item">
                <div class="tip-header">
                    <h4>🔁 Latihan Rutin</h4>
                </div>
                <p>Berlatihlah secara teratur setiap hari, bahkan jika hanya 10-15 menit. Konsistensi adalah kunci untuk menguasai bahasa isyarat.</p>
            </div>
            <div class="tip-item">
                <div class="tip-header">
                    <h4>🔄 Umpan Balik</h4>
                </div>
                <p>Gunakan sistem kami untuk memeriksa akurasi isyarat Anda. Rekam diri sendiri dan bandingkan dengan panduan.</p>
            </div>
            <div class="tip-item">
                <div class="tip-header">
                    <h4>👥 Belajar Bersama</h4>
                </div>
                <p>Jika memungkinkan, berlatihlah dengan partner atau bergabung dengan komunitas bahasa isyarat untuk praktik langsung.</p>
            </div>
            <div class="tip-item">
                <div class="tip-header">
                    <h4>📈 Mulai dari Dasar</h4>
                </div>
                <p>Mulailah dengan alfabet dan angka sebelum beralih ke kata dan kalimat. Kuasai dasar-dasarnya terlebih dahulu.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
# --------------------------
# About Page
# --------------------------
import streamlit as st

def show_about():
    st.markdown("""
    <div class="section-header">
        <h2>Tentang HandTalk</h2>
        <p>Mengenal lebih dalam tentang teknologi di balik aplikasi penerjemah bahasa isyarat ini</p>
    </div>
    """, unsafe_allow_html=True)

    # Teknologi Kami - Bagian 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card">
            <h3 style="font-size: 1.8rem; color: var(--primary-dark); margin-bottom: 1.5rem;">Teknologi Kami</h3>
            <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.7; margin-bottom: 1.5rem;">
                HandTalk AI menggunakan model <strong>Convolutional Neural Network (CNN)</strong> yang telah dilatih dengan lebih dari 2000 gambar bahasa isyarat. 
                Arsitektur model kami terdiri dari 16 lapisan konvolusi yang dirancang untuk mengekstrak fitur kompleks dari gambar tangan.
            </p>
            <p style="color: var(--light-text); font-size: 1.1rem; line-height: 1.7;">
                Sistem kami mencapai akurasi <strong>97.84%</strong> pada dataset uji, dengan waktu deteksi rata-rata hanya <strong>1.8 detik</strong> per gambar.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <style>
            .value-right {
                min-width: 100px;
                text-align: right;
                display: inline-block;
                color: black;
            }
            .card-purple {
                background: linear-gradient(135deg, #6A00FF, #8E2DE2);
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                color: white;
            }
            .card-purple .inner-box {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                color: black;
            }
            .card-purple h3 {
                color: white;
                margin-bottom: 1.5rem;
            }
        </style>

        <div class="card-purple">
            <h3 style="font-size: 1.8rem;">Arsitektur Model</h3>
            <div class="inner-box">
                <div style="display: flex; justify-content: space-between; padding: 0.8rem; border-bottom: 1px solid rgba(0,0,0,0.1);">
                    <span>Input Layer</span>
                    <span class="value-right">100x100x3</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem; border-bottom: 1px solid rgba(0,0,0,0.1);">
                    <span>Convolutional Layers</span>
                    <span class="value-right">4 layers</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem; border-bottom: 1px solid rgba(0,0,0,0.1);">
                    <span>Max Pooling</span>
                    <span class="value-right">4 layers</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem; border-bottom: 1px solid rgba(0,0,0,0.1);">
                    <span>Dropout</span>
                    <span class="value-right">0.5</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem; border-bottom: 1px solid rgba(0,0,0,0.1);">
                    <span>Dense Layers</span>
                    <span class="value-right">2 layers</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 0.8rem;">
                    <span>Output Classes</span>
                    <span class="value-right">36 classes</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Metrics Cards
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 2rem 0;">
        <div style="background: linear-gradient(to right, #10b981, #34d399); color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 2rem; font-weight: 700;">97.84%</div>
            <div style="font-size: 1rem;">Akurasi</div>
        </div>
        <div style="background: linear-gradient(to right, #f59e0b, #fbbf24); color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 2rem; font-weight: 700;">1.8s</div>
            <div style="font-size: 1rem;">Waktu Deteksi</div>
        </div>
        <div style="background: linear-gradient(to right, #8b5cf6, #a78bfa); color: white; padding: 1.5rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 2rem; font-weight: 700;">36</div>
            <div style="font-size: 1rem;">Huruf dan Angka</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tim Pengembang (versi aman)
    st.markdown("### 👨‍💼 Tim Pengembang")

    def image_to_base64(image_path):
        try:
            # Gunakan os.path untuk path yang portable
            full_path = os.path.join(os.path.dirname(__file__), image_path)
            if not os.path.exists(full_path):
                st.error(f"File not found: {full_path}")
                return None
                
            with open(full_path, "rb") as img_file:
                encoded = base64.b64encode(img_file.read()).decode()
                return f"data:image/png;base64,{encoded}"
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
            return None

    # Struktur team dengan path relatif
    team = [
        {"photo": "images/naomi.png", "name": "Naomi Gloria Pasaribu", "role": "Machine Learning Engineer"},
        {"photo": "images/nurfajriyani.png", "name": "Nurfajriyani", "role": "Data Scientist"},
        {"photo": "images/famita.png", "name": "Famita Wibi Wulandari", "role": "Frontend Developer"},
        {"photo": "images/anindya.png", "name": "Anindya Putri Noliza", "role": "UI/UX Designer"},
    ]

    # CSS Styling untuk penyamaan ukuran dan penataan layout
    st.markdown("""
        <style>
        .team-card {
            background: linear-gradient(135deg, #6A00FF, #8E2DE2);
            padding: 1.5rem 1rem;
            border-radius: 16px;
            text-align: center;
            color: white;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            margin: 0.5rem;
            height: 250px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: center;
        }

        .team-photo {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 50%;
            border: 3px solid white;
            margin-bottom: 1rem;
        }

        .team-name {
            font-weight: 600;
            font-size: 1rem;
            height: 2.5em; /* fixed height so all names align */
            line-height: 1.25em;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }

        .team-role {
            font-size: 0.9rem;
            color: #eee;
            height: 2em; /* fixed height for consistent role alignment */
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Buat kolom dan tampilkan kartu tim
    cols = st.columns(len(team))

    for col, member in zip(cols, team):
        with col:
            img_data = image_to_base64(member["photo"])
            st.markdown(f"""
                <div class="team-card">
                    <img src="{img_data}" class="team-photo" />
                    <div class="team-name">{member['name']}</div>
                    <div class="team-role">{member['role']}</div>
                </div>
            """, unsafe_allow_html=True)
        
    # Kontak Kami (versi aman)
    st.markdown("### 📬 Kontak Kami")

    st.write("Punya pertanyaan atau masukan? Kami terbuka untuk kolaborasi dan umpan balik.")

    col_email, col_github, col_twitter = st.columns(3)

    with col_email:
        st.markdown("[📧 Email](mailto:info@handtalkai.com)")

    with col_github:
        st.markdown("[💻 GitHub](https://github.com/handtalkai)")

    with col_twitter:
        st.markdown("[🐦 Twitter](https://twitter.com/handtalkai)")

    st.markdown("""
    <div style="text-align:center; color: gray; font-size: 0.9rem; margin-top: 2rem;">
        © 2025 HandTalk. Dari kami untuk kita.
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# Main App Logic
# --------------------------
def main():
    # Initialize session state
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None
    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None
    
    # Add particles animation
    st.markdown(f"""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: -1; overflow: hidden;">
        {create_particles()}
        <style>
        @keyframes float {{
            0% {{ transform: translateY(0) translateX(0) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            100% {{ transform: translateY(-1000px) translateX(1000px) rotate(720deg); opacity: 0; }}
        }}
        .particle {{
            position: absolute;
            border-radius: 50%;
            animation-timing-function: linear;
        }}
        </style>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    selected_page = sidebar_navigation()
    
    # Page routing
    if selected_page == "Beranda":
        show_home()
    elif selected_page == "Deteksi":
        show_detection()
    elif selected_page == "Panduan":
        show_guide()
    elif selected_page == "Tentang":
        show_about()

if __name__ == "__main__":
    main()
