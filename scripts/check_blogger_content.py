#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check if database has blogger-specific content"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID, CONTENT_FIELD_ID

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        title = ''.join([t.get('plain_text', '') for t in data.get('title', [])])
        print(f'Database Name: {title}')
        print()
        print('Available fields:')
        for key, prop in data.get('properties', {}).items():
            print(f'  "{key}": {prop.get("type")}')
    else:
        print(f'Error: {response.status_code}')

if __name__ == '__main__':
    main()