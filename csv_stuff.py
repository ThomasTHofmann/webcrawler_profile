import os
import glob
import pandas as pd
folder = "C:/Users/Admin/source/repos/webcrawler-profile/Fintech"
industry = "Fintech"
name = industry + "_combined.csv"
os.chdir(folder)
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f, encoding_errors='ignore') for f in all_filenames ])

#drop unnamed columns
combined_csv.drop(combined_csv.columns[combined_csv.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)

#export to csv
combined_csv.to_csv(name, index=False, encoding='utf-8-sig')

path = folder + '/' + name

def relevant_column(path):
    data = pd.read_csv(path, encoding_errors = 'ignore')
    data.drop('Profile URL', inplace=True, axis=1)
    data.drop('Name', inplace=True, axis=1)
    data.drop('Company Name', inplace=True, axis=1)
    data.drop('Title', inplace=True, axis=1)
    data.to_csv(industry + "_combined_relevant.csv", index=False, encoding='utf-8-sig')

def skill_column(path):
    data = pd.read_csv(path, encoding_errors = 'ignore')
    data.drop('Profile URL', inplace=True, axis=1)
    data.drop('Name', inplace=True, axis=1)
    data.drop('Company Name', inplace=True, axis=1)
    data.drop('Title', inplace=True, axis=1)
    data.drop('About', inplace=True, axis=1)
    data.drop('Experience', inplace=True, axis=1)
    data.drop('Education', inplace=True, axis=1)
    data.to_csv(industry + "_combined_skills.csv", index=False, encoding='utf-8-sig')

relevant_column(path)
skill_column(path)
