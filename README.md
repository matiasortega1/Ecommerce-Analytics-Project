# 📊 Análisis de E-commerce — Ingresos, Devoluciones y Segmentación de Clientes

Proyecto de análisis de datos end-to-end sobre un dataset sintético de e-commerce: generación de datos, modelado relacional, exploración en SQL, dashboard en Power BI y un modelo predictivo de devoluciones.

> **Nota sobre los datos**: el dataset es **sintético**, generado programáticamente con relaciones realistas (estacionalidad, tasas de devolución por categoría, antigüedad de cliente vs. frecuencia de compra) para fines de práctica y portfolio. No corresponde a un negocio real.

---

## 🎯 Objetivo del proyecto

Responder tres preguntas de negocio típicas de un equipo de BI en e-commerce:

1. ¿Qué categorías de producto generan más ingresos?
2. ¿Qué categorías tienen mayor tasa de devolución?
3. ¿Qué segmento de clientes compra con más frecuencia, y cuánto aporta al ingreso total?

Y complementarlo con un modelo predictivo que estima la probabilidad de devolución de una orden.

---

## 🗂️ Estructura del repositorio

```
ecommerce-analytics-project/
├── data/                    # Datasets fuente en CSV (4 tablas relacionadas)
│   ├── customers.csv        # 500 clientes
│   ├── products.csv         # 150 productos, 6 categorías
│   ├── orders.csv           # 3.000 órdenes (2024–2025)
│   └── returns.csv          # 251 devoluciones
├── database/
│   └── ecommerce.db         # Base SQLite con las 4 tablas + índices
├── sql/
│   └── queries.sql          # Queries comentadas para las 3 preguntas de negocio
├── dax/
│   ├── medidas_dax.txt              # Medidas base (ingresos, devoluciones, segmentos)
│   └── medidas_dax_dashboard.txt    # Medidas adicionales del dashboard (KPIs, ranking, MoM)
├── scripts/
│   ├── generate_data.py     # Generación del dataset sintético (numpy/pandas)
│   ├── eda.py                # Exploración de datos (EDA)
│   └── model.py               # Modelo de regresión logística (predicción de devoluciones)
├── docs/
│   └── resumen_hallazgos.md # Resumen ejecutivo de los hallazgos del EDA y el modelo
├── dashboard/
│   ├── mockup_dashboard.html # Mockup navegable de las 3 páginas del dashboard
│   └── screenshots/          # Capturas reales del dashboard final en Power BI
│       ├── 01_resumen_ejecutivo.png
│       ├── 02_ventas_y_productos.png
│       └── 03_clientes_y_devoluciones.png
└── README.md
```

---

## 🧱 Modelo de datos

Esquema relacional en estrella, con `orders` como tabla de hechos central:

```
customers (1) ───────< orders (*) >─────── (1) products
                          │
                          │ (1:1)
                          ▼
                       returns
```

| Tabla | Filas | Clave primaria | Relación |
|---|---|---|---|
| `customers` | 500 | `customer_id` | 1 cliente → N órdenes |
| `products` | 150 | `product_id` | 1 producto → N órdenes |
| `orders` | 3.000 | `order_id` | tabla de hechos |
| `returns` | 251 | `return_id` | 1 orden → 0 o 1 devolución |

---

## 🛠️ Stack técnico

- **Python** (pandas, numpy, scikit-learn) — generación de datos, EDA, modelado
- **SQL / SQLite** — consultas analíticas y almacenamiento relacional
- **Power BI** — modelado semántico (DAX) y dashboard interactivo
- **DAX** — medidas de negocio (ingresos, tasa de devolución, segmentación RFM simplificada)

---

## 🚀 Cómo reproducir el proyecto

### 1. Generar los datos
```bash
cd scripts
pip install pandas numpy scikit-learn
python generate_data.py
```
Esto regenera los 4 CSV en `data/` con semilla fija (`random seed = 42`), así los resultados son reproducibles.

### 2. Cargar a SQLite
Los datos ya están cargados en `database/ecommerce.db`. Para regenerarlo desde los CSV:
```python
import pandas as pd, sqlite3
conn = sqlite3.connect('database/ecommerce.db')
for t in ['customers','products','orders','returns']:
    pd.read_csv(f'data/{t}.csv').to_sql(t, conn, if_exists='replace', index=False)
```

### 3. Correr las queries
Abrí `sql/queries.sql` en cualquier cliente SQLite (DB Browser for SQLite, DBeaver) apuntando a `database/ecommerce.db`.

### 4. Levantar el dashboard en Power BI
1. Abrí Power BI Desktop → "Obtener datos" → "Texto o CSV" → importá los 4 archivos de `data/`.
2. Armá las relaciones según el esquema de arriba.
3. Pegá las medidas de `dax/medidas_dax.txt` y `dax/medidas_dax_dashboard.txt`.
4. Usá `dashboard/mockup_dashboard.html` (layout) y las capturas en `dashboard/screenshots/` (resultado final) como referencia.

> El archivo `.pbix` no está incluido en este repo. Podés reconstruirlo siguiendo los pasos de arriba, o abrir directamente las capturas para ver el resultado final.

---

## 🖼️ Capturas del Dashboard

### Página 1 — Resumen Ejecutivo
KPIs generales, tendencia mensual de ingresos e ingresos por categoría.

![Resumen Ejecutivo](dashboard/screenshots/01_resumen_ejecutivo.png)

### Página 2 — Ventas y Productos
Top 10 productos por ingresos, método de pago por categoría y estacionalidad de órdenes.

![Ventas y Productos](dashboard/screenshots/02_ventas_y_productos.png)

### Página 3 — Clientes y Devoluciones
Segmentación por frecuencia de compra, tasa de devolución por categoría, motivos de devolución e ingresos por país.

![Clientes y Devoluciones](dashboard/screenshots/03_clientes_y_devoluciones.png)

---

## 📈 Hallazgos clave

| Pregunta | Resultado |
|---|---|
| Categoría con más ingresos | **Electrónica** — $984 mil (58% del total), muy por encima de Hogar ($273 mil) y Deportes ($208 mil) |
| Categoría con más devoluciones | **Indumentaria** — 14,91% de tasa de devolución (casi 2x el promedio general de 8,37%) |
| Segmento más valioso | **Alta frecuencia (5+ órdenes)** — 2.349 de 2.835 órdenes totales, gasto promedio $5.108,47 vs. $603,67 en clientes de baja frecuencia |
| País con mayor ingreso | **Argentina** — $575 mil, seguido de México ($350 mil) y España ($305 mil) |
| Método de pago líder | **Tarjeta de crédito** — $789 mil (46% del total) |
| Motivo de devolución | Repartido entre "No cumple expectativas", "Talle/medida incorrecta" y "Producto defectuoso" como las tres causas principales |

**KPIs generales**: $1.702.106 en ingresos totales, 462 clientes activos, ticket promedio de $600, tasa de devolución global de 8,37%.

> Los valores de esta tabla son los finales, extraídos directamente del dashboard en Power BI (capturas de arriba). Los números preliminares en `docs/resumen_hallazgos.md` provienen del EDA en Python y pueden diferir levemente por redondeo.

Detalle completo, incluyendo el modelo predictivo y sus limitaciones, en [`docs/resumen_hallazgos.md`](docs/resumen_hallazgos.md).

---

## 🤖 Modelo predictivo

Regresión logística para estimar probabilidad de devolución por orden.

- **AUC-ROC**: 0.59
- **Insight principal**: la variable con mayor peso es la *categoría del producto* (Indumentaria, Electrónica), no el comportamiento de compra (monto, cantidad, medio de pago). Esto sugiere que el riesgo de devolución es un atributo del producto, no del cliente — información accionable para priorizar control de calidad por categoría en vez de scoring de clientes.

Código completo en [`scripts/model.py`](scripts/model.py).

---

## ⚠️ Limitaciones

- Dataset sintético: las relaciones (estacionalidad, tasas de devolución) fueron inyectadas deliberadamente para fines didácticos.
- El poder predictivo del modelo (AUC 0.59) es esperable dado que el dataset fue diseñado con señal concentrada en una sola variable categórica.
- No incluye variables de comportamiento histórico del cliente (devoluciones previas, reviews) que en un dataset real mejorarían sustancialmente el modelo.

---

## 📌 Próximos pasos

- [ ] Segmentación RFM completa (Recencia, Frecuencia, Monto)
- [ ] Modelo de forecasting de ventas (series de tiempo)
- [ ] Publicar el dashboard en Power BI Service (actualmente solo capturas locales, no hay link público)

---

## 👤 Autor

Proyecto de práctica de análisis de datos — SQL, Python y Power BI.
