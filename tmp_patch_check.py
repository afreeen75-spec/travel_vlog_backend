import json
import urllib.request
from urllib.error import HTTPError, URLError

url = 'http://127.0.0.1:8000/api/posts/3/'
data = json.dumps({'title': 'trial', 'description': 'yo ho ni para hghgh'}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='PATCH', headers={
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1NzU1NjA1LCJpYXQiOjE3ODUxNTA4MDUsImp0aSI6IjI2MmYwY2FjNjU2MTRkYmM5YjQyMTllYWIxYzg5NGIyIiwidXNlcl9pZCI6IjIifQ.ZTtooCm7oBwlrhzmtXkGKZ3M0LORUvaY-hSynz3aI9g'
})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        print('status', r.status)
        print(r.read().decode('utf-8'))
except HTTPError as e:
    print('status', e.code)
    print(e.read().decode('utf-8'))
except URLError as e:
    print('url error', e)
except Exception as e:
    print(type(e).__name__, e)
