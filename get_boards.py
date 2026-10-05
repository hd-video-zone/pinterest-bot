import os
import requests

TOKEN = os.environ.get("PINTEREST_TOKEN")

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

res = requests.get("https://api.pinterest.com/v5/boards", headers=headers)
data = res.json()

print("Status Code:", res.status_code)
if "items" in data:
    for b in data["items"]:
        print(f"Board Name: {b['name']} ===> Board ID: {b['id']}")
else:
    print("Response Data:", data)
