import numpy as np
import json


if __name__=='__main__':
    semantic_field_topics = {}
    lda_topics = {}
    with open('semantic_topics_per_file.json', 'r') as json_file:
        semantic_field_topics = json.load(json_file)
    with open('lda_topics_per_file2.json', 'r') as json_file:
        lda_topics = json.load(json_file)

    gesellschaft = []
    mensch = []
    politik = []
    virus = []
    wissenschaft = []
    topic_0 = []
    topic_1 = []
    topic_2 = []
    topic_3 = []
    topic_4 = []
    for i in range(1, 92):
        try:
            gesellschaft.append(semantic_field_topics[str(i)]['gesellschaft'])
        except KeyError:
            gesellschaft.append(0)
        try:
            mensch.append(semantic_field_topics[str(i)]['mensch'])
        except KeyError:
            mensch.append(0)
        try:
            politik.append(semantic_field_topics[str(i)]['politik'])
        except KeyError:
            politik.append(0)
        try:
            virus.append(semantic_field_topics[str(i)]['virus'])
        except KeyError:
            virus.append(0)
        try:
            wissenschaft.append(semantic_field_topics[str(i)]['wissenschaft'])
        except KeyError:
            wissenschaft.append(0)
        try:
            topic_0.append(semantic_field_topics[str(i)]['0'])
        except KeyError:
            topic_0.append(0)
        try:
            topic_1.append(semantic_field_topics[str(i)]['1'])
        except KeyError:
            topic_1.append(0)
        try:
            topic_2.append(semantic_field_topics[str(i)]['2'])
        except KeyError:
            topic_2.append(0)
        try:
            topic_3.append(semantic_field_topics[str(i)]['3'])
        except KeyError:
            topic_3.append(0)
        try:
            topic_4.append(semantic_field_topics[str(i)]['4'])
        except KeyError:
            topic_4.append(0)

    gesellschaft_0 = np.correlate(gesellschaft, topic_0)
    print(f'Gesellschaft, Topic 0: {gesellschaft_0}')
    gesellschaft_1 = np.correlate(gesellschaft, topic_1)
    print(f'Gesellschaft, Topic 1: {gesellschaft_1}')
    gesellschaft_2 = np.correlate(gesellschaft, topic_2)
    print(f'Gesellschaft, Topic 2: {gesellschaft_2}')
    gesellschaft_3 = np.correlate(gesellschaft, topic_3)
    print(f'Gesellschaft, Topic 3: {gesellschaft_3}')
    gesellschaft_4 = np.correlate(gesellschaft, topic_4)
    print(f'Gesellschaft, Topic 4: {gesellschaft_4}')

    mensch_0 = np.correlate(mensch, topic_0)
    print(f'Mensch, Topic 0: {mensch_0}')
    mensch_1 = np.correlate(mensch, topic_1)
    print(f'Mensch, Topic 1: {mensch_1}')
    mensch_2 = np.correlate(mensch, topic_2)
    print(f'Mensch, Topic 2: {mensch_2}')
    mensch_3 = np.correlate(mensch, topic_3)
    print(f'Mensch, Topic 3: {mensch_3}')
    mensch_4 = np.correlate(mensch, topic_4)
    print(f'Mensch, Topic 4: {mensch_4}')

    politik_0 = np.correlate(politik, topic_0)
    print(f'Politik, Topic 0: {politik_0}')
    politik_1 = np.correlate(politik, topic_1)
    print(f'Politik, Topic 1: {politik_1}')
    politik_2 = np.correlate(politik, topic_2)
    print(f'Politik, Topic 2: {politik_2}')
    politik_3 = np.correlate(politik, topic_3)
    print(f'Politik, Topic 3: {politik_3}')
    politik_4 = np.correlate(politik, topic_4)
    print(f'Politik, Topic 4: {politik_4}')

    virus_0 = np.correlate(virus, topic_0)
    print(f'Virus, Topic 0: {virus_0}')
    virus_1 = np.correlate(virus, topic_1)
    print(f'Virus, Topic 1: {virus_1}')
    virus_2 = np.correlate(virus, topic_2)
    print(f'Virus, Topic 2: {virus_2}')
    virus_3 = np.correlate(virus, topic_3)
    print(f'Virus, Topic 3: {virus_3}')
    virus_4 = np.correlate(virus, topic_4)
    print(f'Virus, Topic 4: {virus_4}')

    wissenschaft_0 = np.correlate(wissenschaft, topic_0)
    print(f'Wissenschaft, Topic 0: {wissenschaft_0}')
    wissenschaft_1 = np.correlate(wissenschaft, topic_1)
    print(f'Wissenschaft, Topic 1: {wissenschaft_1}')
    wissenschaft_2 = np.correlate(wissenschaft, topic_2)
    print(f'Wissenschaft, Topic 2: {wissenschaft_2}')
    wissenschaft_3 = np.correlate(wissenschaft, topic_3)
    print(f'Wissenschaft, Topic 3: {wissenschaft_3}')
    wissenschaft_4 = np.correlate(wissenschaft, topic_4)
    print(f'Wissenschaft, Topic 4: {wissenschaft_4}')
