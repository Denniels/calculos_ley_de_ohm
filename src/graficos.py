"""
Módulo de visualizaciones y gráficos
Contiene todas las funciones para crear gráficos y diagramas interactivos
"""

import math
import plotly.graph_objects as go
import numpy as np


def crear_triangulo_potencias(potencia_activa, potencia_reactiva):
    """Crea el gráfico del triángulo de potencias."""
    potencia_aparente = math.sqrt(potencia_activa**2 + potencia_reactiva**2)
    angulo = math.degrees(math.atan2(potencia_reactiva, potencia_activa))
    
    fig = go.Figure()
    
    # Agregar el triángulo
    fig.add_trace(go.Scatter(
        x=[0, potencia_activa, 0, 0],
        y=[0, 0, potencia_reactiva, 0],
        mode='lines+markers',
        line=dict(color='blue', width=3),
        marker=dict(size=8, color='blue'),
        name='Triángulo de Potencias',
        hovertemplate="<b>Triángulo de Potencias</b><br>" +
                     "P (Activa): %{x:.2f} W<br>" +
                     "Q (Reactiva): %{y:.2f} VAR<extra></extra>"
    ))
      # Agregar línea de potencia aparente (hipotenusa)
    fig.add_trace(go.Scatter(
        x=[0, potencia_activa],
        y=[0, potencia_reactiva],
        mode='lines',
        line=dict(color='red', width=3, dash='dash'),
        name='Potencia Aparente',
        hovertemplate="<b>Potencia Aparente</b><br>" +
                     "S: %{customdata[0]:.2f} VA<br>" +
                     "φ: %{customdata[1]:.1f}°<extra></extra>",
        customdata=[[potencia_aparente, angulo], [potencia_aparente, angulo]]
    ))
    
    # Agregar anotaciones
    fig.add_annotation(
        x=potencia_activa/2,
        y=-10,
        text=f'P: {potencia_activa:.2f} W',
        showarrow=True,
        arrowhead=2
    )
    
    fig.add_annotation(
        x=-30,
        y=potencia_reactiva/2,
        text=f'Q: {potencia_reactiva:.2f} VAR',
        showarrow=True,
        arrowhead=2
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
    labels = ['Potencia Activa', 'Potencia Reactiva']
    values = [potencia_activa, potencia_reactiva]
    colors = ['#FF9900', '#00CC96']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent+value',
        texttemplate='%{label}<br>%{value:.2f} %{customdata}<br>%{percent}',
        customdata=['W', 'VAR'],
        hovertemplate="<b>%{label}</b><br>" +
                     "Valor: %{value:.2f} %{customdata}<br>" +
                     "Porcentaje: %{percent}<br>" +
                     "<extra></extra>",
    )])
    
    fig.update_layout(
        title='Distribución de Potencias',
        annotations=[dict(text=f'S: {potencia_aparente:.2f} VA', x=0.5, y=0.5, 
                         font_size=16, showarrow=False)],
        template='plotly_white'
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


def crear_grafico_capacitor(valores, titulos, tipo="DC"):
    """Crea una visualización de los parámetros del capacitor."""
    colores = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=titulos,
        y=valores,
        marker_color=colores[:len(valores)],
        text=[f'{v:.2e}' if v < 0.01 else f'{v:.2f}' for v in valores],
        textposition='auto',
        hovertemplate="<b>%{x}</b><br>" +
                     "Valor: %{y:.2e}<extra></extra>",
    ))
    
    fig.update_layout(
        title=f'Parámetros del Capacitor - {tipo}',
        yaxis_title='Valor',
        template='plotly_white',
        xaxis=dict(tickangle=-45)
    )
    return fig


def crear_diagrama_fasorial_trifasico(voltajes, angulos):
    """Crea un diagrama fasorial para el sistema trifásico."""
    fig = go.Figure()
    
    fases = ['R', 'S', 'T']
    colores = ['#FF0000', '#00FF00', '#0000FF']
    
    for fase, voltaje, angulo, color in zip(fases, voltajes, angulos, colores):
        # Convertir a radianes
        angulo_rad = math.radians(angulo)
        
        # Coordenadas del vector
        x_end = voltaje * math.cos(angulo_rad)
        y_end = voltaje * math.sin(angulo_rad)
        
        # Agregar el vector
        fig.add_trace(go.Scatter(
            x=[0, x_end],
            y=[0, y_end],
            mode='lines+markers+text',
            line=dict(color=color, width=3),
            marker=dict(size=[0, 10], color=color),
            text=['', f'V{fase}'],
            textposition='top center',
            name=f'Fase {fase}',
            hovertemplate="<b>Fase %{text}</b><br>" +
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
            line=dict(color=color, width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Agregar etiqueta del ángulo
        fig.add_annotation(
            x=radio*math.cos(angulo_rad/2),
            y=radio*math.sin(angulo_rad/2),
            text=f'{angulo}°',
            showarrow=False,
            font=dict(size=10, color=color)
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
