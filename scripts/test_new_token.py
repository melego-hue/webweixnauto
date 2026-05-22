#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test new Notion token and find databases"""

import requests

def main():
    new_token = 'ntn_p65367370428mJhjCSr1SHNrMVxmqVwQFTjx3zBG0cl5xc'
    headers = {
        'Authorization': f'Bearer {new_token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    print(f'Testing new token...')
    
    # List all databases
    url = 'https://api.notion.com/v1/search'
    response = requests.post(url, headers=headers, json={
        'filter': {'property': 'object', 'value': 'database'},
        'page_size': 20
    })
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('results', [])
        
        print(f'\nFound {len(results)} databases:')
        for db in results:
            title = ''.join([t.get('plain_text', '') for t in db.get('title', [])])
            db_id = db.get('id', '')
            print(f'\nName: "{title}"')
            print(f'ID: {db_id}')
            
            # Get database properties
            db_url = f'https://api.notion.com/v1/databases/{db_id}'
            db_response = requests.get(db_url, headers=headers)
            if db_response.status_code == 200:
                db_data = db_response.json()
                print('Properties:')
                for key, prop in db_data.get('properties', {}).items():
                    print(f'  "{key}": {prop.get("type")}')
                    
                    if prop.get('type') == 'status':
                        options = prop.get('status', {}).get('options', [])
                        print('    Status options:')
                        for opt in options:
                            print(f'      - "{opt.get("name")}"')
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

if __name__ == '__main__':
    main()