Script Python otomatis untuk mengecek **Hasil Ujian** di SION.

## 🔥 Fitur Utama

- **Auto-Login:** Otomatis mengisi NIM dan Password jika sesi habis.
- **Session Keeper:** Menyimpan Cookies & Cache browser (Profile) agar tidak perlu login berulang-ulang.
- **Notifikasi Perubahan:** Membandingkan data lokal dengan server kemudian memberi tahu di terminal jika ada nilai baru yang keluar.
- **Anti-Cloudflare Loop:** Menggunakan `undetected-chromedriver` untuk mengatasi masalah pada **Infinite Loop** yang membuat driver biasa tidak bisa login.


## 🛠️ Requirements

Pastikan **Google Chrome** sudah terinstall.

Install library Python yang dibutuhkan:

```bash
pip install selenium undetected-chromedriver
```

## ⚙️ Cara Instalasi
1. Cari file `login.py`.
2. Isi dengan data login kamu:
```python
NIM = "XXXXXX"        # Masukkan NIM
PASSWORD = "XXXXXXXX" # Masukkan Password SION
```

## 📂 Struktur File
* `sion.py`: Main Program.
* `login.py`: File kredensial.
* `Profile_SION_Fix/`: Folder otomatis yang menyimpan sesi login Chrome.
* `data_hasil_ujian.txt`: File otomatis yang menyimpan data nilai terakhir.

