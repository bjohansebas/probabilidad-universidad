# Respuestas a las Preguntas de Cierre — Capítulo 1

Reportes técnicos de los tres laboratorios virtuales. Los valores numéricos
citados provienen de ejecutar los scripts de este repositorio con la semilla
`np.random.seed(2026)`.

---

## Taller 1 — Simulación del Tablero (Sección 1.5)

### 1. Volatilidad Muestral Inicial y Estabilización Frecuentista

#### 1.1 Origen de la discrepancia entre `f₅` y el 25% teórico

La causa es la **resolución aritmética** de la muestra, no un error del método.

Con `n = 5` ensayos, la frecuencia relativa `f₅ = n_A / 5` solo puede tomar
seis valores posibles:

| `n_A` | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `f₅` | 0.00 | 0.20 | 0.40 | 0.60 | 0.80 | 1.00 |

El valor teórico `P(A) = 0.25` **no pertenece a ese conjunto**: es
aritméticamente imposible obtenerlo con 5 ensayos. Los valores alcanzables más
cercanos son 0.20 y 0.40, y la tabla del tablero cayó en 0.40.

El segundo factor es el **peso de cada ensayo sobre el acumulado**. Con `n = 5`,
un solo error adicional desplaza la frecuencia en `1/5 = 20 puntos
porcentuales`. Con `n = 100 000`, ese mismo error la desplaza en `1/100 000 =
0.001 puntos porcentuales`. Como la frecuencia relativa es un promedio corrido
cuyo denominador crece, cada resultado individual va perdiendo influencia y la
curva deja de poder saltar: ese es el mecanismo por el cual la Ley de los
Grandes Números fuerza la convergencia.

> **Nota sobre la tabla manual:** la tabla del Paso 3 usa valores de ruido
> escogidos a mano (+0.2, −0.7, +0.8, +0.6, −0.1) y llega a `f₅ = 0.40`. El
> script con semilla 2026 genera otra secuencia y llega a `f₅ = 0.20`. Ambos
> se alejan del 25% por exactamente la misma razón, lo que refuerza el
> argumento: con 5 ensayos el resultado depende del azar particular de esa
> corrida, no del valor teórico.

#### 1.2 Orden de magnitud en que la curva se adhiere al valor exacto

Midiendo sobre la curva simulada, el ensayo a partir del cual la frecuencia se
mantiene dentro de una banda dada alrededor de 0.25 **de forma definitiva**:

| Banda alrededor de `P(A) = 0.25` | Se cumple desde |
|---|---|
| ±20% (0.200 – 0.300) | `N ≈ 82` |
| ±10% (0.225 – 0.275) | `N ≈ 215` |
| ±5% (0.2375 – 0.2625) | `N ≈ 229` |
| ±2% (0.245 – 0.255) | `N ≈ 7 255` |

**Conclusión:** las oscilaciones bruscas terminan en el orden de `N ~ 10²`
(centenas). La adherencia asintótica visible a la línea teórica se logra en el
orden de `N ~ 10³` (millares), y desde `N ~ 10⁴` la curva es prácticamente
indistinguible de la recta. El valor final fue `f = 0.25031` contra el 0.25
exacto.

### 2. Sensibilidad del Sistema ante Cambios en el Umbral (`V_th = 0.2 V`)

#### 2.1 Nueva probabilidad geométrica

Con `v_N ~ U(−1.0 V, +1.0 V)` y zona de error `A = [0.2, 1.0]`:

```
Ancho de la zona de error : 1.0 − 0.2 = 0.8 V
Ancho del rango total (Ω) : 1.0 − (−1.0) = 2.0 V

P(A) = 0.8 / 2.0 = 0.40  (40%)
```

**Interpretación de ingeniería:** al volver más sensible el comparador, la
probabilidad de error sube de 25% a 40%. Un receptor más sensible no es
automáticamente mejor: acerca el umbral al nivel del ruido y el canal se
degrada. Verificado por simulación: `40.07%` con `N = 100 000`.

#### 2.2 Líneas del código a modificar

En `simulaciones/simulacion_tablero.py`:

| Línea | Actual | Nuevo | Tipo |
|---|---|---|---|
| 20 | `Umbral de Error (A): v_N >= 0.5 V` | `... >= 0.2 V` | docstring |
| 21 | `0.5 / 2.0 = 0.25 (25%)` | `0.8 / 2.0 = 0.40 (40%)` | docstring |
| 26 | `# ... ¿v_N >= 0.5 V?` | `# ... ¿v_N >= 0.2 V?` | comentario |
| **27** | `evento_error = (v_N >= 0.5).astype(int)` | `(v_N >= 0.2)` | **cálculo** |
| 50 | `'¿v_N >= 0.5 V?'` | `'¿v_N >= 0.2 V?'` | encabezado |
| **55** | `cond_str = "SÍ" if ruido[i] >= 0.5 else "No"` | `>= 0.2` | **tabla** |
| 63 | `"Probabilidad Teórica Geométrica: 25.00%"` | `40.00%` | impresión |
| **84** | `y=0.25,` | `y=0.40,` | **gráfica** |
| 88 | `'... $P(A) = 0.25$ (25%)'` | `'... $P(A) = 0.40$ (40%)'` | leyenda |

De todas ellas, la **única que altera el resultado numérico es la línea 27**;
la 55 corrige la tabla impresa y la 84 reubica la línea de referencia en la
gráfica. Las demás son texto: si se omiten, la simulación da bien pero el
reporte queda rotulado con el umbral viejo.

---

## Taller 2 — Laboratorio Virtual 1.1: BER (Sección 1.8)

### 1. Análisis Gráfico y Estabilidad

**Tramo `N = 10 → 100`:** con `p = 0.023` se esperan apenas `100 × 0.023 = 2.3`
errores en todo el tramo. En la corrida, el primer error ocurre en el bit 53:

| `N` | Errores | `f` |
|---|---|---|
| 10 | 0 | 0.00000 |
| 50 | 0 | 0.00000 |
| 53 | 1 | 0.01887 |
| 100 | 1 | 0.01000 |

La curva es una recta plana en cero, salta verticalmente al aparecer el primer
error y desde ahí decae como `1/N` hasta el siguiente. No hay estimación
posible: la gráfica describe la posición del primer error, no la BER del canal.

**Tramo `N = 10 000 → 100 000`:** se acumulan de 224 a 2387 errores y la curva
se confina a la banda `0.0220 – 0.0243`, pegada a la línea teórica.

| `N` | Errores | `f` |
|---|---|---|
| 10 000 | 224 | 0.02240 |
| 50 000 | 1 166 | 0.02332 |
| 100 000 | 2 387 | 0.02387 |

**Punto de estabilización:** la curva entra de forma definitiva en la banda
±10% (0.0207 – 0.0253) a partir de `N ≈ 2 137`, es decir en el orden de
`N ~ 10³`. Para una banda ±5% hace falta `N ~ 10⁴–10⁵`. La regla práctica que
se observa es que la estabilización no depende de `N` en abstracto sino de
haber acumulado suficientes **eventos de error**: con ~100 errores la curva ya
es legible, con ~1000 queda plana.

### 2. Impacto en el Tamaño de la Muestra (`N = 50` bits)

Con 50 bits y `p = 0.023` se esperan `50 × 0.023 = 1.15` errores. La medición
solo puede arrojar los valores:

| Errores observados | BER medida | Probabilidad de ese resultado |
|---|---|---|
| 0 | 0.000 (0%) | **31.2%** |
| 1 | 0.020 (2%) | 36.8% |
| 2 | 0.040 (4%) | 20.7% |

El valor real, 0.023, **no es representable** con 50 bits: la resolución del
experimento es `1/50 = 0.02`, casi tan grande como la magnitud que se quiere
medir.

**Por qué el resultado es engañoso:** casi una de cada tres pruebas reporta
**cero errores**, y el ingeniero concluiría que el enlace es perfecto. Otra
buena parte reporta 4%, casi el doble del valor real.

**Riesgos técnicos que implica:**

- **Certificar un enlace como libre de errores** que en realidad corrompe 23
  bits de cada mil, con el fallo apareciendo ya en producción.
- **Dimensionar mal la codificación FEC**: si se diseña para BER = 0 no se
  incluye redundancia, y el enlace queda sin capacidad de corrección.
- **Sobredimensionar por el lado opuesto**: si la prueba arrojó 4%, se gasta
  ancho de banda y potencia en corregir errores que no existen.
- **No poder reproducir la medición**: repetir la prueba da otro número, y sin
  criterio de tamaño muestral el laboratorio no sabe cuál creer.

Un enlace se caracteriza contando **errores**, no bits. Para estimar
`p = 0.023` con confianza se requieren al menos algunas centenas de errores
acumulados, lo que exige `N` del orden de `10⁴` bits en adelante.

---

## Taller 3 — Laboratorio Virtual 1.2: Multicanal (Sección 1.11)

### 1. Escalabilidad y Explosión Combinatoria (LTE / 5G-NR)

#### 1.1 Nueva cardinalidad del espacio muestral

Con `N = 64` subportadoras, `k = 16` activas y modulación 16-QAM (`M = 16`):

```
Etapa 1 — Selección de subportadoras:
  C(64, 16) = 488 526 937 079 580              ≈ 4.885 × 10¹⁴

Etapa 2 — Asignación de símbolos:
  M^k = 16¹⁶ = 2⁶⁴ = 18 446 744 073 709 551 616 ≈ 1.845 × 10¹⁹

Regla del Producto entre etapas:
  |Ω_real| = C(64,16) · 16¹⁶ ≈ 9.012 × 10³³      (≈ 2¹¹²·⁸)
```

Frente a las 160 tramas del modelo pedagógico, el espacio crece en **32
órdenes de magnitud**.

#### 1.2 Por qué `itertools` colapsa la RAM y Monte Carlo no

El problema no es `itertools` en sí, sino el `list(...)` que lo envuelve en la
Sección 3 del código:

```python
posiciones_posibles = list(itertools.combinations(range(N), k))
simbolos_posibles   = list(itertools.product(estados_binarios, repeat=k))
```

`itertools.combinations` devuelve un **generador perezoso**, pero `list()` lo
**materializa completo en memoria**. Y el doble bucle posterior construye
`espacio_muestral` con los `|Ω|` elementos.

Haciendo la cuenta para el caso real, con una estimación conservadora de 100
bytes por tupla de Python:

| Estructura | Elementos | Memoria requerida |
|---|---|---|
| `posiciones_posibles` | 4.9 × 10¹⁴ | ≈ 49 PB |
| `espacio_muestral` | 9.0 × 10³³ | ≈ 9 × 10³⁵ bytes |

El espacio muestral completo exigiría del orden de **10²⁰ petabytes**, muchos
órdenes de magnitud por encima de toda la capacidad de almacenamiento
fabricada en el planeta. El proceso muere por `MemoryError` mucho antes: ya
solo la primera línea, con sus 49 PB, es irrealizable.

**Por qué Monte Carlo sí funciona:** el método nunca necesita ver Ω completo.
Le basta con dos cosas:

1. **Conocer `|Ω|`**, que se obtiene analíticamente con `math.comb(N, k) * M**k`
   — una multiplicación, sin enumerar nada.
2. **Poder generar una muestra uniforme**, que se construye directamente:
   se sortean `k` subportadoras al azar y `k` símbolos al azar.

El consumo de memoria pasa de `O(|Ω|)` a `O(N_simulaciones)`. Con 100 000
tramas simuladas se ocupan unos pocos megabytes, **independientemente de si
`|Ω|` vale 160 o 10³³**. Esa independencia entre el costo computacional y el
tamaño del espacio muestral es exactamente lo que hace viable el método.

> **Detalle de implementación:** al escalar, la línea
> `np.random.randint(0, total_Omega, ...)` también deja de servir, porque
> `9 × 10³³` desborda el entero de 64 bits de NumPy (máximo `9.22 × 10¹⁸`). En
> el caso real hay que sortear la trama directamente (subportadoras + símbolos)
> en lugar de sortear un índice sobre una lista que ya no existe.

### 2. Sensibilidad al Tamaño Muestral y Periodo Promedio de Ocurrencia

#### 2.1 Por qué los eventos raros exigen `N` mucho mayor

El **periodo promedio de ocurrencia** es `1/p`: el número de ensayos que hay
que esperar, en promedio, entre dos apariciones del evento.

| | Laboratorio 1.1 | Laboratorio 1.2 |
|---|---|---|
| Probabilidad `p` | 0.023 (2.3%) | 0.00625 (0.625%) |
| Periodo promedio `1/p` | 43.5 bits | 160 tramas |
| Primera ocurrencia observada | ensayo 53 | ensayo 213 |
| Aciertos acumulados en `N = 100 000` | 2 387 | 623 |

La clave está en la **última fila**: con el mismo `N = 100 000`, el Laboratorio
1.2 acumula **3.8 veces menos eventos**. Y la calidad del estimador
`f = n_A / N` no depende de `N`, sino de `n_A`, el conteo acumulado de
aciertos, porque es ese conteo el que fija la resolución de la fracción.

El razonamiento paso a paso:

1. Mientras no ocurra el primer acierto, `f = 0` exactamente. En el Lab 1.2 eso
   dura hasta el ensayo 213: los primeros 200 ensayos no aportan información.
2. Cuando llega el primer acierto, `f` salta a `1/213 ≈ 0.0047` y luego decae
   como `1/N` hasta el siguiente acierto, 160 ensayos después en promedio. La
   curva avanza a **dientes de sierra**, y cada diente es un evento.
3. Para que los dientes se vuelvan imperceptibles hace falta que un acierto
   adicional casi no mueva el acumulado, y eso solo pasa cuando `n_A` ya es
   grande.

Comparando el `N` necesario para entrar de forma definitiva en cada banda:

| Banda | Lab 1.1 (`p = 0.023`) | Lab 1.2 (`p = 0.00625`) |
|---|---|---|
| ±20% | `N ≈ 1 352` | `N ≈ 4 400` |
| ±10% | `N ≈ 2 137` | `N ≈ 22 824` |
| ±5% | `N ≈ 84 680` | `N ≈ 66 445` |

**Conclusión práctica:** para igualar los 2 387 aciertos del Laboratorio 1.1,
el Laboratorio 1.2 necesitaría `2 387 × 160 ≈ 368 000` tramas. Estimar un
evento `k` veces más raro cuesta aproximadamente `k` veces más ensayos, y esta
es la razón por la que medir BER muy bajas (10⁻⁹ en fibra óptica, por ejemplo)
exige horas de transmisión continua en laboratorio.

#### 2.2 Por qué es obligatoria la escala logarítmica

Toda la información relevante de la simulación ocurre **repartida en cinco
décadas** de `N` (de 10⁰ a 10⁵), y cada década aporta un fenómeno distinto:

| Década | Qué se observa |
|---|---|
| 10⁰ – 10² | Meseta en cero: aún no ocurre ningún acierto |
| 10² – 10³ | Primer salto y oscilaciones violentas |
| 10³ – 10⁴ | Amortiguamiento progresivo |
| 10⁴ – 10⁵ | Adherencia asintótica al valor de Laplace |

Con un **eje lineal**, la mitad del recorrido de la gráfica (`N = 50 000` a
`100 000`) se dedicaría a una recta plana sin información, mientras que todo el
tramo interesante (`N < 5 000`) quedaría comprimido en el **primer 5% del eje**,
literalmente contra el margen izquierdo. Los cuatro fenómenos de la tabla serían
invisibles.

`plt.xscale('log')` asigna **el mismo ancho a cada década**, de modo que el
tramo de 1 a 10 ocupa tanto espacio horizontal como el de 10 000 a 100 000. Eso
permite ver simultáneamente la volatilidad inicial y la convergencia final en
una sola figura.

Además hay una razón conceptual: la convergencia frecuentista progresa por
**órdenes de magnitud de `N`**, no por incrementos absolutos. Pasar de 100 a
1 000 ensayos mejora la estimación tanto como pasar de 10 000 a 100 000, aunque
el segundo salto sea 100 veces mayor en términos absolutos. La escala
logarítmica es simplemente la escala natural del fenómeno que se está
graficando.
