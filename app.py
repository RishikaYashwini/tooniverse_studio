import streamlit as st
from PIL import Image
from utils.classic_cartoonify import run_classic_cartoonify
from utils.ai_style_transfer import run_ai_style_transfer
from utils.segmentation import run_segmentation
from utils.selective_processing import apply_selective_effect, apply_background_blur
from utils.animation import run_animation
from utils.vectorization import convert_to_svg
from utils.presets import CLASSIC_PRESETS, AI_STYLE_PRESETS
import io
import base64
import os
import tempfile

# Page configuration
st.set_page_config(
    page_title="Tooniverse Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded",  # Changed to expanded
    menu_items={
        'About': "# Tooniverse Studio\nAI-Powered Image Cartoonification Platform"
    }
)

# Complete CSS with fixes
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap');
    
    /* Root variables */
    :root {
        --periwinkle: #735DA5;
        --periwinkle-dark: #5d4a88;
        --periwinkle-light: #8b7ab5;
        --lilac: #D3C5E5;
        --lilac-light: #e6ddf2;
        --cream: #F5F3F7;
        --light-gray: #E8E4EC;
        --text-dark: #2d2436;
        --text-medium: #4a3d5a;
        --text-light: #7a6d8a;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #F5F3F7 0%, #ede9f3 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Force text colors */
    .stApp, .stApp * {
        color: var(--text-dark) !important;
    }
    
    /* FIXED: Sidebar visibility - always show in studio mode */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ede9f3 0%, #e0d9ed 100%);
        border-right: 3px solid var(--lilac);
        display: block !important;
    }
    
    [data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
    }
    
    /* Sidebar text visibility */
    [data-testid="stSidebar"] * {
        color: var(--text-dark) !important;
    }
    
    /* Landing page hero section - FIXED COLORS */
    .hero-container {
        text-align: center;
        padding: 2rem 2rem;  /* Reduced from 4rem */
        background: linear-gradient(135deg, #735DA5 0%, #9b87c4 50%, #D3C5E5 100%);
        border-radius: 30px;
        margin: 1rem auto 1.5rem;  /* Reduced margins */
        max-width: 1200px;
        box-shadow: 0 20px 60px rgba(115, 93, 165, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: float 10s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        50% { transform: translate(-30px, 30px) rotate(180deg); }
    }
    
    /* FIXED: Title white, subtitle and description black with center alignment */
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;  /* Reduced from 4rem */
        font-weight: 800;
        color: white !important;
        margin: 0 auto;
        text-shadow: 3px 3px 8px rgba(45, 36, 54, 0.4);
        letter-spacing: 3px;
        position: relative;
        z-index: 1;
        animation: fadeInDown 1s ease-out;
        text-align: center !important;
    }

    .hero-subtitle {
        font-size: 1.2rem;  /* Reduced from 1.4rem */
        color: #2d2436 !important;
        margin: 1rem auto !important;  /* Reduced from 1.5rem */
        font-weight: 600;
        position: relative;
        z-index: 1;
        animation: fadeInUp 1s ease-out 0.3s both;
        max-width: 800px;
        text-align: center !important;
        display: block !important;
    }

    .hero-description {
        font-size: 1rem;  /* Reduced from 1.1rem */
        color: #2d2436 !important;
        max-width: 700px;
        margin: 0.8rem auto 1.5rem !important;  /* Reduced from 1rem auto 2rem */
        line-height: 1.8;
        position: relative;
        z-index: 1;
        animation: fadeInUp 1s ease-out 0.6s both;
        text-align: center !important;
        display: block !important;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--periwinkle) !important;
        font-weight: 600 !important;
    }
    
    /* Subheaders in columns */
    [data-testid="column"] h3 {
        color: var(--periwinkle) !important;
        background: linear-gradient(135deg, #ede9f3 0%, #e0d9ed 100%);
        padding: 1.3rem;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(115, 93, 165, 0.15);
        font-weight: 600 !important;
        border-left: 5px solid var(--periwinkle);
        font-family: 'Playfair Display', serif;
    }
    
    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--periwinkle-dark) !important;
        font-weight: 700 !important;
        padding: 0.9rem;
        background: linear-gradient(135deg, #e0d9ed 0%, #d3c5e5 100%);
        border-radius: 14px;
        margin: 0.6rem 0;
        border-left: 5px solid var(--periwinkle);
    }
    
    /* Studio choice cards */
    .studio-card {
        background: linear-gradient(135deg, #ffffff 0%, #f5f3f7 100%);
        padding: 3rem 2rem;
        border-radius: 25px;
        box-shadow: 0 8px 30px rgba(115, 93, 165, 0.2);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 3px solid var(--lilac-light);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .studio-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(115, 93, 165, 0.08) 0%, transparent 70%);
        transform: scale(0);
        transition: transform 0.6s ease;
    }
    
    .studio-card:hover::before {
        transform: scale(1);
    }
    
    .studio-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 15px 50px rgba(115, 93, 165, 0.35);
        border-color: var(--periwinkle);
    }
    
    .studio-card-icon {
        font-size: 4rem;
        margin-bottom: 1.5rem;
        filter: drop-shadow(0 4px 8px rgba(115, 93, 165, 0.3));
        position: relative;
        z-index: 1;
    }
    
    .studio-card-title {
        font-family: 'Playfair Display', serif;
        font-size: 2rem;
        color: var(--periwinkle);
        margin-bottom: 1rem;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    
    .studio-card-description {
        color: var(--text-medium);
        font-size: 1.05rem;
        line-height: 1.7;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .studio-card-features {
        text-align: left;
        margin: 1.5rem 0;
        position: relative;
        z-index: 1;
    }
    
    .feature-item {
        padding: 0.5rem 0;
        color: var(--text-medium);
        font-size: 0.95rem;
    }
    
    .feature-item::before {
        content: "✨ ";
        margin-right: 0.5rem;
    }
    
    /* Paragraph text */
    p {
        color: var(--text-medium) !important;
        line-height: 1.7;
    }
    
    /* Label text */
    label {
        color: var(--text-dark) !important;
        font-weight: 500 !important;
    }
    
    /* Primary Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #735DA5 0%, #8b7ab5 100%) !important;
        color: white !important;
        border: none;
        border-radius: 14px;
        padding: 0.8rem 1.8rem;
        font-weight: 600 !important;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 18px rgba(115, 93, 165, 0.4);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(115, 93, 165, 0.5);
        background: linear-gradient(135deg, #8b7ab5 0%, #735DA5 100%) !important;
    }
    
    .stButton>button p {
        color: white !important;
    }
    
    /* Download button styling */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #5d4a88 0%, #735DA5 100%) !important;
        color: white !important;
        border-radius: 14px;
        font-weight: 600 !important;
        transition: all 0.3s ease;
        box-shadow: 0 5px 18px rgba(93, 74, 136, 0.4);
    }
    
    .stDownloadButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(93, 74, 136, 0.5);
    }
    
    .stDownloadButton>button p {
        color: white !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background-color: var(--periwinkle) !important;
    }
    
    /* Radio button styling */
    .stRadio > label {
        background: linear-gradient(135deg, #f5f3f7 0%, #ede9f3 100%);
        padding: 0.6rem;
        border-radius: 12px;
        margin: 0.3rem 0;
        color: var(--text-dark) !important;
        border-left: 4px solid var(--lilac);
        transition: all 0.3s ease;
    }
    
    .stRadio > label:hover {
        border-left-color: var(--periwinkle);
        box-shadow: 0 3px 10px rgba(115, 93, 165, 0.15);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 12px;
        border: 2px solid var(--lilac);
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--periwinkle);
    }
    
    /* Alert boxes */
    .stAlert {
        border-radius: 14px;
        border-left: 5px solid var(--periwinkle);
        background: linear-gradient(135deg, #ede9f3 0%, #e6ddf2 100%) !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #e6ddf2 0%, #d9cfe8 100%) !important;
        border-left: 5px solid var(--periwinkle);
        border-radius: 14px;
    }
    
    /* Checkbox styling */
    .stCheckbox {
        background: linear-gradient(135deg, #ede9f3 0%, #e6ddf2 100%);
        padding: 0.6rem;
        border-radius: 12px;
        border-left: 4px solid var(--periwinkle);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #ede9f3 0%, #e6ddf2 100%);
        border-radius: 12px;
        color: var(--text-dark) !important;
        border-left: 4px solid var(--periwinkle);
        font-weight: 600 !important;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, white 0%, #f5f3f7 100%);
        border: 2px dashed var(--lilac);
        border-radius: 14px;
        padding: 1.2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--periwinkle);
        background: linear-gradient(135deg, #f5f3f7 0%, #ede9f3 100%);
        box-shadow: 0 5px 20px rgba(115, 93, 165, 0.2);
    }
    
    /* Image containers */
    [data-testid="stImage"] {
        border-radius: 18px;
        overflow: hidden;
        box-shadow: 0 6px 25px rgba(115, 93, 165, 0.25);
        transition: transform 0.3s ease;
        border: 4px solid var(--lilac-light);
    }
    
    [data-testid="stImage"]:hover {
        transform: scale(1.03);
        box-shadow: 0 10px 35px rgba(115, 93, 165, 0.35);
    }
    
    /* Caption text */
    .stCaption, small {
        color: var(--text-light) !important;
        font-size: 0.9rem;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, var(--lilac), var(--periwinkle), var(--lilac), transparent);
        opacity: 0.6;
        border-radius: 3px;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 3rem auto;
        max-width: 900px;
    }
    
    .stat-item {
        text-align: center;
        padding: 1.5rem;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--periwinkle);
        font-family: 'Playfair Display', serif;
    }
    
    .stat-label {
        font-size: 1rem;
        color: var(--text-medium);
        margin-top: 0.5rem;
    }
    
    /* Compact modern button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #735DA5 0%, #8b7ab5 100%) !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem !important;  /* More compact */
        font-weight: 600 !important;
        font-size: 0.95rem !important;  /* Slightly smaller */
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(115, 93, 165, 0.35);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(115, 93, 165, 0.45);
    }
    
    /* Beautiful Blurred Background for Landing Page */
    .landing-page-wrapper {
        background: linear-gradient(135deg, #735DA5 0%, #D3C5E5 50%, #735DA5 100%);
        background-attachment: fixed;
        backdrop-filter: blur(10px);
        position: relative;
        padding: 1.5rem;
        min-height: 100vh;
        border-radius: 0;
    }

    .landing-page-wrapper::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 20% 80%, rgba(211, 197, 229, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(115, 93, 165, 0.2) 0%, transparent 50%),
                    radial-gradient(circle at 50% 50%, rgba(211, 197, 229, 0.1) 0%, transparent 60%);
        pointer-events: none;
        z-index: -1;
    }

    /* Compact adjustments */
    .compact-section {
        max-width: 1300px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'studio_type' not in st.session_state:
    st.session_state.studio_type = None
if 'original_image' not in st.session_state:
    st.session_state.original_image = None
if 'processed_image' not in st.session_state:
    st.session_state.processed_image = None
if 'uploaded_file_bytes' not in st.session_state:
    st.session_state.uploaded_file_bytes = None

# Helper functions
def process_cartoonify(image_bytes, edge_threshold, bilateral_d, num_colors):
    image = Image.open(io.BytesIO(image_bytes))
    return run_classic_cartoonify(image, edge_threshold, bilateral_d, num_colors)

def process_ai_style(image, style_type, strength):
    return run_ai_style_transfer(image, style_type, strength)

def go_to_studio(studio_type):
    st.session_state.page = 'studio'
    st.session_state.studio_type = studio_type

def go_to_landing():
    st.session_state.page = 'landing'
    st.session_state.studio_type = None
    st.session_state.original_image = None
    st.session_state.processed_image = None

# ==================== LANDING PAGE ====================
if st.session_state.page == 'landing':
    
    # Wrapper with blurred background
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(135deg, #F5F3F7 0%, #ede9f3 100%); z-index: -1;"></div>
    """, unsafe_allow_html=True)
    
    # Blurred gradient overlay
    st.markdown("""
    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; 
                background: 
                    radial-gradient(circle at 20% 80%, rgba(211, 197, 229, 0.15) 0%, transparent 40%),
                    radial-gradient(circle at 80% 20%, rgba(115, 93, 165, 0.12) 0%, transparent 40%),
                    radial-gradient(circle at 50% 50%, rgba(211, 197, 229, 0.08) 0%, transparent 50%);
                backdrop-filter: blur(0.5px);
                z-index: -1;"></div>
    """, unsafe_allow_html=True)
    
    # Compact Hero Section
    st.markdown("""
    <div style="text-align: center; padding: 1.2rem 2rem; background: linear-gradient(135deg, #735DA5 0%, #9b87c4 50%, #D3C5E5 100%); border-radius: 20px; margin: 0 auto 1.2rem; max-width: 1300px; box-shadow: 0 8px 25px rgba(115, 93, 165, 0.3); backdrop-filter: blur(10px);">
        <h1 style="font-family: 'Playfair Display', serif; font-size: 2.3rem; font-weight: 800; color: white; margin: 0; text-shadow: 2px 2px 6px rgba(45, 36, 54, 0.4); letter-spacing: 2px;">
            🎨 Tooniverse Studio
        </h1>
        <p style="font-size: 1rem; color: #2d2436; margin: 0.6rem auto 0.4rem; font-weight: 600; max-width: 700px;">
            Transform Your Photos into Stunning Cartoons
        </p>
        <p style="font-size: 0.9rem; color: #2d2436; max-width: 600px; margin: 0.3rem auto 0; line-height: 1.5;">
            Choose your style, customize, and create instantly ✨
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Studio Selection Cards in 2 columns - More Compact
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f5f3f7 100%); padding: 1.8rem 1.3rem; border-radius: 18px; box-shadow: 0 6px 20px rgba(115, 93, 165, 0.15); border: 2px solid #e6ddf2; backdrop-filter: blur(5px); height: 100%; min-height: 300px;">
            <div style="text-align: center;">
                <div style="font-size: 2.8rem; margin-bottom: 0.6rem;">🎨</div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: #735DA5; margin-bottom: 0.6rem; font-weight: 700;">Classic Studio</h3>
                <p style="color: #4a3d5a; font-size: 0.9rem; line-height: 1.4; margin-bottom: 0.8rem;">
                    Traditional cartoon effects with precision control
                </p>
            </div>
            <div style="background: #f0f9ff; padding: 0.9rem; border-radius: 12px; font-size: 0.8rem;">
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ 4 Professional Presets</div>
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Edge Intensity Control</div>
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Color Customization</div>
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Bilateral Smoothing</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)
        
        if st.button("🚀 Enter Classic Studio", type="primary", use_container_width=True, key="classic_btn"):
            go_to_studio('classic')
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f5f3f7 100%); padding: 1.8rem 1.3rem; border-radius: 18px; box-shadow: 0 6px 20px rgba(115, 93, 165, 0.15); border: 2px solid #e6ddf2; backdrop-filter: blur(5px); height: 100%; min-height: 300px;">
            <div style="text-align: center;">
                <div style="font-size: 2.8rem; margin-bottom: 0.6rem;">🤖</div>
                <h3 style="font-family: 'Playfair Display', serif; font-size: 1.5rem; color: #735DA5; margin-bottom: 0.6rem; font-weight: 700;">AI Style Studio</h3>
                <p style="color: #4a3d5a; font-size: 0.9rem; line-height: 1.4; margin-bottom: 0.8rem;">
                    AI-powered artistic transformations
                </p>
            </div>
            <div style="background: #f0f9ff; padding: 0.9rem; border-radius: 12px; font-size: 0.8rem;">
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Cartoon Style (Western)</div>
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Anime Style (Japanese)</div>
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Comic Style (Graphic)</div>
                <div style="color: #4a3d5a; margin: 0.25rem 0;">✨ Intensity Presets</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)
        
        if st.button("✨ Enter AI Studio", type="primary", use_container_width=True, key="ai_btn"):
            go_to_studio('ai')
            st.rerun()
    
    # Quick Features Bar at Bottom - More Compact
    st.markdown("""
    <div style="margin: 1.2rem auto 0.8rem; padding: 1.3rem; background: linear-gradient(135deg, #f5f3f7 0%, #ede9f3 100%); border-radius: 15px; box-shadow: 0 4px 15px rgba(115, 93, 165, 0.1); max-width: 1300px; backdrop-filter: blur(5px); border: 1px solid rgba(211, 197, 229, 0.3);">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; text-align: center;">
            <div>
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">🎯</div>
                <h4 style="color: #735DA5; font-size: 1rem; margin: 0.4rem 0; font-weight: 600;">Smart Segmentation</h4>
                <p style="color: #4a3d5a; font-size: 0.8rem; margin: 0;">Face detection & selective effects</p>
            </div>
            <div>
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">🎬</div>
                <h4 style="color: #735DA5; font-size: 1rem; margin: 0.4rem 0; font-weight: 600;">Living Animations</h4>
                <p style="color: #4a3d5a; font-size: 0.8rem; margin: 0;">Dynamic GIF creations</p>
            </div>
            <div>
                <div style="font-size: 2.2rem; margin-bottom: 0.4rem;">📐</div>
                <h4 style="color: #735DA5; font-size: 1rem; margin: 0.4rem 0; font-weight: 600;">Vector Export</h4>
                <p style="color: #4a3d5a; font-size: 0.8rem; margin: 0;">Scalable SVG graphics</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Minimal footer
    st.markdown("""
    <div style="text-align: center; padding: 0.8rem; color: #9a8daa; font-size: 0.8rem;">
        <strong style="color: #735DA5;">💜 Tooniverse Studio</strong> | Powered by AI & Computer Vision
    </div>
    """, unsafe_allow_html=True)

# ==================== STUDIO PAGE ====================
else:
    # Header with back button
    col_header1, col_header2 = st.columns([6, 1])
    
    with col_header1:
        if st.session_state.studio_type == 'classic':
            st.markdown("""
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #735DA5 0%, #9b87c4 100%); border-radius: 15px; margin-bottom: 1rem;">
                <h1 style="color: white; margin: 0; font-family: 'Playfair Display', serif;">🎨 Classic Studio</h1>
                <p style="color: white; opacity: 0.9; margin: 0.5rem 0 0 0;">Traditional cartoon effects with precision control</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #735DA5 0%, #9b87c4 100%); border-radius: 15px; margin-bottom: 1rem;">
                <h1 style="color: white; margin: 0; font-family: 'Playfair Display', serif;">🤖 AI Style Studio</h1>
                <p style="color: white; opacity: 0.9; margin: 0.5rem 0 0 0;">AI-powered artistic transformations</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col_header2:
        if st.button("🏠 Home", use_container_width=True):
            go_to_landing()
            st.rerun()
    
    # FIXED: Sidebar controls - always visible in studio mode
    with st.sidebar:
        st.header("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image...", 
            type=['png', 'jpg', 'jpeg']
        )
        
        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            st.session_state.uploaded_file_bytes = file_bytes
            image = Image.open(io.BytesIO(file_bytes))
            st.session_state.original_image = image
            st.success("✅ Image uploaded!")
            st.caption(f"📐 Size: {image.size[0]}x{image.size[1]} px")
        
        # STUDIO-SPECIFIC CONTROLS
        if st.session_state.original_image is not None:
            st.divider()
            
            if st.session_state.studio_type == 'classic':
                # CLASSIC STUDIO CONTROLS
                st.header("🎨 Classic Controls")
                
                use_preset = st.checkbox("Use Preset", value=False)
                
                if use_preset:
                    preset_name = st.selectbox("Choose Preset", list(CLASSIC_PRESETS.keys()))
                    preset = CLASSIC_PRESETS[preset_name]
                    st.caption(f"ℹ️ {preset['description']}")
                    edge_threshold = preset['edge_threshold']
                    smoothness = preset['bilateral_d']
                    num_colors = preset['num_colors']
                    st.caption(f"Edge: {edge_threshold} | Smooth: {smoothness} | Colors: {num_colors}")
                else:
                    edge_threshold = st.slider("Edge Intensity", 1, 200, 100)
                    smoothness = st.slider("Smoothness", 3, 15, 9, step=2)
                    num_colors = st.slider("Color Palette", 4, 16, 8)
                
                if st.button("🎨 Apply Classic Effect", type="primary", use_container_width=True):
                    with st.spinner("Creating cartoon..."):
                        try:
                            st.session_state.processed_image = process_cartoonify(
                                st.session_state.uploaded_file_bytes,
                                edge_threshold, smoothness, num_colors
                            )
                            st.success("✨ Effect applied!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            else:
                # AI STUDIO CONTROLS
                st.header("🤖 AI Style Controls")
                
                col1, col2 = st.columns([2, 1])
                with col1:
                    style_type = st.selectbox("Style", ["Cartoon", "Anime", "Comic"])
                with col2:
                    intensity = st.selectbox("Intensity", list(AI_STYLE_PRESETS.keys()))
                
                ai_strength = AI_STYLE_PRESETS[intensity]
                
                style_info = {
                    "Cartoon": "🎨 Bold edges, flat colors",
                    "Anime": "✨ Vibrant, thin lines",
                    "Comic": "💥 High contrast, dramatic"
                }
                st.caption(style_info[style_type])
                
                if st.button("✨ Apply AI Style", type="primary", use_container_width=True):
                    with st.spinner(f"Creating {style_type.lower()} style..."):
                        try:
                            st.session_state.processed_image = process_ai_style(
                                st.session_state.original_image,
                                style_type.lower(), ai_strength
                            )
                            st.success("🎨 AI style applied!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            # FIXED: ADVANCED FEATURES - Work in both studios
            st.divider()
            st.header("✨ Advanced Features")
            
            # Segmentation - Works in both studios
            with st.expander("🎯 Segmentation"):
                seg_mode = st.radio("Segment Mode:", ["Face Focus", "Foreground"])
                
                if st.button("🔍 Create Mask", key="seg_btn", use_container_width=True):
                    with st.spinner("Detecting regions..."):
                        try:
                            mode = "face" if seg_mode == "Face Focus" else "foreground"
                            mask = run_segmentation(st.session_state.original_image, mode=mode)
                            st.session_state.segmentation_mask = mask
                            st.success("✅ Mask created!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                # Selective effects if mask exists
                if st.session_state.get('segmentation_mask') is not None:
                    st.markdown("**Apply Selective Effects:**")
                    selective_mode = st.radio("Effect Mode:", ["Cartoonify Masked", "Blur Background"])
                    
                    if st.button("🎨 Apply Selective Effect", key="selective_btn", use_container_width=True):
                        if st.session_state.processed_image is not None:
                            with st.spinner("Applying selective effect..."):
                                try:
                                    if selective_mode == "Cartoonify Masked":
                                        result = apply_selective_effect(
                                            st.session_state.original_image,
                                            st.session_state.processed_image,
                                            st.session_state.segmentation_mask
                                        )
                                    else:
                                        result = apply_background_blur(
                                            st.session_state.original_image,
                                            st.session_state.segmentation_mask,
                                            blur_strength=21
                                        )
                                    st.session_state.processed_image = result
                                    st.success("✨ Selective effect applied!")
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                        else:
                            st.warning("⚠️ Apply a cartoon effect first!")
            
            # Animation - Works in both studios
            if st.session_state.get('processed_image') is not None:
                with st.expander("🎬 Animation"):
                    anim_type = st.selectbox("Animation Type", ["Bounce", "Shake"])
                    num_frames = st.slider("Frame Count", 15, 30, 20)
                    
                    if st.button("🎬 Create Animation", key="anim_btn", use_container_width=True):
                        with st.spinner("Creating animation..."):
                            try:
                                frames = run_animation(
                                    st.session_state.processed_image,
                                    animation_type=anim_type.lower(),
                                    num_frames=num_frames
                                )
                                
                                gif_buffer = io.BytesIO()
                                frames[0].save(
                                    gif_buffer,
                                    save_all=True,
                                    append_images=frames[1:],
                                    duration=100,
                                    loop=0,
                                    format='GIF',
                                    optimize=False
                                )
                                gif_buffer.seek(0)
                                
                                st.session_state.animated_gif = gif_buffer.getvalue()
                                st.success("🎉 Animation created!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Animation error: {str(e)}")
            
            # Export Options
            if st.session_state.get('processed_image') is not None:
                st.divider()
                st.header("📥 Export")
                
                # PNG Download
                buf = io.BytesIO()
                st.session_state.processed_image.save(buf, format='PNG')
                st.download_button(
                    label="📥 Download PNG",
                    data=buf.getvalue(),
                    file_name="tooniverse_cartoon.png",
                    mime="image/png",
                    use_container_width=True
                )
                
                # SVG Export
                if st.button("🎨 Generate SVG", use_container_width=True):
                    with st.spinner("Vectorizing..."):
                        try:
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.svg') as tmp:
                                svg_path = tmp.name
                            
                            convert_to_svg(st.session_state.processed_image, svg_path, simplify_level=3)
                            
                            with open(svg_path, 'r') as f:
                                svg_data = f.read()
                            
                            st.session_state.svg_data = svg_data
                            os.unlink(svg_path)
                            st.success("✅ SVG created!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
                if st.session_state.get('svg_data'):
                    st.download_button(
                        label="📥 Download SVG",
                        data=st.session_state.svg_data,
                        file_name="tooniverse_vector.svg",
                        mime="image/svg+xml",
                        use_container_width=True
                    )
    
    # Main display area
    if st.session_state.original_image is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📸 Original")
            st.image(st.session_state.original_image, use_container_width=True)
        
        with col2:
            st.subheader("🎨 Result")
            if st.session_state.processed_image is not None:
                st.image(st.session_state.processed_image, use_container_width=True)
            else:
                st.info("👈 Apply effects from sidebar")
        
        # Show segmentation mask if exists
        if st.session_state.get('segmentation_mask') is not None:
            st.divider()
            col_mask = st.columns([1, 2])[0]
            with col_mask:
                st.subheader("🎯 Segmentation Mask")
                st.image(st.session_state.segmentation_mask, width=300)
        
        # Show animation if exists
        if st.session_state.get('animated_gif') is not None:
            st.divider()
            st.subheader("🎬 Your Animated Cartoon")
            
            col_anim1, col_anim2 = st.columns([3, 1])
            
            with col_anim1:
                gif_base64 = base64.b64encode(st.session_state.animated_gif).decode()
                gif_html = f'<img src="data:image/gif;base64,{gif_base64}" style="width:100%; max-width:600px; border-radius:10px;">'
                st.markdown(gif_html, unsafe_allow_html=True)
            
            with col_anim2:
                st.download_button(
                    label="📥 Download GIF",
                    data=st.session_state.animated_gif,
                    file_name="tooniverse_animation.gif",
                    mime="image/gif",
                    use_container_width=True
                )
                size_kb = len(st.session_state.animated_gif) / 1024
                st.caption(f"📦 Size: {size_kb:.1f} KB")
    
        if st.session_state.get('svg_data') is not None:
            st.divider()
            st.subheader("🎨 Vector Preview (SVG)")
            
            col_svg1, col_svg2 = st.columns([3, 1])
            
            with col_svg1:
                # Display SVG using HTML
                st.markdown(
                    f'<div style="background: white; padding: 1rem; border-radius: 15px; box-shadow: 0 4px 20px rgba(115, 93, 165, 0.2);">{st.session_state.svg_data}</div>',
                    unsafe_allow_html=True
                )
                st.caption("✨ Scalable Vector Graphic")
            
            with col_svg2:
                st.download_button(
                    label="📥 Download SVG",
                    data=st.session_state.svg_data,
                    file_name="tooniverse_vector.svg",
                    mime="image/svg+xml",
                    use_container_width=True
                )
                size_kb = len(st.session_state.svg_data.encode()) / 1024
                st.caption(f"📦 Size: {size_kb:.1f} KB")
    
    else:
        st.info("👈 Upload an image from the sidebar to begin")
