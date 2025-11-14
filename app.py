# app.py
import streamlit as st
import pandas as pd
from detector import analizar_mensaje

st.set_page_config(page_title="SafeHelp", page_icon="🛡️")
st.title("SafeHelp \U0001F6E1️ Triple A")
st.subheader("Tu asistente inteligente contra estafas digitales")

# Visual personalizado (verde, blanco, celeste dinámico)
st.markdown("""
<style>
    .reportview-container {
        background-color: #f0f8ff;
    }
    .sidebar .sidebar-content {
        background-color: #e6f2ff;
    }
</style>
""", unsafe_allow_html=True)

if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Mensaje", "Nivel", "Consejo"])

if "estadisticas" not in st.session_state:
    st.session_state.estadisticas = {"alto": 0, "medio": 0, "bajo": 0}

mensaje = st.text_area("✉️ Escribe o pega el mensaje sospechoso:")

col1, col2 = st.columns(2)

if col1.button("🔍 Analizar mensaje"):
    if mensaje.strip() == "":
        st.warning("Por favor, ingresa un mensaje para analizar.")
    else:
        nivel, razones, consejo = analizar_mensaje(mensaje)
        st.markdown(f"Resultado: {nivel}")
        st.write("**Señales detectadas:**")
        for r in razones:
            st.write(f"- {r}")
        st.info(f"**Consejo:** {consejo}")

        nuevo = pd.DataFrame([[mensaje, nivel, consejo]], columns=["Mensaje", "Nivel", "Consejo"])
        st.session_state.historial = pd.concat([st.session_state.historial, nuevo], ignore_index=True)

        if "Alto" in nivel:
            st.session_state.estadisticas["alto"] += 1
        elif "medio" in nivel:
            st.session_state.estadisticas["medio"] += 1
        else:
            st.session_state.estadisticas["bajo"] += 1

if col2.button("📤 Reportar mensaje anónimo"):
    st.success("Gracias por tu reporte. Será considerado en estadísticas globales.")

st.markdown("---")
st.markdown("### 📊 Estadísticas acumuladas")
st.write("**Mensajes analizados:**", sum(st.session_state.estadisticas.values()))
st.write("- 🔴 Alto riesgo:", st.session_state.estadisticas["alto"])
st.write("- 🟠 Riesgo medio:", st.session_state.estadisticas["medio"])
st.write("- 🟢 Bajo riesgo:", st.session_state.estadisticas["bajo"])

st.markdown("---")
st.markdown("### 🧾 Historial de análisis")

# Búsqueda de mensajes
busqueda = st.text_input("🔎 Buscar mensaje en historial")

if busqueda:
    resultados = st.session_state.historial[st.session_state.historial["Mensaje"].str.contains(busqueda, case=False)]
    st.dataframe(resultados)
else:
    st.dataframe(st.session_state.historial)
