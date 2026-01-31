Script Python otomatis untuk mengecek **Hasil Ujian** di SION.

## 🔥 Fitur Utama

- **Notifikasi Perubahan:** Memberi tahu di terminal jika ada nilai baru yang keluar.
- **Anti-Cloudflare:** Menggunakan `undetected-chromedriver` agar tidak terjebak looping verifikasi.
- **Auto-Login:** Otomatis mengisi NIM dan Password jika sesi habis.
- **Session Keeper:** Menyimpan Cookies & Cache browser (Profile) agar tidak perlu login berulang-ulang.


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

