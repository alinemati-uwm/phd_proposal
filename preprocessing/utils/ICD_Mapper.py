import numpy as np
import pandas as pd


rm_quote = lambda x: x.replace("'", '')

dx_ccsr = pd.read_csv("./utils/DXCCSR_v2021-2.csv",usecols=[0,2],
                 converters={
                            '\'ICD-10-CM CODE\'': rm_quote, 
                            '\'Default CCSR CATEGORY IP': rm_quote})

prc_ccsr =pd.read_csv("./utils/PRCCSR_v2021-1.CSV",usecols=[0,2],
                converters={
                            '\'ICD-10-PCS\'': rm_quote, 
                            '\'PRCCSR\'': rm_quote})

icd9cm_gem = pd.read_csv('./utils/2018_I9gem.txt', delimiter = "\s+", header=None,dtype="string")
icd9pcs_gem = pd.read_csv('./utils/gem_i9pcs.txt', delimiter = "\s+", header=None,dtype="string")


#Convert ICD-10-CM to Clinical Classifications
def icd10cm_to_ccsr(arr,map_df=dx_ccsr):
    out = map_df.index[np.isin(map_df[map_df.columns[0]],arr)]
    l=map_df[map_df.columns[1]].iloc[out]
    return list(set(l))


#Convert ICD-10-prosedure to Clinical Classifications
def icd10prc_to_ccsr(arr,map_df=prc_ccsr):
    out = map_df.index[np.isin(map_df[map_df.columns[0]],arr)]
    l=map_df[map_df.columns[1]].iloc[out]
    return list(set(l))


#Convert ICD-9-CM to ICD-10-CM
def icd9cm_to_icd10cm(arr,map_df=icd9cm_gem):
    out = map_df.index[np.isin(map_df[map_df.columns[1]],arr)]
    l=map_df[map_df.columns[2]].iloc[out]
    return list(set(l))

#Convert ICD-9-procedure to ICD-10-prosedure
def icd9pcs_to_icd10pcs(arr,map_df=icd9pcs_gem):
    out = map_df.index[np.isin(map_df[map_df.columns[1]],arr)]
    l=map_df[map_df.columns[2]].iloc[out]
    return list(set(l))

def icd9cm_to_icd10cm_to_ccsr(arr,map_df=dx_ccsr):
    icd10 = icd9cm_to_icd10cm(arr)
    l = icd10cm_to_ccsr(icd10)
    return list(set(l))


def icd9pcs_to_icd10pcs_to_ccsr(arr,map_df=dx_ccsr):
    icd10 = icd9pcs_to_icd10pcs(arr)
    l = icd10prc_to_ccsr(icd10)
    return list(set(l))