from app import app
import json
import pandas as pd

with app.test_client() as client:
    apply_payload = {'name':'Automated Test','phone':'9999999999','email':'auto@test.local','college':'Test University','resume':'https://example.com/resume','role':'Full Stack'}
    r = client.post('/apply', json=apply_payload)
    print('Apply response:', r.status_code, r.get_json())

    submit_payload = {'name':'Visitor Test','email':'visitor@test.local','interest':'Partnership','message':'Hello from automated test'}
    r2 = client.post('/submit', json=submit_payload)
    print('Submit response:', r2.status_code, r2.get_json())

print('\nChecking Excel files...')
for f in ['applications.xlsx','messages.xlsx']:
    try:
        df = pd.read_excel(f)
        print('\n---', f, '---')
        print(df.tail(5).to_string(index=False))
    except Exception as e:
        print('Failed to read', f, e)
