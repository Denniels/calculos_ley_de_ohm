@echo off
echo 🚀 Iniciando Calculadora de Ley de Ohm...
echo.
echo Verificando dependencias...
python -c "import streamlit, plotly, pandas, numpy; print('✅ Todas las dependencias están instaladas')" 2>nul
if errorlevel 1 (
    echo ❌ Faltan dependencias. Instalando...
    pip install -r requirements.txt
)

echo.
echo 🌐 Iniciando aplicación en el navegador...
echo 📍 URL: http://localhost:8501
echo.
echo Para detener la aplicación, presiona Ctrl+C
echo.
streamlit run ohm_mejorado.py
