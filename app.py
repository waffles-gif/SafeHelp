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
def img_to_base64(img_path: str) -> str | None:
    p = Path(img_path)
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode("utf-8")

LOGO_B64 = img_to_base64("logo.png")  # ✅ tu logo debe llamarse EXACTO: logo.png (misma carpeta)

# =========================
# UI SETTINGS
# =========================
TOPBAR_TOP_PX = 24
TOPBAR_HEIGHT_PX = 130

# 🔥 FIX INFALIBLE: el contenido se empuja con un "spacer" real (Streamlit no lo puede ignorar)
SPACER_HEIGHT_PX = 190  # si aún tapa algo, sube a 210

# =========================
# ESTILOS
# =========================
st.markdown(
    f"""
<style>
/* Fondo general */
.stApp{{
  background-color:#0b1f3a;
  color:white;
}}

/* Contenedor principal: lo dejamos sin padding-top porque lo controla el SPACER */
section.main > div.block-container{{
  max-width: 900px !important;
  padding-top: 0px !important;     /* ✅ important: Streamlit a veces pisa esto */
  padding-bottom: 3rem !important;
}}

/* Inputs */
textarea, input, select, div[data-baseweb="select"] > div{{
  background-color:#1c2e4a !important;
  color:white !important;
  border-radius:12px !important;
}}

/* Labels */
label, .stMarkdown, .stTextInput label, .stTextArea label{{
  color:white !important;
}}

/* Botones */
.stButton > button{{
  background-color:#3a7bd5 !important;
  color:white !important;
  border-radius:12px !important;
  padding:0.65rem 1.2rem !important;
  border:0 !important;
  font-weight:700 !important;
}}
.stButton > button:active{{
  transform: scale(0.99);
}}

/* Tarjetitas */
.safe-card{{
  background: rgba(0,0,0,0.25);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 18px 18px 6px 18px;
  margin-top: 16px;
}}
.small-muted{{
  opacity: 0.85;
  font-size: 0.95rem;
}}

/* HEADER FIJO */
.topbar{{
  position: fixed;
  top: {TOPBAR_TOP_PX}px;
  left: 18px;
  right: 18px;
  height: {TOPBAR_HEIGHT_PX}px;

  background: rgba(0,0,0,0.22);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 18px;

  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
}}

.topbar-title{{
  font-size: 34px;
  font-weight: 900;
  letter-spacing: 0.2px;
  margin: 0;
  line-height: 1.05;
}}

.topbar-sub{{
  font-size: 13px;
  opacity: 0.85;
  margin-top: 6px;
}}

.logo-img{{
  width: 62px;
  height: 62px;
  object-fit: contain;
  border-radius: 14px;
  background: rgba(255,255,255,0.06);
  padding: 8px;
  border: 1px solid rgba(255,255,255,0.10);
}}
</style>
""",
    unsafe_allow_html=True,
)

# =========================
# HEADER (SIEMPRE)
# =========================
if LOGO_B64:
    st.markdown(
        f"""
<div class="topbar">
  <div>
    <div class="topbar-title">🛡️ SafeHelp - Triple A</div>
    <div class="topbar-sub">Tu asistente inteligente contra estafas digitales</div>
  </div>
  <img class="logo-img" src="data:image/png;base64,{LOGO_B64}" alt="Triple A logo" />
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
<div class="topbar">
  <div>
    <div class="topbar-title">🛡️ SafeHelp - Triple A</div>
    <div class="topbar-sub">Tu asistente inteligente contra estafas digitales</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# ✅ SPACER: esto es lo que evita que se TAPEN instrucciones / títulos / IG
st.markdown(f"<div style='height:{SPACER_HEIGHT_PX}px;'></div>", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "modo" not in st.session_state:
    st.session_state.modo = None

if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Mensaje", "Nivel", "Consejo"])

if "reporte_log" not in st.session_state:
    st.session_state.reporte_log = []

def guardar_historial(mensaje_txt: str, nivel: str, consejo: str):
    nuevo = pd.DataFrame([[mensaje_txt, nivel, consejo]], columns=["Mensaje", "Nivel", "Consejo"])
    st.session_state.historial = pd.concat([st.session_state.historial, nuevo], ignore_index=True)

# =========================
# PANTALLA INICIAL (ELEGIR VERSION)
# =========================
if st.session_state.modo is None:
    st.markdown(
        """
<div style="text-align:center; margin-top: 0px; margin-bottom: 26px;">
  <div style="font-size:16px; opacity:0.92;">
    💡 <b>¿Cómo usar SafeHelp?</b><br/>
    1) Copia un mensaje sospechoso<br/>
    2) Pégalo en la caja<br/>
    3) Presiona <b>Analizar</b><br/>
    4) Recibe alerta + consejo
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div style="text-align:center; margin-top: 0px;">
  <h2 style="font-size:46px; margin-bottom:18px;">Elige tu versión</h2>
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    if c1.button("Versión gratuita", use_container_width=True):
        st.session_state.modo = "free"
        st.rerun()

    if c2.button("Versión premium", use_container_width=True):
        st.session_state.modo = "premium"
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
<div style='text-align:center; margin-top:16px;'>
  <p style='opacity:0.85; margin-bottom:10px;'>Síguenos en nuestras redes 💙</p>
  <a href="https://www.instagram.com/triplea_peru" target="_blank" style="text-decoration:none;">
    <button style="
        background-color:#E1306C;
        color:white;
        border:none;
        padding:10px 18px;
        border-radius:10px;
        font-weight:900;
        cursor:pointer;">
        📸 Ir a Instagram
    </button>
  </a>
</div>
""",
        unsafe_allow_html=True,
    )

    st.stop()

# =========================
# VOLVER
# =========================
_, col_back = st.columns([5, 1])
with col_back:
    if st.button("⬅️ Volver", use_container_width=True):
        st.session_state.modo = None
        st.rerun()

st.markdown("---")

# =========================
# INPUT MENSAJE
# =========================
mensaje = st.text_area("✉️ Escribe o pega el mensaje sospechoso:", height=160)

# =========================
# FREE
# =========================
if st.session_state.modo == "free":
    st.subheader("Versión gratuita")
    st.markdown(
        "<div class='small-muted'>Incluye: nivel de riesgo + consejo. (Sin historial, sin reporte, sin detalles)</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='safe-card'>", unsafe_allow_html=True)
    if st.button("🔍 Analizar mensaje", use_container_width=True):
        if mensaje.strip() == "":
            st.warning("Por favor, pega un mensaje para analizar.")
        else:
            nivel, _, consejo = analizar_mensaje(mensaje)
            st.success(f"Nivel detectado: {nivel}")
            st.info(consejo)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PREMIUM
# =========================
elif st.session_state.modo == "premium":
    st.subheader("Versión premium")
    st.markdown(
        "<div class='small-muted'>Incluye: análisis detallado + razones + historial + reporte (encuesta)</div>",
        unsafe_allow_html=True,
    )

    colA, colB = st.columns([1, 1])

    with colA:
        st.markdown("<div class='safe-card'>", unsafe_allow_html=True)
        st.markdown("#### 🔍 Análisis detallado")

        if st.button("Analizar mensaje", use_container_width=True):
            if mensaje.strip() == "":
                st.warning("Por favor, pega un mensaje para analizar.")
            else:
                nivel, razones, consejo = analizar_mensaje(mensaje)
                st.success(f"Nivel: {nivel}")

                st.write("**Señales detectadas:**")
                if razones:
                    for r in razones:
                        st.write(f"- {r}")
                else:
                    st.write("- No se detectaron señales específicas.")

                st.info(f"**Consejo:** {consejo}")
                guardar_historial(mensaje, nivel, consejo)

        st.markdown("</div>", unsafe_allow_html=True)

    with colB:
        st.markdown("<div class='safe-card'>", unsafe_allow_html=True)
        st.markdown("#### 📤 Reportar mensaje (anónimo)")
        st.markdown(
            "<div class='small-muted'>Esto ayuda a mejorar estadísticas y futuras detecciones.</div>",
            unsafe_allow_html=True,
        )

        with st.form("reporte_form", clear_on_submit=True):
            plataforma = st.selectbox(
                "¿Dónde recibiste el mensaje?",
                ["WhatsApp", "Instagram", "SMS", "Correo", "Facebook", "Otro"],
            )

            remitente = st.text_input(
                "Número / cuenta / usuario (opcional)",
                placeholder="Ej: +51 9XX XXX XXX o @cuenta",
            )

            tipo = st.multiselect(
                "¿Qué intentaba hacer el mensaje?",
                [
                    "Pedir dinero/transferencia",
                    "Pedir datos personales (DNI, clave, códigos)",
                    "Mandar un enlace sospechoso",
                    "Ofrecer premio/regalo",
                    "Amenaza/extorsión",
                    "Otro",
                ],
            )

            clic = st.radio(
                "¿Llegaste a hacer clic en un enlace o descargar algo?",
                ["No", "Sí"],
                horizontal=True,
            )

            monto = st.number_input(
                "Si perdiste dinero, ¿cuánto aprox? (opcional)",
                min_value=0.0,
                step=1.0,
            )

            detalle = st.text_area("Pega el mensaje aquí (opcional)", height=100)

            enviar = st.form_submit_button("✅ Enviar reporte")

        if enviar:
            st.session_state.reporte_log.append(
                {
                    "plataforma": plataforma,
                    "remitente": remitente.strip(),
                    "tipo": tipo,
                    "clic": clic,
                    "monto": float(monto),
                    "detalle": detalle.strip(),
                }
            )
            st.success("¡Gracias! Reporte enviado de forma anónima 💙")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧾 Historial de análisis")

    busqueda = st.text_input("🔎 Buscar en historial (premium)")
    if busqueda.strip():
        resultados = st.session_state.historial[
            st.session_state.historial["Mensaje"].str.contains(busqueda, case=False, na=False)
        ]
        st.dataframe(resultados, use_container_width=True)
    else:
        st.dataframe(st.session_state.historial, use_container_width=True)

    st.markdown(
        "<div class='small-muted'>Reportes enviados (demo): "
        f"<b>{len(st.session_state.reporte_log)}</b></div>",
        unsafe_allow_html=True,
    )

# =========================
# FOOTER IG
# =========================
st.markdown("---")
st.markdown(
    """
<div style='text-align:center; margin-top:16px;'>
  <p style='opacity:0.85; margin-bottom:10px;'>Síguenos en nuestras redes 💙</p>
  <a href="https://www.instagram.com/triplea_peru" target="_blank" style="text-decoration:none;">
    <button style="
        background-color:#E1306C;
        color:white;
        border:none;
        padding:10px 18px;
        border-radius:10px;
        font-weight:900;
        cursor:pointer;">
        📸 Ir a Instagram
    </button>
  </a>
</div>
""",
    unsafe_allow_html=True,
)
