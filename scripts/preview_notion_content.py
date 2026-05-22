#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Preview Notion content in proper Chinese encoding"""

import sys
import requests
from send_from_notion import get_notion_token, DATABASE_ID, STATUS_FIELD_ID, CONTENT_FIELD_ID

def main():
    token = get_notion_token()
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28',
    }

    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    response = requests.post(url, headers=headers, json={
        'sorts': [{'timestamp': 'created_time', 'direction': 'descending'}],
        'page_size': 5
    })
    
    data = response.json()
    results = data.get('results', [])
    
    print(f'找到 {len(results)} 条待发布内容\n')
    
    for i, page in enumerate(results, 1):
        props = page.get('properties', {})
        
        # Get status
        status = ''
        for key in props:
            if props[key].get('id') == STATUS_FIELD_ID:
                status = props[key].get('status', {}).get('name', '')
                break
        
        # Skip if already published
        if status == '宸插彂甯?':
            continue
        
        # Get content
        content = ''
        for key in props:
            if props[key].get('id') == CONTENT_FIELD_ID:
                title_data = props[key].get('title', [])
                content = ''.join([t.get('plain_text', '') for t in title_data])
                break
        
        if content:
            print(f'--- 第 {i} 条 ---')
            print(f'状态: {status}')
            print(f'内容: {content}')
            print()
            
            # Save to file for proper viewing
            with open(f'temp_content_{i}.txt', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'已保存到: temp_content_{i}.txt\n')

if __name__ == '__main__':
    main()