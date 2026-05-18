#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Notion content retrieval"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID, STATUS_FIELD, STATUS_COMPLETED, CONTENT_FIELD

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    response = requests.post(url, headers=headers, json={'page_size': 10})
    data = response.json()
    
    results = data.get('results', [])
    print(f'Total pages: {len(results)}')
    print()
    
    pending_count = 0
    empty_count = 0
    
    for page in results:
        props = page.get('properties', {})
        
        # Get status
        status_prop = props.get(STATUS_FIELD, {})
        status = status_prop.get('status', {}).get('name', 'EMPTY')
        
        # Get content from CONTENT_FIELD
        content_prop = props.get(CONTENT_FIELD, {})
        title_data = content_prop.get('title', [])
        content_text = "".join([t.get("plain_text", "") for t in title_data]).strip()
        
        # Fallback to page title
        if not content_text:
            title_prop = props.get("title", {})
            title_data = title_prop.get("title", [])
            content_text = "".join([t.get("plain_text", "") for t in title_data]).strip()
        
        print(f'Status: "{status}" | Content: {"[EMPTY]" if not content_text else content_text[:50]}')
        
        if status != STATUS_COMPLETED and content_text:
            pending_count += 1
        if not content_text:
            empty_count += 1
    
    print(f'\nSummary: {pending_count} pending items, {empty_count} empty items')

if __name__ == '__main__':
    main()