import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import RandomForestRegressor
import os

# --- 1. SETUP WAKTU & DATA ---
tz_bali = timezone(timedelta(hours=8))
waktu_sekarang = datetime.now(tz_bali)
waktu_target_besok = (waktu_sekarang + timedelta(days=1)).replace(hour=8, minute=0, second=0)

df = yf.download('BTC-USD', period='2y', interval='1d')
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# --- 2. FEATURE ENGINEERING (INDIKATOR TEKNIKAL) ---

# A. Menghitung RSI
delta = df['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
df['RSI'] = 100 - (100 / (1 + rs))

# B. Menghitung Bollinger Bands (20 Hari)
df['MA20'] = df['Close'].rolling(window=20).mean()
df['BB_Upper'] = df['MA20'] + (df['Close'].rolling(window=20).std() * 2)
df['BB_Lower'] = df['MA20'] - (df['Close'].rolling(window=20).std() * 2)

# C. Target Prediksi
df['Prediction'] = df['Close'].shift(-1)
df_clean = df.dropna()

# --- 3. TRAINING DENGAN FITUR BARU ---
# Kita masukkan Close, MA20, RSI, dan Bollinger Bands sebagai input
features = ['Close', 'MA20', 'RSI', 'BB_Upper', 'BB_Lower']
X = df_clean[features]
y = df_clean['Prediction']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# --- 4. PREDIKSI ---
ticker = yf.Ticker("BTC-USD")
harga_live = ticker.fast_info['last_price']

data_terakhir = df[features].tail(1)
prediksi_besok = model.predict(data_terakhir)[0]

# --- 5. OUTPUT RAPI ---
print("=" * 60)
print(f"MACHINE LEARNING DENGAN RSI & BB")
print("=" * 60)
print(f"Harga BTC Live   : ${harga_live:,.2f}")
print(f"RSI Saat Ini     : {df['RSI'].iloc[-1]:.2f}")
print(f"Target Besok     : ${prediksi_besok:,.2f}")
print(f"Waktu Target     : {waktu_target_besok.strftime('%d-%m-%Y | 08:00 WITA')}")
print("-" * 60)

# Simpan Log ke CSV tetap jalan seperti biasa
log_data = {
    'TANGGAL': [waktu_sekarang.strftime('%d-%m-%Y')],
    'HARGA_LIVE': [round(harga_live, 2)],
    'RSI': [round(df['RSI'].iloc[-1], 2)],
    'PREDIKSI': [round(prediksi_besok, 2)]
}
log_df = pd.DataFrame(log_data)
log_df.to_csv('history_prediksi_btc.csv', mode='a', index=False, header=not os.path.exists('history_prediksi_btc.csv'))