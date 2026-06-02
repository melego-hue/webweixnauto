#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check database structure and content"""

import sys
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import requests

def main():
    import os
    from pathlib import Path
    token = os.environ.get("NOTION_API_KEY")
    db_id = os.environ.get("NOTION_DATABASE_ID")
    
    if not token or not db_id:
        env_path = Path("d:/AIWork/.env")
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8-sig") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("NOTION_API_KEY="):
                            token = line.split("=", 1)[1].strip()
                        elif line.startswith("NOTION_DATABASE_ID="):
                            db_id = line.split("=", 1)[1].strip()
            except:
                pass
                
    token = token or "your_notion_token_here"
    db_id = db_id or "your_notion_db_id_here"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    print("=== Database Structure ===")
    url = f'https://api.notion.com/v1/databases/{db_id}'
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        title = ''.join([t.get('plain_text', '') for t in data.get('title', [])])
        print(f'Database Name: {title}')
        print()
        print('Available Fields:')
        for key, prop in data.get('properties', {}).items():
            print(f'  Name: "{key}"')
            print(f'  Type: {prop.get("type")}')
            print(f'  ID: {prop.get("id")}')
            if prop.get('type') == 'status':
                options = prop.get('status', {}).get('options', [])
                print('  Options:')
                for opt in options:
                    print(f'    - "{opt.get("name")}"')
            print()
    
    print("\n=== Sample Content ===")
    url_query = f'https://api.notion.com/v1/databases/{db_id}/query'
    response_query = requests.post(url_query, headers=headers, json={'page_size': 3})
    
    if response_query.status_code == 200:
        results = response_query.json().get('results', [])
        print(f'Found {len(results)} pages')
        
        for i, page in enumerate(results, 1):
            print(f'\nPage {i}:')
            props = page.get('