import os
from dotenv import load_dotenv
import requests

load_dotenv()

api_key = os.getenv("NOTION_API_KEY")
page_id = os.getenv("NOTION_PAGE_ID")

print(f"API Key: {api_key[:20]}...")
print(f"Page ID: {page_id}")

# Check if page_id needs to be formatted (remove hyphens)
page_id_no_hyphens = page_id.replace('-', '')
print(f"Page ID (no hyphens): {page_id_no_hyphens}")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Test 1: With hyphens
print("\n--- Testing with hyphens ---")
url1 = f"https://api.notion.com/v1/pages/{page_id}"
try:
    response1 = requests.get(url1, headers=headers, timeout=5)
    print(f"Status: {response1.status_code}")
    print(f"Response: {response1.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Without hyphens
print("\n--- Testing without hyphens ---")
url2 = f"https://api.notion.com/v1/pages/{page_id_no_hyphens}"
try:
    response2 = requests.get(url2, headers=headers, timeout=5)
    print(f"Status: {response2.status_code}")
    print(f"Response: {response2.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
