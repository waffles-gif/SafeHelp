import re
from urllib.parse import urlparse

# DOMINIOS Y TLDs SOSPECHOSOS
DOMINIOS_SOSPECHOSOS = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 't.co',
    'is.gd', 'buff.ly', 'adf.ly', 'shorturl.at'
]

TLDS_PELIGROSOS = [
    '.ru', '.xyz', '.top', '.work', '.click', '.link',
    '.download', '.stream', '.loan', '.racing', '.win',
    '.bid', '.accountant', '.date', '.faith', '.cricket',
    '.science', '.party', '.review', '.trade', '.webcam'
]

#PATRONES DE DETECCIÓN
PATRONES_FINANCIEROS = [
    r'\b(pago|transferencia|cuenta bancaria|tarjeta|cvv|pin)\b',
    r'\b(débito|crédito|efectivo|depósito|retiro)\b',
    r'\b(número de cuenta|clave secreta|contraseña bancaria)\b',
    r'\$\s*\d+|\d+\s*(dólares|soles|euros|pesos)',
]

PATRONES_URGENCIA = [
    r'\b(urgente|inmediatamente|ahora mismo|rápido)\b',
    r'\b(última oportunidad|por tiempo limitado|hoy solamente)\b',
    r'\b(expira|caduca|vence|termina)\b',
    r'\b(actúa ya|no esperes|aprovecha)\b',
]

PATRONES_PREMIOS = [
    r'\b(ganaste|ganador|premio|sorteo|lotería)\b',
    r'\b(felicidades|felicitaciones|has sido seleccionado)\b',
    r'\b(oferta exclusiva|promoción especial|regalo gratis)\b',
    r'\b(reclama tu|reivindica|cobra)\b',
]

PATRONES_PHISHING = [
    r'\b(verifica tu cuenta|confirma tu identidad)\b',
    r'\b(actualiza tus datos|información desactualizada)\b',
    r'\b(suspenderemos|bloquearemos|cerraremos)\b',
    r'\b(haz clic aquí|sigue este enlace|ingresa aquí)\b',
]

PATRONES_DATOS_PERSONALES = [
    r'\b(dni|documento de identidad|cédula|pasaporte)\b',
    r'\b(fecha de nacimiento|dirección|teléfono)\b',
    r'\b(correo electrónico|email|usuario|contraseña)\b',
]

#FUNCIÓN PRINCIPAL DE ANÁLISIS
def analizar_mensaje(texto):
    """
    Analiza un mensaje y determina su nivel de riesgo
    
    Args:
        texto (str): Mensaje a analizar
        
    Returns:
        tuple: (nivel, razones, consejo)
    """
    texto_lower = texto.lower()
    razones = []
    riesgo = 0
    
    # Análisis de patrones financieros
    for patron in PATRONES_FINANCIEROS:
        if re.search(patron, texto_lower):
            riesgo += 2
            razones.append("💰 Menciona información financiera o bancaria")
            break
    
    # Análisis de urgencia
    for patron in PATRONES_URGENCIA:
        if re.search(patron, texto_lower):
            riesgo += 2
            razones.append("⏰ Usa lenguaje de urgencia o presión temporal")
            break
    
    # Análisis de premios/ofertas
    for patron in PATRONES_PREMIOS:
        if re.search(patron, texto_lower):
            riesgo += 2
            razones.append("🎁 Promete premios, recompensas u ofertas sospechosas")
            break
    
    # Análisis de phishing
    for patron in PATRONES_PHISHING:
        if re.search(patron, texto_lower):
            riesgo += 3
            razones.append("🎣 Usa técnicas típicas de phishing")
            break
    
    # Análisis de solicitud de datos personales
    for patron in PATRONES_DATOS_PERSONALES:
        if re.search(patron, texto_lower):
            riesgo += 2
            razones.append("🔐 Solicita datos personales o confidenciales")
            break
    
    # Análisis de enlaces
    urls = extraer_urls(texto)
    if urls:
        riesgo += 1
        razones.append(f"🔗 Contiene {len(urls)} enlace(s)")
        
        # Verificar si hay enlaces sospechosos
        for url in urls:
            dominio, es_sospechoso, tld_peligroso = analizar_dominio(url)
            if es_sospechoso or tld_peligroso:
                riesgo += 2
                razones.append("⚠️ Incluye enlaces con dominios o extensiones sospechosas")
                break
    
    # Análisis de múltiples enlaces
    if len(urls) > 2:
        riesgo += 1
        razones.append("🔗 Contiene múltiples enlaces (puede ser spam)")
    
    # Análisis de errores ortográficos graves (posible phishing)
    if re.search(r'\b(banca|banco)\b', texto_lower) and re.search(r'[0-9]{10,}', texto):
        riesgo += 2
        razones.append("⚠️ Combina términos bancarios con números largos")
    
    # Determinar nivel y consejo
    if riesgo >= 6:
        nivel = "🔴 Alto riesgo"
        consejo = "⛔ ¡ALERTA! No abras enlaces, no compartas ningún dato personal ni financiero. Es muy probable que sea una estafa."
    elif riesgo >= 3:
        nivel = "🟠 Riesgo medio"
        consejo = "⚠️ Ten precaución. Verifica el remitente antes de responder o hacer clic. No compartas información sensible."
    else:
        nivel = "🟢 Bajo riesgo"
        consejo = "✅ El mensaje parece seguro, pero siempre mantén precaución con enlaces y solicitudes de información."
    
    # Si no se detectaron razones específicas
    if not razones:
        razones.append("✅ No se detectaron señales claras de riesgo")
    
    return nivel, razones, consejo


# EXTRACCIÓN DE URLs
def extraer_urls(texto):
    """
    Extrae todas las URLs de un texto
    
    Args:
        texto (str): Texto a analizar
        
    Returns:
        list: Lista de URLs encontradas
    """
    # Patrón mejorado para detectar URLs
    patron_url = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    patron_url2 = r'www\.(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    patron_url3 = r'\b[a-zA-Z0-9][-a-zA-Z0-9]+\.(com|net|org|edu|gov|mil|co|io|xyz|ru|top|click|link|download)\b'
    
    urls = []
    urls.extend(re.findall(patron_url, texto, re.IGNORECASE))
    urls.extend(re.findall(patron_url2, texto, re.IGNORECASE))
    urls.extend(re.findall(patron_url3, texto, re.IGNORECASE))
    
    return list(set(urls))  # Eliminar duplicados


# ANÁLISIS DE DOMINIO
def analizar_dominio(url):
    """
    Analiza un dominio para determinar si es sospechoso
    
    Args:
        url (str): URL a analizar
        
    Returns:
        tuple: (dominio, es_sospechoso, tld_peligroso)
    """
    try:
        # Agregar esquema si no lo tiene
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urlparse(url)
        dominio = parsed.netloc or parsed.path.split('/')[0]
        
        # Verificar si es un dominio sospechoso conocido
        es_sospechoso = any(dom in dominio.lower() for dom in DOMINIOS_SOSPECHOSOS)
        
        # Verificar TLD peligroso
        tld_peligroso = None
        for tld in TLDS_PELIGROSOS:
            if dominio.lower().endswith(tld):
                tld_peligroso = tld
                break
        
        return dominio, es_sospechoso, tld_peligroso
    
    except Exception as e:
        return None, False, None


# FUNCIÓN DE VALIDACIÓN
def es_mensaje_valido(texto):
    """
    Verifica si un mensaje tiene contenido válido para analizar
    
    Args:
        texto (str): Mensaje a validar
        
    Returns:
        bool: True si es válido, False en caso contrario
    """
    if not texto or texto.strip() == "":
        return False
    
    if len(texto.strip()) < 10:
        return False
    
    return True
