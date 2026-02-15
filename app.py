import streamlit as st
import pandas as pd
from detector import analizar_mensaje

st.set_page_config(page_title="SafeHelp", page_icon="🛡️")

# ESTILO AZUL
st.markdown("""
<style>
.stApp {
    background-color: #0b1f3a;
    color: white;
}
textarea, input {
    background-color: #1c2e4a !important;
    color: white !important;
}
button {
    background-color: #3a7bd5 !important;
    color: white !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# Estado
if "modo" not in st.session_state:
    st.session_state.modo = None

# PANTALLA INICIAL
if st.session_state.modo is None:
    st.title("🛡️ SafeHelp Triple A")
    st.subheader("Elige tu versión")

    col1, col2 = st.columns(2)

    if col1.button("🟢 Versión gratuita"):
        st.session_state.modo = "free"

    if col2.button("💎 Versión premium"):
        st.session_state.modo = "premium"

    st.stop()

#  BOTÓN REGRESAR
if st.button("⬅️ Volver"):
    st.session_state.modo = None
    st.rerun()

# INPUT
st.title("🛡️ SafeHelp")
mensaje = st.text_area("✉️ Escribe o pega el mensaje sospechoso:")

# INICIALIZAR DATOS
if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Mensaje", "Nivel", "Consejo"])

# =========================
#  VERSIÓN GRATUITA

if st.session_state.modo == "free":
    st.subheader("Versión gratuita")

    if st.button("🔍 Analizar mensaje"):
        if mensaje.strip() == "":
            st.warning("Escribe un mensaje")
        else:
            nivel, _, consejo = analizar_mensaje(mensaje)

            # SOLO NIVEL + CONSEJO (NO razones)
            st.success(f"Nivel detectado: {nivel}")
            st.info(consejo)

# =========================
#  VERSIÓN PREMIUM

elif st.session_state.modo == "premium":
    st.subheader("Versión premium")

    col1, col2 = st.columns(2)

    if col1.button("🔍 Analizar mensaje"):
        if mensaje.strip() == "":
            st.warning("Escribe un mensaje")
        else:
            nivel, razones, consejo = analizar_mensaje(mensaje)

            st.success(f"Nivel: {nivel}")

            st.write("🔎 Señales detectadas:")
            for r in razones:
                st.write(f"- {r}")

            st.info(f"Consejo: {consejo}")

            nuevo = pd.DataFrame([[mensaje, nivel, consejo]],
                                 columns=["Mensaje", "Nivel", "Consejo"])

            st.session_state.historial = pd.concat(
                [st.session_state.historial, nuevo],
                ignore_index=True
            )

    if col2.button("📤 Reportar mensaje"):
        st.success("Reporte enviado correctamente")

    # 📊 HISTORIAL
    st.markdown("### 📊 Historial")
    st.dataframe(st.session_state.historial)
