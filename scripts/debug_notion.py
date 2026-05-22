#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug Notion database structure"""

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
        print('Page properties structure:')
        print('=' * 50)
        props = page.get('properties', {})
        for key, value in props.items():
            print(f'\nKey: "{key}"')
            print(f'Type: {value.get("type")}')
            print(f'Full value: {value}')

if __name__ == '__main__':
    main()