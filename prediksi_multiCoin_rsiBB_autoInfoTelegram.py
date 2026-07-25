import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from sklearn.ensemble import RandomForestRegressor
import requests
import sys
import time
import io

# FIX EMOJI UNTUK TERMINAL WINDOWS
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- 1. KONFIGURASI BOT TELEGRAM ---
TOKEN = "8683171361:AAGv5iJbvX9GHz33sD_rwZx9G6RxSw67sEM"
CHAT_ID = "406895512" # <-- Pastikan ini ID dari @userinfobot kamu

def kirim_telegram(pesan):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": pesan, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Gagal kirim Telegram: {e}")

# --- 2. FUNGSI UTAMA ANALISIS ---
def jalankan_analisis():
    # Daftar Koin Pilihan David
    koin_list = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'LTC-USD'] 
    pesan_final = "🚀 *LAPORAN PREDIKSI KRIPTO (PER JAM 8 PAGI WITA)*\n"
    pesan_final += "==============================\n\n"

    tz_bali = timezone(timedelta(hours=8))
    waktu_sekarang = datetime.now(tz_bali)

    for koin in koin_list:
        try:
            df = yf.download(koin, period='1y', interval='1d', progress=False)
            if df.empty or len(df) < 30: continue
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            
            # Feature Engineering (RSI & MA)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df['MA5'] = df['Close'].rolling(window=5).mean()
            df['Prediction'] = df['Close'].shift(-1)
            
            df_model = df.dropna()
            
            # Training AI
            X = df_model[['Close', 'MA5', 'RSI']]
            y = df_model['Prediction']
            model = RandomForestRegressor(n_estimators=50, random_state=42)
            model.fit(X, y)
            
            # Data Terkini
            ticker = yf.Ticker(koin)
            harga_live = ticker.fast_info['last_price']
            rsi_sekarang = df['RSI'].iloc[-1]
            
            data_input = df[['Close', 'MA5', 'RSI']].tail(1)
            prediksi_besok = model.predict(data_input)[0]
            
            # Status Psikologi Pasar
            status_rsi = "🟡 NETRAL"
            if rsi_sekarang > 70:
                status_rsi = "🔴 OVERBOUGHT"
            elif rsi_sekarang < 30:
                status_rsi = "🟢 OVERSOLD"

            trend = "📈 NAIK" if prediksi_besok > harga_live else "📉 TURUN"
            
            nama_koin = koin.replace("-USD", "")
            pesan_final += f"🪙 *{nama_koin}*\n"
            pesan_final += f"💰 Price: ${harga_live:,.2f}\n"
            pesan_final += f"📊 RSI: {rsi_sekarang:.2f} ({status_rsi})\n"
            pesan_final += f"🔮 Prediksi: ${prediksi_besok:,.2f} ({trend})\n\n"
            
        except Exception as e:
            print(f"Error pada {koin}: {e}")

    pesan_final += "------------------------------\n"
    pesan_final += f"🕒 {waktu_sekarang.strftime('%d %b | %H:%M')} WITA\n"
    pesan_final += "Developed by: *David Soerdjana*"
    
    kirim_telegram(pesan_final)
    print(f"Laporan terkirim pada {waktu_sekarang.strftime('%H:%M:%S')} WITA")

# --- 3. LOOP PENJADWALAN (SETIAP 4 JAM) ---
tz_bali = timezone(timedelta(hours=8))
# Jam operasional: 00, 04, 08, 12, 16, 20
jam_laporan = [0, 4, 8, 12, 16, 20]

print("=" * 55)
print("   SENTINEL v3.0 AKTIF - JADWAL 6X SEHARI (4 JAM)   ")
print("=" * 55)

# Langsung tes jalankan sekali saat buka
jalankan_analisis()

while True:
    waktu_skrg = datetime.now(tz_bali)
    
    # Cek apakah jam sekarang ada dalam daftar jam_laporan
    if waktu_skrg.hour in jam_laporan and waktu_skrg.minute == 0:
        print(f"Memasuki jadwal jam {waktu_skrg.hour}:00. Mengirim laporan...")
        jalankan_analisis()
        time.sleep(65) # Agar tidak terpicu dua kali dalam menit yang sama
    
    # Cek waktu setiap 30 detik
    time.sleep(30)