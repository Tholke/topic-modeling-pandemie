import json
import re
import stop_words
import string

def load_corpus(json_path):
    corpus = {}

    with open(json_path, 'r') as json_file:
        pdf_list = json.load(json_file)

        for pdf in pdf_list:
            pdf_id = pdf['id']
            document = ''
            with open(pdf['text_path'], 'r') as text_file:
                text = json.load(text_file)
                document = ' '.join([text[page] for page in text])
                corpus[pdf_id] = document

    return corpus

def remove_linebreaks(document):
    linebreak_regex = re.compile('(\\n)')
    return linebreak_regex.sub(' ', document)

def remove_punctuation(document):
    punctuation_regex = re.compile('[' + re.escape(string.punctuation) + ']')
    return punctuation_regex.sub('', document)

def remove_stopwords(tokenized_document):
    stop_words_list = stop_words.STOP_WORDS
    stop_words_list.add('mal')
    # stop_words_list.add('š')
    # stop_words_list.add('œ')
    cleaned_document = []

    for word in tokenized_document:
        if (not word in stop_words_list) and len(word) > 1:
            cleaned_document.append(word)

    return cleaned_document

def to_lower(document):
    return document.lower()

def clean_document(document):
    document = remove_linebreaks(document)
    document = remove_punctuation(document)
    document = to_lower(document)
    document = remove_stopwords(document.split(' '))

    return document

def load_and_clean(json_path):
    corpus = load_corpus(json_path)
    cleaned_corpus = {}

    for document_index in corpus:
        document = clean_document(corpus[document_index])
        cleaned_corpus[document_index] = document

    return cleaned_corpus
