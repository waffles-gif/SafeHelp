import streamlit as st
import pandas as pd
from detector import analizar_mensaje

st.set_page_config(page_title="SafeHelp", page_icon="🛡️")
st.title("SafeHelp")
st.subheader("Tu asistente inteligente contra estafas digitales")

if "historial" not in st.session_state:
    st.session_state.historial = pd.DataFrame(columns=["Mensaje", "Nivel", "Consejo"])

mensaje = st.text_area("✉️ Escribe o pega el mensaje sospechoso:")

if st.button("Analizar mensaje"):
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

st.markdown("Historial de análisis")
st.dataframe(st.session_state.historial)