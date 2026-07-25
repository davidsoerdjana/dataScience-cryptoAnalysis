import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Mengambil data Bitcoin (BTC-USD) dan Emas (GC=F)
# Kita ambil data interval 1 jam untuk melihat volatilitas hari ini
btc_data = yf.download('BTC-USD', period='2d', interval='1h')
gold_data = yf.download('GC=F', period='2d', interval='1h')

# Menampilkan 5 data teratas
print(btc_data.tail())

# Normalisasi DataKenapa harus dinormalisasi? Karena harga Bitcoin (~$\$63.000$) dan Emas (~$\$2.000$) sangat jauh berbeda. Agar bisa dibandingkan dalam satu grafik, kita gunakan persentase perubahan ($Cumulative$ $Return$)
# Menghitung persentase perubahan dari titik awal (2 hari lalu)
btc_returns = (btc_data['Close'] / btc_data['Close'].iloc[0] - 1) * 100
gold_returns = (gold_data['Close'] / gold_data['Close'].iloc[0] - 1) * 100

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(btc_returns, label='Bitcoin (BTC)', color='orange', linewidth=2)
plt.plot(gold_returns, label='Emas (Gold)', color='gold', linewidth=2)

plt.title('Perbandingan Performa: BTC vs Gold (24 Feb 2026)')
plt.xlabel('Waktu (Jam)')
plt.ylabel('Return (%)')
plt.legend()
plt.grid(True)
plt.show()