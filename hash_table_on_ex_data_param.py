from hash_test import Node
from hash_test import HashTable
import pandas as pd
import numpy as np
df = pd.read_excel("COMPLETED_v3sequestration_data_example.xlsx")
img_ids = list(df["submitter_id"])
h = HashTable()
h.init_table(img_ids)
imb_dict = {}
w_dict = {}
weights = []
numsamps = 0
samplesize = 0
try:
    numsamps = int(input("Number of samples: "))
    samplesize = int(input("Sample size: "))
except Exception:
    raise ValueError("Please enter integer values.")
imb_category = input("Choose variable to imbalance by. ")
try:
    imb_order = list(df[imb_category].unique())
    print("The unique entries for this category are: ", str(imb_order))
    imb_prop = input("In the same order that the unique entries appear, list proportions separated by commas. ").split(",")
    for i,val in enumerate(imb_prop):
        imb_prop[i] = float(val)
    if sum(imb_prop) != 1:
        raise Exception("Proportions do not add to 1.")
    if len(imb_order) != len(imb_prop):
        raise Exception("Unequal list sizes.")
    for i,prop in enumerate(imb_prop):
        cat_samples = round(prop * samplesize) #if prop * samplesize is a decimal, round
        imb_dict[imb_order[i]] = cat_samples
    print("The sample makeup is: ", imb_dict)
    weight_category = input("Weight by: ")
    if weight_category == imb_category:
        raise Exception("Weight and imbalance variables must be different.")
    w_order = list(df[weight_category].unique())
    freq = df[weight_category].value_counts()
    print("The unique entries for this category are: ", str(w_order))
    w_prop = input("In the same order that the unique entries appear, list proportions separated by commas. ").split(",")
    for i,val in enumerate(w_prop):
        w_prop[i] = float(val)
    if len(w_order) != len(w_prop):
        raise Exception("Unequal list sizes.")
    if abs(sum(w_prop) != 1):
        raise Exception("Proportions do not add to 1.")
except Exception:
    raise KeyError("Invalid Input")
indexes = {}
cat_prob = {}
sub_img = {}
for ind,val in enumerate(df[imb_category]):
    if val not in indexes:
        indexes[val] = [ind]
        sub_img[val] = [img_ids[ind]]
    else:
        indexes[val].append(ind)
        sub_img[val].append(img_ids[ind])
for key, lst in indexes.items():
    for idx in lst:
        if key not in cat_prob:
            cat_prob[key] = [w_prop[w_order.index(df[weight_category][idx])]/len(df.loc[(df[weight_category] == df[weight_category].iloc[idx]) & (df[imb_category] == df[imb_category].iloc[idx])])]
        else:
            cat_prob[key].append(w_prop[w_order.index(df[weight_category][idx])]/len(df.loc[(df[weight_category] == df[weight_category].iloc[idx]) & (df[imb_category] == df[imb_category].iloc[idx])]))
for cat in indexes:
    cat_prob[cat] = np.array(cat_prob[cat])
    cat_prob[cat] = cat_prob[cat] / cat_prob[cat].sum() #normalize each bucket
for samp_id in range(1,numsamps+1):
    for cat in imb_dict:
        samp = np.random.choice(sub_img[cat], imb_dict[cat], p = cat_prob[cat])
        for img in samp:
            h.insert(samp_id, img, sub_img[cat], cat_prob[cat])
inv_hash = h.invTable(numsamps)
inv_hash.print_hash_inv()
h.show_stats()
#Verifying HashTable Results
lst = input("Enter image IDs separated by a space: ").split(" ")
for i,val in enumerate(lst):
    lst[i] = int(val)
for i in lst:
    print(df.loc[df["submitter_id"] == i]["sex"])
