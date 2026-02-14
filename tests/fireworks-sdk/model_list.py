import requests
import os
import dotenv
dotenv.load_dotenv()
account_id = "motielmakyes-cgqngz7"

import requests

url = "https://api.fireworks.ai/inference/v1/workflows/accounts/fireworks/models/flux-kontext-pro/get_result"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('FIREWORKS_API_KEY')}",
}
data = {
    id: "request_id"
}

response = requests.post(url, headers=headers, json=data)

print(response.text)