import json
import urllib.request
from urllib.error import HTTPError, URLError

url = 'http://127.0.0.1:8000/api/posts/3/'

# Preflight OPTIONS
options_headers = {
    'Origin': 'http://localhost:3000',
    'Access-Control-Request-Method': 'PATCH',
    'Access-Control-Request-Headers': 'authorization,content-type',
}
req = urllib.request.Request(url, method='OPTIONS', headers=options_headers)
print('--- OPTIONS preflight ---')
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print('status', r.status)
        print('headers:')
        for k, v in r.headers.items():
            if 'access-control' in k.lower():
                print(f'{k}: {v}')
        print('body:', r.read().decode('utf-8'))
except HTTPError as e:
    print('status', e.code)
    print('headers:')
    for k, v in e.headers.items():
        if 'access-control' in k.lower():
            print(f'{k}: {v}')
    print('body:', e.read().decode('utf-8'))
except URLError as e:
    print('url error', e)
except Exception as e:
    print(type(e).__name__, e)

# Actual PATCH request
patch_data = json.dumps({'title': 'trial', 'description': 'yo ho ni para hghghffffffd'}).encode('utf-8')
patch_headers = {
    'Origin': 'http://localhost:3000',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1NzU1NjA1LCJpYXQiOjE3ODUxNTA4MDUsImp0aSI6IjI2MmYwY2FjNjU2MTRkYmM5YjQyMTllYWIxYzg5NGIyIiwidXNlcl9pZCI6IjIifQ.ZTtooCm7oBwlrhzmtXkGKZ3M0LORUvaY-hSynz3aI9g',
    'Content-Type': 'application/json',
}
req = urllib.request.Request(url, data=patch_data, method='PATCH', headers=patch_headers)
print('\n--- PATCH request ---')
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print('status', r.status)
        print('headers:')
        for k, v in r.headers.items():
            if 'access-control' in k.lower():
                print(f'{k}: {v}')
        print('body:', r.read().decode('utf-8'))
except HTTPError as e:
    print('status', e.code)
    print('headers:')
    for k, v in e.headers.items():
        if 'access-control' in k.lower():
            print(f'{k}: {v}')
    print('body:', e.read().decode('utf-8'))
except URLError as e:
    print('url error', e)
except Exception as e:
    print(type(e).__name__, e)
