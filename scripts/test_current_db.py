#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test current database structure"""

import requests
from send_from_notion import get_notion_token, DATABASE_ID

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        title = ''.join([t.get('plain_text', '') for t in data.get('title', [])])
        print(f'Database Name: {title}')
        print()
        print('Available fields:')
        for key, prop in data.get('properties', {}).items():
            print(f'  "{key}": {prop.get("type")} (ID: {prop.get("id")})')
            
            if prop.get('type') == 'status':
                options = prop.get('status', {}).get('options', [])
                print('    Status options:')
                for opt in options:
                    print(f'      - "{opt.get("name")}"')
        print()
        
        # Get sample data
        print('Sample content (first 3 pages):')
        url_query = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
        response_query = requests.post(url_query, headers=headers, json={'page_size': 3})
        results = response_query.json().get('results', [])
        
        for i, page in enumerate(results, 1):
            print(f'\nPage {i}:')
            for key, prop in page.get('properties', {}).items():
                if prop.get('type') == 'title':
                    content = ''.join([t.get('plain_text', '') for t in prop.get('title', [])])
                    print(f'  Content: {content[:80]}...')
                elif prop.get('type') == 'status':
                    status = prop.get('status', {}).get('name', '')
                    print(f'  Status: {status}')
                    
    else:
        print(f'Error: {response.status_code}')
        print(response.text)

if __name__ == '__main__':
    main()