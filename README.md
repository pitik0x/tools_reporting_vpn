# Report VPN Petro Tools

## Instalasi

```bash
git clone https://github.com/your-repo/Script_petro.git
cd Script_petro
python -m venv venv
.\venv\Scripts\Activate.ps1       # Windows PowerShell
pip install -r requirements.txt
```

Buat file `.env` dari template:
```bash
copy .env.example .env
```

Edit `.env` dan isi kredensial OpenSearch kita:
```
OPENSEARCH_URL= url
OPENSEARCH_USERNAME=username_wazuh
OPENSEARCH_PASSWORD=isi_password_disini
OPENSEARCH_INDEX_PATTERN=wazuh-alerts-*
```

## Cara Pakai

```bash
python vpn_login.py
```

```bash
 ____                       _    __     ______  _   _   ____      _              _____           _
|  _ \ ___  _ __   ___  _ __| |_  \ \   / /  _ \| \ | | |  _ \ ___| |_ _ __ ___ |_   _|__   ___ | |___
| |_) / _ \| '_ \ / _ \| '__| __|  \ \ / /| |_) |  \| | | |_) / _ \ __| '__/ _ \  | |/ _ \ / _ \| / __|
|  _ <  __/| |_) | (_) | |  | |_    \ V / |  __/| |\  | |  __/  __/ |_| | | (_) | | | (_) | (_) | \__ \
|_| \_\___|| .__/ \___/|_|   \__|    \_/  |_|   |_| \_| |_|   \___|\__|_|  \___/  |_|\___/ \___/|_|___/
            |_|

siapa ini yang lagi shift: Rizki

--- TANGGAL MULAI ---
1. Hari ini (2026-03-05)
2. Kemarin  (2026-03-04)
3. Ketik Manual (YYYY-MM-DD)
Pilih [1/2/3]: 3
Masukkan tanggal manual (Contoh: 2026-03-01): 2026-02-24
Masukkan Jam Mulai (Contoh: 18:00) : 05:00

--- TANGGAL SELESAI ---
1. Hari ini (2026-03-05)
2. Kemarin  (2026-03-04)
3. Ketik Manual (YYYY-MM-DD)
Pilih [1/2/3]: 3
Masukkan tanggal manual (Contoh: 2026-03-01): 2026-02-24
Masukkan Jam Selesai (Contoh: 08:00): 12:00

Sedang menarik dan menganalisis data dari 2026-02-24 05:00 WIB s/d 2026-02-24 12:00 WIB...
```
