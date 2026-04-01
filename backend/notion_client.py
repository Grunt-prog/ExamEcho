import requests
import os
from datetime import datetime

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
    
    def add_qa_block(self, question: str, answer: str) -> bool:
        """
        Add a Question and Answer block to the Notion page
        """
        try:
            url = f"{self.base_url}/blocks/{self.page_id}/children"
            
            # Create a text block with Q&A (no markdown formatting)
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
                return True
            else:
                print(f"Notion API error: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            print(f"Error adding to Notion: {str(e)}")
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
