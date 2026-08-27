import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

customers = pd.read_csv('customers.csv', parse_dates=['signup_date'])
products = pd.read_csv('products.csv')
orders = pd.read_csv('orders.csv', parse_dates=['order_date'])
returns = pd.read_csv('returns.csv')

completed = orders[orders['order_status']=='Completada'].copy()
completed['is_returned'] = completed['order_id'].isin(returns['order_id']).astype(int)

df = completed.merge(products[['product_id','category','price']], on='product_id')
df['order_month'] = df['order_date'].dt.month

# features
X = pd.get_dummies(df[['category','payment_method','quantity','total_amount','order_month']],
                    columns=['category','payment_method'], drop_first=True)
y = df['is_returned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

scaler = StandardScaler()
num_cols = ['quantity','total_amount','order_month']
X_train_s = X_train.copy(); X_test_s = X_test.copy()
X_train_s[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test_s[num_cols] = scaler.transform(X_test[num_cols])

model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_s, y_train)

y_pred = model.predict(X_test_s)
y_proba = model.predict_proba(X_test_s)[:,1]

print("=== Reporte de clasificación ===")
print(classification_report(y_test, y_pred, digits=3))
print("AUC-ROC:", round(roc_auc_score(y_test, y_proba),3))
print("\nMatriz de confusión:")
print(confusion_matrix(y_test, y_pred))

print("\n=== Coeficientes (impacto en log-odds de devolución) ===")
coefs = pd.Series(model.coef_[0], index=X_train.columns).sort_values(ascending=False)
print(coefs)

print("\n=== Tasa de devolución base (test) ===")
print(round(y_test.mean()*100,2), "%")
