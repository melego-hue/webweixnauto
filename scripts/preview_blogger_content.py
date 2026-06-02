#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Preview content from 路飞全自动发稿池V2.5"""

import sys
import requests

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def main():
    import os
    token = os.environ.get("NOTION_API_KEY") or "your_notion_api_token_here"
    db_id = os.environ.get("NOTION_DATABASE_ID") or "your_notion_database_id_here"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    response = requests.post(url, headers=headers, json={
        'sorts': [{'timestamp': 'created_time', 'direction': 'descending'}],
        'page_size': 5
    })
    
    results = response.json().get('results', [])
    
    for i, page in enumerate(results, 1):
        props = page.get('properties', {})
        
        # Get status
        status = props.get('平台/状态', {}).get('status', {}).get('name', '')
        
        # Skip if not pending
        if status != '未开始':
            continue
        
        # Get title
        title_prop = props.get('名称', {})
        title_data = title_prop.get('title', [])
        title = ''.join([t.get('plain_text', '') for t in title_data])
        
        # Get content
        content_prop = props.get('AI朋友圈金句', {})
        rich_text_data = content_prop.get('rich_text', [])
        content = ''.join([t.get('plain_text', '') for t in rich_text_data])
        
        if content:
            # Save to file
            filename = f'blogger_content_{i}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f'标题: {title}\n')
                f.write(f'状态: {status}\n')
                f.write(f'内容:\n{content}')
            print(f'Saved to: {filename}')

if __name__ == '__main__':
    main()