#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug actual page data"""

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
    response = requests.post(url, headers=headers, json={'page_size': 3})
    data = response.json()
    
    results = data.get('results', [])
    for page in results[:3]:
        print('=' * 60)
        props = page.get('properties', {})
        
        print('\nAll property keys:')
        for key in props:
            print(f'  "{key}"')
        
        print('\nStatus field content:')
        status_field = props.get('鍙戝竷鐘舵€?', {})
        print(f'  Full status field: {status_field}')
        
        print('\nContent field content:')
        content_field = props.get('AI鏈嬪弸鍦堟枃妗?', {})
        print(f'  Full content field: {content_field}')

if __name__ == '__main__':
    main()