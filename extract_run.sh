#!/usr/bin/env bash

# need to change the total number
#export TOTAL_NUMBER=20
export EMBEDDING_SIZE=768
export CPC_CLUSTER_MIN_NUM=3
export TITLE_CLUSTER_MIN_NUM=100
export ABSTRACT_CLUSTER_MIN_NUM=100
export TITLE_SUPERGRAPH_CLUSTER=3
export ABSTRACT_SUPERGRAPH_CLUSTER=3
export CLAIM_SUPERGRAPH_CLUSTER=3
export EMBEDDING_BATCH=128
export OLLAMA_URI=http://localhost:11434

venv/bin/python patent/cpc/cpc_phrase_list/cpc_phrase_list.py
venv/bin/python patent/cpc/cpc_embedding/cpc_phrase_embedding_batch.py
venv/bin/python patent/cpc/cpc_clustering/clustering.py

venv/bin/python patent/title/title_candidate/candidate_synthesis.py
venv/bin/python patent/title/title_embedding/title_phrase_embedding_batch.py
venv/bin/python patent/title/title_graph/construct_graph.py
venv/bin/python patent/title/title_score/title_metrics.py
venv/bin/python patent/title/title_score/title_score_normalize.py
venv/bin/python patent/title/title_rank/title_rank.py
venv/bin/python patent/title/title_rank/title_to_text.py
venv/bin/python patent/title/title_rank/title_selection.py
venv/bin/python patent/title/title_clustering/title_clustering.py

venv/bin/python patent/abstract/abstract_candidate/candidate_synthesis.py
venv/bin/python patent/abstract/abstract_embedding/abstract_phrase_embedding_batch.py
venv/bin/python patent/abstract/abstract_graph/construct_graph.py
venv/bin/python patent/abstract/abstract_score/abstract_metrics.py
venv/bin/python patent/abstract/abstract_score/abstract_score_normalize.py
venv/bin/python patent/abstract/abstract_rank/abstract_rank.py
venv/bin/python patent/abstract/abstract_rank/abstract_to_text.py
venv/bin/python patent/abstract/abstract_rank/abstract_selection.py
venv/bin/python patent/abstract/abstract_clustering/abstract_clustering.py

venv/bin/python patent/claim/claim_candidate/candidate_synthesis.py
venv/bin/python patent/claim/claim_embedding/claim_phrase_embedding_batch.py
venv/bin/python patent/claim/claim_graph/construct_graph.py
venv/bin/python patent/claim/claim_score/claim_metrics.py
venv/bin/python patent/claim/claim_score/claim_score_normalize.py
venv/bin/python patent/claim/claim_rank/claim_rank.py
venv/bin/python patent/claim/claim_rank/claim_to_text.py
venv/bin/python patent/claim/claim_rank/claim_selection.py

venv/bin/python result/select_phrase.py
