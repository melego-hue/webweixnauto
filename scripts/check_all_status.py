#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check all status values in database"""

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
    response = requests.post(url, headers=headers, json={'page_size': 50})
    data = response.json()
    
    results = data.get('results', [])
    print(f'Found {len(results)} pages')
    print()
    
    status_counts = {}
    
    for i, page in enumerate(results):
        props = page.get('properties', {})
        
        # Get status
        status_prop = props.get(STATUS_FIELD_KEY, {})
        status = status_prop.get('status', {}).get('name', 'EMPTY')
        
        # Count status values
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print('Status distribution:')
    for status, count in status_counts.items():
        print(f'  "{status}": {count} pages')

if __name__ == '__main__':
    main()