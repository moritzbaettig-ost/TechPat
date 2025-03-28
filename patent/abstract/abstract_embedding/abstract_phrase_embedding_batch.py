import numpy as np
import gensim
import json
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
import ipdb
import pickle
from tqdm import tqdm
from ollama import Client, EmbedResponse
import logging
logging.basicConfig(level=logging.WARNING)
import os
TOTAL_NUMBER = int(os.environ.get('TOTAL_NUMBER'))
EMBEDDING_SIZE = int(os.environ.get('EMBEDDING_SIZE'))
EMBEDDING_BATCH = int(os.environ.get('EMBEDDING_BATCH'))
OLLAMA_URI = os.environ.get('OLLAMA_URI')

from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)


def save_obj(obj, name):
    with open(name, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name, 'rb') as f:
        return pickle.load(f)



def cut_list(lists, cut_len):
    res_data = []
    if len(lists) > cut_len:
        for i in range(int(len(lists) / cut_len)):
            cut_a = lists[cut_len * i:cut_len * (i + 1)]
            res_data.append(cut_a)

        last_data = lists[int(len(lists) / cut_len) * cut_len:]
        if last_data:
            res_data.append(last_data)
    else:
        res_data.append(lists)

    return res_data


def batch_bert_phrase_embedding(cpc_embedding_file, title_phrase_file, output_file, batch_size=EMBEDDING_BATCH):
    client = Client(host=OLLAMA_URI)
    phrase_embedding = load_obj(cpc_embedding_file)
    with open(title_phrase_file, 'r', encoding='utf-8') as f_in:
        title_phrase = json.load(f_in)
    
    phrase_embedding_keys = list(phrase_embedding.keys())
    phrase_embedding_keys_dict = dict(zip(phrase_embedding_keys, phrase_embedding_keys))
    added_keys = []

    for item in tqdm(title_phrase, total=TOTAL_NUMBER):
        for phrase_item in item['superspan']:
            temp_phrase = phrase_item.lower()
            if temp_phrase != '' and temp_phrase not in phrase_embedding_keys_dict:
                added_keys.append(temp_phrase)
                phrase_embedding_keys_dict[temp_phrase] = temp_phrase
    
    batched_keys = cut_list(added_keys, batch_size)

    for batch in tqdm(batched_keys, total=len(batched_keys)):
        res: EmbedResponse = client.embed(model='nomic-embed-text', input=batch)
        batch_embedding = res.embeddings
        for idx in range(len(batch)):
            phrase_embedding[batch[idx]] = batch_embedding[idx]
    
    save_obj(phrase_embedding, output_file)


if __name__ == '__main__':

    cpc_title_embedding_file = 'patent/title/title_embedding/cpc_title_phrase_embedding.pkl'
    abstract_phrase_file = 'patent/abstract/abstract_candidate/abstract_candidate_synthesis.json'
    output_file = 'patent/abstract/abstract_embedding/cpc_title_abstract_phrase_embedding.pkl'
    batch_bert_phrase_embedding(cpc_title_embedding_file, abstract_phrase_file, output_file)
    