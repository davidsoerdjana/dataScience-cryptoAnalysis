import yfinance as yf
import plotly.graph_objects as go

# 1. Ambil data Bitcoin
df = yf.download('BTC-USD', period='1mo', interval='1d')

# 2. Membuat grafik Candlestick
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

# 3. Percantik tampilan
fig.update_layout(title='Grafik Candlestick Bitcoin 1 Bulan Terakhir',
                  yaxis_title='Harga (USD)',
                  xaxis_title='Tanggal')

fig.show()


# cara 1
# Ambil data dua koin
assets = ['BTC-USD', 'ETH-USD']
data = yf.download(assets, period='1mo')['Close']

# Normalisasi data (Mulai dari angka 100 agar perbandingannya adil)
# Ini adalah teknik Data Science agar aset dengan harga beda jauh bisa dibandingkan
normalized_data = (data / data.iloc[0]) * 100

# Plot perbandingannya
normalized_data.plot(figsize=(10, 6), title='Pertumbuhan BTC vs ETH (Base 100)')
import matplotlib.pyplot as plt
plt.show()


# cara 2
import yfinance as yf
import pandas as pd
import time

assets = ['BTC-USD', 'ETH-USD', 'SOL-USD']

# Tambahkan mekanisme 'Retry' sederhana
try:
    print("Sedang mencoba mengambil data...")
    data = yf.download(assets, period='1mo')['Close']
    
    # Cek apakah data kosong
    if data.empty:
        print("Data kosong! Cek koneksi internet atau simbol koin.")
    else:
        # Normalisasi hanya jika data ada
        normalized_data = (data / data.iloc[0]) * 100
        print("Data berhasil diambil dan dinormalisasi!")
        
        # Lanjutkan ke plotting
        import matplotlib.pyplot as plt
        normalized_data.plot(figsize=(10, 6), title='Pertumbuhan BTC vs ETH vs SOL')
        plt.show()

except Exception as e:
    print(f"Terjadi kesalahan: {e}")