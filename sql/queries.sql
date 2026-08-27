-- ============================================================
-- PREGUNTA 1: ¿Qué categorías generan más ingresos?
-- ============================================================
-- Lógica: solo órdenes "Completada" cuentan como ingreso real
-- (las canceladas no facturan). Sumamos total_amount por categoría.
SELECT
    p.category,
    COUNT(o.order_id)              AS cantidad_ordenes,
    SUM(o.total_amount)            AS ingresos_totales,
    ROUND(AVG(o.total_amount), 2)  AS ticket_promedio
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_status = 'Completada'
GROUP BY p.category
ORDER BY ingresos_totales DESC;


-- ============================================================
-- PREGUNTA 2: ¿Qué categorías tienen más tasa de devolución?
-- ============================================================
-- Lógica: tasa = devoluciones / órdenes completadas de esa categoría.
-- Usamos LEFT JOIN desde orders hacia returns para no perder
-- categorías sin devoluciones, y filtramos solo completadas
-- (una cancelada no puede devolverse).
SELECT
    p.category,
    COUNT(DISTINCT o.order_id)                         AS ordenes_completadas,
    COUNT(DISTINCT r.return_id)                         AS devoluciones,
    ROUND(100.0 * COUNT(DISTINCT r.return_id) / COUNT(DISTINCT o.order_id), 2) AS tasa_devolucion_pct
FROM orders o
JOIN products p ON o.product_id = p.product_id
LEFT JOIN returns r ON o.order_id = r.order_id
WHERE o.order_status = 'Completada'
GROUP BY p.category
ORDER BY tasa_devolucion_pct DESC;


-- ============================================================
-- PREGUNTA 3: ¿Qué segmento de clientes compra más seguido?
-- ============================================================
-- Lógica: no hay columna de "segmento" en el dataset, así que la
-- construimos por FRECUENCIA de compra (enfoque RFM). Clasificamos
-- cada cliente según cantidad de órdenes completadas:
--   Baja:  1 orden
--   Media: 2-4 órdenes
--   Alta:  5+ órdenes
-- y comparamos frecuencia promedio e ingreso por segmento.
WITH compras_por_cliente AS (
    SELECT
        o.customer_id,
        COUNT(o.order_id)      AS cant_ordenes,
        SUM(o.total_amount)    AS gasto_total
    FROM orders o
    WHERE o.order_status = 'Completada'
    GROUP BY o.customer_id
),
segmentado AS (
    SELECT
        *,
        CASE
            WHEN cant_ordenes >= 5 THEN 'Alta frecuencia (5+)'
            WHEN cant_ordenes >= 2 THEN 'Media frecuencia (2-4)'
            ELSE 'Baja frecuencia (1)'
        END AS segmento_frecuencia
    FROM compras_por_cliente
)
SELECT
    segmento_frecuencia,
    COUNT(*)                       AS cantidad_clientes,
    ROUND(AVG(cant_ordenes), 2)    AS ordenes_promedio,
    ROUND(AVG(gasto_total), 2)     AS gasto_promedio,
    SUM(gasto_total)               AS gasto_total_segmento
FROM segmentado
GROUP BY segmento_frecuencia
ORDER BY ordenes_promedio DESC;


-- Bonus: mismo segmento, cruzado por país (para ver si la frecuencia
-- de compra varía geográficamente)
WITH compras_por_cliente AS (
    SELECT
        o.customer_id,
        COUNT(o.order_id) AS cant_ordenes
    FROM orders o
    WHERE o.order_status = 'Completada'
    GROUP BY o.customer_id
)
SELECT
    c.country,
    ROUND(AVG(cpc.cant_ordenes), 2) AS ordenes_promedio_cliente,
    COUNT(*) AS cantidad_clientes
FROM compras_por_cliente cpc
JOIN customers c ON cpc.customer_id = c.customer_id
GROUP BY c.country
ORDER BY ordenes_promedio_cliente DESC;
