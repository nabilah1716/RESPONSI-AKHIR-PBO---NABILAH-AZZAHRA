# Deskripsi Aplikasi
Aplikasi ini adalah sistem manajemen produk dan transaksi yang dirancang untuk membantu pengguna mengelola inventaris produk serta mencatat transaksi dengan mudah. Aplikasi ini menggunakan Python dengan GUI berbasis `tkinter` dan menyimpan data dalam database MySQL.
# Fitur Utama:
-Manajemen Produk: Tambah, perbarui, dan hapus produk.
-Manajemen Transaks: Rekam transaksi pembelian produk.
-Tampilan yang User-Friendl: Antar muka sederhana dan intuitif.


## Cara Menjalankan Aplikasi
1.Persiapan Databas:
- Pastikan bahwa kita memiliki server MySQL yang aktif.
- Buat database bernama `inventory_produk`.
- Buat tabel-tabel seperti pada struktur yang dijelaskan di bawah ini.

2.Konfigurasi Aplikas:
- Pastikan Python 3.x terinstal di sistem.
- Instal library yang dibutuhkan dengan perintah seperti berikut:
  ```bash
    pip install mysql-connector-python
  ```
- Simpan file aplikasi Python ini pada direktori pilihan.

3.Menjalankan Aplikas:
- Jalankan file Python menggunakan perintah berikut di terminal atau IDE favorit:
 ```bash
   python app.py
 ```


## Struktur Tabel Database
# Tabel `products`
```sql
CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    harga FLOAT NOT NULL
);
```
# Tabel `transactions`
```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    jumlah_product INT NOT NULL,
    total_harga FLOAT NOT NULL,
    tanggal_transaksi DATE NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(id)
);
"# RESPONSI-AKHIR-PBO---NABILAH-AZZAHRA" 
"# RESPONSI-AKHIR-PBO---NABILAH-AZZAHRA" 
