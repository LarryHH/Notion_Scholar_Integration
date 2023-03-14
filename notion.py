""" Notion Integration Manager """

import inspect
import json
from configparser import ConfigParser
from difflib import SequenceMatcher

import requests

# import parse_titles as pt
# import scholar as gs


def print_rest_status(res):
    """prints REST API call status and func that calls it"""
    print(
        f"--- {res.status_code} - {res.reason} from: {inspect.stack()[1][3]} ---")
    print(res.text)


def read_db():
    """reads notion database and returns data"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    res = requests.request("POST", url, headers=HEADERS)
    print_rest_status(res)
    data = res.json()
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)
    return data


def create_page():
    """create new database entry"""
    page = {
        "parent": {
            "database_id": DATABASE_ID
        },
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"text": {"content": "TEST"}}],
            },
            "Link": {
                "type": "files",
                "files": []
            },
            "Topics": {
                "type": "multi_select",
                "multi_select": []
            },
            "Subtopics": {
                "type": "multi_select",
                "multi_select": []
            },
            "Type": {
                "type": "select",
                "select": None
            },
            "Priority": {
                "type": "select",
                "select": None
            },
            "Citations": {
                "type": "number",
                "number": 42
            },
            "Venue": {
                "type": "rich_text",
                "rich_text": []
            },
            "Status": {
                "type": "status",
                "status": {
                    "name": "Not started"
                }
            },
            "Short Notes": {
                "type": "rich_text",
                "rich_text": []
            },
        }
    }
    return page


def check_duplicate_page(db, page):
    """check if proposed db entry titles is similar to entry already in db"""
    res_titles = [res['properties']['Name']['title']
                  for res in db['results'] if res['properties']['Name']['title']]
    titles = []
    for title in res_titles:
        titles.append(''.join([t['plain_text']
                      for t in title]).replace("\n", " "))

    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    for t in titles:
        score = similar(page['properties']['Name']
                        ['title'][0]['text']['content'], t)
        print(score)
        if score > 0.95:
            return True
    return False


def add_page(page):
    """adds created page to db, provided it passes similarity check"""
    url = 'https://api.notion.com/v1/pages'
    data = json.dumps(page)
    res = requests.request("POST", url, headers=HEADERS, data=data)
    print_rest_status(res)


def load_config_notion(fp):
    """read notion credentials"""
    config = ConfigParser()
    config.read(fp)
    db_id = config.get('NOTION', 'DATABASE_ID')
    token = config.get('NOTION', 'INTEGRATION_TOKEN')
    return db_id, token

if __name__ == "__main__":
    db_id, token = load_config_notion('config.ini')
    INTEGRATION_TOKEN = db_id
    DATABASE_ID = token
    HEADERS = {
        "Authorization": "Bearer " + INTEGRATION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    db = read_db()
    pages = [create_page()]
    add_page(pages[0])
    # for page in pages:
    #     if not check_duplicate_page(db, page):
    #         add_page(page)
