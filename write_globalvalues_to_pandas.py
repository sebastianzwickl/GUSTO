import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def write_globvar_to_paretofront():
    sheetname = 'Global pareto front values'
    globvar = 4

    # get scenario files
    e = glob.glob(os.path.join('..', '*'))
    e.sort(key=lambda x: os.path.getmtime(x))
    wd = os.path.join(e[-1])
    os.chdir(wd)
    name_files = os.listdir()
    for n in reversed(range(len(name_files))):
        if not ('scenario_' in name_files[n] and '.xlsx' in name_files[n] and
                not '~' in name_files[n]):
            name_files.pop(n)
    del[n, wd, e]

    dataframe = pd.DataFrame()
    listvar = []

    for j in name_files:
        if dataframe.empty:
            dataframe = pd.read_excel(j, sheet_name=sheetname,
                                      usecols=lambda x: 'Unnamed' not in x)
            for i in range(globvar):
                if 'cost' in j:
                    listvar.append('Profit maximization')
                if 'local' in j:
                    listvar.append('Local deficit/excess')
                if 'load' in j:
                    listvar.append('Load following')
            dataframe = dataframe.assign(Strategy=listvar)

        else:
            dftemp = pd.read_excel(j, sheet_name=sheetname,
                                   usecols=lambda x: 'Unnamed' not in x)
            listvar.clear()
            for i in range(globvar):
                if 'cost' in j:
                    listvar.append('Profit maximization')
                if 'local' in j:
                    listvar.append('Local deficit/excess')
                if 'load' in j:
                    listvar.append('Load following')

            dftemp = dftemp.assign(Strategy=listvar)
            dataframe = dataframe.append(dftemp, ignore_index=True)

    print(dataframe)

    with plt.style.context('seaborn'):

        x = dataframe.loc[dataframe['Variable'].
                          isin(['Local deficit/excess'])]['Global values'].tolist()
        y = dataframe.loc[dataframe['Variable'].
                          isin(['Total costs'])]['Global values'].tolist()
        y.sort()
        x.sort()
        print('x')
        print(x)
        print('y')
        print(y)
        x = np.flip(x)
        plt.figure()
        plt.plot(x, y)
        plt.scatter(x, y)
        plt.xlabel('Exchanges with the public grid [MWh]', fontsize=12)
        plt.ylabel('Total cost of supply [EUR/a]', fontsize=12)

        group_thousands = ticker.FuncFormatter(
            lambda x, pos: '{:0,d}'.format(int(x)).replace(',', ' '))
        plt.gca().yaxis.set_major_formatter(group_thousands)
        plt.gca().xaxis.set_major_formatter(group_thousands)
    for ext in ['png']:
        plt.savefig('{}.{}'.format('Pareto front', ext),
                    bbox_inches='tight')
    del [dftemp, i, j, globvar, listvar, sheetname, name_files, x, y]


if __name__ == '__main__':
    write_globvar_to_paretofront()
