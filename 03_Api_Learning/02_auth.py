import requests

# ============================================================
#  Auth
# ============================================================

# --- GET ---
url = "https://httpbin.org/basic-auth/myuser/mypassword"

response = requests.get(url, auth=("myuser", "mypassword"))

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")

# --- GET ---
url = "https://httpbin.org/bearer"
token = "my-secret-token"

response = requests.get(url, headers={"Authorization": f"Bearer {token}"})

print(f"狀態碼: {response.status_code}")
print(f"回應內容: {response.json()}")


