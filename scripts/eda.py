import pandas as pd
pd.set_option('display.width', 120)

customers = pd.read_csv('customers.csv', parse_dates=['signup_date'])
products = pd.read_csv('products.csv')
orders = pd.read_csv('orders.csv', parse_dates=['order_date'])
returns = pd.read_csv('returns.csv', parse_dates=['return_date'])

print("=== NULOS ===")
for name, df in [('customers',customers),('products',products),('orders',orders),('returns',returns)]:
    print(name, df.isnull().sum().sum())

print("\n=== ORDERS: estado ===")
print(orders['order_status'].value_counts())

completed = orders[orders['order_status']=='Completada']

print("\n=== Ingresos totales (completadas) ===")
print(round(completed['total_amount'].sum(),2))

print("\n=== Ingresos por categoría ===")
merged = completed.merge(products, on='product_id')
rev_cat = merged.groupby('category')['total_amount'].sum().sort_values(ascending=False)
print(rev_cat)

print("\n=== Ingresos mensuales ===")
monthly = completed.set_index('order_date').resample('ME')['total_amount'].sum()
print(monthly)

print("\n=== Tasa de devolución global ===")
print(round(len(returns)/len(completed)*100,2), "%")

print("\n=== Tasa de devolución por categoría ===")
ret_merged = returns.merge(orders[['order_id','product_id']], on='order_id').merge(products[['product_id','category']], on='product_id')
ret_by_cat = ret_merged['category'].value_counts()
orders_by_cat = merged['category'].value_counts()
rate_by_cat = (ret_by_cat/orders_by_cat*100).round(2).sort_values(ascending=False)
print(rate_by_cat)

print("\n=== Método de pago ===")
print(orders['payment_method'].value_counts(normalize=True).round(3))

print("\n=== Top 5 clientes por gasto ===")
top_cust = completed.groupby('customer_id')['total_amount'].sum().sort_values(ascending=False).head(5)
print(top_cust)

print("\n=== Distribución de edad de clientes ===")
print(customers['age'].describe())
