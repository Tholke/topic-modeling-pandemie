import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import json

if __name__=='__main__':
    BASE_URL = 'https://www.ndr.de'
    SCRAPE_URL = BASE_URL + '/nachrichten/info/Coronavirus-Update-Die-Podcast-Folgen-als-Skript,podcastcoronavirus102.html'
    SAVE_DIR = 'pdfs/'
    JSON_PATH = 'json.json'

    site = requests.get(SCRAPE_URL)
    soup = BeautifulSoup(site.text, 'html.parser')

    divs = soup.findAll('div', class_='teaserpadding')

    pdfs = []
    for div in divs:
        title = div.h2.a.text
        title = title.strip()

        re_id = re.compile(r'\(\d+\)')
        id = re_id.match(title)
        if  id != None:
            podcast_id = title[id.start()+1:id.end()-1]
            podcast_title = title[id.end():]
            re_title = re.compile(r'\- Skript herunterladen')
            podcast_title = re_title.sub('', podcast_title)

            pdfs.append({
                'id': podcast_id,
                'title': podcast_title.strip(),
                'link': BASE_URL + div.h2.a['href']})

    for pdf in pdfs:
        save_path = f'{SAVE_DIR}{pdf["id"]}_{pdf["title"]}.pdf'
        urllib.request.urlretrieve(f'{pdf["link"]}', save_path)
        
        pdf['save_path'] = save_path

    with open(JSON_PATH, 'w') as json_output:
        json.dump(pdfs, json_output, indent = 2, ensure_ascii=False)
