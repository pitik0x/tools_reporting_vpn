import requests
import urllib3
import sys

from config import URL, INDEX_PATTERN, USERNAME, PASSWORD, RULE_DESCRIPTION, EXCLUDED_USERS, MAX_RESULTS
from Logic.input_handler import ambil_input_waktu
from Logic.report_builder import proses_hits, build_laporan

# Matikan warning SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    banner = """
 ____                       _    __     ______  _   _   ____      _              _____           _     
|  _ \\ ___  _ __   ___  _ __| |_  \\ \\   / /  _ \\| \\ | | |  _ \\ ___| |_ _ __ ___ |_   _|__   ___ | |___ 
| |_) / _ \\| '_ \\ / _ \\| '__| __|  \\ \\ / /| |_) |  \\| | | |_) / _ \\ __| '__/ _ \\  | |/ _ \\ / _ \\| / __|
|  _ <  __/| |_) | (_) | |  | |_    \\ V / |  __/| |\\  | |  __/  __/ |_| | | (_) | | | (_) | (_) | \\__ \\
|_| \\_\\___|| .__/ \\___/|_|   \\__|    \\_/  |_|   |_| \\_| |_|   \\___|\\__|_|  \\___/  |_|\\___/ \\___/|_|___/
            |_|                                                                                         
    """
    print(banner)

    nama_pengirim, waktu_mulai_utc, waktu_selesai_utc, waktu_mulai_str, waktu_selesai_str = ambil_input_waktu()

    must_not_clauses = [{"match_phrase": {"data.dstuser": user}} for user in EXCLUDED_USERS]

    query = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"rule.description": RULE_DESCRIPTION}},
                    {"range": {"timestamp": {"gte": waktu_mulai_utc, "lte": waktu_selesai_utc}}},
                ],
                "must_not": must_not_clauses,
            }
        },
        "sort": [{"timestamp": {"order": "asc"}}],
        "size": MAX_RESULTS,
    }

    print(f"\nSedang menarik dan menganalisis data dari {waktu_mulai_str} WIB s/d {waktu_selesai_str} WIB...\n")

    try:
        response = requests.get(
            f"{URL}/{INDEX_PATTERN}/_search",
            auth=(USERNAME, PASSWORD),
            json=query,
            verify=False,
        )

        if response.status_code != 200:
            print(f"Gagal mengambil data. Status Code: {response.status_code}")
            sys.exit()

        hits = response.json()["hits"]["hits"]

        if not hits:
            print("Tidak ada aktivitas login VPN di luar jam kerja.")
            sys.exit()

        # 3. PROSES DATA
        all_entries, user_login_counts, user_ips_used, user_ip_times, ip_country_map, all_countries = proses_hits(hits)

        # 4. BUILD & CETAK LAPORAN
        laporan = build_laporan(all_entries, user_login_counts, user_ips_used, user_ip_times, ip_country_map, all_countries, nama_pengirim)

        print("=" * 50)
        print("TINGGAL COPY AJA INI CUI")
        print("=" * 50 + "\n")
        print(laporan)

    except Exception as e:
        print(f"Terjadi kesalahan koneksi/sistem: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program dibatalkan")
        sys.exit(0)