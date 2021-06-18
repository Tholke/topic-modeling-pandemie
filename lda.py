import data_loading
import gensim
import json

if __name__=='__main__':
    JSON_PATH = 'metadata.json'

    corpus = data_loading.load_and_clean(JSON_PATH)

    id2word = gensim.corpora.Dictionary([corpus[document_id] for document_id in corpus])

    training_data = [id2word.doc2bow(corpus[document_id]) for document_id in corpus]
    lda_model = gensim.models.ldamodel.LdaModel(corpus=training_data, id2word=id2word, num_topics=5, chunksize=1, passes=1)

    lda_model.save('lda_model/model')

    topics = {}
    for topic in range(5):
        topics[topic] = [x[0] for x in lda_model.show_topic(topic, topn=20)]

    for topic in range(5):
        print(lda_model.show_topic(topic, topn=4))

    with open('lda_topics.json', 'w') as json_file:
         json.dump(topics, json_file, indent = 2, ensure_ascii=False)

    corpus_topics = {}
    for document_id in corpus:
        document_topics = {}
        lda_topics = lda_model[id2word.doc2bow(corpus[document_id])]
        for topic in lda_topics:
            document_topics[topic[0]] = str(topic[1])
        corpus_topics[document_id] = document_topics

    with open('lda_topics_per_file.json', 'w') as json_file:
         json.dump(corpus_topics, json_file, indent = 2, ensure_ascii=False)
