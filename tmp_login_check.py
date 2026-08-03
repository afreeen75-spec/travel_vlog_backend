import json
import urllib.request

payload = json.dumps({'username': 'Aayesha', 'password': 'Aayesha123'}).encode()
req = urllib.request.Request('http://127.0.0.1:8000/api/login/', data=payload, headers={'Content-Type': 'application/json'})
try:
    with urllib.request.urlopen(req, timeout=20) as response:
        print('status', response.status)
        print(response.read().decode())
except Exception as exc:
    print(type(exc).__name__, exc)
