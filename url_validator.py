# Block 2: Input handler URL validator
import re
import requests

def valid_url(url):
    return bool(re.match(r"^(http|https)://", url))

def is_reachable(url):
    try:
        resp = requests.head(url, allow_redirects=True, timeout=5)
        return resp.status_code < 400
    except requests.RequestException:
        return False