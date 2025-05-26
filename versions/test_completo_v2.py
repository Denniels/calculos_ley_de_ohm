#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Completo para la Calculadora de Ley de Ohm
===============================================
Este archivo contiene pruebas exhaustivas para todas las funcionalidades
de la aplicación, incluyendo validación de inputs y cálculos.
"""

import sys
import os
import math
import pandas as pd
import numpy as np
from datetime import datetime
import traceback

# Importar las funciones de los archivos principales
try:
    from ohm_mejorado import *
except ImportError:
    try:
        from ohm import *
    except ImportError:
        print("Error: No se pudo importar ninguno de los archivos principales")
        sys.exit(1)

class TestCalculadoraOhm:
    """Clase para realizar pruebas exhaustivas de la calculadora"""
    
    def __init__(self):
        self.resultados_pruebas = []
        self.errores_encontrados = []
        self.warnings = []
        
    def log_resultado(self, prueba, esperado, obtenido, status="PASS", mensaje=""):
        """Registra el resultado de una prueba"""
        resultado = {
            'prueba': prueba,
            'esperado': esperado,
            'obtenido': obtenido,
            'status': status,
            'mensaje': mensaje,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.resultados_pruebas.append(resultado)
        
        if status == "FAIL":
            self.errores_encontrados.append(resultado)
        elif status == "WARNING":
            self.warnings.append(resultado)
    
    def comparar_float(self, a, b, tolerancia=1e-6):
        """Compara dos números flotantes con tolerancia"""
        return abs(a - b) < tolerancia
    
    def test_validaciones_entrada(self):
        """Prueba las validaciones de entrada"""
        print("🔍 Probando validaciones de entrada...")
        
        # Test 1: Voltaje negativo
        error = validar_entrada(-10, 5, 0.8)
        self.log_resultado(
            "Validación voltaje negativo",
            "El voltaje debe ser mayor que 0",
            error,
            "PASS" if error == "El voltaje debe ser mayor que 0" else "FAIL"
        )
        
        # Test 2: Corriente negativa
        error = validar_entrada(10, -5, 0.8)
        self.log_resultado(
            "Validación corriente negativa",
            "La corriente debe ser mayor que 0",
            error,
            "PASS" if error == "La corriente debe ser mayor que 0" else "FAIL"
        )
        
        # Test 3: Factor de potencia fuera de rango
        error = validar_entrada(10, 5, 1.5)
        self.log_resultado(
            "Validación factor de potencia alto",
            "El factor de potencia debe estar entre -1 y 1",
            error,
            "PASS" if error == "El factor de potencia debe estar entre -1 y 1" else "FAIL"
        )
        
        # Test 4: Valores válidos
        error = validar_entrada(10, 5, 0.8)
        self.log_resultado(
            "Validación valores correctos",
            None,
            error,
            "PASS" if error is None else "FAIL"
        )
    
    def test_calculos_dc(self):
        """Prueba los cálculos de corriente continua"""
        print("🔍 Probando cálculos DC...")
        
        # Valores de prueba
        voltaje = 12.0
        corriente = 2.0
        
        # Cálculos esperados
        resistencia_esperada = voltaje / corriente  # 6.0 Ω
        potencia_esperada = voltaje * corriente     # 24.0 W
        
        # Ejecutar función
        try:
            resistencia, potencia = calcular_dc(voltaje, corriente)
            
            self.log_resultado(
                "Cálculo resistencia DC",
                resistencia_esperada,
                resistencia,
                "PASS" if self.comparar_float(resistencia, resistencia_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Cálculo potencia DC",
                potencia_esperada,
                potencia,
                "PASS" if self.comparar_float(potencia, potencia_esperada) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función calcular_dc",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_calculos_ac(self):
        """Prueba los cálculos de corriente alterna"""
        print("🔍 Probando cálculos AC...")
        
        # Valores de prueba
        voltaje = 220.0
        corriente = 10.0
        coseno_fi = 0.8
        
        # Cálculos esperados
        potencia_activa_esperada = voltaje * corriente * coseno_fi  # 1760 W
        angulo_fi = math.acos(coseno_fi)
        potencia_reactiva_esperada = voltaje * corriente * math.sin(angulo_fi)  # 1320 VAR
        potencia_aparente_esperada = voltaje * corriente  # 2200 VA
        
        # Ejecutar función
        try:
            potencia_activa, potencia_reactiva, potencia_aparente = calcular_potencias(
                voltaje, corriente, coseno_fi
            )
            
            self.log_resultado(
                "Cálculo potencia activa AC",
                potencia_activa_esperada,
                potencia_activa,
                "PASS" if self.comparar_float(potencia_activa, potencia_activa_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Cálculo potencia reactiva AC",
                potencia_reactiva_esperada,
                potencia_reactiva,
                "PASS" if self.comparar_float(potencia_reactiva, potencia_reactiva_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Cálculo potencia aparente AC",
                potencia_aparente_esperada,
                potencia_aparente,
                "PASS" if self.comparar_float(potencia_aparente, potencia_aparente_esperada) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función calcular_potencias",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_impedancias_ac(self):
        """Prueba los cálculos de impedancias"""
        print("🔍 Probando cálculos de impedancias AC...")
        
        # Valores de prueba
        voltaje = 220.0
        corriente = 10.0
        coseno_fi = 0.8
        
        # Cálculos esperados
        impedancia_esperada = voltaje / corriente  # 22 Ω
        resistencia_esperada = impedancia_esperada * coseno_fi  # 17.6 Ω
        angulo_fi = math.acos(coseno_fi)
        reactancia_esperada = impedancia_esperada * math.sin(angulo_fi)  # 13.2 Ω
        
        # Ejecutar función
        try:
            impedancia, resistencia, reactancia = calcular_impedancias(
                voltaje, corriente, coseno_fi
            )
            
            self.log_resultado(
                "Cálculo impedancia AC",
                impedancia_esperada,
                impedancia,
                "PASS" if self.comparar_float(impedancia, impedancia_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Cálculo resistencia AC",
                resistencia_esperada,
                resistencia,
                "PASS" if self.comparar_float(resistencia, resistencia_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Cálculo reactancia AC",
                reactancia_esperada,
                reactancia,
                "PASS" if self.comparar_float(reactancia, reactancia_esperada) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función calcular_impedancias",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_sistema_trifasico_estrella(self):
        """Prueba los cálculos del sistema trifásico en estrella"""
        print("🔍 Probando sistema trifásico estrella...")
        
        # Valores de prueba
        vl = 380.0  # Voltaje de línea
        il = 10.0   # Corriente de línea
        coseno_fi = 0.85
        
        # Cálculos esperados para estrella
        vf_esperado = vl / math.sqrt(3)  # 219.39 V
        if_esperado = il  # 10.0 A
        p_total_esperado = math.sqrt(3) * vl * il * coseno_fi  # 5594.23 W
        
        # Ejecutar función
        try:
            resultados = calcular_sistema_trifasico_estrella(vl, il, coseno_fi)
            
            self.log_resultado(
                "Voltaje de fase - Estrella",
                vf_esperado,
                resultados['voltaje_fase'],
                "PASS" if self.comparar_float(resultados['voltaje_fase'], vf_esperado) else "FAIL"
            )
            
            self.log_resultado(
                "Corriente de fase - Estrella",
                if_esperado,
                resultados['corriente_fase'],
                "PASS" if self.comparar_float(resultados['corriente_fase'], if_esperado) else "FAIL"
            )
            
            self.log_resultado(
                "Potencia activa total - Estrella",
                p_total_esperado,
                resultados['potencia_activa_total'],
                "PASS" if self.comparar_float(resultados['potencia_activa_total'], p_total_esperado) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función sistema trifásico estrella",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_sistema_trifasico_delta(self):
        """Prueba los cálculos del sistema trifásico en delta"""
        print("🔍 Probando sistema trifásico delta...")
        
        # Valores de prueba
        vl = 380.0  # Voltaje de línea
        il = 10.0   # Corriente de línea
        coseno_fi = 0.85
        
        # Cálculos esperados para delta
        vf_esperado = vl  # 380.0 V
        if_esperado = il / math.sqrt(3)  # 5.77 A
        p_total_esperado = math.sqrt(3) * vl * il * coseno_fi  # 5594.23 W
        
        # Ejecutar función
        try:
            resultados = calcular_sistema_trifasico_delta(vl, il, coseno_fi)
            
            self.log_resultado(
                "Voltaje de fase - Delta",
                vf_esperado,
                resultados['voltaje_fase'],
                "PASS" if self.comparar_float(resultados['voltaje_fase'], vf_esperado) else "FAIL"
            )
            
            self.log_resultado(
                "Corriente de fase - Delta",
                if_esperado,
                resultados['corriente_fase'],
                "PASS" if self.comparar_float(resultados['corriente_fase'], if_esperado) else "FAIL"
            )
            
            self.log_resultado(
                "Potencia activa total - Delta",
                p_total_esperado,
                resultados['potencia_activa_total'],
                "PASS" if self.comparar_float(resultados['potencia_activa_total'], p_total_esperado) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función sistema trifásico delta",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_desequilibrio_corrientes(self):
        """Prueba el análisis de desequilibrio de corrientes"""
        print("🔍 Probando análisis de desequilibrio...")
        
        # Caso 1: Sistema balanceado
        ir1, is1, it1 = 10.0, 10.0, 10.0
        try:
            resultado1 = calcular_desequilibrio_corrientes(ir1, is1, it1)
            
            self.log_resultado(
                "Desequilibrio sistema balanceado",
                0.0,
                resultado1['desequilibrio_porcentaje'],
                "PASS" if self.comparar_float(resultado1['desequilibrio_porcentaje'], 0.0) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función desequilibrio (balanceado)",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
        
        # Caso 2: Sistema desbalanceado
        ir2, is2, it2 = 10.0, 8.0, 12.0
        promedio_esperado = (ir2 + is2 + it2) / 3  # 10.0 A
        max_desviacion = max(abs(ir2 - promedio_esperado), 
                           abs(is2 - promedio_esperado), 
                           abs(it2 - promedio_esperado))  # 2.0 A
        desequilibrio_esperado = (max_desviacion / promedio_esperado) * 100  # 20.0%
        
        try:
            resultado2 = calcular_desequilibrio_corrientes(ir2, is2, it2)
            
            self.log_resultado(
                "Desequilibrio sistema desbalanceado",
                desequilibrio_esperado,
                resultado2['desequilibrio_porcentaje'],
                "PASS" if self.comparar_float(resultado2['desequilibrio_porcentaje'], desequilibrio_esperado) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función desequilibrio (desbalanceado)",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_eficiencia_energetica(self):
        """Prueba el análisis de eficiencia energética"""
        print("🔍 Probando análisis de eficiencia energética...")
        
        # Caso 1: Eficiencia excelente
        p_activa = 1000.0
        p_aparente = 1053.0  # Factor de potencia ≈ 0.95
        fp = 0.95
        
        try:
            resultado = analizar_eficiencia_energetica(p_activa, p_aparente, fp)
            
            self.log_resultado(
                "Categoría eficiencia excelente",
                "Excelente",
                resultado['categoria'],
                "PASS" if resultado['categoria'] == "Excelente" else "FAIL"
            )
            
            eficiencia_esperada = fp * 100  # 95%
            self.log_resultado(
                "Eficiencia factor de potencia",
                eficiencia_esperada,
                resultado['eficiencia_fp'],
                "PASS" if self.comparar_float(resultado['eficiencia_fp'], eficiencia_esperada) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función eficiencia energética",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_calidad_energia(self):
        """Prueba el análisis de calidad de energía"""
        print("🔍 Probando análisis de calidad de energía...")
        
        # Caso de prueba
        desequilibrio = 1.5  # Aceptable
        fp = 0.92  # Bueno
        p_aparente = 1000.0
        
        try:
            resultado = analizar_calidad_energia(desequilibrio, fp, p_aparente)
            
            # La puntuación debería estar cerca de 100 (sin penalizaciones importantes)
            self.log_resultado(
                "Puntuación calidad energía",
                ">= 85",
                resultado['puntuacion'],
                "PASS" if resultado['puntuacion'] >= 85 else "FAIL",
                f"Puntuación obtenida: {resultado['puntuacion']}"
            )
            
            self.log_resultado(
                "Análisis calidad - estructura",
                "dict con claves requeridas",
                str(type(resultado)),
                "PASS" if all(key in resultado for key in ['puntuacion', 'problemas', 'perdidas_kw', 'costo_anual']) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función calidad energía",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_capacitor_dc(self):
        """Prueba los cálculos del capacitor en DC"""
        print("🔍 Probando cálculos capacitor DC...")
        
        voltaje = 12.0
        capacitancia = 0.001  # 1000 µF
        
        # Cálculos esperados
        carga_esperada = capacitancia * voltaje  # 0.012 C
        energia_esperada = 0.5 * capacitancia * (voltaje ** 2)  # 0.072 J
        
        try:
            carga, energia = calcular_capacitor_dc(voltaje, capacitancia)
            
            self.log_resultado(
                "Carga capacitor DC",
                carga_esperada,
                carga,
                "PASS" if self.comparar_float(carga, carga_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Energía capacitor DC",
                energia_esperada,
                energia,
                "PASS" if self.comparar_float(energia, energia_esperada) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función capacitor DC",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_capacitor_ac(self):
        """Prueba los cálculos del capacitor en AC"""
        print("🔍 Probando cálculos capacitor AC...")
        
        voltaje = 220.0
        frecuencia = 60.0
        capacitancia = 0.00001  # 10 µF
        
        # Cálculos esperados
        reactancia_esperada = 1 / (2 * math.pi * frecuencia * capacitancia)  # 265.26 Ω
        corriente_esperada = voltaje / reactancia_esperada  # 0.829 A
        potencia_reactiva_esperada = voltaje * corriente_esperada  # 182.41 VAR
        
        try:
            reactancia, corriente, potencia_reactiva = calcular_capacitor_ac(voltaje, frecuencia, capacitancia)
            
            self.log_resultado(
                "Reactancia capacitiva AC",
                reactancia_esperada,
                reactancia,
                "PASS" if self.comparar_float(reactancia, reactancia_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Corriente capacitor AC",
                corriente_esperada,
                corriente,
                "PASS" if self.comparar_float(corriente, corriente_esperada) else "FAIL"
            )
            
            self.log_resultado(
                "Potencia reactiva capacitor AC",
                potencia_reactiva_esperada,
                potencia_reactiva,
                "PASS" if self.comparar_float(potencia_reactiva, potencia_reactiva_esperada) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función capacitor AC",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_consumo(self):
        """Prueba el cálculo de consumo"""
        print("🔍 Probando cálculo de consumo...")
        
        potencia = 1500.0  # 1.5 kW
        horas = 8.0
        
        consumo_esperado = potencia * horas / 1000  # 12.0 kWh
        
        try:
            consumo = calcular_consumo(potencia, horas)
            
            self.log_resultado(
                "Cálculo consumo kWh",
                consumo_esperado,
                consumo,
                "PASS" if self.comparar_float(consumo, consumo_esperado) else "FAIL"
            )
            
        except Exception as e:
            self.log_resultado(
                "Función calcular consumo",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def test_casos_limite(self):
        """Prueba casos límite y valores extremos"""
        print("🔍 Probando casos límite...")
        
        # Caso 1: Valores muy pequeños
        try:
            resultado = calcular_dc(0.001, 0.001)
            self.log_resultado(
                "Valores muy pequeños DC",
                "Sin errores",
                "OK",
                "PASS"
            )
        except Exception as e:
            self.log_resultado(
                "Valores muy pequeños DC",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
        
        # Caso 2: Valores muy grandes
        try:
            resultado = calcular_dc(10000, 1000)
            self.log_resultado(
                "Valores muy grandes DC",
                "Sin errores",
                "OK",
                "PASS"
            )
        except Exception as e:
            self.log_resultado(
                "Valores muy grandes DC",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
        
        # Caso 3: Factor de potencia = 1 (resistivo puro)
        try:
            resultado = calcular_potencias(220, 10, 1.0)
            self.log_resultado(
                "Factor potencia = 1",
                "Sin errores",
                "OK",
                "PASS"
            )
        except Exception as e:
            self.log_resultado(
                "Factor potencia = 1",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
        
        # Caso 4: Factor de potencia = 0 (reactivo puro)
        try:
            resultado = calcular_potencias(220, 10, 0.0)
            self.log_resultado(
                "Factor potencia = 0",
                "Sin errores",
                "OK",
                "PASS"
            )
        except Exception as e:
            self.log_resultado(
                "Factor potencia = 0",
                "Sin errores",
                f"Error: {str(e)}",
                "FAIL"
            )
    
    def ejecutar_todas_las_pruebas(self):
        """Ejecuta todas las pruebas"""
        print("🚀 Iniciando pruebas exhaustivas de la Calculadora de Ley de Ohm")
        print("=" * 70)
        
        # Ejecutar todas las pruebas
        self.test_validaciones_entrada()
        self.test_calculos_dc()
        self.test_calculos_ac()
        self.test_impedancias_ac()
        self.test_sistema_trifasico_estrella()
        self.test_sistema_trifasico_delta()
        self.test_desequilibrio_corrientes()
        self.test_eficiencia_energetica()
        self.test_calidad_energia()
        self.test_capacitor_dc()
        self.test_capacitor_ac()
        self.test_consumo()
        self.test_casos_limite()
        
        print("\n✅ Todas las pruebas completadas")
        return self.generar_informe()
    
    def generar_informe(self):
        """Genera un informe completo en formato Markdown"""
        
        total_pruebas = len(self.resultados_pruebas)
        pruebas_exitosas = len([r for r in self.resultados_pruebas if r['status'] == 'PASS'])
        pruebas_fallidas = len([r for r in self.resultados_pruebas if r['status'] == 'FAIL'])
        warnings = len([r for r in self.resultados_pruebas if r['status'] == 'WARNING'])
        
        porcentaje_exito = (pruebas_exitosas / total_pruebas) * 100 if total_pruebas > 0 else 0
        
        informe = f"""# 📊 Informe de Pruebas - Calculadora de Ley de Ohm

## 📈 Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| **Total de Pruebas** | {total_pruebas} |
| **Pruebas Exitosas** | {pruebas_exitosas} |
| **Pruebas Fallidas** | {pruebas_fallidas} |
| **Advertencias** | {warnings} |
| **Porcentaje de Éxito** | {porcentaje_exito:.1f}% |
| **Fecha de Ejecución** | {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} |

## 🎯 Estado General

"""
        
        if porcentaje_exito >= 95:
            informe += "✅ **EXCELENTE**: La aplicación funciona correctamente sin problemas significativos.\n\n"
        elif porcentaje_exito >= 80:
            informe += "🟡 **BUENO**: La aplicación funciona bien con algunos problemas menores.\n\n"
        elif porcentaje_exito >= 60:
            informe += "🟠 **REGULAR**: La aplicación tiene problemas que requieren atención.\n\n"
        else:
            informe += "🔴 **CRÍTICO**: La aplicación tiene problemas serios que deben ser corregidos.\n\n"
        
        # Sección de errores críticos
        if self.errores_encontrados:
            informe += "## 🚨 Errores Críticos Encontrados\n\n"
            for error in self.errores_encontrados:
                informe += f"### ❌ {error['prueba']}\n"
                informe += f"- **Esperado**: {error['esperado']}\n"
                informe += f"- **Obtenido**: {error['obtenido']}\n"
                if error['mensaje']:
                    informe += f"- **Mensaje**: {error['mensaje']}\n"
                informe += f"- **Timestamp**: {error['timestamp']}\n\n"
        
        # Sección de advertencias
        if self.warnings:
            informe += "## ⚠️ Advertencias\n\n"
            for warning in self.warnings:
                informe += f"### 🟡 {warning['prueba']}\n"
                informe += f"- **Esperado**: {warning['esperado']}\n"
                informe += f"- **Obtenido**: {warning['obtenido']}\n"
                if warning['mensaje']:
                    informe += f"- **Mensaje**: {warning['mensaje']}\n"
                informe += f"- **Timestamp**: {warning['timestamp']}\n\n"
        
        # Resultados detallados por categoría
        categorias = {
            'Validaciones': [r for r in self.resultados_pruebas if 'validación' in r['prueba'].lower() or 'validacion' in r['prueba'].lower()],
            'Cálculos DC': [r for r in self.resultados_pruebas if 'dc' in r['prueba'].lower()],
            'Cálculos AC': [r for r in self.resultados_pruebas if 'ac' in r['prueba'].lower() and 'trifasico' not in r['prueba'].lower()],
            'Sistema Trifásico': [r for r in self.resultados_pruebas if 'trifasico' in r['prueba'].lower() or 'estrella' in r['prueba'].lower() or 'delta' in r['prueba'].lower()],
            'Análisis Avanzados': [r for r in self.resultados_pruebas if any(x in r['prueba'].lower() for x in ['desequilibrio', 'eficiencia', 'calidad'])],
            'Capacitores': [r for r in self.resultados_pruebas if 'capacitor' in r['prueba'].lower()],
            'Otros': [r for r in self.resultados_pruebas if not any(cat in r['prueba'].lower() for cat in ['validacion', 'dc', 'ac', 'trifasico', 'estrella', 'delta', 'desequilibrio', 'eficiencia', 'calidad', 'capacitor'])]
        }
        
        for categoria, pruebas in categorias.items():
            if pruebas:
                informe += f"## 📋 {categoria}\n\n"
                informe += "| Prueba | Estado | Esperado | Obtenido | Mensaje |\n"
                informe += "|--------|--------|----------|----------|----------|\n"
                
                for prueba in pruebas:
                    estado_emoji = {"PASS": "✅", "FAIL": "❌", "WARNING": "⚠️"}.get(prueba['status'], "❓")
                    esperado_str = str(prueba['esperado'])[:50] + "..." if len(str(prueba['esperado'])) > 50 else str(prueba['esperado'])
                    obtenido_str = str(prueba['obtenido'])[:50] + "..." if len(str(prueba['obtenido'])) > 50 else str(prueba['obtenido'])
                    mensaje_str = prueba['mensaje'][:30] + "..." if len(prueba['mensaje']) > 30 else prueba['mensaje']
                    
                    informe += f"| {prueba['prueba']} | {estado_emoji} {prueba['status']} | {esperado_str} | {obtenido_str} | {mensaje_str} |\n"
                
                informe += "\n"
        
        # Recomendaciones
        informe += "## 💡 Recomendaciones\n\n"
        
        if pruebas_fallidas == 0:
            informe += "✅ **Excelente trabajo**: Todas las pruebas han pasado exitosamente.\n\n"
        else:
            informe += f"🔧 **Acciones requeridas**: Se encontraron {pruebas_fallidas} pruebas fallidas que requieren atención.\n\n"
            
            # Recomendaciones específicas basadas en los errores
            errores_validacion = [e for e in self.errores_encontrados if 'validación' in e['prueba'].lower()]
            errores_calculo = [e for e in self.errores_encontrados if any(x in e['prueba'].lower() for x in ['cálculo', 'calculo'])]
            errores_funcion = [e for e in self.errores_encontrados if 'función' in e['prueba'].lower()]
            
            if errores_validacion:
                informe += "- **Validaciones**: Revisar las funciones de validación de entrada.\n"
            if errores_calculo:
                informe += "- **Cálculos**: Verificar las fórmulas matemáticas implementadas.\n"
            if errores_funcion:
                informe += "- **Funciones**: Revisar la implementación de las funciones que están fallando.\n"
        
        if warnings > 0:
            informe += f"⚠️ **Atención**: Se encontraron {warnings} advertencias que podrían requerir revisión.\n\n"
        
        # Estadísticas de rendimiento
        informe += "## 📊 Estadísticas Detalladas\n\n"
        informe += f"- **Tiempo de ejecución**: {datetime.now().strftime('%H:%M:%S')}\n"
        informe += f"- **Plataforma**: {sys.platform}\n"
        informe += f"- **Versión Python**: {sys.version.split()[0]}\n"
        informe += f"- **Directorio de trabajo**: {os.getcwd()}\n\n"
        
        # Próximos pasos
        informe += "## 🚀 Próximos Pasos\n\n"
        if pruebas_fallidas > 0:
            informe += "1. **Prioritario**: Corregir las pruebas fallidas identificadas\n"
            informe += "2. **Medio**: Revisar las advertencias y mejorar donde sea necesario\n"
            informe += "3. **Opcional**: Agregar más pruebas para casos de uso específicos\n\n"
        else:
            informe += "1. **Opcional**: Agregar pruebas adicionales para casos extremos\n"
            informe += "2. **Mejora continua**: Implementar pruebas de rendimiento\n"
            informe += "3. **Documentación**: Actualizar la documentación basada en los resultados\n\n"
        
        # Footer
        informe += "---\n"
        informe += f"*Informe generado automáticamente el {datetime.now().strftime('%Y-%m-%d a las %H:%M:%S')}*\n"
        
        return informe

def main():
    """Función principal para ejecutar las pruebas"""
    
    print("🔧 Inicializando entorno de pruebas...")
    
    # Verificar que los archivos necesarios existen
    archivos_requeridos = ['ohm.py', 'ohm_mejorado.py']
    archivos_encontrados = []
    
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            archivos_encontrados.append(archivo)
    
    if not archivos_encontrados:
        print("❌ Error: No se encontraron los archivos de la aplicación")
        return
    
    print(f"✅ Archivos encontrados: {', '.join(archivos_encontrados)}")
    
    # Crear instancia de pruebas
    tester = TestCalculadoraOhm()
    
    try:
        # Ejecutar todas las pruebas
        informe = tester.ejecutar_todas_las_pruebas()
        
        # Guardar el informe
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"informe_pruebas_{timestamp}.md"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(informe)
        
        print(f"\n📄 Informe guardado en: {nombre_archivo}")
        print("\n" + "="*70)
        print("📊 RESUMEN DEL INFORME:")
        print("="*70)
        
        # Mostrar resumen en consola
        total = len(tester.resultados_pruebas)
        exitosas = len([r for r in tester.resultados_pruebas if r['status'] == 'PASS'])
        fallidas = len([r for r in tester.resultados_pruebas if r['status'] == 'FAIL'])
        
        print(f"Total de pruebas: {total}")
        print(f"Exitosas: {exitosas}")
        print(f"Fallidas: {fallidas}")
        print(f"Porcentaje de éxito: {(exitosas/total)*100:.1f}%")
        
        if fallidas == 0:
            print("\n🎉 ¡TODAS LAS PRUEBAS PASARON! La aplicación está funcionando correctamente.")
        else:
            print(f"\n⚠️  Se encontraron {fallidas} problemas que requieren atención.")
            print("📋 Revisa el informe completo para más detalles.")
        
        return nombre_archivo
        
    except Exception as e:
        print(f"❌ Error durante la ejecución de pruebas: {str(e)}")
        print(f"📍 Traceback completo:\n{traceback.format_exc()}")
        return None

if __name__ == "__main__":
    archivo_informe = main()
    if archivo_informe:
        print(f"\n📖 Para ver el informe completo, abre: {archivo_informe}")
