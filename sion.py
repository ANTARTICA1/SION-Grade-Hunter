import time
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

try:
    import login
except ImportError:
    print("[ERROR] File login.py tidak ditemukan!")
    exit()

TARGET_URL   = "https://sion.stikom-bali.ac.id/perkuliahan"
FILE_CATATAN = "data_nilai_lengkap_fix.txt"
profile_folder = os.path.join(os.getcwd(), "Profile_SION_Fix")

def main():
    print(f"[*] SION Scraper: MODE ACCORDION FIX...")
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_folder}")
    options.add_argument("--start-maximized")
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=144)
        driver.get(TARGET_URL)
        time.sleep(3) 

        # --- LOGIN ---
        if "login" in driver.current_url:
            try:
                driver.find_element(By.NAME, "username").send_keys(login.NIM)
                driver.find_element(By.NAME, "password").send_keys(login.PASSWORD + "\n")
                time.sleep(5)
            except: pass

        if TARGET_URL not in driver.current_url:
            driver.get(TARGET_URL)
            time.sleep(3)

        # --- BUKA TAB HASIL ---
        try:
            print("[-] Membuka tab Hasil Ujian...")
            driver.find_element(By.ID, "hasilujian_").click()
            time.sleep(5) 
        except: pass

        # --- SCAN MATKUL ---
        container = driver.find_element(By.ID, "hasilujian")
        tombol_matkul = container.find_elements(By.CLASS_NAME, "btn-mk")
        
        hasil_scan = []
        print(f"[-] Menemukan {len(tombol_matkul)} Mata Kuliah di Hasil Ujian.")

        for btn in tombol_matkul:
            try:
                judul = btn.text.replace("\n", " ").strip()
                print(f"    > Scanning: {judul}")
                
                # 1. Buka Panel Utama Matkul
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1) # Tunggu panel terbuka

                id_target = btn.get_attribute("data-target")
                panel = driver.find_element(By.ID, id_target)

                # 2. AMBIL NILAI AKHIR (Biasanya di footer, tidak terpengaruh accordion)
                full_text_panel = panel.text.split('\n')
                nilai_akhir_angka = "-"
                nilai_akhir_huruf = "-"
                for idx, txt in enumerate(full_text_panel):
                    if "Nilai Angka" in txt and idx+1 < len(full_text_panel):
                        nilai_akhir_angka = full_text_panel[idx+1].strip()
                    if "Nilai Huruf" in txt and idx+1 < len(full_text_panel):
                        nilai_akhir_huruf = full_text_panel[idx+1].strip()

                # 3. LOGIKA ACCORDION (Jalan satu-satu)
                komponen_nilai = []
                seen_entries = set() # Untuk cegah duplikat
                
                # Cari tombol CPMK
                tombol_cpmk = panel.find_elements(By.CSS_SELECTOR, ".btn-cpmk")
                
                if len(tombol_cpmk) > 0:
                    # Loop klik satu per satu
                    for i, cpmk in enumerate(tombol_cpmk):
                        try:
                            # Klik tombol CPMK ke-i
                            driver.execute_script("arguments[0].click();", cpmk)
                            time.sleep(1) # Wajib tunggu animasi slideDown
                            
                            # Scrape Data yang SEDANG TERLIHAT sekarang
                            # Kita scan ulang baris tabel setiap kali klik
                            rows = panel.find_elements(By.TAG_NAME, "tr")
                            
                            for row in rows:
                                # Ambil teks row
                                cols = row.find_elements(By.TAG_NAME, "td")
                                if len(cols) >= 3:
                                    nama = cols[0].text.strip()
                                    nilai = cols[2].text.strip() # Asumsi kolom 3 adalah nilai
                                    
                                    # Fallback cek kolom 2 jika kolom 3 kosong/bukan angka
                                    if not nilai.replace('.', '').isdigit() and len(cols) > 1:
                                        if cols[1].text.strip().replace('.', '').isdigit():
                                            nilai = cols[1].text.strip()

                                    # Filter Sampah
                                    blacklist = ["Nama Nilai", "Bobot", "Total", "Maksimal", "Nilai x Bobot", "Status", "CPMK", "Nilai Angka", "Nilai Huruf"]
                                    is_sampah = any(x.lower() in nama.lower() for x in blacklist)
                                    
                                    if not is_sampah and nilai.replace('.', '').isdigit():
                                        # Kunci unik: Nama + Nilai (misal: "UTS : 100")
                                        entry = f"{nama} : {nilai}"
                                        
                                        # Simpan jika belum pernah diambil
                                        if entry not in seen_entries:
                                            komponen_nilai.append(f"   > {nama:<20} : {nilai}")
                                            seen_entries.add(entry)
                        except: pass
                else:
                    # Jika tidak ada tombol CPMK (matkul simpel), scan langsung tabelnya
                    rows = panel.find_elements(By.TAG_NAME, "tr")
                    for row in rows:
                        cols = row.find_elements(By.TAG_NAME, "td")
                        if len(cols) >= 3:
                            nama = cols[0].text.strip()
                            nilai = cols[2].text.strip()
                            if nilai.replace('.', '').isdigit():
                                entry = f"{nama} : {nilai}"
                                if entry not in seen_entries:
                                    komponen_nilai.append(f"   > {nama:<20} : {nilai}")
                                    seen_entries.add(entry)

                # 4. Susun Laporan Matkul
                out = f"=== {judul} ===\n"
                out += f"FINAL: {nilai_akhir_angka} ({nilai_akhir_huruf})\n"
                out += "DETAIL:\n"
                if komponen_nilai:
                    # Sortir biar rapi (opsional)
                    komponen_nilai.sort() 
                    out += "\n".join(komponen_nilai)
                else:
                    out += "   (Tidak ada detail nilai)"
                out += "\n" + "="*40 + "\n"
                
                hasil_scan.append(out)

                # Tutup Panel Matkul Utama
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.5)

            except Exception as e:
                print(f"[!] Gagal scan {judul}: {e}")

        driver.quit()

        # SIMPAN
        final_text = "\n".join(hasil_scan)
        print("\n" + final_text)
        with open(FILE_CATATAN, "w", encoding="utf-8") as f:
            f.write(final_text)
        print(f"\n[SUKSES] Data disimpan di: {FILE_CATATAN}")

    except Exception as e:
        print(f"[CRITICAL] {e}")

if __name__ == "__main__":
    main()