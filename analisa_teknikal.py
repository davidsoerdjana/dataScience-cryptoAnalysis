import yfinance as yf
import matplotlib.pyplot as plt

# 1. Ambil data 6 bulan agar trennya kelihatan
df = yf.download('BTC-USD', period='6mo', interval='1d')

# 2. Membuat MA-20 (Jangka Pendek) dan MA-50 (Jangka Menengah)
# .rolling() adalah fungsi sakti untuk menghitung rata-rata bergerak
df['MA20'] = df['Close'].rolling(window=20).mean()
df['MA50'] = df['Close'].rolling(window=50).mean()

# 3. Visualisasi Tren
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Harga Asli', alpha=0.5) # alpha=0.5 agar agak transparan
plt.plot(df['MA20'], label='MA 20 (Tren Pendek)', color='orange')
plt.plot(df['MA50'], label='MA 50 (Tren Menengah)', color='red')

plt.title('Bitcoin Trend Analysis: Moving Average')
plt.legend()
plt.show()

# Menghapus baris yang mengandung NaN
df_clean = df.dropna()

print("Data setelah dibersihkan (baris awal yang kosong dibuang):")
print(df_clean.head())