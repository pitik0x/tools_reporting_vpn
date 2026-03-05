from datetime import datetime
import pytz

from config import TIMEZONE, MIN_LOGIN_INTERVAL_SECONDS
from Logic.geo_lookup import get_country


def proses_hits(hits):
    wib = pytz.timezone(TIMEZONE)
    utc = pytz.utc

    all_entries = []
    user_last_log_time = {}
    user_login_counts = {}
    user_ips_used = {}          # {username: set(ip)}
    user_ip_times = {}          # {username: [(ip, waktu_wib), ...]}
    ip_country_map = {}         # {ip: country}
    all_countries = set()

    for hit in hits:
        sumber = hit['_source']
        username = sumber.get('data', {}).get('dstuser', 'Unknown User')
        ip_address = sumber.get('data', {}).get('srcip', 'Unknown IP')

        # Parsing waktu
        waktu_log_utc = datetime.strptime(sumber['timestamp'][:19], "%Y-%m-%dT%H:%M:%S")
        waktu_log_utc = utc.localize(waktu_log_utc)

        # Filter jika kedekatan waktu 1 jam itu gak bakal duplicate 
        if username in user_last_log_time:
            selisih_detik = (waktu_log_utc - user_last_log_time[username]).total_seconds()
            if selisih_detik <= MIN_LOGIN_INTERVAL_SECONDS:
                continue

        user_last_log_time[username] = waktu_log_utc

        # Hitung login & IP per user
        user_login_counts[username] = user_login_counts.get(username, 0) + 1
        if username not in user_ips_used:
            user_ips_used[username] = set()
        user_ips_used[username].add(ip_address)

        # Geolocation
        country = get_country(ip_address, sumber)
        all_countries.add(country)
        ip_country_map[ip_address] = country

        # Konversi ke WIB
        waktu_log_wib = waktu_log_utc.astimezone(wib)
        all_entries.append((username, ip_address, waktu_log_wib))

        # Track IP + waktu per user (untuk Notes detail)
        if username not in user_ip_times:
            user_ip_times[username] = []
        user_ip_times[username].append((ip_address, waktu_log_wib))

    return all_entries, user_login_counts, user_ips_used, user_ip_times, ip_country_map, all_countries


def build_laporan(all_entries, user_login_counts, user_ips_used, user_ip_times, ip_country_map, all_countries, nama_pengirim):
    """Build laporan akhir siap copy-paste.
    Return: string laporan lengkap.
    """
    # logic list login terlama (tanggal mulai) di awal
    user_latest = {}
    for username, ip, waktu in all_entries:
        if username not in user_latest or waktu > user_latest[username][2]:
            user_latest[username] = (username, ip, waktu)

    sorted_entries = sorted(user_latest.values(), key=lambda x: x[2])

    laporan_logins = []
    for username, ip, waktu in sorted_entries:
        format_waktu = waktu.strftime("%b %#d, %Y @ %H:%M")  # %#d khusus Windows
        laporan_logins.append(f"- {username} connected from {ip} at {format_waktu}")

    teks_detail = "\n".join(laporan_logins)

    # NOTES
    notes_section = []

    # Multiple logins
    multiple_users = [user for user, count in user_login_counts.items() if count > 1]
    if multiple_users:
        notes_section.append("\nUser with multiple login sessions:")
        for user in multiple_users:
            count = user_login_counts[user]
            # Build detail: skip IP jika sama dengan sebelumnya
            ip_time_parts = []
            last_ip = None
            for ip, waktu in user_ip_times[user]:
                jam_str = waktu.strftime("%H:%M")
                if ip != last_ip:
                    ip_time_parts.append(f"{ip}:@{jam_str}")
                    last_ip = ip
                else:
                    ip_time_parts.append(f"@{jam_str}")
            detail = " ; ".join(ip_time_parts)
            notes_section.append(f"-{user} ({count}x login, IPs: {detail})")

    # Geolocation: user dari luar Indonesia
    non_id_entries = []
    for username, ip, waktu in all_entries:
        country = ip_country_map.get(ip, "Unknown")
        if country.lower() != "indonesia":
            non_id_entries.append((username, ip, country, waktu))

    if non_id_entries:
        notes_section.append("\nAll IPs are confirmed to be from Indonesia, but there are users who log in from other countries.")
        # Group per user: hanya tampilkan user, IP unik, dan negara
        foreign_users = {}
        for username, ip, country, waktu in non_id_entries:
            if username not in foreign_users:
                foreign_users[username] = {"ips": set(), "country": country}
            foreign_users[username]["ips"].add(ip)
        for user, info in foreign_users.items():
            ips = ", ".join(info["ips"])
            notes_section.append(f"- {user} ({ips}, {info['country']})")
    else:
        # Semua Indonesia
        notes_section.append("\n- All IP addresses are located in Indonesia.")

    teks_notes = "\n".join(notes_section)

    # PESAN NYA
    laporan = f"""Dear RHPetrogas Team,

Several VPN login activities have been detected originating from remote IP addresses, including access occurring outside of standard working hours.

Detail as follow:

{teks_detail}

Notes:{teks_notes}

Thank you.
Regards,
{nama_pengirim}"""

    return laporan
