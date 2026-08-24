# -*- coding: utf-8 -*-
"""Genera las figuras de las simulaciones sin modificar los scripts.

Ejecuta cada simulación reemplazando `plt.show()` por un guardado en PNG
dentro de la carpeta `figuras/`, de modo que el código de los laboratorios
se mantenga idéntico al del documento.

Uso:
    python herramientas/generar_figuras.py
"""

import pathlib
import runpy

import matplotlib

matplotlib.use('Agg')  # Backend sin ventana, para entornos sin pantalla
import matplotlib.pyplot as plt

RAIZ = pathlib.Path(__file__).resolve().parent.parent
FIGURAS = RAIZ / 'figuras'

SIMULACIONES = [
    'simulacion_tablero.py',
    'laboratorio_1_1_ber.py',
    'laboratorio_1_2_multicanal.py',
]


def main():
  FIGURAS.mkdir(exist_ok=True)
  show_original = plt.show

  for nombre in SIMULACIONES:
    destino = FIGURAS / (pathlib.Path(nombre).stem + '.png')

    # Reemplaza plt.show() por el guardado de la figura activa
    plt.show = lambda *a, **kw: plt.savefig(destino, dpi=150)

    print(f"--- Ejecutando {nombre} ---")
    runpy.run_path(str(RAIZ / 'simulaciones' / nombre), run_name='__main__')
    plt.close('all')
    print(f"Figura guardada en: {destino.relative_to(RAIZ)}\n")

  plt.show = show_original


if __name__ == '__main__':
  main()
