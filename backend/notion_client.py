import requests
import os
from datetime import datetime
from typing import Optional, Tuple

class NotionClient:
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.page_id = os.getenv("NOTION_PAGE_ID")
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def add_qa_block(self, question: str, answer: str) -> Tuple[bool, Optional[str]]:
        """
        Add a Question and Answer block to the Notion page and return the new block ID.
        """
        try:
            url = f"{self.base_url}/blocks/{self.page_id}/children"

            qa_text = f"Q: {question}\n\nA: {answer}\n\n---"

            payload = {
                "children": [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": qa_text
                                    }
                                }
                            ]
                        }
                    }
                ]
            }

            response = requests.patch(url, json=payload, headers=self.headers, timeout=10)

            if response.status_code == 200:
                block_id = self._find_last_block_id_by_text(qa_text)
                return True, block_id
            else:
                print(f"Notion API error: {response.status_code} - {response.text}")
                return False, None
        except Exception as e:
            print(f"Error adding to Notion: {str(e)}")
            return False, None

    def _find_last_block_id_by_text(self, qa_text: str) -> Optional[str]:
        try:
            url = f"{self.base_url}/blocks/{self.page_id}/children"
            params = {"page_size": 100}
            next_cursor = None
            matching_id = None

            while True:
                if next_cursor:
                    params["start_cursor"] = next_cursor
                response = requests.get(url, headers=self.headers, params=params, timeout=10)
                if response.status_code != 200:
                    return None

                data = response.json()
                for block in data.get("results", []):
                    if block.get("type") != "paragraph":
                        continue

                    rich_text = block.get("paragraph", {}).get("rich_text", [])
                    content = "".join(
                        item.get("text", {}).get("content", "")
                        for item in rich_text
                        if item.get("type") == "text"
                    )

                    if content == qa_text:
                        matching_id = block.get("id")

                if not data.get("has_more"):
                    break

                next_cursor = data.get("next_cursor")

            return matching_id
        except Exception as e:
            print(f"Error finding block id: {str(e)}")
            return None

    def remove_block(self, block_id: str) -> bool:
        try:
            if not block_id:
                return False

            url = f"{self.base_url}/blocks/{block_id}"
            payload = {"archived": True}
            response = requests.patch(url, json=payload, headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error removing Notion block: {str(e)}")
            return False
    
    def check_connection(self) -> bool:
        """
        Check if Notion connection is valid
        """
        try:
            url = f"{self.base_url}/pages/{self.page_id}"
            response = requests.get(url, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False
