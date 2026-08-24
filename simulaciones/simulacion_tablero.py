# -*- coding: utf-8 -*-
"""Simulación Montecarlo del ejercicio de tablero.

Capítulo 1, Sección 1.5: Guía de Clase - Explicación de Monte Carlo en el
Tablero (Paso a Paso).
"""

import matplotlib.pyplot as plt
import numpy as np

# Fijar la semilla para reproducibilidad en la cátedra
np.random.seed(2026)


def simular_monte_carlo_tablero(n_ensayos):
  """Simula el ejercicio del tablero (Paso 3 y 4 de la Guía de Clase).

  Transmisión: Bit 0 (0.0 V)
  Ruido v_N ~ Uniforme(-1.0 V, +1.0 V)
  Umbral de Error (A): v_N >= 0.5 V
  Probabilidad Teórica Geométricamente Calculada: 0.5 / 2.0 = 0.25 (25%)
  """
  # 1. Generar tensión de ruido v_N distribuida Uniforme en [-1.0, +1.0] V
  v_N = np.random.uniform(-1.0, 1.0, size=n_ensayos)

  # 2. Condición de Error (Evento A): ¿v_N >= 0.5 V?
  evento_error = (v_N >= 0.5).astype(int)

  # 3. Suma acumulada de errores (n_A)
  errores_acumulados = np.cumsum(evento_error)

  # 4. Frecuencia relativa ensayo a ensayo (f_i = n_A / i)
  ensayos = np.arange(1, n_ensayos + 1)
  frecuencias_relativas = errores_acumulados / ensayos

  return v_N, evento_error, ensayos, frecuencias_relativas


# ---------------------------------------------------------
# EJECUCIÓN DE LA SIMULACIÓN
# ---------------------------------------------------------
N_total = 100000  # Cien mil ensayos computacionales
ruido, errores, ensayos, frecuencias = simular_monte_carlo_tablero(N_total)

# ---------------------------------------------------------
# IMPRESIÓN DE LOS PRIMEROS 5 ENSAYOS (Coincide con la Tabla Manual)
# ---------------------------------------------------------
print("=== DEMOSTRACIÓN SIMULACIÓN MANUAL DEL TABLERO (Primeros 5 Ensayos) ===")
print(
    f"{'i':<4} | {'v_N (V)':<10} | {'¿v_N >= 0.5 V?':<15} | {'Error (A)':<10}"
    f" | {'n_A':<6} | {'f_i (Monte Carlo)':<18}"
)
print("-" * 75)
for i in range(5):
  cond_str = "SÍ" if ruido[i] >= 0.5 else "No"
  print(
      f"{i+1:<4} | {ruido[i]:^+10.3f} | {cond_str:<15} | {errores[i]:^10} |"
      f" {np.sum(errores[:i+1]):^6} | {frecuencias[i]*100:>6.2f}%"
  )

p_final = frecuencias[-1]
print("-" * 75)
print("Probabilidad Teórica Geométrica: 25.00%")
print(
    f"Probabilidad Estimada Monte Carlo (N = {N_total}): {p_final*100:.2f}%\n"
)

# ---------------------------------------------------------
# GRAFICACIÓN DE LA CONVERGENCIA FRECUENTISTA
# ---------------------------------------------------------
plt.figure(figsize=(11, 5.5))

# Curva de convergencia
plt.plot(
    ensayos,
    frecuencias,
    color='#1f77b4',
    lw=1.5,
    label='Frecuencia Relativa $f_i = n_A / i$ (Monte Carlo)',
)

# Línea del valor teórico geométrico
plt.axhline(
    y=0.25,
    color='#d62728',
    linestyle='--',
    lw=2,
    label='Probabilidad Teórica Exacta $P(A) = 0.25$ (25%)',
)

# Resaltar los primeros 5 ensayos del tablero
plt.scatter(
    ensayos[:5],
    frecuencias[:5],
    color='#2ca02c',
    s=60,
    zorder=5,
    label='Primeros 5 Ensayos (Ejercicio del Tablero)',
)

# Configuración de ejes logarítmicos
plt.xscale('log')
plt.title(
    'Demostración Monte Carlo del Canal con Ruido (Ejercicio de Clase)',
    fontsize=13,
    fontweight='bold',
)
plt.xlabel(
    'Número de Transmisiones Simuladas ($N$ en escala logarítmica)', fontsize=11
)
plt.ylabel('Frecuencia Relativa de Error $P(A)$', fontsize=11)
plt.grid(True, which='both', linestyle='--', alpha=0.6)
plt.legend(fontsize=10, loc='upper right')

plt.tight_layout()
plt.show()
