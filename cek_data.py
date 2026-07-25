import yfinance as yf
import matplotlib.pyplot as plt

print("Sedang mengambil data Bitcoin... Tunggu sebentar.")

# 1. Mengambil data harga Bitcoin 7 hari terakhir
data = yf.download('BTC-USD', period='7d', interval='1h')

# 2. Menampilkan 5 baris data teratas di terminal
print("\nData Berhasil Diambil:")
print(data.head())

# 3. Membuat grafik sederhana (Visualisasi)
data['Close'].plot(figsize=(10, 5), title="Pergerakan Harga BTC 7 Hari Terakhir")
plt.xlabel("Waktu")
plt.ylabel("Harga (USD)")
plt.grid()

print("\nMenampilkan grafik... Tutup jendela grafik untuk mengakhiri program.")
plt.show()
