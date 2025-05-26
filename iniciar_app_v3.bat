@echo off
echo 🚀 Iniciando Calculadora de Ley de Ohm v3.0 (Modular)...
echo.
echo ⚡ Verificando dependencias...
python -c "import streamlit, plotly, pandas, numpy; print('✅ Todas las dependencias están instaladas')" 2>nul
if errorlevel 1 (
    echo ❌ Faltan dependencias. Instalando...
    pip install -r requirements.txt
)

echo.
echo 🧪 Ejecutando pruebas del sistema modular...
python test_modular.py
if errorlevel 1 (
    echo ❌ Error en las pruebas. Verifique la configuración.
    pause
    exit /b 1
)

echo.
echo 🌐 Iniciando aplicación modular en el navegador...
echo 📍 URL: http://localhost:8501
echo.
echo Para detener la aplicación, presiona Ctrl+C
echo.
streamlit run app.py
