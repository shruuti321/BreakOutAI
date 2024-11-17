import requests

url = "http://127.0.0.1:5000/perform_search"
payload = {
    "queries": ["nextq", "Panacea"]
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print("Response Status Code:", response.status_code)
print("Response JSON:", response.json())