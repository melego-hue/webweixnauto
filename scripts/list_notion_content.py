#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""List all content in Notion database"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID, STATUS_FIELD

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    response = requests.post(url, headers=headers, json={'page_size': 50})
    data = response.json()
    
    results = data.get('results', [])
    print(f'Total pages found: {len(results)}')
    print()
    
    for i, page in enumerate(results, 1):
        props = page.get('properties', {})
        
        # Get status
        status_prop = props.get(STATUS_FIELD, {})
        status = status_prop.get('status', {}).get('name', 'Unknown')
        
        # Get title/content
        content_prop = props.get('AI鏈嬪弸鍦堟枃妗?', {})
        title_data = content_prop.get('title', [])
        content = ''.join([t.get('plain_text', '') for t in title_data])
        
        print(f'{i}. Status: "{status}"')
        print(f'   Content: {content[:100]}...')
        print()

if __name__ == '__main__':
    main()