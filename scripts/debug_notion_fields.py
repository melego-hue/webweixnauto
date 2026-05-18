#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug Notion database fields"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID

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
    
    print('=== Database Properties ===')
    props = data.get('properties', {})
    for key in props:
        prop = props[key]
        prop_type = prop.get('type')
        print(f'\nName: "{key}"')
        print(f'Type: {prop_type}')
        print(f'ID: {prop.get("id")}')
        
        if prop_type == 'status':
            options = prop.get('status', {}).get('options', [])
            print('Options:')
            for opt in options:
                print(f'  - "{opt.get("name")}"')

if __name__ == '__main__':
    main()