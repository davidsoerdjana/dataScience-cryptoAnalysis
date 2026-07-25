import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import RandomForestRegressor

# --- 1. SETUP WAKTU BALI (WITA) ---
tz_bali = timezone(timedelta(hours=8))
waktu_sekarang = datetime.now(tz_bali)
hari_ini = waktu_sekarang.strftime('%A, %d %B %Y')
besok = (waktu_sekarang + timedelta(days=1)).strftime('%A, %d %B %Y')

# --- 2. AMBIL DATA & TRAINING ---
ticker_symbol = 'BTC-USD'
df = yf.download(ticker_symbol, period='1y', interval='1d')
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Ambil Harga Live
ticker = yf.Ticker(ticker_symbol)
harga_live = ticker.fast_info['last_price']

# Feature Engineering
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA20'] = df['Close'].rolling(window=20).mean()
df['Prediction'] = df['Close'].shift(-1)
df_model = df.dropna()

X = df_model[['Close', 'MA5', 'MA20']]
y = df_model['Prediction']
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# --- 3. PROSES PREDIKSI ---
data_terakhir = df[['Close', 'MA5', 'MA20']].tail(1)
prediksi_besok = model.predict(data_terakhir)[0]

# --- 4. EXPORT DATA (Buku Catatan Digital) ---
log_data = {
    'Waktu_Cek': [waktu_sekarang.strftime('%Y-%m-%d %H:%M:%S')],
    'Harga_Live': [harga_live],
    'Prediksi_Besok': [prediksi_besok],
    'Trend': ['NAIK' if prediksi_besok > harga_live else 'TURUN']
}
log_df = pd.DataFrame(log_data)
# Menyimpan ke CSV (akan terus bertambah setiap kamu jalankan skripnya)
log_df.to_csv('history_prediksi_btc.csv', mode='a', index=False, header=not pd.io.common.file_exists('history_prediksi_btc.csv'))

# --- 5. VISUALISASI DASHBOARD ---
plt.figure(figsize=(12, 6))
plt.plot(df.index[-30:], df['Close'][-30:], label='Harga Histori (30 Hari Terakhir)', color='blue', marker='o')
plt.axhline(y=prediksi_besok, color='red', linestyle='--', label=f'Prediksi Besok: ${prediksi_besok:,.2f}')
plt.scatter(waktu_sekarang, harga_live, color='green', s=100, label=f'Harga Live Saat Ini: ${harga_live:,.2f}', zorder=5)

plt.title(f'Dashboard Prediksi Bitcoin - {hari_ini}', fontsize=14)
plt.xlabel('Tanggal')
plt.ylabel('Harga (USD)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# --- 6. OUTPUT TERMINAL ---
print("=" * 60)
print(f"DASHBOARD DATA SCIENCE BITCOIN (WITA) ")
print("=" * 60)
print(f"Waktu Pengecekan : {waktu_sekarang.strftime('%d %B %Y | %H:%M:%S')} WITA")
print(f"Harga BTC Live   : ${harga_live:,.2f}")
print(f"Target Besok     : ${prediksi_besok:,.2f} ({besok})")
print("-" * 60)
print(f"STATUS EXPORT    : Berhasil disimpan ke 'history_prediksi_btc.csv'")
print(f"Developed by     : David Soerdjana")
print("=" * 60)