import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

try:
    import login
except ImportError:
    print("[ERROR] File login.py tidak ditemukan! Buat dulu isi NIM & Pass.")
    exit()

TARGET_URL   = "https://sion.stikom-bali.ac.id/perkuliahan"
FILE_CATATAN = "data_hasil_ujian.txt"
profile_folder = os.path.join(os.getcwd(), "Profile_SION_Fix")

def main():
    print(f"[*] Membuka SION (Auto Login)...")
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_folder}")
    options.add_argument("--start-maximized")
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=144)
        driver.get(TARGET_URL)
        
        time.sleep(3) 
        
        # --- LOGIKA LOGIN ---
        if "login" in driver.current_url or "Log in" in driver.page_source:
            print("[-] Terdeteksi halaman Login...")
            try:
                user_field = driver.find_element(By.NAME, "username") 
                pass_field = driver.find_element(By.NAME, "password")
                
                user_field.clear()
                user_field.send_keys(login.NIM)
                time.sleep(0.5)
                pass_field.clear()
                pass_field.send_keys(login.PASSWORD)
                pass_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
            except Exception as e:
                print(f"[!] Gagal Auto-Login: {e}")

        # --- PASTIKAN DASHBOARD ---
        print("[-] Memastikan masuk dashboard...")
        sudah_masuk = False
        for i in range(60):
            if TARGET_URL in driver.current_url:
                sudah_masuk = True
                break
            elif "sion.stikom-bali.ac.id" in driver.current_url and "login" not in driver.current_url:
                driver.get(TARGET_URL)
            time.sleep(1)

        if not sudah_masuk:
            print("[!] Gagal masuk dashboard.")
            driver.quit()
            return

        # --- AMBIL NILAI ---
        print("[-] Berhasil masuk. Mengambil data nilai...")
        try:
            # 1. Klik Tab Hasil Ujian
            driver.find_element(By.ID, "hasilujian_").click()
            time.sleep(5) 
            
            # 2. Cari Tombol Matkul
            container = driver.find_element(By.ID, "hasilujian")
            tombol_matkul = container.find_elements(By.CLASS_NAME, "btn-mk")
            
            print(f"[-] Mengecek {len(tombol_matkul)} mata kuliah...")
            
            hasil_lengkap = [] 

            for btn in tombol_matkul:
                try:
                    # Ambil Nama Matkul & Kelas dari tombol (Header)
                    # Format teks btn biasanya: "KODE - NAMA \n Kelas XYZ"
                    # Kita ganti baris baru jadi spasi biar rapi satu baris
                    header_text = btn.text.replace("\n", " | ").strip()
                    
                    # Scroll & Klik
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(0.5)
                    btn.click()
                    time.sleep(0.5) # Tunggu laci terbuka
                    
                    # Cari panel isi yang terbuka sesuai target tombol
                    id_target = btn.get_attribute("data-target")
                    panel_isi = driver.find_element(By.ID, id_target)
                    
                    # --- BAGIAN FILTERING (CUMA AMBIL ANGKA & HURUF) ---
                    teks_isi = panel_isi.text
                    baris_isi = teks_isi.split('\n')
                    
                    n_angka = "-"
                    n_huruf = "-"
                    
                    # Loop setiap baris untuk cari kata kuncinya
                    for i, baris in enumerate(baris_isi):
                        if "Nilai Angka" in baris:
                            # Ambil baris setelahnya (index i + 1)
                            if i + 1 < len(baris_isi):
                                n_angka = baris_isi[i+1].strip()
                        
                        if "Nilai Huruf" in baris:
                            # Ambil baris setelahnya
                            if i + 1 < len(baris_isi):
                                n_huruf = baris_isi[i+1].strip()
                    
                    # Simpan data yang sudah rapi
                    hasil_lengkap.append(f"{header_text}\n   => Angka: {n_angka} | Huruf: {n_huruf}\n")
                        
                except Exception as e:
                    print(f"[!] Skip error: {e}")

            driver.quit() 
            
            # --- GABUNGKAN DATA ---
            data_final = "\n".join(hasil_lengkap)

            # --- CEK PERUBAHAN ---
            if os.path.exists(FILE_CATATAN):
                with open(FILE_CATATAN, "r", encoding="utf-8") as f:
                    data_lama = f.read()
            else:
                data_lama = ""

            # Kita bandingkan isinya
            if data_final.strip() != data_lama.strip():
                print("\n" + "#"*40)
                print("###  ADA UPDATE NILAI BARU!  ###")
                print("#"*40 + "\n")
                print(data_final)
                
                with open(FILE_CATATAN, "w", encoding="utf-8") as f:
                    f.write(data_final)
            else:
                print("\n[AMAN] Belum ada nilai baru.")
                
        except Exception as e:
            print(f"[ERROR] Gagal ambil elemen: {e}")

    except Exception as e:
        print(f"[ERROR GLOBAL] {e}")

if __name__ == "__main__":
    main()