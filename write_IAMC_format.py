import pyam
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import xlsxwriter
import os
import glob
import math


def write_to_iamc_format():
    # define model name
    model_name = 'GUSTO v1.0'

    # get scenario files from current directiory
    e = glob.glob(os.path.join('Output', '*'))
    e.sort(key=lambda x: os.path.getmtime(x))
    e = e[-1]

    # get file names
    wd = os.path.join(e)
    os.chdir(wd)
    name_files = os.listdir()

    # keep 'scenario*.xlsx' files
    for n in reversed(range(len(name_files))):
        if not ('scenario_' in name_files[n] and '.xlsx' in name_files[n]):
            name_files.pop(n)
    del[n]

    list_ts = []
    name_scenario = []
    name_year_region = []

    # get following names of: scenarios, year, and regions
    for fn in name_files:
        file_excel = xlrd.open_workbook(filename=fn, on_demand=True)
        for tstemp in file_excel.sheet_names():
            if 'timeseries' in tstemp:
                name_scenario.append(
                    fn.replace('scenario_', '').replace('.xlsx', ''))
                df = pd.read_excel(fn, sheet_name=tstemp)
                list_ts.append(df)
                name_year_region.append(tstemp.split('.')[0:2])


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

    # write data to IAMC format
    for index in range(len(name_scenario)):
        length = list_ts[
            index].shape[0] - 2  # first two lines contain no data
        start = list_ts[index].iloc[0].to_list().index('Level')
        for sto in range(3):  # 3 output curves(level, input, output)
            for row in range(length):
                # write model
                worksheet.write('A'+str(row+2+length*sto+index*3*length),
                                model_name)
                # write scenario
                worksheet.write('B'+str(row+2+length*sto+index*3*length),
                                name_scenario[index])
                # write region
                worksheet.write('C'+str(row+2+length*sto+index*3*length),
                                name_year_region[index][1])
                # write variable
                worksheet.write('D' + str(row+2+length*sto+index*3*length),
                                list_ts[index].iloc[0][start + sto])
                # write unit
                worksheet.write('E'+str(row+2+length*sto+index*3*length),
                                'MWh'
                                if sto == 0
                                else 'MW')
                # write year
                worksheet.write('F' + str(row+2+length*sto+index*3*length),
                                list_ts[index].iloc[row + 2][0])
                # write value
                worksheet.write('G' + str(row+2+length*sto+index*3*length),
                                list_ts[index].iloc[row + 2][start + sto]
                                if not math.isnan(list_ts[index].iloc[row + 2][start + sto])
                                else 0)
    workbook.close()

    # clean working directory
    del[bold, workbook, worksheet, index, length, row,
        model_name, file_excel, fn, tstemp, df, name_files]

    # use pyam package to display results
    df = pd.read_excel('GUSTO_results.xlsx')
    df = pyam.IamDataFrame(df, encoding='utf-8')
    fig, ax = plt.subplots(figsize=(10, 10))
    df_filter = df.filter(variable='Retrieved')
    df_filter.line_plot(ax=ax, color='variable', fill_between=dict(alpha=0.75))
    fig.set_size_inches(30, 12)
    for ext in ['png']:
        fig.savefig('{}.{}'.format('Scenarios_Retrieved', ext),
                    bbox_inches='tight')


if __name__ == '__main__':
    write_to_iamc_format()

df = pd.read_excel('GUSTO_results.xlsx')
df = pyam.IamDataFrame(df, encoding='utf-8')
print(df.head())
fig, ax = plt.subplots(figsize=(10, 10))
# df.line_plot(ax=ax, color='variable', fill_between=dict(alpha=0.75))
df.line_plot(ax=ax, color='variable')
plt.show()
