# Análisis E-commerce — Resumen de Hallazgos

## 1. Dataset
4 tablas relacionadas (integridad referencial por ID):
- `customers.csv` — 500 clientes
- `products.csv` — 150 productos, 6 categorías
- `orders.csv` — 3.000 órdenes (2024–2025)
- `returns.csv` — 251 devoluciones (subconjunto de órdenes completadas)

## 2. Hallazgos de exploración
- **Ingresos totales**: $1.702.106 (solo órdenes completadas; 5.5% de órdenes canceladas).
- **Electrónica domina los ingresos** ($983.668 — 58% del total), a pesar de no ser la categoría más vendida en unidades, por su ticket promedio alto.
- **Estacionalidad marcada**: noviembre y diciembre concentran los picos de venta (~$123K y ~$113K en 2024, patrón similar en 2025), consistente con campañas de fin de año.
- **Tasa de devolución global: 8.85%**. Varía fuerte por categoría:
  - Indumentaria: 15.7% (la más alta — típico de talles/medidas)
  - Electrónica: 8.9%
  - Belleza: 4.5% (la más baja)
- **Medio de pago**: tarjeta de crédito lidera (43.8%), seguida de débito (25%).
- **Concentración de gasto**: los top 5 clientes superan los $12K individuales, sugiriendo una cola larga típica de e-commerce (pocos clientes de alto valor).

## 3. Modelo: predicción de devoluciones
- **Enfoque**: regresión logística (interpretable) para estimar probabilidad de devolución por orden.
- **Resultado**: AUC-ROC = 0.59 — señal débil a nivel de orden individual.
- **Insight clave**: el coeficiente más fuerte es la *categoría del producto* (Indumentaria y Electrónica), no el monto, cantidad ni medio de pago. Esto indica que el riesgo de devolución es un atributo del producto, no del comportamiento de compra.
- **Implicancia de negocio**: priorizar control de calidad y descripciones/guías de talles en Indumentaria tendría más impacto que un modelo de scoring por cliente.

## 4. Limitaciones (honestas)
- Dataset sintético: las relaciones (estacionalidad, tasa de devolución por categoría) fueron inyectadas deliberadamente para fines didácticos, no reflejan un negocio real.
- El AUC bajo es esperable dado que solo la categoría tiene señal real; con más variables de comportamiento (historial de devoluciones previas del cliente, reviews, etc.) un modelo real tendría mejor poder predictivo.

## 5. Próximos pasos sugeridos
- Segmentación RFM (Recencia, Frecuencia, Monto) de clientes.
- Análisis de cohortes por mes de alta.
- Modelo de forecasting de ventas (series de tiempo) usando la serie mensual.
