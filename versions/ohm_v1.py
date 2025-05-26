import streamlit as st
import math
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime
import os
from fpdf import FPDF
import tempfile

def validar_entrada(voltaje, corriente, coseno_fi):
    """Valida los parámetros de entrada y retorna un mensaje de error si hay problemas."""
    if voltaje <= 0:
        return "El voltaje debe ser mayor que 0"
    if corriente <= 0:
        return "La corriente debe ser mayor que 0"
    if not -1 <= coseno_fi <= 1:
        return "El factor de potencia debe estar entre -1 y 1"
    return None

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

def crear_triangulo_potencias(potencia_activa, potencia_reactiva):
    """Crea el gráfico del triángulo de potencias."""
    potencia_aparente = math.sqrt(potencia_activa**2 + potencia_reactiva**2)
    angulo = math.degrees(math.atan2(potencia_reactiva, potencia_activa))
    
    fig = go.Figure()
    
    # Agregar el triángulo
    fig.add_trace(go.Scatter(
        x=[0, potencia_activa, 0, 0],
        y=[0, 0, potencia_reactiva, 0],
        fill='toself',
        name='Triángulo de Potencias',
        hovertemplate='<b>%{text}</b><br>' +
                      'Valor: %{customdata:.2f}<extra></extra>',
        text=['Origen', 'P. Activa', 'P. Reactiva', 'Origen'],
        customdata=[0, potencia_activa, potencia_reactiva, 0],
        line=dict(color='royalblue', width=2)
    ))
    
    # Agregar anotaciones para los valores
    fig.add_annotation(
        x=potencia_activa/2,
        y=0,
        text=f'P: {potencia_activa:.2f} W',
        showarrow=True,
        arrowhead=2,
        yshift=-20
    )
    
    fig.add_annotation(
        x=0,
        y=potencia_reactiva/2,
        text=f'Q: {potencia_reactiva:.2f} VAR',
        showarrow=True,
        arrowhead=2,
        xshift=-20
    )
    
    fig.add_annotation(
        x=potencia_activa/2,
        y=potencia_reactiva/2,
        text=f'S: {potencia_aparente:.2f} VA\nφ: {angulo:.1f}°',
        showarrow=True,
        arrowhead=2
    )
    
    fig.update_layout(
        title={
            'text': 'Triángulo de Potencias',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title='Potencia Activa (W)',
        yaxis_title='Potencia Reactiva (VAR)',
        showlegend=True,
        hovermode='closest',
        template='plotly_white',
        xaxis=dict(zeroline=True, showgrid=True),
        yaxis=dict(zeroline=True, showgrid=True, scaleanchor="x", scaleratio=1),
        hoverlabel=dict(bgcolor="white", font_size=12)
    )
    return fig

def crear_grafico_circular(potencia_activa, potencia_reactiva, potencia_aparente):
    """Crea el gráfico circular de potencias."""
    fig = go.Figure()
    
    valores = [potencia_activa, potencia_reactiva, potencia_aparente]
    labels = ['Potencia Activa (W)', 'Potencia Reactiva (VAR)', 'Potencia Aparente (VA)']
    colores = ['#00CC96', '#EF553B', '#636EFA']
    
    fig.add_trace(go.Pie(
        values=valores,
        labels=labels,
        hole=0.4,
        marker=dict(colors=colores),
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>" +
                     "Valor: %{value:.2f}<br>" +
                     "Porcentaje: %{percent}<extra></extra>",
        textfont=dict(size=12)
    ))
    
    fig.update_layout(
        title={
            'text': 'Distribución de Potencias',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        annotations=[dict(
            text='Potencias',
            x=0.5, y=0.5,
            font_size=14,
            showarrow=False
        )],
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        )
    )
    return fig

def crear_grafico_circuito_dc(voltaje, corriente, resistencia):
    """Crea una visualización del circuito DC."""
    fig = go.Figure()
    
    # Datos para el gráfico
    parametros = ['Voltaje (V)', 'Corriente (A)', 'Resistencia (Ω)']
    valores = [voltaje, corriente, resistencia]
    colores = ['#FF9900', '#00CC96', '#AB63FA']
    
    # Agregar barras con más estilo
    fig.add_trace(go.Bar(
        x=parametros,
        y=valores,
        marker_color=colores,
        text=[f'{v:.2f}' for v in valores],
        textposition='auto',
        hovertemplate="<b>%{x}</b><br>" +
                     "Valor: %{y:.2f}<extra></extra>",
        width=0.6
    ))
    
    # Agregar línea de tendencia
    fig.add_trace(go.Scatter(
        x=parametros,
        y=valores,
        mode='lines',
        name='Tendencia',
        line=dict(color='royalblue', width=2, dash='dot'),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title={
            'text': 'Parámetros del Circuito DC',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis_title='Valor',
        template='plotly_white',
        showlegend=False,
        barmode='group',
        hoverlabel=dict(bgcolor="white"),
        yaxis=dict(zeroline=True, gridwidth=1),
        xaxis=dict(tickangle=-45)
    )
    return fig

def calcular_capacitor_dc(voltaje, capacitancia):
    """Calcula la carga y energía almacenada en un capacitor DC."""
    carga = capacitancia * voltaje  # Q = C * V
    energia = 0.5 * capacitancia * (voltaje ** 2)  # E = 1/2 * C * V²
    return carga, energia

def calcular_capacitor_ac(voltaje, frecuencia, capacitancia):
    """Calcula parámetros del capacitor en AC."""
    # Reactancia capacitiva: Xc = 1/(2πfC)
    reactancia_capacitiva = 1 / (2 * math.pi * frecuencia * capacitancia)
    # Corriente: I = V/Xc
    corriente = voltaje / reactancia_capacitiva
    # Potencia reactiva: Q = V * I
    potencia_reactiva = voltaje * corriente
    return reactancia_capacitiva, corriente, potencia_reactiva

def crear_grafico_capacitor(valores, titulos, tipo="DC"):
    """Crea una visualización de los parámetros del capacitor."""
    fig = go.Figure()
    
    colores = ['#FF9900', '#00CC96', '#AB63FA', '#EF553B']
    
    # Agregar barras con mejoras visuales
    fig.add_trace(go.Bar(
        x=titulos,
        y=valores,
        marker_color=colores[:len(valores)],
        text=[f'{v:.2e}' if abs(v) < 0.01 or abs(v) > 1000 else f'{v:.2f}' for v in valores],
        textposition='auto',
        hovertemplate="<b>%{x}</b><br>" +
                     "Valor: %{y:.2e}<extra></extra>",
        width=0.6
    ))
    
    # Agregar marcadores de puntos
    fig.add_trace(go.Scatter(
        x=titulos,
        y=valores,
        mode='markers',
        marker=dict(
            size=12,
            symbol='diamond',
            color=colores[:len(valores)],
            line=dict(
                color='white',
                width=1
            )
        ),
        hoverinfo='skip',
        showlegend=False
    ))
    
    fig.update_layout(
        title={
            'text': f'Parámetros del Capacitor - {tipo}',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis_title='Valor (escala logarítmica)',
        template='plotly_white',
        showlegend=False,
        yaxis_type='log',
        hoverlabel=dict(bgcolor="white"),
        yaxis=dict(
            gridwidth=1,
            tickformat='.2e'
        ),
        xaxis=dict(tickangle=-45)
    )
    return fig

def guardar_historico(datos):
    """Guarda los resultados en un archivo CSV."""
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_nuevo = pd.DataFrame([{**datos, 'fecha': fecha}])
    
    archivo_historico = "historico_calculos.csv"
    if os.path.exists(archivo_historico):
        df_existente = pd.read_csv(archivo_historico)
        df_actualizado = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_actualizado = df_nuevo
    
    df_actualizado.to_csv(archivo_historico, index=False)
    return len(df_actualizado)

def cargar_historico():
    """Carga el histórico de cálculos desde el archivo CSV."""
    archivo_historico = "historico_calculos.csv"
    if os.path.exists(archivo_historico):
        return pd.read_csv(archivo_historico)
    return None

def mostrar_historico():
    """Muestra el histórico de cálculos en la interfaz."""
    df = cargar_historico()
    if df is not None and not df.empty:
        st.subheader("Histórico de Cálculos")
        
        # Agregar filtros
        col1, col2 = st.columns(2)
        with col1:
            tipo_circuito_filtro = st.multiselect(
                "Filtrar por tipo de circuito",
                options=df['tipo_circuito'].unique()
            )
        with col2:
            tipo_corriente_filtro = st.multiselect(
                "Filtrar por tipo de corriente",
                options=df['tipo_corriente'].unique()
            )
        
        # Aplicar filtros
        if tipo_circuito_filtro:
            df = df[df['tipo_circuito'].isin(tipo_circuito_filtro)]
        if tipo_corriente_filtro:
            df = df[df['tipo_corriente'].isin(tipo_corriente_filtro)]
        
        # Mostrar el dataframe con estilos
        st.dataframe(
            df.style.format({col: '{:.2f}' for col in df.select_dtypes('float64').columns}),
            use_container_width=True
        )
        
        # Opción para descargar
        csv = df.to_csv(index=False)
        st.download_button(
            "Descargar histórico",
            csv,
            "historico_calculos.csv",
            "text/csv",
            key='download-csv'
        )
        
        # Mostrar estadísticas
        if st.checkbox("Mostrar estadísticas"):
            st.subheader("Estadísticas del histórico")
            col1, col2 = st.columns(2)
            with col1:
                st.write("Número total de cálculos:", len(df))
                st.write("Tipos de circuitos más comunes:")
                st.write(df['tipo_circuito'].value_counts())
            with col2:
                st.write("Rango de fechas:")
                st.write("- Desde:", df['fecha'].min())
                st.write("- Hasta:", df['fecha'].max())

def crear_pdf_reporte(datos, graficos=None):
    """Crea un informe PDF con los resultados del cálculo."""
    pdf = FPDF()
    pdf.add_page()
    
    # Configuración de la página
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", "B", 16)
    
    # Título
    pdf.cell(0, 10, "Informe de Cálculos Eléctricos", ln=True, align='C')
    pdf.ln(10)
    
    # Información general
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, f"Tipo de circuito: {datos['tipo_circuito']}", ln=True)
    pdf.cell(0, 10, f"Tipo de corriente: {datos['tipo_corriente']}", ln=True)
    pdf.ln(10)
    
    # Parámetros y resultados
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Resultados del cálculo:", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 12)
    for key, value in datos.items():
        if key not in ['tipo_circuito', 'tipo_corriente', 'fecha']:
            if isinstance(value, float):
                pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value:.2f}", ln=True)
            else:
                pdf.cell(0, 10, f"{key.replace('_', ' ').title()}: {value}", ln=True)
    
    # Agregar gráficos si existen
    if graficos:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Gráficos:", ln=True)
        pdf.ln(5)
        
        for nombre, fig in graficos.items():
            # Guardar el gráfico temporalmente
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                fig.write_image(tmp.name)
                pdf.image(tmp.name, x=10, w=190)
                os.unlink(tmp.name)  # Eliminar archivo temporal
            pdf.ln(10)
    
    # Generar el archivo PDF
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"reporte_calculos_{timestamp}.pdf"
    pdf.output(pdf_filename)
    return pdf_filename

def mostrar_resultados(resultados):
    """Muestra los resultados con formato mejorado."""
    for titulo, valor, unidad in resultados:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write(f"**{titulo}:**")
        with col2:
            st.write(f"{valor:.2f} {unidad}")

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

def crear_diagrama_fasorial_trifasico(voltajes, angulos):
    """Crea un diagrama fasorial para el sistema trifásico."""
    fig = go.Figure()
    
    # Colores para cada fase
    colores = {'R': '#FF0000', 'S': '#00FF00', 'T': '#0000FF'}
    
    # Agregar fasores
    for fase, voltaje, angulo in zip(['R', 'S', 'T'], voltajes, angulos):
        # Convertir a coordenadas cartesianas
        x = voltaje * math.cos(math.radians(angulo))
        y = voltaje * math.sin(math.radians(angulo))
        
        # Agregar línea del fasor
        fig.add_trace(go.Scatter(
            x=[0, x],
            y=[0, y],
            mode='lines+markers',
            name=f'Fase {fase}',
            line=dict(color=colores[fase], width=2),
            hovertemplate=f'Fase {fase}<br>' +
                         'Voltaje: %{customdata[0]:.2f} V<br>' +
                         'Ángulo: %{customdata[1]:.1f}°<extra></extra>',
            customdata=[[voltaje, angulo]]*2
        ))
        
        # Agregar arco para mostrar el ángulo
        radio = voltaje * 0.2
        angulo_rad = math.radians(angulo)
        arco_x = [radio * math.cos(th) for th in np.linspace(0, angulo_rad, 50)]
        arco_y = [radio * math.sin(th) for th in np.linspace(0, angulo_rad, 50)]
        
        fig.add_trace(go.Scatter(
            x=arco_x,
            y=arco_y,
            mode='lines',
            line=dict(color=colores[fase], width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Agregar etiqueta del ángulo
        fig.add_annotation(
            x=radio*math.cos(angulo_rad/2),
            y=radio*math.sin(angulo_rad/2),
            text=f'{angulo}°',
            showarrow=False,
            font=dict(size=10, color=colores[fase])
        )
    
    # Configuración del layout
    fig.update_layout(
        title='Diagrama Fasorial Trifásico',
        xaxis_title='Componente Real',
        yaxis_title='Componente Imaginaria',
        showlegend=True,
        xaxis=dict(
            scaleanchor="y",
            scaleratio=1,
            showgrid=True,
            zeroline=True,
            showline=True,
            mirror=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=True,
            showline=True,
            mirror=True
        ),
        template='plotly_white'
    )
    
    return fig

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
    elif eficiencia_fp >= 80:
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

def crear_grafico_desequilibrio(corrientes_fases, nombres_fases):
    """Crea un gráfico de barras mostrando el desequilibrio de corrientes."""
    fig = go.Figure()
    
    colores = ['#FF0000', '#00FF00', '#0000FF']  # R, S, T
    
    fig.add_trace(go.Bar(
        x=nombres_fases,
        y=corrientes_fases,
        marker_color=colores,
        text=[f'{i:.2f} A' for i in corrientes_fases],
        textposition='auto',
        hovertemplate="<b>Fase %{x}</b><br>" +
                     "Corriente: %{y:.2f} A<extra></extra>"
    ))
    
    # Línea del promedio
    promedio = sum(corrientes_fases) / len(corrientes_fases)
    fig.add_hline(y=promedio, line_dash="dash", line_color="red",
                  annotation_text=f"Promedio: {promedio:.2f} A")
    
    fig.update_layout(
        title='Corrientes por Fase - Análisis de Desequilibrio',
        xaxis_title='Fases',
        yaxis_title='Corriente (A)',
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def main():
    st.set_page_config(page_title="Calculadora Ley de Ohm", layout="wide")
    st.title('Calculadora de Ley de Ohm')
    
    # Tabs para la navegación
    tab1, tab2 = st.tabs(["Calculadora", "Histórico"])
    
    with tab1:
        tipo_circuito = st.radio(
            "Selecciona el tipo de circuito",
            ["Resistivo", "Capacitivo", "Trifásico"],
            help="Elige el tipo de circuito para realizar los cálculos correspondientes"        )
        
        if tipo_circuito == "Trifásico":
            st.header("Sistema Trifásico")
            conexion = st.radio(
                "Tipo de conexión",
                ["Estrella (Y)", "Delta (Δ)"],
                help="Selecciona el tipo de conexión del sistema trifásico"
            )
            
            # Configuración de parámetros básicos
            col1, col2, col3 = st.columns(3)
            with col1:
                voltaje_linea = st.number_input('Voltaje de línea (VL)', min_value=0.0,
                                              value=380.0,
                                              help="Voltaje entre líneas del sistema trifásico")
            with col2:
                corriente_linea = st.number_input('Corriente de línea (IL)', min_value=0.0,
                                                value=10.0,
                                                help="Corriente de línea del sistema trifásico")
            with col3:
                factor_potencia = st.number_input('Factor de potencia (cos φ)',
                                                min_value=-1.0, max_value=1.0, value=0.85,
                                                help="Factor de potencia del sistema trifásico")
            
            # Entrada de corrientes individuales para análisis de desequilibrio
            st.subheader("Corrientes Individuales por Fase (para análisis de desequilibrio)")
            col1, col2, col3 = st.columns(3)
            with col1:
                corriente_r = st.number_input('Corriente Fase R (IR)', min_value=0.0,
                                            value=corriente_linea,
                                            help="Corriente en la fase R")
            with col2:
                corriente_s = st.number_input('Corriente Fase S (IS)', min_value=0.0,
                                            value=corriente_linea,
                                            help="Corriente en la fase S")
            with col3:
                corriente_t = st.number_input('Corriente Fase T (IT)', min_value=0.0,
                                            value=corriente_linea,
                                            help="Corriente en la fase T")

            # Validación de entrada
            if voltaje_linea <= 0 or corriente_linea <= 0:
                st.error("El voltaje y la corriente deben ser mayores que 0")
                return
            
            if corriente_r <= 0 or corriente_s <= 0 or corriente_t <= 0:
                st.error("Las corrientes de fase deben ser mayores que 0")
                return

            # Cálculos según el tipo de conexión
            if conexion == "Estrella (Y)":
                resultados = calcular_sistema_trifasico_estrella(voltaje_linea, corriente_linea, factor_potencia)
            else:  # Delta
                resultados = calcular_sistema_trifasico_delta(voltaje_linea, corriente_linea, factor_potencia)

            # Análisis de desequilibrio
            desequilibrio = calcular_desequilibrio_corrientes(corriente_r, corriente_s, corriente_t)
            
            # Análisis de eficiencia energética
            eficiencia = analizar_eficiencia_energetica(
                resultados['potencia_activa_total'],
                resultados['potencia_aparente_total'],
                factor_potencia
            )
            
            # Análisis de calidad de energía
            calidad = analizar_calidad_energia(
                desequilibrio['desequilibrio_porcentaje'],
                factor_potencia,
                resultados['potencia_aparente_total']
            )

            # Mostrar resultados principales
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Parámetros por Fase")
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
                st.subheader("Parámetros Totales del Sistema")
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
                # Gráfico de corrientes por fase
                fig_desequilibrio = crear_grafico_desequilibrio(
                    [corriente_r, corriente_s, corriente_t], 
                    ['R', 'S', 'T']
                )
                st.plotly_chart(fig_desequilibrio, use_container_width=True)

            # Análisis de Eficiencia Energética
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
                # Métricas de eficiencia
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
                
                # Mostrar problemas detectados
                st.write("**Estado del sistema:**")
                for problema in calidad['problemas']:
                    st.write(f"{problema}")
                    
            with col2:
                st.write("**Análisis económico:**")
                st.write(f"• Pérdidas estimadas: {calidad['perdidas_kw']:.2f} kW")
                st.write(f"• Costo anual estimado: ${calidad['costo_anual']:.2f}")
                
                # Indicador de calidad visual
                if calidad['puntuacion'] >= 80:
                    st.success(f"🟢 Calidad buena ({calidad['puntuacion']:.0f}/100)")
                elif calidad['puntuacion'] >= 60:
                    st.warning(f"🟡 Calidad regular ({calidad['puntuacion']:.0f}/100)")
                else:
                    st.error(f"🔴 Calidad deficiente ({calidad['puntuacion']:.0f}/100)")

            # Diagrama fasorial
            st.subheader("📐 Diagrama Fasorial")
            voltajes = [resultados['voltaje_fase']] * 3
            angulos = [0, -120, 120]  # Ángulos típicos para sistema trifásico balanceado
            st.plotly_chart(crear_diagrama_fasorial_trifasico(voltajes, angulos), use_container_width=True)

            # Resumen y recomendaciones
            st.subheader("📋 Resumen y Recomendaciones")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Estado general del sistema:**")
                
                # Determinar estado general
                estado_general = "Excelente"
                color_estado = "🟢"
                if calidad['puntuacion'] < 80 or desequilibrio['desequilibrio_porcentaje'] > 2:
                    estado_general = "Bueno"
                    color_estado = "🟡"
                if calidad['puntuacion'] < 60 or desequilibrio['desequilibrio_porcentaje'] > 5:
                    estado_general = "Requiere atención"
                    color_estado = "🔴"
                    
                st.write(f"{color_estado} **{estado_general}**")
                
            with col2:
                st.write("**Principales métricas:**")
                st.write(f"• Potencia total: {resultados['potencia_activa_total']/1000:.1f} kW")
                st.write(f"• Factor de potencia: {factor_potencia:.3f}")
                st.write(f"• Desequilibrio: {desequilibrio['desequilibrio_porcentaje']:.1f}%")
                st.write(f"• Eficiencia: {eficiencia['eficiencia_fp']:.1f}%")

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
            st.success(f"Cálculo guardado en el histórico (Total: {total_registros} registros)")
            
        else:
            tipo_corriente = st.radio(
                "Selecciona el tipo de corriente",
                ["Corriente Continua (DC)", "Corriente Alterna (AC)"],
                help="Elige el tipo de corriente para realizar los cálculos correspondientes"
            )
            
            with st.sidebar:
                st.header("Parámetros de entrada")
                
                if tipo_circuito == "Resistivo":
                    voltaje = st.number_input('Voltaje (V)', min_value=0.0, help="Introduce el voltaje en voltios")
                    corriente = st.number_input('Corriente (A)', min_value=0.0, help="Introduce la corriente en amperios")
                else:  # Circuito Capacitivo
                    voltaje = st.number_input('Voltaje (V)', min_value=0.0, help="Introduce el voltaje en voltios")
                    capacitancia = st.number_input('Capacitancia (F)', min_value=0.0, format="%.9f", 
                                                 help="Introduce la capacitancia en Faradios")
                    if tipo_corriente == "Corriente Alterna (AC)":
                        frecuencia = st.number_input('Frecuencia (Hz)', min_value=0.0, value=60.0,
                                                   help="Introduce la frecuencia en Hertz")
                
                if tipo_corriente == "Corriente Alterna (AC)" and tipo_circuito == "Resistivo":
                    coseno_fi = st.number_input('Factor de potencia (cos φ)', min_value=-1.0, max_value=1.0, 
                                              help="Introduce el factor de potencia (entre -1 y 1)")
                
                horas = st.number_input('Horas de funcionamiento', min_value=0.0, 
                                     help="Introduce las horas de funcionamiento para calcular el consumo")
            
            if tipo_circuito == "Capacitivo":
                # Lógica existente para circuito capacitivo
                if voltaje <= 0 or capacitancia <= 0:
                    st.error("El voltaje y la capacitancia deben ser mayores que 0")
                    return
                    
                if tipo_corriente == "Corriente Continua (DC)":
                    # Cálculos capacitor DC
                    carga, energia = calcular_capacitor_dc(voltaje, capacitancia)
                    
                    st.header("Resultados - Capacitor DC")
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
                        
                else:  # Capacitor AC
                    if frecuencia <= 0:
                        st.error("La frecuencia debe ser mayor que 0")
                        return
                        
                    reactancia_capacitiva, corriente, potencia_reactiva = calcular_capacitor_ac(voltaje, frecuencia, capacitancia)
                    
                    st.header("Resultados - Capacitor AC")
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

            else:  # Circuito Resistivo
                if tipo_corriente == "Corriente Continua (DC)":
                    error = validar_entrada_dc(voltaje, corriente)
                    if error:
                        st.error(error)
                        return

                    if voltaje > 0 and corriente > 0:
                        # Cálculos DC
                        resistencia, potencia = calcular_dc(voltaje, corriente)
                        consumo = calcular_consumo(potencia, horas)

                        # Mostrar resultados DC
                        st.header("Resultados - Corriente Continua")
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

                else:  # Corriente Alterna (AC)
                    error = validar_entrada(voltaje, corriente, coseno_fi)
                    if error:
                        st.error(error)
                        return

                    if voltaje > 0 and corriente > 0:
                        # Cálculos AC
                        potencia_activa, potencia_reactiva, potencia_aparente = calcular_potencias(voltaje, corriente, coseno_fi)
                        impedancia, resistencia, reactancia = calcular_impedancias(voltaje, corriente, coseno_fi)
                        consumo = calcular_consumo(potencia_activa, horas)

                        # Mostrar resultados AC
                        st.header("Resultados - Corriente Alterna")
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

                        # Visualizaciones AC
                        col1, col2 = st.columns(2)
                        with col1:
                            st.plotly_chart(crear_triangulo_potencias(potencia_activa, potencia_reactiva), use_container_width=True)
                        with col2:
                            st.plotly_chart(crear_grafico_circular(potencia_activa, potencia_reactiva, potencia_aparente), use_container_width=True)

                # Guardar resultados en el histórico después de cada cálculo
                if tipo_circuito == "Capacitivo":
                    if voltaje > 0 and capacitancia > 0:
                        datos = {
                            'tipo_circuito': 'Capacitivo',
                            'tipo_corriente': tipo_corriente,
                            'voltaje': voltaje,
                            'capacitancia': capacitancia,
                        }
                        if tipo_corriente == "Corriente Alterna (AC)":
                            datos.update({
                                'frecuencia': frecuencia,
                                'reactancia_capacitiva': reactancia_capacitiva,
                                'corriente': corriente,
                                'potencia_reactiva': potencia_reactiva
                            })
                        else:
                            datos.update({
                                'carga': carga,
                                'energia': energia
                            })
                        total_registros = guardar_historico(datos)
                        st.success(f"Cálculo guardado en el histórico (Total: {total_registros} registros)")
                
                else:  # Circuito Resistivo
                    if voltaje > 0 and corriente > 0:
                        datos = {
                            'tipo_circuito': 'Resistivo',
                            'tipo_corriente': tipo_corriente,
                            'voltaje': voltaje,
                            'corriente': corriente
                        }
                        if tipo_corriente == "Corriente Alterna (AC)":
                            datos.update({
                                'coseno_fi': coseno_fi,
                                'potencia_activa': potencia_activa,
                                'potencia_reactiva': potencia_reactiva,
                                'potencia_aparente': potencia_aparente,
                                'impedancia': impedancia,
                                'resistencia': resistencia,
                                'reactancia': reactancia
                            })
                        else:
                            datos.update({
                                'resistencia': resistencia,
                                'potencia': potencia
                            })
                        total_registros = guardar_historico(datos)
                        st.success(f"Cálculo guardado en el histórico (Total: {total_registros} registros)")
    
    with tab2:
        mostrar_historico()

if __name__ == "__main__":
    main()