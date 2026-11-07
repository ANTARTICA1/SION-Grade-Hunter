# SION Grade Hunter - Academic Results Monitoring Automation

A Python automation utility engineered to monitor, scrape, and detect updates to semester examination results published on the ITB STIKOM Bali Academic Information System (SION - Sistem Informasi Online). Powered by Selenium and `undetected-chromedriver`, the tool handles browser fingerprinting, bypasses anti-bot verification challenges, persists user sessions, and audits grade mutations against localized snapshots.

## Overview

Student portals frequently publish examination results unpredictably across multiple evaluation intervals, requiring repetitive manual authentication and page refreshing. SION Grade Hunter automates this observation loop. By maintaining persistent Chrome profile caches and diffing remote tabular grade data against local historical records, students receive instant terminal alerts whenever new course grades or grade modifications are posted.

## Technical Architecture and Features

- Anti-Bot & Cloudflare Bypass: Utilizes `undetected-chromedriver` (`uc.Chrome`) to patch Chromedriver binary fingerprints in memory, avoiding infinite verification loops and WebGL/WebDriver detection flags.
- Session Persistence (User Data Directory): Retains authenticated cookies, local storage, and session caches inside an isolated browser profile (`Profile_SION_Fix`), preventing repetitive login handshakes.
- Automated Authentication Fallback: Inspects `driver.current_url`. If redirected to the login endpoint, the script injects credentials configured in `login.py` and navigates directly to the target academic registry.
- Tabular Grade Scraping: Programmatically clicks the examination results view (`#hasilujian_`), locates relevant semester tables, parses course codes, subject titles, credit weights (SKS), and letter grades.
- Diff & Mutation Auditing: Compares freshly scraped examination data against `data_nilai_lengkap_fix.txt`. If discrepancies or newly published grades are detected, differences are highlighted directly in the terminal interface and saved.

## System Requirements

- Python 3.9 or higher
- Google Chrome browser installed on host system
- Operating System: Windows, Linux, or macOS

## Project Structure

```
SION-Grade-Hunter/
├── sion.py                     # Primary scraping, session manager, and diff engine
├── login.py                    # Credential storage module (NIM & Password)
├── Profile_SION_Fix/           # Persistent Chrome user profile and session storage (generated)
├── data_nilai_lengkap_fix.txt  # Local snapshot of recorded examination results (generated)
├── .gitignore                  # Git exclusions for credentials and browser profiles
└── README.md                   # Technical documentation
```

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ANTARTICA1/SION-Grade-Hunter.git
   cd SION-Grade-Hunter
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Linux/macOS
   source venv/bin/activate
   ```

3. Install required Python packages:
   ```bash
   pip install selenium undetected-chromedriver
   ```

4. Configure Credentials:
   Open or create `login.py` in the root directory:
   ```python
   # login.py
   NIM = "YOUR_STUDENT_ID"
   PASSWORD = "YOUR_SION_PASSWORD"
   ```

5. Execute the monitor:
   ```bash
   python sion.py
   ```

## Security and Privacy Notice

- Never commit `login.py` containing plain-text credentials to public version control repositories. Ensure `login.py` and `Profile_SION_Fix/` are declared inside `.gitignore`.
- This utility is strictly intended for individual academic tracking and personal productivity. Please respect campus server load by configuring reasonable polling intervals.

## Author

Anak Agung Ngurah Krisna Artha Wibawa ([ANTARTICA1](https://github.com/ANTARTICA1))  
Institut Teknologi dan Bisnis (ITB) STIKOM Bali

## License

This project is licensed under the MIT License.