"""
Calculadora Avanzada de Ley de Ohm - Aplicación Principal
Versión 2.0 - Modular y Optimizada

Aplicación web para cálculos completos de sistemas eléctricos:
- Corriente Continua (DC) y Alterna (AC)
- Sistemas Trifásicos (Estrella y Delta)
- Análisis de Desequilibrio, Eficiencia y Calidad Energética
- Capacitores DC y AC
"""

import streamlit as st
import sys
import os

# Agregar src al path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from calculos import (
    validar_entrada, validar_entrada_dc, calcular_dc, calcular_potencias,
    calcular_impedancias, calcular_consumo, calcular_capacitor_dc,
    calcular_capacitor_ac, calcular_sistema_trifasico_estrella,
    calcular_sistema_trifasico_delta, calcular_desequilibrio_corrientes,
    analizar_eficiencia_energetica, analizar_calidad_energia
)

from graficos import (
    crear_triangulo_potencias, crear_grafico_circular, crear_grafico_circuito_dc,
    crear_grafico_capacitor, crear_diagrama_fasorial_trifasico,
    crear_grafico_desequilibrio
)

from datos import (
    guardar_historico, mostrar_historico, mostrar_resultados
)


def configurar_pagina():
    """Configura la página de Streamlit."""
    st.set_page_config(
        page_title="Calculadora Ley de Ohm v2.0",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title('⚡ Calculadora Avanzada de Ley de Ohm v2.0')
    st.markdown("---")


def mostrar_info_version():
    """Muestra información sobre la versión actual."""
    with st.expander("ℹ️ Información de la Aplicación"):
        st.markdown("""
        **Versión:** 2.0 - Modular y Optimizada
        
        **Características:**
        - ✅ Cálculos DC/AC completos
        - ✅ Sistemas trifásicos (Estrella/Delta)
        - ✅ Análisis de desequilibrio de fases
        - ✅ Evaluación de eficiencia energética
        - ✅ Análisis de calidad de energía
        - ✅ Capacitores DC y AC
        - ✅ Visualizaciones interactivas
        - ✅ Histórico de cálculos
        - ✅ Arquitectura modular
        
        **Módulos:**
        - `calculos.py`: Funciones de cálculo
        - `graficos.py`: Visualizaciones
        - `datos.py`: Gestión de datos
        """)


def procesar_circuito_trifasico():
    """Procesa los cálculos para sistemas trifásicos."""
    st.header("🔺 Sistema Trifásico")
    
    conexion = st.radio(
        "Tipo de conexión",
        ["Estrella (Y)", "Delta (Δ)"],
        help="Selecciona el tipo de conexión del sistema trifásico"
    )
    
    # Parámetros básicos
    col1, col2, col3 = st.columns(3)
    with col1:
        voltaje_linea = st.number_input(
            'Voltaje de línea (VL)', 
            min_value=0.0, 
            value=380.0,
            help="Voltaje entre líneas del sistema trifásico"
        )
    with col2:
        corriente_linea = st.number_input(
            'Corriente de línea (IL)', 
            min_value=0.0,
            value=10.0,
            help="Corriente de línea del sistema trifásico"
        )
    with col3:
        factor_potencia = st.number_input(
            'Factor de potencia (cos φ)',
            min_value=-1.0, 
            max_value=1.0, 
            value=0.85,
            help="Factor de potencia del sistema trifásico"
        )
    
    # Corrientes individuales por fase
    st.subheader("📊 Corrientes Individuales por Fase")
    col1, col2, col3 = st.columns(3)
    with col1:
        corriente_r = st.number_input(
            'Corriente Fase R (IR)', 
            min_value=0.0,
            value=corriente_linea,
            help="Corriente en la fase R"
        )
    with col2:
        corriente_s = st.number_input(
            'Corriente Fase S (IS)', 
            min_value=0.0,
            value=corriente_linea,
            help="Corriente en la fase S"
        )
    with col3:
        corriente_t = st.number_input(
            'Corriente Fase T (IT)', 
            min_value=0.0,
            value=corriente_linea,
            help="Corriente en la fase T"
        )
    
    # Validaciones
    if voltaje_linea <= 0 or corriente_linea <= 0:
        st.error("El voltaje y la corriente deben ser mayores que 0")
        return
    
    if corriente_r <= 0 or corriente_s <= 0 or corriente_t <= 0:
        st.error("Las corrientes de fase deben ser mayores que 0")
        return
    
    # Cálculos
    if conexion == "Estrella (Y)":
        resultados = calcular_sistema_trifasico_estrella(voltaje_linea, corriente_linea, factor_potencia)
    else:
        resultados = calcular_sistema_trifasico_delta(voltaje_linea, corriente_linea, factor_potencia)
    
    # Análisis avanzados
    desequilibrio = calcular_desequilibrio_corrientes(corriente_r, corriente_s, corriente_t)
    eficiencia = analizar_eficiencia_energetica(
        resultados['potencia_activa_total'],
        resultados['potencia_aparente_total'],
        factor_potencia
    )
    calidad = analizar_calidad_energia(
        desequilibrio['desequilibrio_porcentaje'],
        factor_potencia,
        resultados['potencia_aparente_total']
    )
    
    # Mostrar resultados
    mostrar_resultados_trifasico(resultados, desequilibrio, eficiencia, calidad, 
                                corriente_r, corriente_s, corriente_t, conexion, 
                                voltaje_linea, corriente_linea, factor_potencia)


def mostrar_resultados_trifasico(resultados, desequilibrio, eficiencia, calidad, 
                                corriente_r, corriente_s, corriente_t, conexion,
                                voltaje_linea, corriente_linea, factor_potencia):
    """Muestra los resultados del análisis trifásico."""
    
    # Resultados principales
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚡ Parámetros por Fase")
        mostrar_resultados([
            ("Voltaje de fase", resultados['voltaje_fase'], "V"),
            ("Corriente de fase", resultados['corriente_fase'], "A"),
            ("Potencia activa por fase", resultados['potencia_activa_fase'], "W"),
            ("Potencia reactiva por fase", resultados['potencia_reactiva_fase'], "VAR"),
            ("Potencia aparente por fase", resultados['potencia_aparente_fase'], "VA"),
            ("Impedancia por fase", resultados['impedancia_fase'], "Ω"),
            ("Resistencia por fase", resultados['resistencia_fase'], "Ω"),
            ("Reactancia por fase", resultados['reactancia_fase'], "Ω")
        ])
    
    with col2:
        st.subheader("⚡ Parámetros Totales del Sistema")
        mostrar_resultados([
            ("Voltaje de línea", resultados['voltaje_linea'], "V"),
            ("Corriente de línea", resultados['corriente_linea'], "A"),
            ("Potencia activa total", resultados['potencia_activa_total'], "W"),
            ("Potencia reactiva total", resultados['potencia_reactiva_total'], "VAR"),
            ("Potencia aparente total", resultados['potencia_aparente_total'], "VA"),
            ("Factor de potencia", resultados['factor_potencia'], ""),
            ("Ángulo φ", resultados['angulo_fi'], "°")
        ])
    
    # Análisis de Desequilibrio
    st.subheader("📊 Análisis de Desequilibrio de Fases")
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Resultados del análisis:**")
        st.write(f"• Corriente promedio: {desequilibrio['corriente_promedio']:.2f} A")
        st.write(f"• Desequilibrio: {desequilibrio['desequilibrio_porcentaje']:.2f}%")
        
        if desequilibrio['desequilibrio_porcentaje'] <= 2:
            st.success("🟢 Desequilibrio aceptable (≤ 2%)")
        elif desequilibrio['desequilibrio_porcentaje'] <= 5:
            st.warning("🟡 Desequilibrio moderado (2-5%)")
        else:
            st.error("🔴 Desequilibrio alto (> 5%)")
    
    with col2:
        fig_desequilibrio = crear_grafico_desequilibrio(
            [corriente_r, corriente_s, corriente_t], 
            ['R', 'S', 'T']
        )
        st.plotly_chart(fig_desequilibrio, use_container_width=True)
    
    # Análisis de Eficiencia
    st.subheader("⚡ Análisis de Eficiencia Energética")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{eficiencia['color']} Categoría: {eficiencia['categoria']}**")
        st.write(f"• Eficiencia del factor de potencia: {eficiencia['eficiencia_fp']:.1f}%")
        st.write(f"• Pérdidas reactivas: {eficiencia['perdidas_reactivas']:.1f}%")
        
        if eficiencia['recomendaciones']:
            st.write("**Recomendaciones:**")
            for rec in eficiencia['recomendaciones']:
                st.write(f"• {rec}")
    
    with col2:
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric(
                "Factor de Potencia",
                f"{factor_potencia:.3f}",
                f"{eficiencia['eficiencia_fp']:.1f}%"
            )
        with col_b:
            st.metric(
                "Pérdidas Reactivas",
                f"{eficiencia['perdidas_reactivas']:.1f}%",
                delta=f"vs ideal: {eficiencia['perdidas_reactivas']:.1f}%",
                delta_color="inverse"
            )
    
    # Análisis de Calidad de Energía
    st.subheader("🔍 Análisis de Calidad de Energía")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Puntuación de calidad: {calidad['puntuacion']:.0f}/100**")
        st.write("**Estado del sistema:**")
        for problema in calidad['problemas']:
            st.write(f"{problema}")
    
    with col2:
        st.write("**Análisis económico:**")
        st.write(f"• Pérdidas estimadas: {calidad['perdidas_kw']:.2f} kW")
        st.write(f"• Costo anual estimado: ${calidad['costo_anual']:.2f}")
        
        if calidad['puntuacion'] >= 80:
            st.success(f"🟢 Calidad buena ({calidad['puntuacion']:.0f}/100)")
        elif calidad['puntuacion'] >= 60:
            st.warning(f"🟡 Calidad regular ({calidad['puntuacion']:.0f}/100)")
        else:
            st.error(f"🔴 Calidad deficiente ({calidad['puntuacion']:.0f}/100)")
    
    # Diagrama fasorial
    st.subheader("📐 Diagrama Fasorial")
    voltajes = [resultados['voltaje_fase']] * 3
    angulos = [0, -120, 120]
    st.plotly_chart(crear_diagrama_fasorial_trifasico(voltajes, angulos), use_container_width=True)
    
    # Guardar en histórico
    datos = {
        'tipo_circuito': 'Trifásico',
        'conexion': conexion,
        'voltaje_linea': voltaje_linea,
        'corriente_linea': corriente_linea,
        'factor_potencia': factor_potencia,
        'potencia_activa_total': resultados['potencia_activa_total'],
        'potencia_reactiva_total': resultados['potencia_reactiva_total'],
        'potencia_aparente_total': resultados['potencia_aparente_total'],
        'corriente_r': corriente_r,
        'corriente_s': corriente_s,
        'corriente_t': corriente_t,
        'desequilibrio_porcentaje': desequilibrio['desequilibrio_porcentaje'],
        'eficiencia_fp': eficiencia['eficiencia_fp'],
        'calidad_puntuacion': calidad['puntuacion']
    }
    total_registros = guardar_historico(datos)
    st.success(f"✅ Cálculo guardado en el histórico (Total: {total_registros} registros)")


def procesar_circuito_resistivo():
    """Procesa los cálculos para circuitos resistivos."""
    st.header("⚡ Circuito Resistivo")
    
    tipo_corriente = st.radio(
        "Selecciona el tipo de corriente",
        ["Corriente Continua (DC)", "Corriente Alterna (AC)"],
        help="Elige el tipo de corriente para realizar los cálculos correspondientes"
    )
    
    # Parámetros de entrada
    with st.sidebar:
        st.header("📝 Parámetros de entrada")
        voltaje = st.number_input('Voltaje (V)', min_value=0.0, help="Introduce el voltaje en voltios")
        corriente = st.number_input('Corriente (A)', min_value=0.0, help="Introduce la corriente en amperios")
        
        if tipo_corriente == "Corriente Alterna (AC)":
            coseno_fi = st.number_input('Factor de potencia (cos φ)', min_value=-1.0, max_value=1.0, 
                                      help="Introduce el factor de potencia (entre -1 y 1)")
        
        horas = st.number_input('Horas de funcionamiento', min_value=0.0, 
                               help="Introduce las horas de funcionamiento para calcular el consumo")
    
    if tipo_corriente == "Corriente Continua (DC)":
        procesar_dc(voltaje, corriente, horas)
    else:
        procesar_ac(voltaje, corriente, coseno_fi, horas)


def procesar_dc(voltaje, corriente, horas):
    """Procesa cálculos DC."""
    error = validar_entrada_dc(voltaje, corriente)
    if error:
        st.error(error)
        return
    
    if voltaje > 0 and corriente > 0:
        resistencia, potencia = calcular_dc(voltaje, corriente)
        consumo = calcular_consumo(potencia, horas)
        
        st.subheader("📊 Resultados - Corriente Continua")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parámetros del circuito")
            mostrar_resultados([
                ("Voltaje", voltaje, "V"),
                ("Corriente", corriente, "A"),
                ("Resistencia", resistencia, "Ω"),
                ("Potencia", potencia, "W"),
                ("Consumo", consumo, "kWh")
            ])
        
        with col2:
            st.plotly_chart(crear_grafico_circuito_dc(voltaje, corriente, resistencia), use_container_width=True)
        
        # Guardar histórico
        datos = {
            'tipo_circuito': 'Resistivo',
            'tipo_corriente': 'DC',
            'voltaje': voltaje,
            'corriente': corriente,
            'resistencia': resistencia,
            'potencia': potencia
        }
        total_registros = guardar_historico(datos)
        st.success(f"✅ Cálculo guardado en el histórico (Total: {total_registros} registros)")


def procesar_ac(voltaje, corriente, coseno_fi, horas):
    """Procesa cálculos AC."""
    error = validar_entrada(voltaje, corriente, coseno_fi)
    if error:
        st.error(error)
        return
    
    if voltaje > 0 and corriente > 0:
        potencia_activa, potencia_reactiva, potencia_aparente = calcular_potencias(voltaje, corriente, coseno_fi)
        impedancia, resistencia, reactancia = calcular_impedancias(voltaje, corriente, coseno_fi)
        consumo = calcular_consumo(potencia_activa, horas)
        
        st.subheader("📊 Resultados - Corriente Alterna")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Potencias")
            mostrar_resultados([
                ("Potencia activa", potencia_activa, "W"),
                ("Potencia reactiva", potencia_reactiva, "VAR"),
                ("Potencia aparente", potencia_aparente, "VA"),
                ("Consumo", consumo, "kWh")
            ])
        
        with col2:
            st.subheader("Impedancias")
            mostrar_resultados([
                ("Impedancia total", impedancia, "Ω"),
                ("Resistencia", resistencia, "Ω"),
                ("Reactancia", reactancia, "Ω"),
                ("Factor de potencia", coseno_fi, "")
            ])
        
        # Visualizaciones
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(crear_triangulo_potencias(potencia_activa, potencia_reactiva), use_container_width=True)
        with col2:
            st.plotly_chart(crear_grafico_circular(potencia_activa, potencia_reactiva, potencia_aparente), use_container_width=True)
        
        # Guardar histórico
        datos = {
            'tipo_circuito': 'Resistivo',
            'tipo_corriente': 'AC',
            'voltaje': voltaje,
            'corriente': corriente,
            'coseno_fi': coseno_fi,
            'potencia_activa': potencia_activa,
            'potencia_reactiva': potencia_reactiva,
            'potencia_aparente': potencia_aparente,
            'impedancia': impedancia,
            'resistencia': resistencia,
            'reactancia': reactancia
        }
        total_registros = guardar_historico(datos)
        st.success(f"✅ Cálculo guardado en el histórico (Total: {total_registros} registros)")


def procesar_circuito_capacitivo():
    """Procesa los cálculos para circuitos capacitivos."""
    st.header("🔋 Circuito Capacitivo")
    
    tipo_corriente = st.radio(
        "Selecciona el tipo de corriente",
        ["Corriente Continua (DC)", "Corriente Alterna (AC)"],
        key="capacitivo_tipo"
    )
    
    # Parámetros de entrada
    with st.sidebar:
        st.header("📝 Parámetros de entrada")
        voltaje = st.number_input('Voltaje (V)', min_value=0.0, key="cap_voltaje")
        capacitancia = st.number_input('Capacitancia (F)', min_value=0.0, format="%.9f", 
                                     help="Introduce la capacitancia en Faradios")
        
        if tipo_corriente == "Corriente Alterna (AC)":
            frecuencia = st.number_input('Frecuencia (Hz)', min_value=0.0, value=60.0,
                                       help="Introduce la frecuencia en Hertz")
    
    if voltaje <= 0 or capacitancia <= 0:
        st.error("El voltaje y la capacitancia deben ser mayores que 0")
        return
    
    if tipo_corriente == "Corriente Continua (DC)":
        carga, energia = calcular_capacitor_dc(voltaje, capacitancia)
        
        st.subheader("📊 Resultados - Capacitor DC")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parámetros del capacitor")
            mostrar_resultados([
                ("Voltaje", voltaje, "V"),
                ("Capacitancia", capacitancia, "F"),
                ("Carga almacenada", carga, "C"),
                ("Energía almacenada", energia, "J")
            ])
        
        with col2:
            valores = [voltaje, capacitancia, carga, energia]
            titulos = ['Voltaje (V)', 'Capacitancia (F)', 'Carga (C)', 'Energía (J)']
            st.plotly_chart(crear_grafico_capacitor(valores, titulos, "DC"), use_container_width=True)
    
    else:  # AC
        if frecuencia <= 0:
            st.error("La frecuencia debe ser mayor que 0")
            return
        
        reactancia_capacitiva, corriente, potencia_reactiva = calcular_capacitor_ac(voltaje, frecuencia, capacitancia)
        
        st.subheader("📊 Resultados - Capacitor AC")
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parámetros del capacitor")
            mostrar_resultados([
                ("Voltaje", voltaje, "V"),
                ("Capacitancia", capacitancia, "F"),
                ("Frecuencia", frecuencia, "Hz"),
                ("Reactancia capacitiva", reactancia_capacitiva, "Ω"),
                ("Corriente", corriente, "A"),
                ("Potencia reactiva", potencia_reactiva, "VAR")
            ])
        
        with col2:
            valores = [voltaje, corriente, reactancia_capacitiva, potencia_reactiva]
            titulos = ['Voltaje (V)', 'Corriente (A)', 'Reactancia (Ω)', 'P. Reactiva (VAR)']
            st.plotly_chart(crear_grafico_capacitor(valores, titulos, "AC"), use_container_width=True)


def main():
    """Función principal de la aplicación."""
    configurar_pagina()
    mostrar_info_version()
    
    # Navegación principal
    tab1, tab2 = st.tabs(["🧮 Calculadora", "📊 Histórico"])
    
    with tab1:
        tipo_circuito = st.radio(
            "Selecciona el tipo de circuito",
            ["Resistivo", "Capacitivo", "Trifásico"],
            help="Elige el tipo de circuito para realizar los cálculos correspondientes"
        )
        
        st.markdown("---")
        
        if tipo_circuito == "Trifásico":
            procesar_circuito_trifasico()
        elif tipo_circuito == "Capacitivo":
            procesar_circuito_capacitivo()
        else:  # Resistivo
            procesar_circuito_resistivo()
    
    with tab2:
        mostrar_historico()


if __name__ == "__main__":
    main()
