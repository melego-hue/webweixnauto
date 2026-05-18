#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug property keys"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID

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
        
        print('Property keys:')
        for key in props:
            print(f"Key: {repr(key)}")
            print(f"Type: {type(key)}")
            print(f"Value type: {props[key].get('type')}")
            if props[key].get('type') == 'status':
                status_value = props[key].get('status', {})
                print(f"Status name: {repr(status_value.get('name'))}")
            print()

if __name__ == '__main__':
    main()