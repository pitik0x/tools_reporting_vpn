from datetime import datetime, timedelta
import pytz

from config import TIMEZONE

#INPUTAN 

def pilih_tanggal(teks_judul):
    sekarang = datetime.now()
    kemarin = sekarang - timedelta(days=1)

    while True:
        print(f"\n{teks_judul}")
        print(f"1. Hari ini ({sekarang.strftime('%Y-%m-%d')})")
        print(f"2. Kemarin  ({kemarin.strftime('%Y-%m-%d')})")
        print("3. Ketik Manual (YYYY-MM-DD)")

        pilihan = input("Pilih [1/2/3]: ").strip()

        if pilihan == '1':
            return sekarang.strftime('%Y-%m-%d')
        elif pilihan == '2':
            return kemarin.strftime('%Y-%m-%d')
        elif pilihan == '3':
            while True:
                manual_date = input("Masukkan tanggal manual (Contoh: 2026-03-01): ").strip()
                try:
                    datetime.strptime(manual_date, "%Y-%m-%d")
                    return manual_date
                except ValueError:
                    print("   [!] Format salah! Harus YYYY-MM-DD (Contoh: 2026-03-02). Coba lagi.")
        else:
            print(f"   [!] Pilihan '{pilihan}' tidak valid. Silakan pilih 1, 2, atau 3.")


def input_jam(teks_prompt):
    """Minta input jam dengan validasi format HH:MM. Loop sampai valid."""
    while True:
        jam = input(teks_prompt).strip()
        try:
            datetime.strptime(jam, "%H:%M")
            return jam
        except ValueError:
            print(f"   [!] Format jam '{jam}' salah! Harus HH:MM (Contoh: 08:00, 18:30). Coba lagi.")


def ambil_input_waktu():
    
    """Mengambil semua input dari user: nama, rentang waktu. 
    Return: (nama_pengirim, waktu_mulai_utc, waktu_selesai_utc, waktu_mulai_str, waktu_selesai_str)
    """
    wib = pytz.timezone(TIMEZONE)
    utc = pytz.utc

    nama_pengirim = input("siapa ini yang lagi shift: ").strip()
    while not nama_pengirim:
        print("[!] Nama tidak boleh kosong.")
        nama_pengirim = input("siapa ini yang lagi shift: ").strip()

    tgl_mulai = pilih_tanggal("--- TANGGAL MULAI ---")
    jam_mulai = input_jam("Masukkan Jam Mulai (Contoh: 18:00) : ")
    waktu_mulai_str = f"{tgl_mulai} {jam_mulai}"

    while True:
        tgl_selesai = pilih_tanggal("--- TANGGAL SELESAI ---")
        jam_selesai = input_jam("Masukkan Jam Selesai (Contoh: 08:00): ")
        waktu_selesai_str = f"{tgl_selesai} {jam_selesai}"

        waktu_mulai_wib = wib.localize(datetime.strptime(waktu_mulai_str, "%Y-%m-%d %H:%M"))
        waktu_selesai_wib = wib.localize(datetime.strptime(waktu_selesai_str, "%Y-%m-%d %H:%M"))

        if waktu_selesai_wib <= waktu_mulai_wib:
            print(f"\n   [!] Waktu selesai ({waktu_selesai_str}) harus LEBIH BESAR dari waktu mulai ({waktu_mulai_str})!")
            print("   [!] Silakan input ulang tanggal & jam selesai.")
            continue

        break

    waktu_mulai_utc = waktu_mulai_wib.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    waktu_selesai_utc = waktu_selesai_wib.astimezone(utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return nama_pengirim, waktu_mulai_utc, waktu_selesai_utc, waktu_mulai_str, waktu_selesai_str
