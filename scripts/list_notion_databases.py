#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List all databases in Notion workspace"""

import requests
from send_from_notion import get_notion_token

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = 'https://api.notion.com/v1/search'
    response = requests.post(url, headers=headers, json={
        'filter': {'property': 'object', 'value': 'database'},
        'page_size': 20
    })
    
    data = response.json()
    results = data.get('results', [])
    
    print(f'Found {len(results)} databases:')
    print()
    
    for db in results:
        title = db.get('title', [])
        title_text = ''.join([t.get('plain_text', '') for t in title])
        db_id = db.get('id', '')
        print(f'Name: "{title_text}"')
        print(f'ID: {db_id}')
        print()

if __name__ == '__main__':
    main()