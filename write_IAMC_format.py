import pyam
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import xlsxwriter
import os
import glob

model_name = 'GUSTO v1.0'


# get scenario files from current directiory
e = glob.glob(os.path.join('Output', '*'))
e.sort(key=lambda  x: os.path.getmtime(x))
e = e[-1]

wd = os.path.join(e)
os.chdir(wd)
name_files = os.listdir()







for n in reversed(range(len(name_files))):
    if not ('scenario_' in name_files[n] and '.xlsx' in name_files[n]):
        name_files.pop(n)
del[n]

list_ts=[]
name_scenario=[]
name_year_region=[]

for fn in name_files:
    file_excel = xlrd.open_workbook(filename=fn, on_demand=True)
    for tstemp in file_excel.sheet_names():
        if 'timeseries' in tstemp:
            name_scenario.append(
                fn.replace('scenario_','').replace('.xlsx',''))
            df = pd.read_excel(fn, sheet_name=tstemp)
            list_ts.append(df)
            name_year_region.append(tstemp.split('.')[0:2])
del[file_excel, fn, tstemp, df, name_files]


# create IAMC-format template
workbook = xlsxwriter.Workbook('GUSTO_results.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1', 'model', bold)
worksheet.write('B1', 'scenario', bold)
worksheet.write('C1', 'region', bold)
worksheet.write('D1', 'variable', bold)
worksheet.write('E1', 'unit', bold)
worksheet.write('F1', 'year', bold)
worksheet.write('G1', 'value', bold)

for index in range(len(name_scenario)):
    length = list_ts[
        index].shape[0] - 2 # first two lines contain no data
    start = list_ts[index].iloc[0].to_list().index('Level')
    for sto in range(3): # 3 output curves(level, input, output)
        for row in range(length):
            worksheet.write('A'+str(row+2+length*sto+index*3*length), 
                            model_name)
            worksheet.write('B'+str(row+2+length*sto+index*3*length), 
                            name_scenario[index])
            worksheet.write('C'+str(row+2+length*sto+index*3*length), 
                            name_year_region[index][1])
            worksheet.write('D' + str(row+2+length*sto+index*3*length),
                            list_ts[index].iloc[0][start + sto])
            worksheet.write('E'+str(row+2+length*sto+index*3*length),
                            'MWh'
                            if sto == 0
                            else 'MW')
            worksheet.write('F' + str(row+2+length*sto+index*3*length),
                            list_ts[index].iloc[row + 2][0])
            worksheet.write('G' + str(row+2+length*sto+index*3*length),
                            list_ts[index].iloc[row + 2][start + sto])
workbook.close()
del[bold, workbook, worksheet, index, length, row, model_name]
            
df = pd.read_excel('GUSTO_results.xlsx')
df = pyam.IamDataFrame(df, encoding='utf-8')
print(df.head())
fig, ax = plt.subplots(figsize=(10, 10))
#df.line_plot(ax=ax, color='variable', fill_between=dict(alpha=0.75))
df.line_plot(ax=ax, color='variable')
plt.show()        
    









