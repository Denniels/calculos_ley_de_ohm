import streamlit as st
import math
import plotly.graph_objects as go
import pandas as pd

st.title('Calculadora de Ley de Ohm en Corriente Alterna')

# Entradas del usuario
horas = st.number_input('Introduce las horas de funcionamiento', min_value=0.0)
coseno_fi = st.number_input('Introduce el coseno de φ (factor de potencia)', min_value=-1.0, max_value=1.0)
voltaje = st.number_input('Introduce el voltaje (en voltios)', min_value=0.0)
corriente = st.number_input('Introduce la corriente (en amperios)', min_value=0.0)

# Control de corriente alterna
if corriente != 0 and -1 <= coseno_fi <= 1:
    # Calcula la impedancia
    impedancia = voltaje / corriente

    # Calcula las potencias
    potencia_activa = voltaje * corriente * coseno_fi
    potencia_reactiva = voltaje * corriente * math.sin(math.acos(coseno_fi))
    potencia_aparente = voltaje * corriente

    # Calcula el consumo en kWh
    consumo = potencia_activa * horas / 1000

    # Muestra los resultados
    st.write('La potencia activa (en vatios) es: ', potencia_activa)
    st.write('La potencia reactiva (en var) es: ', potencia_reactiva)
    st.write('La potencia aparente (en voltiamperios) es: ', potencia_aparente)
    st.write('El factor de potencia es: ', coseno_fi)
    st.write('El consumo (en kWh) es: ', consumo)

    # Crear el gráfico del triángulo de potencias
    fig = go.Figure(data=go.Scatter(x=[0, potencia_activa, 0, 0], y=[0, 0, potencia_reactiva, 0], fill='toself'))
    fig.update_layout(title='Triángulo de Potencias', xaxis_title='Potencia Activa (W)', yaxis_title='Potencia Reactiva (VAR)')
    st.plotly_chart(fig)

    # Crear el gráfico de círculo con las potencias
    fig = go.Figure(data=[go.Pie(labels=['Potencia Activa', 'Potencia Reactiva', 'Potencia Aparente'], values=[potencia_activa, potencia_reactiva, potencia_aparente])])
    fig.update_layout(title='Gráfico de Círculo de Potencias')
    st.plotly_chart(fig)
else:
    st.write('La corriente no puede ser cero y el coseno de φ debe estar entre -1 y 1.')