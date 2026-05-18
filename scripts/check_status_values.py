#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check actual status values in database"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID, STATUS_FIELD_ID

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    response = requests.post(url, headers=headers, json={'page_size': 5})
    data = response.json()
    
    results = data.get('results', [])
    print(f'Found {len(results)} pages')
    print()
    
    for i, page in enumerate(results):
        props = page.get('properties', {})
        
        # Get status
        status_prop = props.get(STATUS_FIELD_ID, {})
        status = status_prop.get('status', {}).get('name', 'EMPTY')
        
        # Get content
        content_prop = props.get('title', {})
        title_data = content_prop.get('title', [])
        content = "".join([t.get("plain_text", "") for t in title_data])[:50]
        
        print(f'Page {i+1}:')
        print(f'  Status: "{status}"')
        print(f'  Content: "{content}"')
        print()

if __name__ == '__main__':
    main()