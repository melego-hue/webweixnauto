#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Feishu Bitable (Lark Multidimensional Table) API Client
Supports fetching pending WeChat Moments and updating statuses
"""

import sys
import logging
import requests
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FeishuClient")


class FeishuBitableClient:
    """Client to interact with Feishu Bitable (Multidimensional Table) Open API"""

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self._tenant_access_token = None
        self._token_expires_at = 0

    def get_tenant_access_token(self):
        """Fetch tenant_access_token (internal app model)"""
        # Quick caching check
        import time
        if self._tenant_access_token and time.time() < self._token_expires_at:
            return self._tenant_access_token

        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to get tenant_access_token. HTTP Status: {response.status_code}")
                return None

            res_json = response.json()
            if res_json.get("code") != 0:
                logger.error(f"Feishu Auth Error: {res_json.get('msg')}")
                return None

            self._tenant_access_token = res_json.get("tenant_access_token")
            # Cache token for 1 hour (expires_in is typically 7200s, use 3500s buffer)
            expires_in = res_json.get("expire", 3600)
            self._token_expires_at = time.time() + expires_in - 100
            logger.info("Successfully fetched new tenant_access_token from Feishu")
            return self._tenant_access_token
        except Exception as e:
            logger.error(f"Connection error to Feishu Auth API: {e}")
            return None

    def fetch_records(self, app_token, table_id, filter_field=None, filter_value=None):
        """
        Fetch records from Feishu Bitable.
        Can optionally filter by field value (Note: Bitable filter syntax or manual filtering).
        We do client-side filtering for robust column-agnostic matching.
        """
        token = self.get_tenant_access_token()
        if not token:
            logger.error("Cannot fetch records without a valid tenant_access_token")
            return []

        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        records = []
        page_token = None
        has_more = True

        while has_more:
            params = {"page_size": 100}
            if page_token:
                params["page_token"] = page_token

            try:
                response = requests.get(url, headers=headers, params=params, timeout=15)
                if response.status_code != 200:
                    logger.error(f"Failed to fetch Bitable records. HTTP Status: {response.status_code}")
                    break

                res_json = response.json()
                if res_json.get("code") != 0:
                    logger.error(f"Feishu API Error: {res_json.get('msg')}")
                    break

                data = res_json.get("data", {})
                items = data.get("items", [])
                
                for item in items:
                    record_id = item.get("record_id")
                    fields = item.get("fields", {})
                    
                    # Apply client-side filter if specified
                    if filter_field and filter_value:
                        actual_val = fields.get(filter_field)
                        # Option values can be dict/list/string, convert to string comparison
                        if isinstance(actual_val, list):
                            actual_str = ",".join([str(v) for v in actual_val])
                        elif isinstance(actual_val, dict):
                            actual_str = str(actual_val.get("text", ""))
                        else:
                            actual_str = str(actual_val) if actual_val is not None else ""
                        
                        if actual_str.strip() != filter_value.strip():
                            continue
                            
                    records.append({
                        "record_id": record_id,
                        "fields": fields
                    })

                has_more = data.get("has_more", False)
                page_token = data.get("page_token")
            except Exception as e:
                logger.error(f"Error fetching Bitable records: {e}")
                break

        logger.info(f"Fetched {len(records)} matching records from Bitable table {table_id}")
        return records

    def update_record_status(self, app_token, table_id, record_id, status_field, status_value):
        """Update a specific record's status in Bitable"""
        token = self.get_tenant_access_token()
        if not token:
            logger.error("Cannot update status without a valid tenant_access_token")
            return False

        url = f"{self.base_url}/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # Bitable record update expects fields block
        payload = {
            "fields": {
                status_field: status_value
            }
        }

        try:
            response = requests.patch(url, headers=headers, json=payload, timeout=10)
            if response.status_code != 200:
                logger.error(f"Failed to update Bitable record. HTTP Status: {response.status_code}")
                return False

            res_json = response.json()
            if res_json.get("code") != 0:
                logger.error(f"Feishu API Update Error: {res_json.get('msg')}")
                return False

            logger.info(f"Successfully updated Bitable record {record_id}: {status_field} -> {status_value}")
            return True
        except Exception as e:
            logger.error(f"Connection error to Feishu Update API: {e}")
            return False


if __name__ == "__main__":
    # Standard quick dry run test with mock keys
    client = FeishuBitableClient("cli_mock_id", "mock_secret")
    print("FeishuBitableClient initialized successfully")
