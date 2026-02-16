import streamlit as st
import pandas as pd
from detector import analizar_mensaje

# CONFIG
st.set_page_config(page_title="SafeHelp", page_icon="🛡️", layout="centered")

# ESTILOS (AZUL + CENTRADO)
st.markdown("""
<style>
/* Fondo general */
.stApp{
  background-color:#0b1f3a;
  color:white;
}

/* Contenedor centrado y sin espacio "desperdiciado" */
section.main > div.block-container{
  max-width: 820px;
  padding-top: 3.5rem;
  padding-bottom: 3rem;
}

/* Inputs */
textarea, input, select, div[data-baseweb="select"] > div{
  background-color:#1c2e4a !important;
  color:white !important;
  border-radius:12px !important;
}

/* Labels */
label, .stMarkdown, .stTextInput label, .stTextArea label{
  color:white !important;
}

/* Botones */
.stButton > button{
  background-color:#3a7bd5 !important;
  color:white !important;
  border-radius:12px !important;
  padding:0.65rem 1.2rem !important;
  border:0 !important;
  font-weight:600 !important;
}

/* Botones "full width" se ven más pro */
.stButton > button:active{
  transform: scale(0.99);
}

/* Tarjetitas */
.safe-card{
  background: rgba(0,0,0,0.25);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 18px 18px 6px 18px;
  margin-top: 16px;
}
.small-muted{
  opacity: 0.85;
  font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if "modo" not in st.session_state:
  st.session_state.modo = None

if "historial" not in st.session_state:
  st.session_state.historial = pd.DataFrame(columns=["Mensaje", "Nivel", "Consejo"])

if "reporte_log" not in st.session_state:
  # para MVP: guardamos reportes en memoria (no persistente)
  st.session_state.reporte_log = []

# =========================
# PANTALLA INICIAL (ELEGIR VERSION)
# =========================
if st.session_state.modo is None:
  left, mid, right = st.columns([1, 2, 1])

  with mid:
    st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
    st.title("🛡️ SafeHelp - Triple A")
    st.markdown("<div class='small-muted'>Tu asistente inteligente contra estafas digitales</div>", unsafe_allow_html=True)
    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("Elige tu versión")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    if c1.button("Versión gratuita", use_container_width=True):
      st.session_state.modo = "free"
      st.rerun()

    if c2.button("Versión premium", use_container_width=True):
      st.session_state.modo = "premium"
      st.rerun()

  st.stop()

# =========================
# HEADER + VOLVER
# =========================
top_left, top_right = st.columns([5, 1])
with top_left:
  st.title("🛡️ SafeHelp - Triple A")
  st.markdown("<div class='small-muted'>Analiza mensajes sospechosos y recibe recomendaciones claras</div>", unsafe_allow_html=True)
with top_right:
  if st.button("⬅️ Volver", use_container_width=True):
    st.session_state.modo = None
    st.rerun()

st.markdown("---")

# =========================
# INPUT MENSAJE
# =========================
mensaje = st.text_area("✉️ Escribe o pega el mensaje sospechoso:", height=160)

# =========================
# UTIL
# =========================
def guardar_historial(mensaje_txt: str, nivel: str, consejo: str):
  nuevo = pd.DataFrame([[mensaje_txt, nivel, consejo]], columns=["Mensaje", "Nivel", "Consejo"])
  st.session_state.historial = pd.concat([st.session_state.historial, nuevo], ignore_index=True)

# =========================
# FREE
# =========================
if st.session_state.modo == "free":
  st.subheader("Versión gratuita")
  st.markdown("<div class='small-muted'>Incluye: nivel de riesgo + consejo. (Sin historial, sin reporte, sin detalles)</div>", unsafe_allow_html=True)

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
  st.markdown("<div class='small-muted'>Incluye: análisis detallado + razones + historial + reporte (encuesta)</div>", unsafe_allow_html=True)

  # --- Análisis + Reporte en columnas
  colA, colB = st.columns([1, 1])

  # ====== ANALISIS DETALLADO
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

  # ====== REPORTE TIPO ENCUESTA
  with colB:
    st.markdown("<div class='safe-card'>", unsafe_allow_html=True)
    st.markdown("#### 📤 Reportar mensaje (anónimo)")
    st.markdown("<div class='small-muted'>Esto ayuda a mejorar estadísticas y futuras detecciones.</div>", unsafe_allow_html=True)

    with st.form("reporte_form", clear_on_submit=True):
      plataforma = st.selectbox(
        "¿Dónde recibiste el mensaje?",
        ["WhatsApp", "Instagram", "SMS", "Correo", "Facebook", "Otro"]
      )

      remitente = st.text_input(
        "Número / cuenta / usuario (opcional)",
        placeholder="Ej: +51 9XX XXX XXX o @cuenta"
      )

      tipo = st.multiselect(
        "¿Qué intentaba hacer el mensaje?",
        [
          "Pedir dinero/transferencia",
          "Pedir datos personales (DNI, clave, códigos)",
          "Mandar un enlace sospechoso",
          "Ofrecer premio/regalo",
          "Amenaza/extorsión",
          "Otro"
        ]
      )

      clic = st.radio("¿Llegaste a hacer clic en un enlace o descargar algo?", ["No", "Sí"], horizontal=True)

      monto = st.number_input("Si perdiste dinero, ¿cuánto aprox? (opcional)", min_value=0.0, step=1.0)

      detalle = st.text_area("Pega el mensaje aquí (opcional)", height=100)

      enviar = st.form_submit_button("✅ Enviar reporte")

    if enviar:
      st.session_state.reporte_log.append({
        "plataforma": plataforma,
        "remitente": remitente.strip(),
        "tipo": tipo,
        "clic": clic,
        "monto": float(monto),
        "detalle": detalle.strip()
      })
      st.success("¡Gracias! Reporte enviado de forma anónima 💙")

    st.markdown("</div>", unsafe_allow_html=True)

  st.markdown("---")

  # ====== HISTORIAL (PREMIUM)
  st.markdown("### 🧾 Historial de análisis")

  busqueda = st.text_input("🔎 Buscar en historial (premium)")
  if busqueda.strip():
    resultados = st.session_state.historial[
      st.session_state.historial["Mensaje"].str.contains(busqueda, case=False, na=False)
    ]
    st.dataframe(resultados, use_container_width=True)
  else:
    st.dataframe(st.session_state.historial, use_container_width=True)

  # (Opcional) contador de reportes, solo para demo
  st.markdown("<div class='small-muted'>Reportes enviados (demo): "
              f"<b>{len(st.session_state.reporte_log)}</b></div>", unsafe_allow_html=True)
