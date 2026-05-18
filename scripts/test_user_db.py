#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test user's database"""

import requests
from send_from_notion import get_notion_token

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    # User's database ID
    user_db_id = '3391859eb11280b9948cc1cbc77b46a3'
    
    print(f'Testing database: {user_db_id}')
    url = f'https://api.notion.com/v1/databases/{user_db_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        title = ''.join([t.get('plain_text', '') for t in data.get('title', [])])
        print(f'Success! Database Name: {title}')
        print('\nProperties:')
        for key, prop in data.get('properties', {}).items():
            print(f'  Key: "{key}"')
            print(f'  Type: {prop.get("type")}')
            print(f'  ID: {prop.get("id")}')
            
            if prop.get('type') == 'status':
                options = prop.get('status', {}).get('options', [])
                print('  Status options:')
                for opt in options:
                    print(f'    - "{opt.get("name")}"')
            print()
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

if __name__ == '__main__':
    main()