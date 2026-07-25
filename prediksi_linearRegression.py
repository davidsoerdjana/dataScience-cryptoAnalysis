from datetime import timedelta
import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 1. Ambil data & Rapikan kolom (Antisipasi Multi-index)
df = yf.download('BTC-USD', period='5y', interval='1d')
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# 2. Persiapan Data (Seperti sebelumnya)
df['Prediction'] = df['Close'].shift(-1)
X = df[['Close']][:-1].values
y = df['Prediction'][:-1].values

# 3. Training
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)

# --- BAGIAN DETAIL WAKTU & PREDIKSI ---

# 1. Ambil Waktu dan Harga Terakhir
last_date = df.index[-1] # Mengambil tanggal terakhir di dataset
last_price_val = float(df['Close'].iloc[-1])

# 2. Hitung Tanggal Besok (Untuk label prediksi)
tomorrow_date = last_date + pd.Timedelta(days=1)

# 3. Lakukan Prediksi
last_price_2d = np.array([[last_price_val]])
predicted_price = model.predict(last_price_2d)
hasil_final = predicted_price.flatten()[0]

# 4. Tampilan Hasil yang Rinci (Tanpa Emoji agar tidak Error)
# --- BAGIAN TAMPILAN HASIL DENGAN WAKTU BALI ---

# Konversi Waktu (Yahoo Finance biasanya UTC 00:00, jadi kita tambah 8 jam untuk Bali)
# Kita asumsikan data harian ditutup pada akhir hari UTC
waktu_bali = last_date + timedelta(hours=8) 

print("-" * 40)
print(f"RINGKASAN ANALISIS BITCOIN (WITA)")
print("-" * 40)
print(f"Harga Penutupan Terakhir : ${last_price_val:,.2f}")

# Menampilkan Tanggal dan Jam Penutupan (08:00 WITA)
print(f"Waktu Penutupan (Bali)   : {waktu_bali.strftime('%A, %d %B %Y | %H:%M')} WITA")
print("-" * 40)

print(f"PREDIKSI AI UNTUK BESOK")
print(f"Estimasi Tanggal         : {tomorrow_date.strftime('%A, %d %B %Y')}")
print(f"Prediksi Harga           : ${hasil_final:,.2f}")
print("-" * 40)

# Menghitung selisih
selisih = hasil_final - last_price_val
status = "NAIK" if selisih > 0 else "TURUN"
print(f"Analisis Trend           : Prediksi {status} sekitar ${abs(selisih):,.2f}")
print("-" * 40)