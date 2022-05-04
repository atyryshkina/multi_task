#!/bin/python3





import pandas as pd
import os

code2sample_dir = '/data5/UK_Biobank/phenotypes/icd10_codes/2022_04_01/icd10_codes2samples'






df = pd.read_csv('ukb_phenotypes_general.csv')
df = df.set_index('eid', drop=False)



code_files = os.listdir(code2sample_dir)


for code_file in code_files:
	print(code_file)
	code = code_file.split('.')[0]
	fin = open(f'{code2sample_dir}/{code_file}', 'r')
	samples_with_diagnosis = fin.readlines()
	fin.close()
	
	samples_with_diagnosis = [int(s.strip()) for s in samples_with_diagnosis]
	df[code] = df['eid'].isin(samples_with_diagnosis)




df.to_csv('ukb_phenotypes_icd10.csv', index=False)















