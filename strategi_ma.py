import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. Ambil data 1 tahun agar tren jangka panjang terlihat
df = yf.download('BTC-USD', period='1y', interval='1d')

# 2. Hitung MA-20 dan MA-50
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# 3. Logika Sinyal (Data Scientist Thinking)
# Kita buat kolom 'Sinyal' di mana 1 artinya MA20 > MA50
df['Sinyal'] = 0.0
df['Sinyal'] = (df['MA20'] > df['MA50']).astype(float)

# 4. Deteksi momen persilangan (Crossover)
# .diff() melihat perubahan dari baris sebelumnya
df['Position'] = df['Sinyal'].diff()

print("Momen Golden Cross (Sinyal Beli) Terdeteksi pada Tanggal:")
print(df[df['Position'] == 1].index)


# 1. Menyimpan data yang sudah ada MA dan Sinyal-nya ke file CSV
df.to_csv('hasil_analisis_btc.csv')
print("File CSV berhasil disimpan!")

# 2. Coba simpan ke Excel dengan penanganan error yang lebih bersih
try:
    import openpyxl
    df.to_excel('laporan_crypto_februari.xlsx')
    print("File Excel berhasil disimpan!")
except ModuleNotFoundError:
    print("Gagal simpan Excel: Kamu perlu install library dulu (pip install openpyxl)")
except Exception as e:
    print(f"Terjadi error lain saat simpan Excel: {e}")