import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import RandomForestRegressor

# 1. Ambil data & Training
df = yf.download('BTC-USD', period='2y', interval='1d')
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Ambil harga real-time saat ini
ticker = yf.Ticker("BTC-USD")
live_data = ticker.history(period="1d")
current_price = live_data['Close'].iloc[-1]

df['Prediction'] = df['Close'].shift(-1)
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()
df.dropna(inplace=True)

X = df[['Close', 'MA5', 'MA20']]
y = df['Prediction']
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X, y)

# --- LOGIKA PREDIKSI ---
last_close = float(df['Close'].iloc[-1])
data_terakhir = df[['Close', 'MA5', 'MA20']].tail(1)
prediksi_besok = model_rf.predict(data_terakhir)[0]

selisih_total = prediksi_besok - last_close
step = selisih_total / 4

prediksi_siang = last_close + (step * 1)
prediksi_sore  = last_close + (step * 2)
prediksi_malam = last_close + (step * 3)

# --- PENGATURAN WAKTU AKURAT (BALI UTC+8) ---
# Memaksa sistem menggunakan zona waktu Bali (UTC+8)
tz_bali = timezone(timedelta(hours=8))
waktu_sekarang = datetime.now(tz_bali)

hari_ini = waktu_sekarang.strftime('%A, %d %B %Y')
besok = (waktu_sekarang + timedelta(days=1)).strftime('%A, %d %B %Y')

# Waktu penutupan pasar harian terakhir (Selalu jam 8 pagi di hari pengecekan)
# Jika sekarang masih di bawah jam 8 pagi, maka penutupan terakhir adalah hari sebelumnya
if waktu_sekarang.hour < 8:
    tgl_tutup = waktu_sekarang - timedelta(days=1)
else:
    tgl_tutup = waktu_sekarang
waktu_penutupan_terakhir = tgl_tutup.replace(hour=8, minute=0, second=0, microsecond=0)

print("=" * 60)
print(f"PREDIKSI HARGA BITCOIN (WAKTU BALI) ")
print("=" * 60)
print(f"Waktu Pengecekan Sekarang : {waktu_sekarang.strftime('%d %B %Y | %H:%M:%S')} WITA")
print(f"Harga Saat Ini            : ${current_price:,.2f} (Live)")
print(f"Harga Penutupan Terakhir  : ${last_close:,.2f}")
print(f"Tanggal Penutupan Terakhir: {waktu_penutupan_terakhir.strftime('%A, %d %B %Y | 08:00')} WITA")
print("-" * 60)

print(f"ESTIMASI PERGERAKAN HARI INI ({hari_ini}):")
print(f"1. SIANG (12:00 WITA)     : ${prediksi_siang:,.2f}")
print(f"2. SORE  (17:00 WITA)     : ${prediksi_sore:,.2f}")
print(f"3. MALAM (21:00 WITA)     : ${prediksi_malam:,.2f}")
print("-" * 60)

print(f"PREDIKSI HARGA (BESOK):")
print(f"TANGGAL: {besok}")
print(f"WAKTU  : Tepat Jam 08:00 WITA (Penutupan Pasar Resmi)")
print(f"HARGA  : ${prediksi_besok:,.2f}")
print("-" * 60)

# Indikator Tren
status = "BULLISH (NAIK)" if selisih_total > 0 else "BEARISH (TURUN)"
print(f"KESIMPULAN TREN           : {status}")
print(f"Machine Learning Model    : Random Forest Regressor")
print(f"Learned & Developed by    : David Soerdjana")
print("=" * 60)