import pandas as pd
import os


def scenario_baseline(data, ub):
    return data


def scenario_HighxElectrification(data, ub):
    return data


def scenario_austria(data, ub):

    # adjust solar radiation for an Austrian neighborhood
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')  # read in solar radiation from input file
    _solar = _solar.loc[_solar['region'] == 'Austria']  # filter solar radiation accordingly

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values  # overwrite and set solar radiation parameter
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    # adjust heat pump efficiency time series not necessary - default values for an Austrian location

    # set electricity (selling/buying) and heating (buying) prices - default values for an Austrian location

    return data


def scenario_france(data, ub):

    data = scenario_austria(data, ub)  # simplification: assume the same solar radiation and heat pump efficiency
    # set residential electricity prices accordingly
    data['buy_sell_price']['Elec buy', ] = 0.1765  # EUR/kWh
    data['buy_sell_price']['Elec sell', ] = 0.1765 * 0.15  # Assume selling electricity prices of 15%
    data['buy_sell_price']['Heat buy', ] = 0.056

    # 2040
    _price = pd.read_excel('files/Prices_2040.xlsx')['France']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634 # taxes

    # 2055
    _price = pd.read_excel('files/Prices_2055.xlsx')['France']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes
    return data


def scenario_poland(data, ub):

    data = scenario_austria(data, ub)  # simplification: assume the same solar radiation and heat pump efficiency
    # set residential electricity prices accordingly
    data['buy_sell_price']['Elec buy', ] = 0.1475  # EUR/kWh
    data['buy_sell_price']['Elec sell', ] = 0.1475 * 0.15  # Assume selling electricity prices of 15%
    data['buy_sell_price']['Heat buy', ] = 0.066

    # 2040
    _price = pd.read_excel('files/Prices_2040.xlsx')['Poland']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    # 2055
    _price = pd.read_excel('files/Prices_2055.xlsx')['Poland']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes
    return data


def scenario_portugal(data, ub):

    # set solar radiation
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')  # read in solar radiation from input file
    _solar = _solar.loc[_solar['region'] == 'ES41']  # filter solar radiation accordingly

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values  # overwrite and set solar radiation parameter
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    # set heat pump efficiency higher than in Austria due to average temperatures
    data['eff_factor']['LMAB1', 'Heat Pump (air water)'] += 0.42  # 10% higher efficiency in average

    # set residential electricity prices accordingly
    data['buy_sell_price']['Elec buy', ] = 0.2231  # EUR/kWh
    data['buy_sell_price']['Elec sell', ] = 0.2231 * 0.15  # Assume selling electricity prices of 15%
    data['buy_sell_price']['Heat buy', ] = 0.071

    # decrease residential heating demand for southern countries
    data['demand']['LMAB1', 'Heat'] *= 0.6
    data['demand']['LMAB2', 'Heat'] *= 0.6
    data['demand']['LMAB3', 'Heat'] *= 0.6
    data['demand']['LMAB4', 'Heat'] *= 0.6
    data['demand']['LMAB5', 'Heat'] *= 0.6
    data['demand']['LMAB6', 'Heat'] *= 0.6
    data['demand']['LMAB7', 'Heat'] *= 0.6
    data['demand']['LMAB8', 'Heat'] *= 0.6
    data['demand']['LMAB9', 'Heat'] *= 0.6
    data['demand']['LMAB10', 'Heat'] *= 0.6

    # 2040
    _price = pd.read_excel('files/Prices_2040.xlsx')['Portugal']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    # 2055
    _price = pd.read_excel('files/Prices_2055.xlsx')['Poland']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    return data


def scenario_spain(data, ub):

    # set solar radiation
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')  # read in solar radiation from input file
    _solar = _solar.loc[_solar['region'] == 'ES41']  # filter solar radiation accordingly

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values  # overwrite and set solar radiation parameter
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    # set heat pump efficiency higher than in Austria due to average temperatures
    data['eff_factor']['LMAB1', 'Heat Pump (air water)'] += 0.63  # 15% higher efficiency in average

    # set residential electricity prices accordingly
    data['buy_sell_price']['Elec buy', ] = 0.2383 # EUR/kWh
    data['buy_sell_price']['Elec sell', ] = 0.2383 * 0.15  # Assume selling electricity prices of 15%
    data['buy_sell_price']['Heat buy', ] = 0.0665

    # decrease residential heating demand for southern countries
    data['demand']['LMAB1', 'Heat'] *= 0.6
    data['demand']['LMAB2', 'Heat'] *= 0.6
    data['demand']['LMAB3', 'Heat'] *= 0.6
    data['demand']['LMAB4', 'Heat'] *= 0.6
    data['demand']['LMAB5', 'Heat'] *= 0.6
    data['demand']['LMAB6', 'Heat'] *= 0.6
    data['demand']['LMAB7', 'Heat'] *= 0.6
    data['demand']['LMAB8', 'Heat'] *= 0.6
    data['demand']['LMAB9', 'Heat'] *= 0.6
    data['demand']['LMAB10', 'Heat'] *= 0.6

    # 2040
    _price = pd.read_excel('files/Prices_2040.xlsx')['Portugal']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    # 2055
    _price = pd.read_excel('files/Prices_2055.xlsx')['Portugal']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    return data


def scenario_norway(data, ub):
    # set solar radiation
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')  # read in solar radiation from input file
    _solar = _solar.loc[_solar['region'] == 'Norway|Finnmark']  # filter solar radiation accordingly

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values  # overwrite and set solar radiation parameter
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    # set heat pump efficiency higher than in Austria due to average temperatures
    data['eff_factor']['LMAB1', 'Heat Pump (air water)'] -= 0.63  # 15% lower efficiency in average

    # set residential electricity prices accordingly
    data['buy_sell_price']['Elec buy', ] = 0.2171  # EUR/kWh
    data['buy_sell_price']['Elec sell', ] = 0.2172 * 0.15  # Assume selling electricity prices of 15%
    data['buy_sell_price']['Heat buy', ] = 0.073

    # 2040
    _price = pd.read_excel('files/Prices_2040.xlsx')['Norway']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    # 2055
    _price = pd.read_excel('files/Prices_2055.xlsx')['Norway']
    data['buy_sell_price']['Elec buy',] = _price.values
    data['buy_sell_price']['Elec sell',] = _price.values - 0.1634  # taxes

    return data






































########################################################################################################################
# Model Energy Communities (MEC)S

def scenario_City_EC(data, ub):
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['LMAB'].values
    data['demand']['LMAB1', 'Elec'] = _demand
    data['demand']['LMAB2', 'Elec'] = _demand
    data['demand']['LMAB3', 'Elec'] = _demand
    data['demand']['LMAB4', 'Elec'] = _demand
    data['demand']['LMAB5', 'Elec'] = _demand
    data['demand']['LMAB6', 'Elec'] = _demand
    data['demand']['LMAB7', 'Elec'] = _demand
    data['demand']['LMAB8', 'Elec'] = _demand
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'inst-cap'] = 15
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 15
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'inst-cap'] = 55
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'cap-up'] = 55
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'inst-cap'] = 55
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'cap-up'] = 55


    pro = data['storage']
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-c'] = 65
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-c'] = 65
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-c'] = 65
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-p'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-p'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-p'] = 8

    return data


def scenario_Rural_EC(data, ub):
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3 = _demand['SFH3'].values

    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'inst-cap'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'inst-cap'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'cap-up'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'inst-cap'] = 5
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'cap-up'] = 5

    pro = data['storage']
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-c'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-c'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-c'] = 8
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-p'] = 5

    return data


def scenario_Town_EC(data, ub):
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['SMAB'].values
    data['demand']['LMAB1', 'Elec'] = _demand
    data['demand']['LMAB2', 'Elec'] = _demand
    data['demand']['LMAB3', 'Elec'] = _demand
    data['demand']['LMAB4', 'Elec'] = _demand
    data['demand']['LMAB5', 'Elec'] = _demand
    data['demand']['LMAB6', 'Elec'] = _demand
    data['demand']['LMAB7', 'Elec'] = _demand
    data['demand']['LMAB8', 'Elec'] = _demand
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'inst-cap'] = 8
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 8
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'inst-cap'] = 16
    pro.loc[(pro.index.get_level_values('Process') == 'Supply from public grid'), 'cap-up'] = 16
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'inst-cap'] = 16
    pro.loc[(pro.index.get_level_values('Process') == 'Feed-in public grid'), 'cap-up'] = 16

    pro = data['storage']
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-c'] = 20
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-c'] = 20
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-c'] = 20
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'inst-cap-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-lo-p'] = 5
    pro.loc[(pro.index.get_level_values('Storage') == 'Battery'), 'cap-up-p'] = 5

    return data


def scenario_Mixed_EC(data, ub):
    data = scenario_Rural_EC(data, ub)
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['LMAB'].values
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
                pro.index.get_level_values('Process') == 'Solar|PV')), 'inst-cap'] = 15
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Process') == 'Solar|PV')), 'cap-up'] = 15
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
                pro.index.get_level_values('Process') == 'Solar|PV')), 'inst-cap'] = 15
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Process') == 'Solar|PV')), 'cap-up'] = 15

    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
                pro.index.get_level_values('Process') == 'Supply from public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Process') == 'Supply from public grid')), 'cap-up'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
                pro.index.get_level_values('Process') == 'Supply from public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Process') == 'Supply from public grid')), 'cap-up'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
                pro.index.get_level_values('Process') == 'Feed-in public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Process') == 'Feed-in public grid')), 'cap-up'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
                pro.index.get_level_values('Process') == 'Feed-in public grid')), 'inst-cap'] = 60
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Process') == 'Feed-in public grid')), 'cap-up'] = 60

    pro = data['storage']
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB9') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-p'] = 8

    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-c'] = 65
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'inst-cap-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-lo-p'] = 8
    pro.loc[((pro.index.get_level_values('Site') == 'LMAB10') & (
            pro.index.get_level_values('Storage') == 'Battery')), 'cap-up-p'] = 8

    return data


def scenario_Austria(data, ub):
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'Austria']

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region'] == 'Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy',] = _price
    data['buy_sell_price']['Elec sell',] = _price * 0.98  # to prevent buying and selling at same time step.

    return data

def scenario_IBERIAN(data, ub):
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'ES11']

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region'] == 'Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy',] = _price
    data['buy_sell_price']['Elec sell',] = _price * 0.98  # to prevent buying and selling at same time step.

    return data


def scenario_norwegian_radiation(data, ub):

    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'Norway|Vestmidt']

    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    return data

########################################################################################################################
########################################################################################################################
########################################################################################################################
# AUSTRIA

def scenario_Societal_CommitmentxAustriaxCityEC(data, ub):
    data = scenario_City_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data


def scenario_Societal_CommitmentxAustriaxTownEC(data, ub):
    data = scenario_Town_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data


def scenario_Societal_CommitmentxAustriaxMixedEC(data, ub):
    data = scenario_Mixed_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data


def scenario_Societal_CommitmentxAustriaxRuralEC(data, ub):
    data = scenario_Rural_EC(data, ub)
    data = scenario_Austria(data, ub)
    return data

########################################################################################################################
# SPAIN & PORTUGAL (IBERIAN PENINSULA)

def scenario_SocietalxCommitmentxIBERIANxCityEC(data, ub):
    data = scenario_City_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

def scenario_SocietalxCommitmentxIBERIANxTownEC(data, ub):
    data = scenario_Town_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

def scenario_SocietalxCommitmentxIBERIANxMixedEC(data, ub):
    data = scenario_Mixed_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

def scenario_SocietalxCommitmentxIBERIANxRuralEC(data, ub):
    data = scenario_Rural_EC(data, ub)
    data = scenario_IBERIAN(data, ub)

    return data

########################################################################################################################
# NORWAY

def scenario_SocietalxCommitmentxNORWAY_RURALEC(data, ub):
    data = scenario_Rural_EC(data, ub)
    data = scenario_Norway(data, ub)
    return data


def scenario_TechnoxFriendlyxNORWAY_RURALEC(data, ub):

    data = scenario_SocietalxCommitmentxNORWAY_RURALEC(data, ub)

    _demand = pd.read_excel('files/SP_loadprofile_TF.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3 = _demand['SFH3'].values
    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1

    return data


def scenario_DirectedxTransitionxNORWAY_RURALEC(data, ub):
    data = scenario_SocietalxCommitmentxNORWAY_RURALEC(data, ub)

    _demand = pd.read_excel('files/SP_loadprofile_DT.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3 = _demand['SFH3'].values
    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1

    return data


def scenario_GradualxDevelopmentxNORWAY_RURALEC(data, ub):
    data = scenario_SocietalxCommitmentxNORWAY_RURALEC(data, ub)

    _demand = pd.read_excel('files/SP_loadprofile_GD.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3 = _demand['SFH3'].values
    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1

    return data

########################################################################################################################
########################################################################################################################
########################################################################################################################























def scenario_SocietalxCommitment_Norway(data, ub):
    # set solar radiation or Loadfactor|Electricity|Solar accordingly 
    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region']=='Norway|Vestmidt']
    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values
    # print( data['supim']['LMAB10', 'Solar'])
    
    
    # set electricity demand of the buidlings within the neighborhood
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')
    _demand1 = _demand['SFH1'].values
    _demand2 = _demand['SFH2'].values
    _demand3= _demand['SFH3'].values
    
    data['demand']['LMAB1', 'Elec'] = _demand1
    data['demand']['LMAB2', 'Elec'] = _demand1
    data['demand']['LMAB3', 'Elec'] = _demand1
    data['demand']['LMAB4', 'Elec'] = _demand2
    data['demand']['LMAB5', 'Elec'] = _demand2
    data['demand']['LMAB6', 'Elec'] = _demand2
    data['demand']['LMAB7', 'Elec'] = _demand3
    data['demand']['LMAB8', 'Elec'] = _demand3
    data['demand']['LMAB9', 'Elec'] = _demand3
    data['demand']['LMAB10', 'Elec'] = _demand1
    # print(data['demand']['LMAB10', 'Elec'])
    
    _price = pd.read_excel('files/EMPSW_elprices_mean.xlsx')
    _price = _price.loc[_price['region']=='Norway|Vestmidt']['2030'].values
    data['buy_sell_price']['Elec buy', ] = _price
    data['buy_sell_price']['Elec sell', ] = _price*0.98 # to prevent buying and selling at same time step.
    # print(data['buy_sell_price']['Elec sell', ])
    return data


def scenario_Austrian_RuralxEC(data, ub):
    data = scenario_SocietalxCommitment_Norway(data, ub)

    _solar = pd.read_excel('files/NUTS2_loadfactor_solar.xlsx')
    _solar = _solar.loc[_solar['region'] == 'Austria']
    data['supim']['LMAB1', 'Solar'] = _solar['value'].values
    data['supim']['LMAB2', 'Solar'] = _solar['value'].values
    data['supim']['LMAB3', 'Solar'] = _solar['value'].values
    data['supim']['LMAB4', 'Solar'] = _solar['value'].values
    data['supim']['LMAB5', 'Solar'] = _solar['value'].values
    data['supim']['LMAB6', 'Solar'] = _solar['value'].values
    data['supim']['LMAB7', 'Solar'] = _solar['value'].values
    data['supim']['LMAB8', 'Solar'] = _solar['value'].values
    data['supim']['LMAB9', 'Solar'] = _solar['value'].values
    data['supim']['LMAB10', 'Solar'] = _solar['value'].values

    return data

def scenario_Austria_TownxEC(data, ub):
    data = scenario_Austrian_RuralxEC(data, ub) # set solar profile and electricity price accordingly

    # set demand profiles in the EC
    _demand = pd.read_excel('files/SP_loadprofile_SC.xlsx')['SMAB'].values
    data['demand']['LMAB1', 'Elec'] = _demand
    data['demand']['LMAB2', 'Elec'] = _demand
    data['demand']['LMAB3', 'Elec'] = _demand
    data['demand']['LMAB4', 'Elec'] = _demand
    data['demand']['LMAB5', 'Elec'] = _demand
    data['demand']['LMAB6', 'Elec'] = _demand
    data['demand']['LMAB7', 'Elec'] = _demand
    data['demand']['LMAB8', 'Elec'] = _demand
    data['demand']['LMAB9', 'Elec'] = _demand
    data['demand']['LMAB10', 'Elec'] = _demand

    pro = data['process']
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'),'inst-cap'] = 8
    pro.loc[(pro.index.get_level_values('Process') == 'Solar|PV'), 'cap-up'] = 8
    print(data['process'])

    return data













def scenario_base(data):
    return data

#______________________________________________________________________________
    
"""
2_No Combined Heat Pump Unit
"""

def scenario_mod_CO2_price(data):
    commodities = data['commodity']
    co2_commodities_only = (commodities.index.get_level_values('Type') == 'Env')
    commodities.loc[co2_commodities_only, 'price'] = 50
    data['buy_sell_price']['Elec buy', ] *= 1.065
    data['buy_sell_price']['Elec sell', ] *= 1.065
    return data

def scenario_very_high_CO2_price(data):
    commodities = data['commodity']
    co2_commodities_only = (commodities.index.get_level_values('Type') == 'Env')
    commodities.loc[co2_commodities_only, 'price'] = 100
    data['buy_sell_price']['Elec buy', ] *= 1.189
    data['buy_sell_price']['Elec sell', ] *= 1.189
    return data

#def scenario_very_very_high_CO2_price(data):
#    commodities = data['commodity']
#    co2_commodities_only = (commodities.index.get_level_values('Type') == 'Env')
#    commodities.loc[co2_commodities_only, 'price'] = 150
#    data['buy_sell_price']['Elec buy',] *= 1.31
#    data['buy_sell_price']['Elec sell',] *= 1.31
#    return data

#______________________________________________________________________________
    
"""
3_Green_Field
"""

def scenario_Green_Field(data):
    data['process']['inst-cap'] = 0
    data['process']['cap-lo'] = 0
    data['process']['cap-up'] = 10
    return data

#______________________________________________________________________________
def scenario_DH_Favored(data):
    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (
                pro.index.get_level_values('Process') == 'District Heating')), 'cap-lo'] = 5
    pro.loc[((pro.index.get_level_values('Site') == 'Neubau') & (
                pro.index.get_level_values('Process') == 'District Heating')), 'cap-lo'] = 3
    return data
#______________________________________________________________________________



"""
4_Cooling_Demand
"""

def scenario_district_heating_all(data):
    data = scenario_high_CO2_price(data)
    pr = data['process']
    district_heating_only = (pr.index.get_level_values('Process') == 'District Heating')
    pr.loc[district_heating_only, 'inst-cap'] = 5
    pr.loc[district_heating_only, 'cap-up'] = 5
    absorption_machine_only = (pr.index.get_level_values('Process') == 'Absorption Machine')
    pr.loc[absorption_machine_only, 'inv-cost'] *= 1/5
    pr.loc[absorption_machine_only, 'fix-cost'] *= 1/5
    #data['buy_sell_price']['Heat buy', ] *= 0.5
    return data
    
#______________________________________________________________________________

"""
5_No_Geothermal
"""
def scenario_high_CO2_price(data):
    commodities = data['commodity']
    co2_commodities_only = (commodities.index.get_level_values('Type') == 'Env')
    commodities.loc[co2_commodities_only, 'price'] = 250
    data['buy_sell_price']['Elec buy', ] *= 1.56
    data['buy_sell_price']['Elec sell', ] *= 1.56
    return data

def scenario_No_Geothermal_GF(data):
    data = scenario_high_CO2_price(data)
    data['process']['inst-cap'] = 0
    data['process']['cap-lo'] = 0
    data['process']['cap-up'] = 100
    pr = data['process']
    geothermal_only = (pr.index.get_level_values('Process') == 'Geothermal')
    pr.loc[geothermal_only, 'inv-cost'] = 999999999
    pr.loc[geothermal_only, 'inst-cap'] = 0
    pr.loc[geothermal_only, 'cap-lo'] = 0
    geothermal_cooling_only = (pr.index.get_level_values('Process') == 'Geothermal Cooling')
    pr.loc[geothermal_cooling_only, 'inv-cost'] = 999999999
    pr.loc[geothermal_cooling_only, 'inst-cap'] = 0
    pr.loc[geothermal_cooling_only, 'cap-lo'] = 0
    return data

#______________________________________________________________________________

"""
6_High_HP_Efficiency 
"""

def scenario_high_efficiency_heat_pump_high_CO2(data):
    data = scenario_very_high_CO2_price(data)
    data['eff_factor']['Neubau', 'Heat Pump (air water)'] += 1
    return data

def scenario_high_CO2_and_HPeff_GF(data):
    data = scenario_high_efficiency_heat_pump_high_CO2(data)
    data = scenario_Green_Field(data)
    return data

#______________________________________________________________________________

"""
7_No_Storages_and_Transmission
"""

def scenario_no_storages(data):
    data['storage']['cap-up-c']=0
    return data

def scenario_no_transmission(data):
    data['transmission']['cap-up'] = 0
    return data

def scenario_no_storages_and_transmission(data):
    data['storage']['cap-up-c'] = 0
    data['transmission']['cap-up'] = 0
    return data

#______________________________________________________________________________
"""
8_Geothermal_Efficiency
"""

def scenario_Geothermal_3_Efficiency(data):
    pro_co = data['process_commodity']
    geothermal_only = ((pro_co.index.get_level_values('Process') == 'Geothermal') & (pro_co.index.get_level_values('Commodity') == 'Heat'))
    pro_co.loc[geothermal_only, 'ratio'] = 3
    return data
    
#______________________________________________________________________________
    
"""
9_Competition between District Heating and CHPU at Viertel2
"""

def scenario_CHPU_vs_DH_Base_CO2(data):
    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'cap-up'] = 5
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'inv-cost'] = 60000
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'fix-cost'] = 60000*2/100
    return data

def scenario_CHPU_vs_DH_Mod_CO2(data):
    data = scenario_mod_CO2_price(data)
    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'cap-up'] = 5
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'inv-cost'] = 60000
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'fix-cost'] = 60000*2/100
    return data

def scenario_CHPU_vs_DH_Interim_CO2(data):
    commodities = data['commodity']
    co2_commodities_only = (commodities.index.get_level_values('Type') == 'Env')
    commodities.loc[co2_commodities_only, 'price'] = 150
    data['buy_sell_price']['Elec buy', ] *= 1.31
    data['buy_sell_price']['Elec sell', ] *= 1.31
    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'cap-up'] = 5
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'inv-cost'] = 60000
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'fix-cost'] = 60000*2/100
    return data
    
def scenario_CHPU_vs_DH_High_CO2(data):
    data = scenario_high_CO2_price(data)
    pro = data['process']
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'cap-up'] = 5
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'inv-cost'] = 60000
    pro.loc[((pro.index.get_level_values('Site') == 'Viertel2') & (pro.index.get_level_values('Process') == 'District Heating')),'fix-cost'] = 60000*2/100
    return data   
    
def scenario_Mod_Neubau_Heat_Demand(data):
    data = scenario_Green_Field(data)
    data['demand']['Neubau', 'Heat'] *= 4
    print(data['demand']['Neubau', 'Heat'])
    return data

def scenario_baseline90(data, ub):
    data['global_prop']['value'][2050, 'Cost limit'] = ub*0.9
    return data

def scenario_baseline1(data, ub):
    data['global_prop']['value'][2050, 'Cost limit'] = ub*0.8
    return data

def scenario_baseline2(data, ub):
    data['global_prop']['value'][2050, 'Cost limit'] = ub*0.8
    return data

def scenario_baseline3(data, ub):
    data['global_prop']['value'][2050, 'Cost limit'] = ub*0.8
    return data

def scenario_baseline4(data, ub):
    data['global_prop']['value'][2050, 'Cost limit'] = ub*0.9
    return data


def scenario_greenfield(data):
    # set existing capacities to zero (supply from scratch)
    data['process']['inst-cap'] = 0
    data['process']['cap-lo'] = 0
    data['transmission']['inst-cap'] = 0
    data['storage']['inst-cap-c'] = 0
    return data


    
    
    
    