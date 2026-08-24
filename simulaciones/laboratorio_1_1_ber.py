# -*- coding: utf-8 -*-
"""Laboratorio Virtual 1.1: Estimación de BER mediante Monte Carlo.

Capítulo 1, Sección 1.7.
"""

import matplotlib.pyplot as plt
import numpy as np

# Fijar la semilla para garantizar la reproducibilidad científica de los datos
np.random.seed(2026)


def simular_canal_frecuentista(N_max):
  """Simula la transmisión de bits sobre un canal con degradación.

  Probabilidad teórica de error de bit (BER) = 0.023 (2.3%)
  """
  # En este caso no podemos calcular de forma a priori la ber_teorica, solo la
  # sabemos cuando se llega a la convergencia.
  ber_teorica = 0.023

  # Generar N_max ensayos aleatorios uniformes en [0, 1)
  datos_aleatorios = np.random.rand(N_max)

  # Si el número aleatorio es menor a la BER, ocurre un error de bit (1)
  errores = (datos_aleatorios < ber_teorica).astype(int)

  # Calcular la suma acumulada de errores paso a paso
  errores_acumulados = np.cumsum(errores)

  # Calcular la frecuencia relativa para cada paso del experimento
  ensayos = np.arange(1, N_max + 1)
  frecuencias_relativas = errores_acumulados / ensayos

  return ensayos, frecuencias_relativas


# Configuración de la escala de la simulación
N_total = 100000  # Cien mil transmisiones simuladas
ensayos, frecuencias = simular_canal_frecuentista(N_total)

# Generación del gráfico de convergencia estocástica
plt.figure(figsize=(12, 6))
plt.plot(
    ensayos,
    frecuencias,
    label='BER Simulada (Frecuencia Relativa)',
    color='#1f77b4',
    lw=1.5,
)
plt.axhline(
    y=0.023,
    color='r',
    linestyle='--',
    label='BER Teórica Exacta (0.023)',
    lw=2,
)

# Configuración de ejes en escala logarítmica
plt.xscale('log')
plt.xlabel(
    'Número de Bits Transmitidos ($N$ en escala logarítmica)', fontsize=11
)
plt.ylabel('Frecuencia Relativa de Errores', fontsize=11)
plt.title(
    'Convergencia del Enfoque Frecuentista (Simulación Monte Carlo)',
    fontsize=13,
    fontweight='bold',
)
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend(fontsize=10, loc='upper right')

plt.tight_layout()
plt.show()
