import requests
import time
from random import randint

def make_request(url, headers=None, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException:
            wait_time = randint(1, 3) * (2 ** i)  # Exponential backoff
            if i < retries - 1:
                time.sleep(wait_time)
            else:
                return None
