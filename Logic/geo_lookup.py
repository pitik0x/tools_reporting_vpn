import requests
from collections import Counter

# Cache agar tidak spamming API eksternal untuk IP yang sama
_ip_country_cache = {}


def verify_with_external_apis(ip_address):
    results = []

    # ip-api.com (gratis, 45 req/menit)
    try:
        res = requests.get(f"http://ip-api.com/json/{ip_address}?fields=country", timeout=5)
        if res.status_code == 200:
            country = res.json().get("country")
            if country:
                results.append(country)
    except Exception:
        pass

    # ipapi.co (gratis, 1000 req/hari)
    try:
        res = requests.get(
            f"https://ipapi.co/{ip_address}/country_name/",
            timeout=5,
            headers={"User-Agent": "vpn-report-script"},
        )
        if res.status_code == 200 and len(res.text) < 100 and "error" not in res.text.lower():
            results.append(res.text.strip())
    except Exception:
        pass

    if results:
        most_common = Counter(results).most_common(1)[0][0]
        return most_common

    return None


def get_country(ip_address, data_sumber):
    """Ambil nama negara dari IP. Wazuh dulu, lalu verifikasi API jika bukan Indonesia."""

    # Cek cache
    if ip_address in _ip_country_cache:
        return _ip_country_cache[ip_address]

    # Cek data Wazuh
    wazuh_country = data_sumber.get('GeoLocation', {}).get('country_name')

    # Jika di Wazuh Indonesia skip tidak akan cek
    if wazuh_country and wazuh_country.lower() == 'indonesia':
        _ip_country_cache[ip_address] = wazuh_country
        return wazuh_country

    # Jika Wazuh di wazuh BUKAN Indonesia atau n/a → verifikasi API eksternal
    print(f"   [*] Verifikasi IP {ip_address} (Wazuh: {wazuh_country or 'N/A'}) dengan API eksternal...")
    verified_country = verify_with_external_apis(ip_address)

    if verified_country:
        if wazuh_country and wazuh_country.lower() != verified_country.lower():
            print(f"   [!] KOREKSI: IP {ip_address} -> Wazuh='{wazuh_country}', API Eksternal='{verified_country}' -> Pakai: {verified_country}")
        else:
            print(f"   [OK] Terkonfirmasi: IP {ip_address} -> {verified_country}")
        _ip_country_cache[ip_address] = verified_country
        return verified_country

    # Fallback ke data Wazuh jika semua API gagal
    if wazuh_country:
        print(f"   [!] API Eksternal gagal, fallback ke data Wazuh: {wazuh_country}")
        _ip_country_cache[ip_address] = wazuh_country
        return wazuh_country

    return "Unknown Country"
