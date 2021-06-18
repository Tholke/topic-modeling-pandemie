import gensim
import json

if __name__=='__main__':
    corpus = []
    JSON_PATH = 'metadata.json'

    with open(JSON_PATH, 'r') as json_file:
        pdf_list = json.load(json_file)

        for pdf in pdf_list:
            pdf_id = pdf["id"]
            document = ''
            with open(pdf["text_path"], 'r') as text_file:
                text = json.load(text_file)
                document = ' '.join([text[page] for page in text])
                document = document.split(' ')
                corpus.append((pdf_id, document))

    id2word = gensim.corpora.Dictionary([document[1] for document in corpus])
    corpus = [(document[0], id2word.doc2bow(document[1])) for document in corpus]

    text_corpus = [document[1] for document in corpus]
    tf_idf = gensim.models.tfidfmodel.TfidfModel(corpus=text_corpus, id2word=id2word)

    cleaned_corpus = []
    for document in text_corpus:
        tf_idf_matrix = tf_idf[document]
        tf_idf_matrix = sorted(tf_idf_matrix, reverse=True, key=lambda word: word[1])

        cleaned_document = []
        for word in document:
            for tf_word in tf_idf_matrix[:100]:
                if word[0] == tf_word[0]:
                    cleaned_document.append(word)
                    break
        cleaned_corpus.append(cleaned_document)

    lda_model = gensim.models.ldamodel.LdaModel(corpus=cleaned_corpus, id2word=id2word, num_topics=5)

    topics = {}
    for topic in range(5):
        topics[topic] = [x[0] for x in lda_model.show_topic(topic, topn=20)]

    with open('lda_topics.json', 'w') as json_file:
         json.dump(topics, json_file, indent = 2, ensure_ascii=False)

    corpus_topics = {}
    for document in corpus:
        document_topics = {}
        lda_topics = lda_model[document[1]]
        for topic in lda_topics:
            document_topics[topic[0]] = str(topic[1])
        corpus_topics[document[0]] = document_topics

    with open('lda_topics_per_file.json', 'w') as json_file:
         json.dump(corpus_topics, json_file, indent = 2, ensure_ascii=False)
