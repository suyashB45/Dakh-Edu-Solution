import pandas as pd
import os

files = ['applications.xlsx', 'messages.xlsx']
for f in files:
    print('\n---', f, '---')
    if not os.path.exists(f):
        print('File not found')
        continue
    try:
        df = pd.read_excel(f)
        if df.empty:
            print('No rows')
        else:
            print(df.tail(5).to_string(index=False))
    except Exception as e:
        print('Failed to read', f, e)
