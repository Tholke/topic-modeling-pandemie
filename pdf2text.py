import PyPDF2
import re
import json
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

FILE_HANDLER = logging.FileHandler('pdf2text.log')
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(logging.ERROR)

STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STREAM_HANDLER)

def extract_header(text: str) -> str:
    regex = re.compile('[\s\S]+FOLGE \d+')
    header = regex.match(text)

    if not header:
        regex = re.compile('[0-9]+/[0-9]+')
        header = regex.match(text)

        if not header:
            raise ValueError('No matching header found.')

    return header.group(0)

def clean_header(text: str) -> str:
    header = extract_header(text)
    regex = re.compile(header)

    return regex.sub('', text)

def clean_linebreak_dashes(text: str) -> str:
    regex = re.compile('\\n-(?=[a-z|ä-ü])')
    return regex.sub('', text)

def clean_name_headers(text: str) -> str:
    name_regex = re.compile('(?<=\n)([A-Z][a-z|.]+[\s\S]){2,}(?=\n)')
    return name_regex.sub('\n', text)

def clean_linebreaks(text: str) -> str:
    linebreak_regex = re.compile('(?<=.)\\n')
    text = linebreak_regex.sub('', text)

    linebreak_regex = re.compile('(\\n){2,}')
    return linebreak_regex.sub('\n', text)

def clean_text(text: str) -> str:
    text = clean_header(text)
    text = clean_linebreak_dashes(text)
    text = clean_name_headers(text)
    text = clean_linebreaks(text)

    return text.strip()

def extract_text(page_object: PyPDF2.pdf.PageObject) -> str:
    page_text = page_object.extractText().strip()
    return clean_text(page_text)

def extract_pages(path: str) -> dict:
    reader = PyPDF2.PdfFileReader(path)
    num_pages = reader.getNumPages()

    pages = {}
    for i in range(num_pages):
        page_object = reader.getPage(i)
        try:
            page_text = extract_text(page_object)
            pages[i+1] = page_text
        except ValueError:
            LOGGER.error(f"Couldn't extract page {i+1} in {path}. Skipping.")
            continue
    return pages

def main():
    JSON_PATH = 'metadata.json'
    SAVE_DIR = 'texts/'

    pdf_list = []
    with open(JSON_PATH, 'r') as json_file:
        pdf_list = json.load(json_file)

        for pdf in pdf_list:
            pdf_name = f'{pdf["id"]}_{pdf["title"]}'
            LOGGER.info(f'Working on {pdf_name}')
            pages = extract_pages(pdf['save_path'])

            text_path = f'{SAVE_DIR}{pdf_name}.json'
            with open(text_path, 'w') as text_file:
                json.dump(pages, text_file, indent = 2, ensure_ascii=False)

            pdf['text_path'] = text_path

    with open(JSON_PATH, 'w') as json_file:
        json.dump(pdf_list, json_file, indent = 2, ensure_ascii=False)

if __name__=='__main__':
    main()
