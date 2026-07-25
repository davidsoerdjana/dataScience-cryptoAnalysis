import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# 1. AMBIL DATA DULU (Bahan Baku)
df = yf.download('BTC-USD', period='6mo', interval='1d')

# FIX: Ratakan kolom jika yfinance menggunakan Multi-Index
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# 2. HITUNG MA20 (Wajib ada sebelum Bollinger Bands)
df['MA20'] = df['Close'].rolling(window=20).mean()

# 3. BARU HITUNG BOLLINGER BANDS (Analisis Volatilitas)
df['STD20'] = df['Close'].rolling(window=20).std()
df['Upper'] = df['MA20'] + (df['STD20'] * 2)
df['Lower'] = df['MA20'] - (df['STD20'] * 2)

# 4. PLOTTING HASIL
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Harga Close', alpha=0.3)
plt.plot(df['Upper'], label='Upper Band (Resistance)', color='red', linestyle='--')
plt.plot(df['Lower'], label='Lower Band (Support)', color='green', linestyle='--')
plt.fill_between(df.index, df['Lower'], df['Upper'], color='gray', alpha=0.1)

plt.title('Bitcoin Bollinger Bands: Mengukur Titik Jenuh Harga')
plt.legend()
plt.show()