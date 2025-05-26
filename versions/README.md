# 📁 Versiones del Proyecto

Este directorio contiene todas las versiones del proyecto para mantener un historial completo del desarrollo.

## 📋 Archivos por Versión

### Versión 1.0 (Original)
- `ohm_v1.py` - Archivo original de la calculadora

### Versión 2.0 (Mejorada - Monolítica)
- `ohm_v2.py` - Versión mejorada con funcionalidades avanzadas
- `test_simple_v2.py` - Pruebas funcionales de la v2
- `test_completo_v2.py` - Suite completa de pruebas de la v2

## 🔄 Historial de Cambios

### v1.0 → v2.0
- ✅ Añadido análisis de sistemas trifásicos
- ✅ Implementado análisis de desequilibrio
- ✅ Agregada evaluación de eficiencia energética
- ✅ Incluido análisis de calidad de energía
- ✅ Corregido bug del botón `st.rerun()`
- ✅ Mejoradas las visualizaciones
- ✅ Añadido histórico de cálculos

### v2.0 → v3.0 (Actual - Modular)
- ✅ Arquitectura modular separada en módulos
- ✅ Separación de responsabilidades:
  - `calculos.py` - Lógica de cálculo
  - `graficos.py` - Visualizaciones
  - `datos.py` - Gestión de datos
- ✅ Código más limpio y mantenible
- ✅ Mejor organización del proyecto
- ✅ Aplicación principal simplificada (`app.py`)

## 🎯 Uso de Versiones

- **Para desarrollo actual**: Usar `app.py` en el directorio raíz
- **Para referencia**: Consultar versiones anteriores en este directorio
- **Para rollback**: Copiar versión deseada al directorio raíz

## 🔧 Compatibilidad

Todas las versiones son compatibles con los mismos archivos de datos:
- `historico_calculos.csv`
- `requirements.txt`
