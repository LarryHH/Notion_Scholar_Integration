""" Notion Integration Manager """

import inspect
import json
from configparser import ConfigParser
from difflib import SequenceMatcher
import requests

import scholar as gs


def print_rest_status(res):
    """prints REST API call status and func that calls it"""
    print(
        f"--- {res.status_code} - {res.reason} from: {inspect.stack()[1][3]} ---")
    # print(res.text)
    # print('\n\n')


def read_db():
    """reads notion database and returns data"""
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    res = requests.request("POST", url, headers=HEADERS)
    print_rest_status(res)
    data = res.json()
    # with open('./db.json', 'w', encoding='utf8') as f:
    #     json.dump(data, f, ensure_ascii=False)
    return data


def format_authors(authors):
    """convert authors in list form into Notion multi-select property"""
    if authors:
        return [{"name": str(author)} for author in authors]
    return []


def format_venue(venue):
    """convert venue in str form into Notion select property"""
    if venue:
        return {"name": venue}
    return None


def format_link(link):
    """convert link in str form into Notion files property"""
    if link:
        return [
            {
                "name": link[:50],
                "external": {
                    "url": link
                }
            }
        ]
    return []


def create_page(name=None, authors=None, year=None, venue=None, link=None, citations=None):
    """create new database entry"""
    page = {
        "parent": {
            "database_id": NOTION_DATABASE_ID
        },
        "properties": {
            "Name": {
                "type": "title",
                "title": [{"text": {"content": name}}],
            },
            "Link": {
                "type": "files",
                "files": format_link(link)
            },
            "Topics": {
                "type": "multi_select",
                "multi_select": []
            },
            "Subtopics": {
                "type": "multi_select",
                "multi_select": []
            },
            "Authors": {
                "type": "multi_select",
                "multi_select": format_authors(authors)
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
                "number": citations
            },
            "Year": {
                "type": "number",
                "number": year
            },
            "Venue": {
                "type": "select",
                "select": format_venue(venue)
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

def bulk_add_to_db(scholar, papers):
    """add list of papers to Notion db"""
    for i, paper in enumerate(papers):
        print(f"--- PAPER INDEX: {i} ---\n{paper}")
        scholar.get_pub_by_title(paper)
        page = create_page(
            name=scholar.name,
            year=scholar.year,
            citations=scholar.citations,
            authors=scholar.authors,
            link=scholar.link,
            venue=scholar.venue
        )
        if not check_duplicate_page(db, page):
            add_page(page)

def read_papers_from_txt(fp):
    """read in a list of papers from text file"""
    with open(fp, encoding='utf8') as f:
        papers = f.read().splitlines() 
    return papers

def load_config(fp):
    """read notion credentials"""
    config = ConfigParser()
    config.read(fp)
    notion_db_id = config.get('NOTION', 'DATABASE_ID')
    notion_token = config.get('NOTION', 'INTEGRATION_TOKEN')
    scraperapi_key = config.get('SCRAPER_API', 'API_KEY')
    return notion_db_id, notion_token, scraperapi_key

if __name__ == "__main__":
    NOTION_DATABASE_ID, NOTION_INTEGRATION_TOKEN, SCRAPER_API_KEY = load_config('config.ini')
    HEADERS = {
        "Authorization": "Bearer " + NOTION_INTEGRATION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    db = read_db()
    papers = read_papers_from_txt('papers.txt')
    scholar = gs.Scholar(SCRAPER_API_KEY)
    bulk_add_to_db(scholar, papers)
    