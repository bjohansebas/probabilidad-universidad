# -*- coding: utf-8 -*-
"""Laboratorio Virtual 1.2: Validación Monte Carlo del Espacio Muestral en
Transmisión Multicanal.

Capítulo 1, Sección 1.11.
"""

import itertools
import math  # Uso de math.comb para compatibilidad con NumPy 2.x

import matplotlib.pyplot as plt
import numpy as np

# Fijar la semilla para reproducibilidad científica
np.random.seed(2026)

# ---------------------------------------------------------
# 1. PARÁMETROS DEL SISTEMA DE TELECOMUNICACIONES
# ---------------------------------------------------------
N = 6  # Dispositivos/canales totales
k = 3  # Dispositivos/canales a sondear por trama
estados_binarios = [0, 1]  # (M = 2 niveles discretos)
M = len(estados_binarios)

# ---------------------------------------------------------
# 2. CÁLCULO ANALÍTICO FORMAL
# ---------------------------------------------------------
C_sub = math.comb(N, k)  # C(6, 3) = 20
C_simb = M**k  # 2^3 = 8
total_Omega = C_sub * C_simb  # |Omega| = 160
p_teorica = 1.0 / total_Omega  # P(E*) = 1/160 = 0.00625

print("=== CÁLCULOS ANALÍTICOS EXACTOS ===")
print(f"1. Selección de canales C({N}, {k}): {C_sub}")
print(f"2. Combinaciones de estados binarios ({M}^{k}): {C_simb}")
print(f"3. Cardinalidad del espacio muestral |Omega|: {total_Omega}")
print(f"4. Probabilidad teórica de E*: 1/{total_Omega} = {p_teorica:.6f}\n")

# ---------------------------------------------------------
# 3. CONSTRUCCIÓN EXPLÍCITA DEL ESPACIO MUESTRAL (Omega)
# ---------------------------------------------------------
posiciones_posibles = list(itertools.combinations(range(N), k))
simbolos_posibles = list(itertools.product(estados_binarios, repeat=k))

espacio_muestral = []
for pos in posiciones_posibles:
  for sim in simbolos_posibles:
    espacio_muestral.append((pos, sim))

# Definición de la Trama E*: Canales (0, 2, 5) con estados binarios (1, 0, 1)
evento_objetivo = ((0, 2, 5), (1, 0, 1))
indice_objetivo = espacio_muestral.index(evento_objetivo)

# ---------------------------------------------------------
# 4. SIMULACIÓN MONTE CARLO DEL CANAL
# ---------------------------------------------------------
N_simulaciones = 100000

# Muestreo aleatorio uniforme sobre los índices del espacio muestral
muestras_indices = np.random.randint(0, total_Omega, size=N_simulaciones)

# Evaluación de aciertos (frecuencia relativa de transmisión)
aciertos = muestras_indices == indice_objetivo
aciertos_acumulados = np.cumsum(aciertos)
ensayos = np.arange(1, N_simulaciones + 1)
probabilidad_simulada = aciertos_acumulados / ensayos

p_empirica_final = probabilidad_simulada[-1]

print("=== RESULTADOS SIMULACIÓN MONTE CARLO ===")
print(f"Ensayos totales (N): {N_simulaciones}")
print(f"Probabilidad empírica observada: {p_empirica_final:.6f}")
print(
    'Error absoluto respecto a la teoría:'
    f' {abs(p_empirica_final - p_teorica):.6f}'
)

# ---------------------------------------------------------
# 5. GRAFICACIÓN DE CONVERGENCIA FRECUENTISTA
# ---------------------------------------------------------
plt.figure(figsize=(11, 5))
plt.plot(
    ensayos,
    probabilidad_simulada,
    color='#1f77b4',
    lw=1.5,
    label='Probabilidad Empírica (Monte Carlo)',
)
plt.axhline(
    y=p_teorica,
    color='r',
    linestyle='--',
    lw=2,
    label=f'Valor Teórico Laplace (1/{total_Omega} = {p_teorica:.6f})',
)

plt.xscale('log')
plt.title(
    'Convergencia Monte Carlo en Selección de Tramas Multicanal',
    fontsize=12,
    fontweight='bold',
)
plt.xlabel(
    'Número de Tramas Transmitidas ($N$ en escala logarítmica)', fontsize=10
)
plt.ylabel('Probabilidad Estimada $P(E^*)$', fontsize=10)
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend(fontsize=10, loc='upper right')
plt.tight_layout()
plt.show()
