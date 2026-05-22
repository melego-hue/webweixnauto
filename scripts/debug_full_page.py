#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug full page data"""

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
        print('Full page data:')
        print('=' * 60)
        print(page)

if __name__ == '__main__':
    main()