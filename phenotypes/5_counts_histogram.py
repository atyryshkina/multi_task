#!/bin/python3



import pandas as pd
import os
import subprocess
import sys

# libraries related to plotting
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
sns.set_style({'font.family':'sans-serif', 'font.sans-serif':'Arial'})
from matplotlib.backends.backend_pdf import PdfPages



# subprocess.run('mkdir figures/by_combo', shell=True)

group = sys.argv[1]
comparison = sys.argv[2]
num_combos = int(sys.argv[3])



stats_df = pd.read_csv(f'/data5/UK_Biobank/bmi_project/combinations/all_combinations/combinations/{group}/{comparison}_{num_combos}.csv')





pdf = PdfPages(f'figures/histograms/{group}_{comparison}_{num_combos}.pdf')


for i, row in stats_df.iterrows():
	if num_combos == 2:
		gene1 = row['Item_1']
		gene2 = row['Item_2']
		df = pd.read_csv(f'tables/by_combo/{group}/{comparison}/{num_combos}/{gene1}_{gene2}.csv')
		title = f'{row["Item_1_symbol"]}, {row["Item_2_symbol"]}'
	if num_combos == 3:
		gene1 = row['Item_1']
		gene2 = row['Item_2']
		gene3 = row['Item_3']
		df = pd.read_csv(f'tables/by_combo/{group}/{comparison}/{num_combos}/{gene1}_{gene2}_{gene3}.csv')
		title = f'{row["Item_1_symbol"]}, {row["Item_2_symbol"]}, {row["Item_3_symbol"]}'
	single_hit_df = df[df.combo_hit.isna()]
	two_hit_df = df[~df.combo_hit.isna()]

	fig = plt.figure(figsize=(2,3.5))
	g = sns.histplot(data=single_hit_df, x='bmi_residuals', binwidth=0.1)
	sns.histplot(data=two_hit_df, x='bmi_residuals', color='tab:red', binwidth=0.1)
	plt.axvline(x=single_hit_df['bmi_residuals'].mean(), color='blue')
	plt.axvline(x=two_hit_df['bmi_residuals'].mean(), color='red')
	plt.text(x=single_hit_df['bmi_residuals'].mean(), y=10, s='{:.2f}'.format(single_hit_df['bmi_residuals'].mean()))
	plt.text(x=two_hit_df['bmi_residuals'].mean(), y=15, s='{:.2f}'.format(two_hit_df['bmi_residuals'].mean()))
	g.set_title(title)
	pdf.savefig(fig, bbox_inches='tight')
	plt.close()





pdf.close()










