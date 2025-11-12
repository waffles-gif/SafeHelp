#detector.py
import re

def analizar_mensaje(texto):
    texto = texto.lower()
    razones = []
    riesgo = 0

    if re.search(r"pago|transferencia|cuenta bancaria", texto):
        riesgo += 2
        razones.append("Menciona dinero o pagos.")
    if re.search(r"urgente|inmediatamente|última oportunidad", texto):
        riesgo += 2
        razones.append("Usa lenguaje de urgencia.")
    if re.search(r"http|www|link|enlace", texto):
        riesgo += 1
        razones.append("Incluye un enlace sospechoso.")
    if re.search(r"premio|ganaste|oferta", texto):
        riesgo += 2
        razones.append("Promete premios o recompensas.")

    if riesgo >= 5:
        nivel = "🔴 Alto riesgo"
        consejo = "No abras enlaces ni compartas datos personales."
    elif riesgo >= 3:
        nivel = "🟠 Riesgo medio"
        consejo = "Verifica el remitente antes de responder."
    else:
        nivel = "🟢 Bajo riesgo"
        consejo = "El mensaje parece seguro, pero mantén precaución."

    return nivel, razones, consejo