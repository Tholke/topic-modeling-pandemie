import gensim
import json

if __name__=='__main__':
    corpus = []
    JSON_PATH = 'json.json'

    with open(JSON_PATH, 'r') as json_file:
        pdf_list = json.load(json_file)

        for pdf in pdf_list:
            pdf_id = pdf["id"]
            document = ''
            with open(pdf["text_path"], 'r') as text_file:
                text = json.load(text_file)
                document = ' '.join([text[page] for page in text])
                document = document.split(' ')
                corpus.append(document)

    id2word = gensim.corpora.Dictionary(corpus)
    corpus = [id2word.doc2bow(document) for document in corpus]

    tf_idf = gensim.models.tfidfmodel.TfidfModel(corpus=corpus, id2word=id2word)

    cleaned_corpus = []
    for document in corpus:
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

    for topic in range(5):
        print(f'Topic {topic}: {lda_model.print_topic(topic)}')
