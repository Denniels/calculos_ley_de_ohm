"""
Módulo de gestión de datos
Contiene funciones para guardar, cargar y manejar el histórico de cálculos
"""

import pandas as pd
import datetime
import os
import streamlit as st
from fpdf import FPDF
import tempfile


def guardar_historico(datos):
    """Guarda los resultados en un archivo CSV."""
    archivo_historico = 'historico_calculos.csv'
    
    # Agregar timestamp
    datos['fecha'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Crear DataFrame con los nuevos datos
    nuevo_df = pd.DataFrame([datos])
    
    # Si el archivo existe, cargarlo y agregar los nuevos datos
    if os.path.exists(archivo_historico):
        df_existente = pd.read_csv(archivo_historico)
        df_final = pd.concat([df_existente, nuevo_df], ignore_index=True)
    else:
        df_final = nuevo_df
    
    # Guardar el DataFrame actualizado
    df_final.to_csv(archivo_historico, index=False)
    
    return len(df_final)


def cargar_historico():
    """Carga el histórico de cálculos desde el archivo CSV."""
    archivo_historico = 'historico_calculos.csv'
    
    if os.path.exists(archivo_historico):
        try:
            df = pd.read_csv(archivo_historico)
            # Convertir la columna de fecha
            df['fecha'] = pd.to_datetime(df['fecha'])
            return df
        except Exception as e:
            st.error(f"Error al cargar el histórico: {e}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()


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
                options=df['tipo_corriente'].unique() if 'tipo_corriente' in df.columns else []
            )
        
        # Aplicar filtros
        if tipo_circuito_filtro:
            df = df[df['tipo_circuito'].isin(tipo_circuito_filtro)]
        if tipo_corriente_filtro and 'tipo_corriente' in df.columns:
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
    else:
        st.info("No hay datos en el histórico aún.")


def crear_pdf_reporte(datos, graficos=None):
    """Crea un informe PDF con los resultados del cálculo."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    
    # Título
    pdf.cell(0, 10, 'Informe de Cálculo - Ley de Ohm', 0, 1, 'C')
    pdf.ln(10)
    
    # Fecha y hora
    pdf.set_font('Arial', '', 10)
    fecha_actual = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    pdf.cell(0, 10, f'Generado el: {fecha_actual}', 0, 1, 'L')
    pdf.ln(5)
    
    # Datos del cálculo
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Parámetros de entrada:', 0, 1, 'L')
    pdf.set_font('Arial', '', 10)
    
    for key, value in datos.items():
        if key != 'fecha':
            pdf.cell(0, 8, f'{key}: {value}', 0, 1, 'L')
    
    # Guardar en archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf.output(temp_file.name)
    return temp_file.name


def mostrar_resultados(resultados):
    """Muestra los resultados con formato mejorado."""
    for titulo, valor, unidad in resultados:
        col1, col2 = st.columns([2, 3])
        with col1:
            st.write(f"**{titulo}:**")
        with col2:
            st.write(f"{valor:.2f} {unidad}")
