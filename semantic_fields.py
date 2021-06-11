import glob
import json
import os.path
from typing import Dict, List, Tuple

def create_fields(topic_path: str) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:

    topics = {}
    words = {}
    for filename in glob.glob(topic_path + '*.txt'):
        topic_name = os.path.split(filename)[-1]
        topic_name = topic_name.split('.')[0]

        semantic_field = []

        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                semantic_field.append(line)
                try:
                    word_topics = words[line]
                    word_topics.append(topic_name)
                    words[line] = word_topics
                    print(f'{line} kommt häufiger vor!')
                except KeyError:
                    words[line] = [topic_name]
        topics[topic_name] = semantic_field

    return topics, words

if __name__=='__main__':
    TOPIC_PATH = 'topics/'
    JSON_PATH = 'json.json'

    fields_by_topic, fields_by_word = create_fields(TOPIC_PATH)

    topics = {}
    for key in fields_by_topic:
        topics[key] = {}

    with open(JSON_PATH, 'r') as json_file:
        pdf_list = json.load(json_file)

        for pdf in pdf_list:
            pdf_id = pdf["id"]
            with open(pdf["text_path"], 'r') as text_file:
                text = json.load(text_file)
                topics_in_text = {}

                for page in text:
                    for word in text[page].split(' '):
                        if word in fields_by_word.keys():
                            for topic in fields_by_word[word]:
                                try:
                                    topics_in_text[topic] = topics_in_text[topic] + 1
                                except KeyError:
                                    topics_in_text[topic] = 1

                for topic in topics_in_text:
                    topics[topic][pdf_id] = topics_in_text[topic]


    with open('topics.json', 'w') as json_file:
        json.dump(topics, json_file, indent = 2, ensure_ascii=False)
