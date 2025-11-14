import re

def analizar_mensaje(texto):
    texto = texto.lower()
    texto = texto.strip()
    razones = []
    riesgo = 0

    # --- Patrón 1: Dinero y pagos sospechosos
    if re.search(r"(pago|transferencia|cuenta bancaria|saldo|dep[oó]sito|factura|tarjeta de cr[eé]dito)", texto):
        riesgo += 2
        razones.append("Menciona temas financieros o pagos sospechosos.")

    # --- Patrón 2: Urgencia o presión
    if re.search(r"(urgente|inmediatamente|última oportunidad|responde ya|actúa ahora|en menos de 24 horas)", texto):
        riesgo += 2
        razones.append("Usa lenguaje de urgencia o presión psicológica.")

    # --- Patrón 3: Enlaces peligrosos (dominios raros)
    if re.search(r"(http|www|\.[a-z]{2,3}/)", texto):
        riesgo += 2
        razones.append("Contiene enlaces potencialmente peligrosos.")

    # --- Patrón 4: Premios, sorteos y regalos
    if re.search(r"(ganaste|premio|sorteo|felicidades|has sido elegido|bono especial)", texto):
        riesgo += 2
        razones.append("Promete recompensas que podrían ser falsas.")

    # --- Patrón 5: Solicitud de información personal
    if re.search(r"(verifica tu identidad|dni|clave|contrase[nñ]a|datos personales)", texto):
        riesgo += 3
        razones.append("Solicita datos sensibles del usuario.")

    # --- Patrón 6: Nombre de bancos u organizaciones falsas comunes
    if re.search(r"(bbva|bcp|scotiabank|sunat|reniec|apple id|paypal|amazon)", texto):
        riesgo += 1
        razones.append("Menciona instituciones que suelen ser usadas en fraudes.")

    # --- Clasificación final
    if riesgo >= 6:
        nivel = "🔴 Alto riesgo"
        consejo = "No abras enlaces ni compartas datos personales. Podría tratarse de una estafa."
    elif riesgo >= 3:
        nivel = "🟠 Riesgo medio"
        consejo = "Ten precaución. Verifica si es un remitente legítimo antes de interactuar."
    else:
        nivel = "🟢 Bajo riesgo"
        consejo = "No se detectaron señales de estafa. Aun así, mantente alerta."

    return nivel, razones, consejo
