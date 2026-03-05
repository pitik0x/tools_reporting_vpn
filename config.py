import os
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("OPENSEARCH_URL", "https://10.30.1.161:9200")
INDEX_PATTERN = os.getenv("OPENSEARCH_INDEX_PATTERN", "wazuh-alerts-*")
USERNAME = os.getenv("OPENSEARCH_USERNAME")
PASSWORD = os.getenv("OPENSEARCH_PASSWORD")

RULE_DESCRIPTION = "Fortigate: VPN user connected."
EXCLUDED_USERS = ["soc"]
MAX_RESULTS = 1000

TIMEZONE = "Asia/Jakarta"
MIN_LOGIN_INTERVAL_SECONDS = 60  # Filter login biar gak duplikat dalam rentang detik 
