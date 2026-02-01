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
    print(f"[*] SION Scraper")
    
    options = uc.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_folder}")
    options.add_argument("--start-maximized")
    
    try:
        driver = uc.Chrome(options=options, use_subprocess=True, version_main=144)
        driver.get(TARGET_URL)
        time.sleep(3) 

        if "login" in driver.current_url:
            try:
                driver.find_element(By.NAME, "username").send_keys(login.NIM)
                driver.find_element(By.NAME, "password").send_keys(login.PASSWORD + "\n")
                time.sleep(5)
            except: pass

        if TARGET_URL not in driver.current_url:
            driver.get(TARGET_URL)
            time.sleep(3)

        try:
            print("[-] Membuka tab Hasil Ujian...")
            driver.find_element(By.ID, "hasilujian_").click()
            time.sleep(5) 
        except: pass

        container = driver.find_element(By.ID, "hasilujian")
        tombol_matkul = container.find_elements(By.CLASS_NAME, "btn-mk")
        
        hasil_scan = []
        print(f"[-] Menemukan {len(tombol_matkul)} Mata Kuliah di Hasil Ujian.")

        for btn in tombol_matkul:
            try:
                judul = btn.text.replace("\n", " ").strip()
                print(f"    > Scanning: {judul}")
                
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(1) 

                id_target = btn.get_attribute("data-target")
                panel = driver.find_element(By.ID, id_target)

                full_text_panel = panel.text.split('\n')
                nilai_akhir_angka = "-"
                nilai_akhir_huruf = "-"
                for idx, txt in enumerate(full_text_panel):
                    if "Nilai Angka" in txt and idx+1 < len(full_text_panel):
                        nilai_akhir_angka = full_text_panel[idx+1].strip()
                    if "Nilai Huruf" in txt and idx+1 < len(full_text_panel):
                        nilai_akhir_huruf = full_text_panel[idx+1].strip()

                komponen_nilai = []
                seen_entries = set()

                tombol_cpmk = panel.find_elements(By.CSS_SELECTOR, ".btn-cpmk")
                
                if len(tombol_cpmk) > 0:
                    for i, cpmk in enumerate(tombol_cpmk):
                        try:
                            driver.execute_script("arguments[0].click();", cpmk)
                            time.sleep(1) 
                            rows = panel.find_elements(By.TAG_NAME, "tr")
                            for row in rows:
                                cols = row.find_elements(By.TAG_NAME, "td")
                                if len(cols) >= 3:
                                    nama = cols[0].text.strip()
                                    nilai = cols[2].text.strip() 
                                    if not nilai.replace('.', '').isdigit() and len(cols) > 1:
                                        if cols[1].text.strip().replace('.', '').isdigit():
                                            nilai = cols[1].text.strip()

                                    blacklist = ["Nama Nilai", "Bobot", "Total", "Maksimal", "Nilai x Bobot", "Status", "CPMK", "Nilai Angka", "Nilai Huruf"]
                                    is_sampah = any(x.lower() in nama.lower() for x in blacklist)
                                    
                                    if not is_sampah and nilai.replace('.', '').isdigit():
                                        entry = f"{nama} : {nilai}"
                                        if entry not in seen_entries:
                                            komponen_nilai.append(f"   > {nama:<20} : {nilai}")
                                            seen_entries.add(entry)
                        except: pass
                else:
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

                out = f"=== {judul} ===\n"
                out += f"FINAL: {nilai_akhir_angka} ({nilai_akhir_huruf})\n"
                out += "DETAIL:\n"
                
                if komponen_nilai:
                    priority = {"KUIS": 1, "TUGAS": 2, "UTS": 3, "UAS": 4}
                    
                    def sort_logic(item):
                        clean_item = item.strip().upper()
                        rank = 99
                        for key, val in priority.items():
                            if key in clean_item:
                                rank = val
                                break
                        return (rank, clean_item)

                    komponen_nilai.sort(key=sort_logic)
                    out += "\n".join(komponen_nilai)
                else:
                    out += "   (Tidak ada detail nilai)"
                
                out += "\n" + "="*40 + "\n"
                hasil_scan.append(out)

                driver.execute_script("arguments[0].click();", btn)
                time.sleep(0.5)

            except Exception as e:
                print(f"[!] Gagal scan {judul}: {e}")

        driver.quit()

        final_text = "\n".join(hasil_scan)
        print("\n" + final_text)
        
        with open(FILE_CATATAN, "w", encoding="utf-8") as f:
            f.write(final_text)
            
        print(f"\n[SUKSES] Data disimpan di: {os.path.abspath(FILE_CATATAN)}")

    except Exception as e:
        print(f"[CRITICAL] {e}")

if __name__ == "__main__":
    main()