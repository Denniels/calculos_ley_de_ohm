"""
Módulo de cálculos eléctricos básicos
Contiene todas las funciones de validación y cálculo para sistemas DC, AC y trifásicos
"""

import math


def validar_entrada(voltaje, corriente, coseno_fi):
    """Valida los parámetros de entrada y retorna un mensaje de error si hay problemas."""
    if voltaje <= 0:
        return "El voltaje debe ser mayor que 0"
    if corriente <= 0:
        return "La corriente debe ser mayor que 0"
    if not -1 <= coseno_fi <= 1:
        return "El factor de potencia debe estar entre -1 y 1"
    return None


def validar_entrada_dc(voltaje, corriente):
    """Valida los parámetros de entrada para corriente continua."""
    if voltaje <= 0:
        return "El voltaje debe ser mayor que 0"
    if corriente <= 0:
        return "La corriente debe ser mayor que 0"
    return None


def calcular_dc(voltaje, corriente):
    """Calcula los parámetros en corriente continua."""
    resistencia = voltaje / corriente
    potencia = voltaje * corriente
    return resistencia, potencia


def calcular_potencias(voltaje, corriente, coseno_fi):
    """Calcula las diferentes potencias en el circuito."""
    potencia_activa = voltaje * corriente * coseno_fi
    angulo_fi = math.acos(coseno_fi)
    potencia_reactiva = voltaje * corriente * math.sin(angulo_fi)
    potencia_aparente = voltaje * corriente
    return potencia_activa, potencia_reactiva, potencia_aparente


def calcular_impedancias(voltaje, corriente, coseno_fi):
    """Calcula las impedancias del circuito."""
    impedancia = voltaje / corriente
    angulo_fi = math.acos(coseno_fi)
    resistencia = impedancia * coseno_fi
    reactancia = impedancia * math.sin(angulo_fi)
    return impedancia, resistencia, reactancia


def calcular_consumo(potencia_activa, horas):
    """Calcula el consumo en kWh."""
    return potencia_activa * horas / 1000


def calcular_capacitor_dc(voltaje, capacitancia):
    """Calcula la carga y energía almacenada en un capacitor DC."""
    carga = capacitancia * voltaje
    energia = 0.5 * capacitancia * voltaje ** 2
    return carga, energia


def calcular_capacitor_ac(voltaje, frecuencia, capacitancia):
    """Calcula parámetros del capacitor en AC."""
    reactancia_capacitiva = 1 / (2 * math.pi * frecuencia * capacitancia)
    corriente = voltaje / reactancia_capacitiva
    potencia_reactiva = voltaje * corriente
    return reactancia_capacitiva, corriente, potencia_reactiva


def calcular_sistema_trifasico_estrella(vl, il, coseno_fi):
    """Calcula los parámetros del sistema trifásico en conexión estrella."""
    # Voltaje de fase = Voltaje de línea / √3
    vf = vl / math.sqrt(3)
    # Corriente de fase = Corriente de línea
    if_fase = il
    # Potencia activa total
    p_total = math.sqrt(3) * vl * il * coseno_fi
    # Potencia reactiva total
    angulo_fi = math.acos(coseno_fi)
    q_total = math.sqrt(3) * vl * il * math.sin(angulo_fi)
    # Potencia aparente total
    s_total = math.sqrt(3) * vl * il
    # Potencias por fase
    p_fase = p_total / 3
    q_fase = q_total / 3
    s_fase = s_total / 3
    # Impedancia por fase
    z_fase = vf / if_fase
    # Resistencia y reactancia por fase
    r_fase = z_fase * coseno_fi
    x_fase = z_fase * math.sin(angulo_fi)
    
    return {
        'voltaje_fase': vf,
        'voltaje_linea': vl,
        'corriente_fase': if_fase,
        'corriente_linea': il,
        'potencia_activa_total': p_total,
        'potencia_reactiva_total': q_total,
        'potencia_aparente_total': s_total,
        'potencia_activa_fase': p_fase,
        'potencia_reactiva_fase': q_fase,
        'potencia_aparente_fase': s_fase,
        'impedancia_fase': z_fase,
        'resistencia_fase': r_fase,
        'reactancia_fase': x_fase,
        'factor_potencia': coseno_fi,
        'angulo_fi': math.degrees(angulo_fi)
    }


def calcular_sistema_trifasico_delta(vl, il, coseno_fi):
    """Calcula los parámetros del sistema trifásico en conexión delta."""
    # Voltaje de fase = Voltaje de línea
    vf = vl
    # Corriente de fase = Corriente de línea / √3
    if_fase = il / math.sqrt(3)
    # Potencia activa total
    p_total = math.sqrt(3) * vl * il * coseno_fi
    # Potencia reactiva total
    angulo_fi = math.acos(coseno_fi)
    q_total = math.sqrt(3) * vl * il * math.sin(angulo_fi)
    # Potencia aparente total
    s_total = math.sqrt(3) * vl * il
    # Potencias por fase
    p_fase = p_total / 3
    q_fase = q_total / 3
    s_fase = s_total / 3
    # Impedancia por fase
    z_fase = vf / if_fase
    # Resistencia y reactancia por fase
    r_fase = z_fase * coseno_fi
    x_fase = z_fase * math.sin(angulo_fi)
    
    return {
        'voltaje_fase': vf,
        'voltaje_linea': vl,
        'corriente_fase': if_fase,
        'corriente_linea': il,
        'potencia_activa_total': p_total,
        'potencia_reactiva_total': q_total,
        'potencia_aparente_total': s_total,
        'potencia_activa_fase': p_fase,
        'potencia_reactiva_fase': q_fase,
        'potencia_aparente_fase': s_fase,
        'impedancia_fase': z_fase,
        'resistencia_fase': r_fase,
        'reactancia_fase': x_fase,
        'factor_potencia': coseno_fi,
        'angulo_fi': math.degrees(angulo_fi)
    }


def calcular_desequilibrio_corrientes(ir, is_, it):
    """Calcula el desequilibrio de corrientes en sistema trifásico."""
    corrientes = [ir, is_, it]
    corriente_promedio = sum(corrientes) / 3
    
    # Desviaciones respecto al promedio
    desviaciones = [abs(i - corriente_promedio) for i in corrientes]
    max_desviacion = max(desviaciones)
    
    # Porcentaje de desequilibrio
    desequilibrio_porcentaje = (max_desviacion / corriente_promedio) * 100 if corriente_promedio > 0 else 0
    
    return {
        'corriente_promedio': corriente_promedio,
        'desequilibrio_porcentaje': desequilibrio_porcentaje,
        'corrientes': corrientes,
        'desviaciones': desviaciones
    }


def analizar_eficiencia_energetica(potencia_activa, potencia_aparente, factor_potencia):
    """Analiza la eficiencia energética del sistema."""
    # Eficiencia del factor de potencia
    eficiencia_fp = factor_potencia * 100
    
    # Pérdidas reactivas como porcentaje
    perdidas_reactivas = ((potencia_aparente - potencia_activa) / potencia_aparente) * 100 if potencia_aparente > 0 else 0
      # Clasificación de eficiencia
    if eficiencia_fp >= 95:
        categoria_eficiencia = "Excelente"
        color_eficiencia = "🟢"
    elif eficiencia_fp >= 90:
        categoria_eficiencia = "Buena"
        color_eficiencia = "🟡"
    elif eficiencia_fp > 80:
        categoria_eficiencia = "Regular"
        color_eficiencia = "🟠"
    else:
        categoria_eficiencia = "Deficiente"
        color_eficiencia = "🔴"
    
    # Recomendaciones
    recomendaciones = []
    if factor_potencia < 0.9:
        recomendaciones.append("Instalar banco de capacitores para compensación")
    if perdidas_reactivas > 20:
        recomendaciones.append("Revisar cargas inductivas y considerar filtros")
    if factor_potencia < 0.8:
        recomendaciones.append("Evaluar reemplazo de equipos ineficientes")
    
    return {
        'eficiencia_fp': eficiencia_fp,
        'perdidas_reactivas': perdidas_reactivas,
        'categoria': categoria_eficiencia,
        'color': color_eficiencia,
        'recomendaciones': recomendaciones
    }


def analizar_calidad_energia(desequilibrio_porcentaje, factor_potencia, potencia_aparente):
    """Analiza la calidad de la energía del sistema."""
    problemas = []
    puntuacion_calidad = 100
    
    # Análisis de desequilibrio
    if desequilibrio_porcentaje > 5:
        problemas.append(f"🔴 Desequilibrio de fases alto: {desequilibrio_porcentaje:.1f}%")
        puntuacion_calidad -= 20
    elif desequilibrio_porcentaje > 2:
        problemas.append(f"🟡 Desequilibrio de fases moderado: {desequilibrio_porcentaje:.1f}%")
        puntuacion_calidad -= 10
    else:
        problemas.append(f"🟢 Desequilibrio de fases aceptable: {desequilibrio_porcentaje:.1f}%")
    
    # Análisis de factor de potencia
    if factor_potencia < 0.85:
        problemas.append(f"🔴 Factor de potencia bajo: {factor_potencia:.2f}")
        puntuacion_calidad -= 25
    elif factor_potencia < 0.9:
        problemas.append(f"🟡 Factor de potencia mejorable: {factor_potencia:.2f}")
        puntuacion_calidad -= 15
    else:
        problemas.append(f"🟢 Factor de potencia bueno: {factor_potencia:.2f}")
    
    # Costo estimado de pérdidas (estimación simplificada)
    perdidas_estimadas_kw = potencia_aparente * (1 - factor_potencia) / 1000
    costo_anual_estimado = perdidas_estimadas_kw * 8760 * 0.15  # $0.15/kWh promedio
    
    return {
        'puntuacion': max(0, puntuacion_calidad),
        'problemas': problemas,
        'perdidas_kw': perdidas_estimadas_kw,
        'costo_anual': costo_anual_estimado
    }
