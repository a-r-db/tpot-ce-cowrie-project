#!/usr/bin/env python
# coding: utf-8

# In[168]:


# Notes
# Author: Austin Hogan
# Purpose: CKDF 150 - Capstone Project
# Creation Date: Fri May 27 2020
#
# Change Sat May 28 2020: Built Markov Chains

# Teacher's Minimum Requirements Request
"""
Option C - Predicting Future Attacks
Is it possible to predict future attacks? For this option, you will employ the Hidden Markov Model against all the data (non-Tor and Tor) and against the non-Tor data.
A. Which gives a better result and why?
B. Create a graph for each.
C. Provide a written summary about the results.
D. Explain the results in terms of information and intelligence. How are the results useful?
"""


# In[190]:


# imports
# elastic for querying the database
# pandas for data processing

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import pandas as pd
from pprint import pprint
import networkx as nx
import pydot
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[191]:


# Hive Information Class
class HiveInfo:
    def __init__(self) -> None:
        self.city = None,
        self.country = None
        self.code_name = None
        self.ip = None


# In[192]:


# populate hive information
hive_base = HiveInfo()
hive_sensors = [HiveInfo()] * 6
# sink
hive_base.city = "Toronto"
hive_base.country = "Canada"
hive_base.code_name = "rulingcommittee"
hive_base.ip = "216.238.83.8"
# src 0
hive_sensors[0].city = "Toronto"
hive_sensors[0].country = "Canada"
hive_sensors[0].code_name = "rulingcommittee"
hive_sensors[0].ip = "216.238.83.8"
# src 1
hive_sensors[1].city = "Seoul"
hive_sensors[1].country = "Korea"
hive_sensors[1].code_name = "attractivescow"
hive_sensors[1].ip = "158.247.238.143"
# src 2
hive_sensors[2].city = "Melbourne"
hive_sensors[2].country = "Austrailia"
hive_sensors[2].code_name = "deadinlay"
hive_sensors[2].ip = "67.219.98.203"
# src 3
hive_sensors[3].city = "Stockholm"
hive_sensors[3].country = "Sweden"
hive_sensors[3].code_name = "longtermresult"
hive_sensors[3].ip = "65.20.115.181"
# src 4
hive_sensors[4].city = "Mumbai"
hive_sensors[4].country = "India"
hive_sensors[4].code_name = "sadproduce"
hive_sensors[4].ip = "65.20.68.106"
# src 5
hive_sensors[4].city = "Los Angeles"
hive_sensors[4].country = "United States"
hive_sensors[4].code_name = "reasonantnorse"
hive_sensors[4].ip = "149.248.9.4"
# index search value
# matches for year 202[0-9] or 2020-2029
# sufficient for our requirements
indice_search_tag = "logstash-202*"


# In[193]:


# connect to elasticsearch data
es = Elasticsearch("http://localhost:9200")


# In[194]:


# query elasticsearch and return dataframe function
def query_es_return_dataframe(index, query):
    search_context = Search(using=es, index=index)
    s = search_context.query("query_string", query=query)
    response = s.execute()
    if response.success():
        df = pd.DataFrame((d.to_dict() for d in s.scan()))
    return df


# In[195]:


# Markov Chain and Models

# query database for Cowrie honeypot data
df = query_es_return_dataframe(indice_search_tag, "type.keyword: \"Cowrie\"")
# show dataframe
df


# In[196]:


# print column keys
print(df.keys())


# In[197]:


# print sorted unique event ids
unique_event_ids = df['eventid'].unique()
unique_event_ids.sort()
print(unique_event_ids)


# In[198]:


# pretty print unique event ids
event_id_from_int = {}
int_from_event_id = {}
for i, unique_event_id in enumerate(unique_event_ids):
    print("{:02d} {}".format(i, unique_event_id))
    event_id_from_int[i] = unique_event_id
    int_from_event_id[unique_event_id] = i


# In[199]:


# group dataframe by session and aggregate eventids
df_grouped = df.groupby("session")['eventid'].agg(list)


# In[200]:


df_grouped


# In[201]:


df_grouped.keys()


# In[202]:


# calculate markov probabalities
# note total transitions
total_transitions = 0
# transition dictionary collection
transition_dict = {}
# transition matrix (N X N) where N is the number of states
for event_id in unique_event_ids:
    transition_dict[event_id] = [0] * len(unique_event_ids)
# iterate over grouped session and state
# populate transition dictionary
for session, states in df_grouped.items():
    for i in range(len(states) - 1):
        transition_dict[states[i]][int_from_event_id[states[i+1]]] += 1
print(transition_dict)


# In[203]:


# put data into dataframe
transition_df = pd.DataFrame(columns=unique_event_ids, index=unique_event_ids)
for row_event_id, col_event_int in transition_dict.items():
    total = sum(col_event_int)
    transition_df.loc[row_event_id] = [v / total for v in col_event_int]


# In[204]:


# view probability matrix
transition_df


# In[205]:


v = transition_df.values


# In[206]:


print('\n', v, v.shape, '\n')
print(transition_df.sum(axis=1))


# In[207]:


# create a function that maps transition probability dataframe 
# to markov edges and weights
def _get_markov_edges(Q):
    edges = {}
    for col in Q.columns:
        for idx in Q.index:
            edges[(idx,col)] = Q.loc[idx,col]
    return edges

edges_wts = _get_markov_edges(transition_df)
pprint(edges_wts)


# In[208]:


# create graph of system
G = nx.MultiDiGraph()

# add nodes
G.add_nodes_from(unique_event_ids)
    
# print nodes
print("Nodes:\n{}".format(G.nodes()))
    
# add edges from transition probabilities
for key, value in edges_wts.items():
    key_source, key_destination = key[0], key[1]
    G.add_edge(key_source, key_destination, weight=value, label=value)

# print edges
print("Edges: ")
pprint(G.edges(data=True))

# create graphic
pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
nx.draw_networkx(G, pos)

# create edge labels
edge_labels = {(n1,n2):d['label'] for n1,n2,d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
nx.drawing.nx_pydot.write_dot(G, 'markov.dot')

