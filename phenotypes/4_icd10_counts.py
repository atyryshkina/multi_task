#!/bin/python3






import pandas as pd
import numpy as np


df = pd.read_csv('coding19.tsv', sep='\t')
df = df.set_index('coding', drop=False)

pdf = pd.read_csv('ukb_phenotypes_icd10.csv')




df['count_wes'] = np.nan
df['count_wes_white_british'] = np.nan
for code in df.coding:
	count = df[code].sum()
	count_white_british = df[df['genetic_ethnic_grouping'] == 1][code].sum()
	df.at[code, 'count_wes'] = count




df.to_csv('coding19_counts.csv', index=False)


















