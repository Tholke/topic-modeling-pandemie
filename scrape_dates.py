import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import json

def convert_date(date: str) -> dict:
    date_dict = {}

    date_regex = re.compile('(?P<date>(\d+\.){2}\d+) (?P<time>\d+\:\d+)')
    date_match = date_regex.match(date)

    day, month, year = date_match.group('date').split('.')

    date_dict['year'] = int(year)
    date_dict['month'] = int(month)
    date_dict['day'] = int(day)
    date_dict['time'] = date_match.group('time')

    return date_dict

if __name__=='__main__':
    SCRAPE_URL = 'https://www.ndr.de/nachrichten/info/podcast4684.html'
    SAVE_DIR = 'pdfs/'
    JSON_PATH = 'json.json'

    site = requests.get(SCRAPE_URL)
    soup = BeautifulSoup(site.text, 'html.parser')

    divs = soup.findAll('div', class_='teaserpadding')

    pdf_list = []
    with open(JSON_PATH, 'r') as json_file:
        pdf_list = json.load(json_file)

        for div in divs:
            title = div.h2.a.text
            title = title.strip()

            re_id = re.compile('\(\d+\)')
            id = re_id.match(title)

            if id == None:
                continue
            else:
                id = id.group(0)[1:-1]
            for desc in div.descendants:
                if desc.name == 'div' and 'date' in desc.get('class'):
                    date = convert_date(desc.text)

                    for pdf in pdf_list:
                        if pdf['id'] == id:
                            pdf['date'] = date
                            break

    with open(JSON_PATH, 'w') as json_file:
        json.dump(pdf_list, json_file, indent = 2, ensure_ascii=False)
