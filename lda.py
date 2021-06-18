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

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=id2word, num_topics=5)
    print(lda_model.print_topics())
