#!/usr/bin/env python
# coding: utf-8

# In[31]:


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
strat_pop = {}
try:
    numsamp = 0
    ssize = 0
    choice = input("Type 'w' or 'i' for weights or imbalanced dataset selecting, or 'enter' to skip.\n")
    if choice != 'i':
        numsamp = int(input("Number of samples: "))
        ssize = int(input("Sample Size: "))
    if choice == 'w':
        weight_category = input("Weight by: ")
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
        if abs(sum(weights) - 1) > 0.001: #allow for one-thousandth margin of error
            raise Exception("The sum of probabilities for weights do not equal 1.")
        for i, cat in enumerate(w_order):
            w_dict[cat] = (weights[i],i)
        for val in df[weight_category]:
            elements_prob.append(w_dict[val][0]/freq[w_dict[val][1]])
        elements_prob = np.array(elements_prob)
        elements_prob = elements_prob / elements_prob.sum() #normalize to reduce rounding error: source - https://stackoverflow.com/questions/46539431/np-random-choice-probabilities-do-not-sum-to-1
    elif choice == 'i':
        try:
            distribution_by  = input("Choose from: ")
            w_order = df[distribution_by].unique()
            print("The unique entries for this category are: ", str(w_order))
            num_samps_lst = list(input("In the order that appears above, list number of samples for each unique entry, separated by commas.\n").split(","))
            samp_size_lst = list(input("In the order that appears above, list size of sample for each unique entry, separated by commas.\n").split(","))
            if (len(num_samps_lst) != len(samp_size_lst)):
                raise Exception("The lengths of num_samps_lst and samp_size_lst are not equal.")
            if (len(num_samps_lst) != len(w_order) or len(samp_size_lst) != len(w_order)):
                raise Exception("The lengths of num_samps_lst or samp_size_lst do not match the number of unique entries.")
            for sub in w_order:
                strat_pop[sub] = list(df.loc[df[distribution_by] == sub]["submitter_id"])      
        except Exception:
            raise KeyError("Invalid Key.")
        index = 0
        s_id_start = 0
        size = 0
        for sub,pop in strat_pop.items():
            num_samples = int(num_samps_lst[index])
            size += num_samples
            sample_size = int(samp_size_lst[index])
            for s_id in range(1,num_samples+1):
                samp = np.random.choice(pop, sample_size)
                for img in samp:
                    h.insert(s_id+s_id_start, img, pop)
            s_id_start += num_samples
            index += 1
        inv_hash = h.invTable(size)
        inv_hash.print_hash_inv()
        h.show_stats()
except Exception:
    raise Exception("Invalid Input")
if choice != 'i':
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
    h.show_stats()


# In[ ]:




