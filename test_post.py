import json
import urllib.request

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8')
            print('URL:', url)
            print('Status:', resp.getcode())
            print('Body:', body)
    except Exception as e:
        print('Request failed for', url, e)

post('http://localhost:5000/apply', {'name':'Automated Test','phone':'9999999999','email':'auto@test.local','college':'Test University','resume':'https://example.com/resume','role':'Full Stack'})
post('http://localhost:5000/submit', {'name':'Visitor Test','email':'visitor@test.local','interest':'Partnership','message':'Hello from automated test'})
