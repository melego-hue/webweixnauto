#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check Notion database fields with their IDs"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}'
    response = requests.get(url, headers=headers)
    data = response.json()
    
    print('Database Properties (Name -> ID -> Type):')
    props = data.get('properties', {})
    for key in props:
        prop_type = props[key].get('type')
        prop_id = props[key].get('id')
        print(f'  "{key}" -> "{prop_id}" -> {prop_type}')
        
        if prop_type == 'status':
            options = props[key].get('status', {}).get('options', [])
            print('    Status options:')
            for opt in options:
                print(f'      - "{opt.get("name")}" -> "{opt.get("id")}"')

if __name__ == '__main__':
    main()