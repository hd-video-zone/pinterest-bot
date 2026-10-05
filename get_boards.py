import os
import requests

TOKEN = os.environ.get("PINTEREST_TOKEN", "").strip()

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Try Production
print("Testing Production...")
res_prod = requests.get("https://api.pinterest.com/v5/boards", headers=headers)
print("Prod Status:", res_prod.status_code, res_prod.text)

# 2. Try Sandbox
print("\nTesting Sandbox...")
res_sand = requests.get("https://api-sandbox.pinterest.com/v5/boards", headers=headers)
print("Sandbox Status:", res_sand.status_code, res_sand.text)
