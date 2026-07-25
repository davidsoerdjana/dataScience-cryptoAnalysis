import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import RandomForestRegressor

# 1. Ambil data Historis untuk Training
df = yf.download('BTC-USD', period='2y', interval='1d')
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# --- AMBIL HARGA LIVE & WAKTU BALI (WITA) ---
tz_bali = timezone(timedelta(hours=8))
waktu_sekarang = datetime.now(tz_bali)

# Ambil harga real-time detik ini
ticker = yf.Ticker("BTC-USD")
harga_live = ticker.fast_info['last_price']

# 2. Feature Engineering
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

# Hitung langkah harga dari HARGA LIVE menuju PREDIKSI BESOK
selisih_total = prediksi_besok - harga_live
step = selisih_total / 4

prediksi_siang = harga_live + (step * 1)
prediksi_sore  = harga_live + (step * 2)
prediksi_malam = harga_live + (step * 3)

# Logika Waktu Penutupan (Jam 8 Pagi WITA)
if waktu_sekarang.hour < 8:
    tgl_tutup = waktu_sekarang - timedelta(days=1)
else:
    tgl_tutup = waktu_sekarang
waktu_penutupan = tgl_tutup.replace(hour=8, minute=0, second=0, microsecond=0)

# Tanggal Besok
tgl_besok = waktu_sekarang + timedelta(days=1)

print("=" * 60)
print(f"PREDIKSI HARGA BITCOIN (WAKTU BALI) ")
print("=" * 60)
print(f"Waktu Pengecekan Sekarang : {waktu_sekarang.strftime('%A, %d %B %Y | %H:%M:%S')} WITA")
print(f"Harga BTC Saat Ini (Live) : ${harga_live:,.2f}")
print("-" * 60)
print(f"Harga Penutupan Terakhir  : ${last_close:,.2f}")
print(f"Waktu Penutupan Terakhir  : {waktu_penutupan.strftime('%A, %d %B %Y | 08:00')} WITA")
print("-" * 60)

print(f"ESTIMASI PERGERAKAN HARI INI ({waktu_sekarang.strftime('%d %B')}):")
print(f"1. SIANG (12:00 WITA)     : ${prediksi_siang:,.2f}")
print(f"2. SORE  (17:00 WITA)     : ${prediksi_sore:,.2f}")
print(f"3. MALAM (21:00 WITA)     : ${prediksi_malam:,.2f}")
print("-" * 60)

print(f"PREDIKSI HARGA (BESOK):")
print(f"TANGGAL: {tgl_besok.strftime('%A, %d %B %Y')}")
print(f"WAKTU  : Tepat Jam 08:00 WITA (Penutupan Pasar Resmi)")
print(f"HARGA  : ${prediksi_besok:,.2f}")
print("-" * 60)

# Indikator Tren
status = "BULLISH (NAIK)" if selisih_total > 0 else "BEARISH (TURUN)"
print(f"KESIMPULAN TREN           : {status}")
print(f"Machine Learning Model    : Linear Interpolation")
print(f"Learned & Developed by    : David Soerdjana")
print("=" * 60)