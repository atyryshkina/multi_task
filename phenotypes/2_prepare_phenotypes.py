#!/bin/python3



import pandas as pd
from pandarallel import pandarallel


pandarallel.initialize(nb_workers=15)



column_keys = {
	'22006-0.0':'genetic_ethnic_grouping',
	'22001-0.0':'genetic_sex',
	'21003-0.0':'age_when_attended_assessment_centre1',
	'21003-1.0':'age_when_attended_assessment_centre2',
	'21003-2.0':'age_when_attended_assessment_centre3',
	'21000-0.0':'ethnic_background1',
	'21000-1.0':'ethnic_background2',
	'21000-2.0':'ethnic_background3',
	'31-0.0':'sex',
	'34-0.0':'year_of_birth'
}



columns_wanted = ['eid'] + list(column_keys.keys())


df = pd.read_csv('/data4/UK_Biobank/download/ukb30075.csv', encoding='unicode_escape', usecols=columns_wanted)
columns = list(df.columns)


new_columns = [column_keys[s] if s in column_keys.keys() else s for s in columns]
df.columns = new_columns




#=======================
# Add readable ethnicity
#=======================

coding_df = pd.read_csv('coding1001.tsv', sep='\t')
coding_df['coding'] = coding_df['coding'].astype(int)
coding_df = coding_df.set_index('coding')


def get_coding_meaning(s):
	if s!=s:
		return ''
	return coding_df.at[int(s), 'meaning']


df['ethnic_background1'] = df['ethnic_background1'].apply(get_coding_meaning)
df['ethnic_background2'] = df['ethnic_background2'].apply(get_coding_meaning)
df['ethnic_background3'] = df['ethnic_background3'].apply(get_coding_meaning)


#=======================
# Make consensus column for ethnicity
#=======================


def get_consensus(row):	
	values = list(row.unique())
	values = [s for s in values if s != '']
			
	if len(values) > 1:
		return 'inconsistent'
	if len(values) == 0:
		return ''
	
	return values[0]



df['ethnic_background'] = df[['ethnic_background1', 'ethnic_background2', 'ethnic_background3']].parallel_apply(get_consensus, axis=1)

df = df.drop(['ethnic_background1', 'ethnic_background2', 'ethnic_background3'], axis=1)


#=======================
# Get Mean value for age
#=======================

def get_mean_value(row):
	mean = row.mean()
	return mean



df['age_when_attended_assessment_centre'] = df[['age_when_attended_assessment_centre1', 'age_when_attended_assessment_centre2', 'age_when_attended_assessment_centre3']].apply(get_mean_value, axis=1)

df = df.drop(['bmi1', 'bmi2', 'bmi3', 'age_when_attended_assessment_centre1', 'age_when_attended_assessment_centre2', 'age_when_attended_assessment_centre3'], axis=1)


#=======================
# Add genetic principle components
#=======================


# need to get Genotyping_process_and_sample_QC	22009	Genetic principal components
dwl_df = pd.read_csv('/data4/UK_Biobank/download/ukb30075.csv', encoding='unicode_escape', nrows=1)
columns = list(dwl_df.columns)
columns = [s for s in dwl_df if s.startswith('22009-')]
columns_wanted = ['eid'] + columns


dwl_df = pd.read_csv('/data4/UK_Biobank/download/ukb30075.csv', encoding='unicode_escape', usecols=columns_wanted)
dwl_df = dwl_df.set_index('eid')


for i in range(1, 41):
	df[f'PC{i}'] = df['eid'].map(dwl_df[f'22009-0.{i}'])



#=======================
# only keep samples with WES
#=======================


wes_df = pd.read_csv('/data5/UK_Biobank/annotations/annovar/2022_01_30/samples.csv')

df = df[df.eid.isin(wes_df.Sample)]


#=======================
# Save Table
#=======================




df.to_csv('ukb_phenotypes_general.csv', index=False)










