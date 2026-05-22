#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug key matching issue"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID, STATUS_FIELD_KEY

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    response = requests.post(url, headers=headers, json={'page_size': 1})
    data = response.json()
    
    if data.get('results'):
        page = data['results'][0]
        props = page.get('properties', {})
        
        print(f"Defined STATUS_FIELD_KEY: {repr(STATUS_FIELD_KEY)}")
        print(f"Defined STATUS_FIELD_KEY type: {type(STATUS_FIELD_KEY)}")
        print()
        
        print("Available property keys:")
        for key in props:
            print(f"  Key: {repr(key)}")
            print(f"  Key type: {type(key)}")
            print(f"  Key == STATUS_FIELD_KEY: {key == STATUS_FIELD_KEY}")
            print(f"  Key id: {props[key].get('id')}")
            
            if props[key].get('type') == 'status':
                status_data = props[key].get('status', {})
                print(f"  Status name: {repr(status_data.get('name'))}")
                print(f"  Status id: {repr(status_data.get('id'))}")
            print()

if __name__ == '__main__':
    main()