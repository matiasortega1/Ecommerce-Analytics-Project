import numpy as np
import pandas as pd
from datetime import datetime, timedelta

rng = np.random.default_rng(42)

# ---------- 1. CUSTOMERS ----------
N_CUST = 500
countries = ['Argentina','México','España','Chile','Colombia','Perú','Uruguay']
country_w = [0.35,0.20,0.15,0.10,0.10,0.06,0.04]
cities = {
    'Argentina': ['Buenos Aires','Córdoba','Rosario','Mendoza'],
    'México': ['CDMX','Guadalajara','Monterrey'],
    'España': ['Madrid','Barcelona','Valencia'],
    'Chile': ['Santiago','Valparaíso'],
    'Colombia': ['Bogotá','Medellín'],
    'Perú': ['Lima','Arequipa'],
    'Uruguay': ['Montevideo'],
}
first_names = ['Juan','María','Carlos','Ana','Luis','Laura','Diego','Sofía','Pedro','Valentina',
               'Martín','Camila','José','Lucía','Andrés','Julieta','Miguel','Florencia','Pablo','Agustina']
last_names = ['González','Rodríguez','Fernández','López','Martínez','Díaz','Pérez','Sánchez','Romero','Torres']

signup_start = datetime(2022,1,1)
signup_end = datetime(2025,12,31)

cust_country = rng.choice(countries, size=N_CUST, p=country_w)
customers = pd.DataFrame({
    'customer_id': range(1, N_CUST+1),
    'first_name': rng.choice(first_names, N_CUST),
    'last_name': rng.choice(last_names, N_CUST),
    'country': cust_country,
    'city': [rng.choice(cities[c]) for c in cust_country],
    'age': rng.integers(18, 70, N_CUST),
    'gender': rng.choice(['F','M','Otro'], N_CUST, p=[0.48,0.48,0.04]),
    'signup_date': [signup_start + timedelta(days=int(d)) for d in rng.integers(0,(signup_end-signup_start).days, N_CUST)],
})
customers['email'] = (customers['first_name'].str.lower() + '.' + customers['last_name'].str.lower()
                       + customers['customer_id'].astype(str) + '@mail.com')
customers = customers[['customer_id','first_name','last_name','email','country','city','age','gender','signup_date']]
customers = customers.sort_values('signup_date').reset_index(drop=True)

# ---------- 2. PRODUCTS ----------
N_PROD = 150
categories = {
    'Electrónica': (80, 1200, 0.09),
    'Indumentaria': (10, 150, 0.15),
    'Hogar': (15, 400, 0.06),
    'Deportes': (20, 300, 0.08),
    'Belleza': (5, 90, 0.05),
    'Juguetería': (8, 120, 0.07),
}
cat_names = list(categories.keys())
cat_probs = [0.22,0.25,0.18,0.15,0.12,0.08]
prod_cat = rng.choice(cat_names, N_PROD, p=cat_probs)

prices, costs, return_rate = [], [], []
for c in prod_cat:
    lo, hi, rr = categories[c]
    price = round(rng.uniform(lo, hi), 2)
    cost = round(price * rng.uniform(0.45, 0.7), 2)
    prices.append(price); costs.append(cost); return_rate.append(rr)

products = pd.DataFrame({
    'product_id': range(1, N_PROD+1),
    'product_name': [f"{c[:4].upper()}-{i:03d}" for i,c in zip(range(1,N_PROD+1), prod_cat)],
    'category': prod_cat,
    'price': prices,
    'cost': costs,
    'stock': rng.integers(0, 500, N_PROD),
    'base_return_rate': return_rate,  # probabilidad "real" subyacente por categoría
})

# ---------- 3. ORDERS ----------
N_ORD = 3000
order_start = datetime(2024,1,1)
order_end = datetime(2025,12,31)
total_days = (order_end-order_start).days

# estacionalidad: más ventas en noviembre (black friday) y diciembre
day_offsets = rng.integers(0, total_days, N_ORD)
order_dates = [order_start + timedelta(days=int(d)) for d in day_offsets]
month_boost = np.array([1.6 if d.month in (11,12) else (0.7 if d.month==2 else 1.0) for d in order_dates])
# resample con boost de temporada
keep_prob = month_boost / month_boost.max()
mask = rng.random(N_ORD) < keep_prob
extra_needed = N_ORD - mask.sum()
# completar si faltan filas por el filtro
while mask.sum() < N_ORD:
    extra = rng.integers(0, total_days, N_ORD)
    extra_dates = [order_start + timedelta(days=int(d)) for d in extra]
    extra_boost = np.array([1.6 if d.month in (11,12) else (0.7 if d.month==2 else 1.0) for d in extra_dates])
    extra_mask = rng.random(N_ORD) < (extra_boost/extra_boost.max())
    need = N_ORD - mask.sum()
    idxs = np.where(extra_mask)[0][:need]
    for i in idxs:
        order_dates.append(extra_dates[i])
    mask = np.concatenate([mask, np.ones(len(idxs), dtype=bool)])

order_dates = [d for d,m in zip(order_dates, mask) if m][:N_ORD]

# clientes más antiguos compran con más frecuencia (peso por antigüedad)
cust_signup_days = (pd.Timestamp('2026-01-01') - customers['signup_date']).dt.days
cust_weight = cust_signup_days / cust_signup_days.sum()
order_customers = rng.choice(customers['customer_id'], N_ORD, p=cust_weight)

order_products = rng.choice(products['product_id'], N_ORD)
prod_lookup = products.set_index('product_id')

quantities = rng.integers(1,5, N_ORD)
unit_prices = prod_lookup.loc[order_products,'price'].values
totals = np.round(quantities * unit_prices, 2)

payment_methods = rng.choice(['Tarjeta de crédito','Tarjeta de débito','Transferencia','Billetera virtual'],
                              N_ORD, p=[0.45,0.25,0.15,0.15])
status = rng.choice(['Completada','Cancelada'], N_ORD, p=[0.94,0.06])

orders = pd.DataFrame({
    'order_id': range(1, N_ORD+1),
    'customer_id': order_customers,
    'product_id': order_products,
    'order_date': order_dates,
    'quantity': quantities,
    'unit_price': unit_prices,
    'total_amount': totals,
    'payment_method': payment_methods,
    'order_status': status,
})
orders = orders.sort_values('order_date').reset_index(drop=True)

# ---------- 4. RETURNS ----------
# probabilidad de devolución = tasa base de la categoría + ruido, solo sobre órdenes completadas
orders_completed = orders[orders['order_status']=='Completada'].copy()
base_rr = prod_lookup.loc[orders_completed['product_id'], 'base_return_rate'].values
return_prob = np.clip(base_rr + rng.normal(0,0.02, len(orders_completed)), 0.01, 0.4)
is_returned = rng.random(len(orders_completed)) < return_prob
returned_orders = orders_completed[is_returned]

reasons = ['Producto defectuoso','No cumple expectativas','Talle/medida incorrecta','Llegó dañado','Cambio de opinión','Producto equivocado enviado']
reason_probs = [0.20,0.20,0.20,0.15,0.15,0.10]

returns = pd.DataFrame({
    'return_id': range(1, len(returned_orders)+1),
    'order_id': returned_orders['order_id'].values,
    'return_date': [d + timedelta(days=int(x)) for d,x in zip(returned_orders['order_date'], rng.integers(1,20,len(returned_orders)))],
    'reason': rng.choice(reasons, len(returned_orders), p=reason_probs),
    'refund_amount': returned_orders['total_amount'].values,
})

# limpiar columna auxiliar antes de exportar products
products_export = products.drop(columns=['base_return_rate'])

customers.to_csv('customers.csv', index=False)
products_export.to_csv('products.csv', index=False)
orders.to_csv('orders.csv', index=False)
returns.to_csv('returns.csv', index=False)

print("customers:", customers.shape)
print("products:", products_export.shape)
print("orders:", orders.shape)
print("returns:", returns.shape)
