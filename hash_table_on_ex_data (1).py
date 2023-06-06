#!/usr/bin/env python
# coding: utf-8

# In[6]:


from hash_test import Node
from hash_test import HashTable
import pandas as pd
import numpy as np
df = pd.read_excel("COMPLETED_v3sequestration_data_example.xlsx")
img_ids = list(df["submitter_id"])
h = HashTable()
weights = []
w_order = []
w_dict = {}
elements_prob = []
h.init_table(img_ids)
try:
    numsamp = int(input("Number of samples: "))
    ssize = int(input("Sample Size: "))
    weight_category = input("Weight by: ")
    if weight_category != "":
        try:
            w_order = df[weight_category].unique()
            freq = df[weight_category].value_counts()
            print("The unique entries for this category are:\n" + str(w_order))
        except Exception:
            raise Exception("Invalid Key.")
        cat_weights_str = list(input("In the order that appears above, list weights for each unique entry, separated by commas.\n").split(","))
        for stri in cat_weights_str:
            weights.append(float(stri))
        if (len(w_order) != len(weights)):
            raise Exception("Length of unique entries do not match length of input")
        if abs(sum(weights) - 1) > 0.001:
            raise Exception("The sum of probabilities for weights do not equal 1.")
        for i, cat in enumerate(w_order):
            w_dict[cat] = (weights[i],i)
        for val in df[weight_category]:
            elements_prob.append(w_dict[val][0]/freq[w_dict[val][1]])
        elements_prob = np.array(elements_prob)
        elements_prob = elements_prob / elements_prob.sum() #normalize to reduce rounding error: source - https://stackoverflow.com/questions/46539431/np-random-choice-probabilities-do-not-sum-to-1
except Exception:
    raise Exception("Invalid Input")
for s_id in range(1,numsamp+1):
    if len(elements_prob) == 0:
        samp = np.random.choice(img_ids, ssize)
        for img in samp:
            h.insert(s_id, img, img_ids)
    else:
        samp = np.random.choice(img_ids, ssize, p = elements_prob)
        for img in samp:
            h.insert(s_id, img, img_ids, elements_prob)
inv_hash = h.invTable(numsamp)
inv_hash.print_hash_inv()


# In[18]:


df

