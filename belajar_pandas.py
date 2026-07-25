import yfinance as yf
import pandas as pd


# Ambil data BTC 1 bulan terakhir
df = yf.download('BTC-USD', period='1mo', interval='1d')


# Menampilkan 5 data teratas
print("--- 5 DATA TERATAS ---")
print(df.head())


# Mencari hari saat harga penutupan (Close) di atas $50,000
# (Sesuaikan angka ini dengan harga pasar saat ini jika perlu)
high_prices = df[df['Close'] > 65000]

print("\nHari dengan harga di atas $50,000:")
print(high_prices[['Close']])


# Menghitung selisih High dan Low
df['Selisih'] = df['High'] - df['Low']


# Mencari hari dengan volatilitas paling gila
hari_paling_volatil = df[df['Selisih'] == df['Selisih'].max()]

print("\nHari dengan pergerakan harga paling ekstrem:")
print(hari_paling_volatil[['High', 'Low', 'Selisih']])


# 1. Menghitung persentase perubahan dari harga hari sebelumnya
df['Persentase_Harian'] = df['Close'].pct_change() * 100


# 2. Mencari hari di mana harga turun lebih dari 2% (Potensi Serok/Buy)
diskon_hari_ini = df[df['Persentase_Harian'] < -2]

print("\nHari-hari saat Bitcoin 'Diskon' (Turun > 2%):")
print(diskon_hari_ini[['Close', 'Persentase_Harian']])


# 3. Menghitung total keuntungan jika kamu simpan selama sebulan
total_return = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
print(f"\nTotal Return Bitcoin selama 1 bulan ini: {float(total_return.iloc[0]):.2f}%")


# Perintah ini akan memberitahu apakah ada data yang "bolong" (kosong) atau tidak. Dalam data keuangan, data kosong bisa merusak prediksi AI kita nanti.
print(df.isnull().sum())


# Menampilkan statistik deskriptif (Mean, Min, Max, Standar Deviasi, dll)
print("\n--- RINGKASAN STATISTIK BITCOIN ---")
print(df.describe())


# Menghitung rata-rata dari kolom 'Volume' saja
rata_rata_volume = df['Volume'].mean()

# Kita gunakan float() dan .iloc[0] jika muncul error format seperti tadi
if isinstance(rata_rata_volume, pd.Series):
    rata_rata_volume = float(rata_rata_volume.iloc[0])

# Catatan Kode: Simbol :,.0f di bagian akhir itu fungsinya untuk memberikan pemisah ribuan (koma) agar angkanya lebih mudah dibaca (misal: 1,000,000 bukan 1000000.0)
print(f"\nRata-rata Volume Perdagangan Harian: {rata_rata_volume:,.0f}")