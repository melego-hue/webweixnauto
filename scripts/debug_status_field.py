#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug status field structure"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID, STATUS_FIELD

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    # Get database structure
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}'
    response = requests.get(url, headers=headers)
    data = response.json()
    
    props = data.get('properties', {})
    
    print(f'Checking field: "{STATUS_FIELD}"')
    if STATUS_FIELD in props:
        prop = props[STATUS_FIELD]
        print(f'Type: {prop.get("type")}')
        print(f'ID: {prop.get("id")}')
        
        if prop.get('type') == 'status':
            options = prop.get('status', {}).get('options', [])
            print('Status options:')
            for opt in options:
                print(f'  - "{opt.get("name")}"')
    else:
        print(f'Field "{STATUS_FIELD}" not found!')
        print('Available fields:')
        for key in props:
            print(f'  - "{key}"')

if __name__ == '__main__':
    main()