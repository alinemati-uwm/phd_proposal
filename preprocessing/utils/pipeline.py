#libraries
import pandas as pd
import psycopg2 as pg
import re
import itertools
import numpy as np


#function to combine different column together    
def combine_disease_codes(df,columns,new_column):
    
    df[new_column] = df[columns].agg(' '.join, axis=1)
    df = df.drop(list(columns), axis=1)
    
    df[new_column] = df[new_column].to_list()
    df[new_column] = [re.split(' +', i) for i in df[new_column]]
    
    return df
    
    
#Function to remove some features that are not frequent in dataset(mainly disease codes)
#def remove_redundant_features(df,column,THRESHOLD=5):
    
    #big_list = df[column].to_list()
    #big_list = pd.DataFrame(itertools.chain(*big_list))
    #big_list = big_list.value_counts().loc[lambda x : x>THRESHOLD]
    #final_disease_list = [idx[0] for idx in big_list.index]
    #for i in range(len(df[column])):
    #    df[column][i] = set(list([j for j in df[column][i] if j in final_disease_list if j!="0"]))
    #return df

