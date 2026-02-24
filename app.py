# app.py
import streamlit as st
import pandas as pd
from detector import analizar_mensaje
from pathlib import Path
import base64

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="SafeHelp", page_icon="🛡️", layout="centered")

# =========================
# HELPERS
# =========================
def img_to_base64(img_path: str):
    p = Path(img_path)
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode()

LOGO_B64 = img_to_base64("logo.png")

# =========================
# AJUSTES VISUALES
# =========================
TOPBAR_TOP = 55        # 🔥 mueve el header (ANTES 24)
TOPBAR_HEIGHT = 120
SPACER = 200           # 🔥 espacio para que no tape nada

# =========================
# ESTILOS
# =========================
st.markdown(f"""
<style>
.stApp {{
    background-color:#0b1f3a;
    color:white;
}}

section.main > div.block-container {{
    max-width: 900px !important;
    padding-top: 0px !important;
}}

.topbar {{
    position: fixed;
    top: {TOPBAR_TOP}px;
    left: 18px;
    right: 18px;
    height: {TOPBAR_HEIGHT}px;

    background: rgba(0,0,0,0.25);
    border-radius: 18px;
    backdrop-filter: blur(10px);

    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 18px;
    z-index: 9999;
}}

.topbar-title {{
    font-size: 34px;
    font-weight: 900;
}}

.topbar-sub {{
    font-size: 13px;
    opacity: 0.8;
}}

.logo {{
    width:60px;
    border-radius:12px;
}}

.stButton > button {{
    background-color:#3a7bd5 !important;
    color:white !important;
    border-radius:12px !important;
}}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
if LOGO_B64:
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">🛡️ SafeHelp - Triple A</div>
            <div class="topbar-sub">Tu asistente inteligente contra estafas digitales</div>
        </div>
        <img class="logo" src="data:image/png;base64,{LOGO_B64}">
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="topbar">
        <div>
            <div class="topbar-title">🛡️ SafeHelp - Triple A</div>
            <div class="topbar-sub">Tu asistente inteligente contra estafas digitales</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 🔥 ESPACIADOR (CLAVE)
st.markdown(f"<div style='height:{SPACER}px'></div>", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "modo" not in st.session_state:
    st.session_state.modo = None

# =========================
# PANTALLA INICIAL
# =========================
if st.session_state.modo is None:

    st.markdown("""
    <div style="text-align:center;">
    💡 <b>¿Cómo usar SafeHelp?</b><br>
    1) Copia un mensaje sospechoso<br>
    2) Pégalo en la caja<br>
    3) Presiona Analizar<br>
    4) Recibe alerta + consejo
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;'>Elige tu versión</h1>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    if c1.button("Versión gratuita", use_container_width=True):
        st.session_state.modo = "free"
        st.rerun()

    if c2.button("Versión premium", use_container_width=True):
        st.session_state.modo = "premium"
        st.rerun()

    st.markdown("---")

    st.markdown("""
    <div style='text-align:center;'>
    Síguenos en nuestras redes 💙<br><br>
    <a href="https://www.instagram.com/triplea_peru" target="_blank">
    <button style="background:#E1306C;color:white;border:none;padding:10px 18px;border-radius:10px;font-weight:bold;">
    📸 Ir a Instagram
    </button>
    </a>
    </div>
    """, unsafe_allow_html=True)

    st.stop()
