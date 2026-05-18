#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check Notion database structure"""

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
    
    print('Database Properties:')
    props = data.get('properties', {})
    for key in props:
        prop_type = props[key].get('type')
        print(f'  {key}: {prop_type}')
        
        # Check status options
        if prop_type == 'status':
            options = props[key].get('status', {}).get('options', [])
            print('    Status options:')
            for opt in options:
                print(f'      - {opt.get("name")}')

if __name__ == '__main__':
    main()