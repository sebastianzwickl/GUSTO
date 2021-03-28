import pandas as pd
from .input import get_input
from .output import get_constants, get_timeseries
from .util import is_string
import numpy as np
from datetime import datetime, timedelta


def _get_valid_iamc_timestamp(time):
    [_year, _hour] = str(time).split('|')
    _str = str(_year)+'-01-01 00:00'
    _var_time = datetime.strptime(_str, '%Y-%m-%d %H:%M')
    _to_ret = str(_var_time + timedelta(hours=int(_hour)))+' +01:00'
    return _to_ret


def _get_variable_names_from_nomenclature(_var=None):
    _dict_with_nomenclature_variable_names = {
        # Process capacities
        'Feed-in public grid': 'Capacity|Electricity|Network|Imported',
        'Heat Pump (air water)': 'Capacity|Electricity|Heat Pump',
        'Heat Pump (ground)': 'Capacity|Electricity|Geothermal',
        'Initial heat system': 'Capacity|Heat|Init Heat System',
        'Solarthermal': 'Capacity|Heat|Solarthermal',
        'Solar|PV': 'Capacity|Electricity|Solar PV',
        'Supply from public grid': 'Capacity|Electricity|Network|Exported',
        'Wind|Onshore': 'Capacity|Electricity|OnShore',

        # Distribution line capacities
        'Capacity|Distribution line': 'Network|Distribution|Electricity|Maximum Flow',

        # Commodity sums need to be adjusted

        # Timeseries and energy production
        'Created|Supply from public grid': 'Active Power|Electricity|Network|Imported'
    }

    if _var in _dict_with_nomenclature_variable_names.keys():
        return _dict_with_nomenclature_variable_names[_var]
    else:
        return _var


def write_iamc(output_df, model, scenario, region, variable, unit, time, values):

    if isinstance(variable, list):
        for _index, _val in enumerate(variable):
            variable[_index] = _get_variable_names_from_nomenclature(_val)

        for _index, _val in enumerate(time):
            if '|' in str(_val):
                time[_index] = _get_valid_iamc_timestamp(_val)
            else:
                pass
    else:
        variable = _get_variable_names_from_nomenclature(variable)
        if '|' in str(time):
            time = _get_valid_iamc_timestamp(time)
        else:
            pass

    if isinstance(values, list):
        _df = pd.DataFrame({'model': model,
                            'scenario': scenario,
                            'region': region,
                            'variable': variable,
                            'unit': unit,
                            'year': time,
                            'value': values})
    elif np.isscalar(values):
        _df = pd.DataFrame({'model': model,
                            'scenario': scenario,
                            'region': region,
                            'variable': variable,
                            'unit': unit,
                            'year': time,
                            'value': values}, index=[0])
    else:
        _df = pd.DataFrame({'model': model,
                            'scenario': scenario,
                            'region': region,
                            'variable': variable,
                            'unit': unit,
                            'year': time,
                            'value': values})

    output_df = output_df.append(_df)
    return output_df


def report(instance, filename, report_tuples=None, report_sites_name={}, scenario=None, input_file_name=None):
    print(filename)
    _to_results = filename.split('scenario')[0]

    """Write result summary to a spreadsheet file

    Args:
        - instance: a urbs model instance;
        - filename: Excel spreadsheet filename, will be overwritten if exists;
        - report_tuples: (optional) list of (sit, com) tuples for which to
          create detailed timeseries sheets;
        - report_sites_name: (optional) dict of names for created timeseries
          sheets
    """

    # default to all demand (sit, com) tuples if none are specified
    if report_tuples is None:
        report_tuples = get_input(instance, 'demand').columns

    costs, cpro, ctra, csto, df = get_constants(instance)

    # write results in extended iamc format to results.xlsx file
    _model = 'GUSTO v1.0'

    _scenario = scenario.split('_')[1]
    if 'x' in _scenario:
        _scenario = _scenario.replace('x', ' ', 1)

    _region = input_file_name.split('_')[0]
    _variable = costs.keys()
    # or overwrite according to nomenclature
    _variable = ['Investment|Energy Supply', 'Fixed Cost|Energy Supply', 'Variable Cost|Energy Supply',
                 'Fuel Cost|Energy Supply', 'External Cost', 'Revenues', 'Purchase']
    _unit = 'EUR'
    _year = input_file_name.split('_')[2].split('.')[0]
    _value = np.round(costs.values, 3)

    _write_dataframe = pd.DataFrame()
    _write_dataframe = write_iamc(_write_dataframe, _model, _scenario, _region, _variable, _unit, _year, _value)

    _writer = pd.ExcelWriter(_to_results+'Results_in_extended_IAMC_format.xlsx')
    _write_dataframe.to_excel(_writer, 'Total costs', index=False)

    _write_dataframe = pd.DataFrame()
    _unit = 'kW'
    for _a, _b, _c in cpro['Total'].index:
        _write_dataframe = write_iamc(
            _write_dataframe, _model, _scenario, _b, _c, _unit, _a, np.round(cpro['Total'][_a, _b, _c], 3))
    _write_dataframe.to_excel(_writer, 'Process capacities', index=False)

    _write_dataframe = pd.DataFrame()
    _unit = 'kW'

    for _a, _in, _out, _typ, _com in ctra['Total'].index:
        _write_dataframe = write_iamc(
            _write_dataframe, _model, _scenario, _in+'>'+_out, 'Capacity|Distribution line', _unit, _a, np.round(ctra['Total'][_a, _in, _out, _typ, _com], 3))
    _write_dataframe.to_excel(_writer, 'Distribution line capacities', index=False)

    # create spreadsheet writer object
    with pd.ExcelWriter(filename) as writer:

        # write constants to spreadsheet
        costs.to_frame().to_excel(writer, 'Costs')
        cpro.to_excel(writer, 'Process caps')
        ctra.to_excel(writer, 'Transmission caps')
        csto.to_excel(writer, 'Storage caps')
        df.to_excel(writer, 'Global pareto front values', index=False)


        # initialize timeseries tableaus
        energies = []
        timeseries = {}
        help_ts = {}

        # collect timeseries data
        for stf, sit, com in report_tuples:

            # wrap single site name in 1-element list for consistent behavior
            if is_string(sit):
                help_sit = [sit]
            else:
                help_sit = sit
                sit = tuple(sit)

            # check existence of predefined names, else define them
            try:
                report_sites_name[sit]
            except BaseException:
                report_sites_name[sit] = str(sit)

            for lv in help_sit:
                (created, consumed, stored, imported, exported,
                 dsm, voltage_angle) = get_timeseries(instance, stf, com, lv)

                overprod = pd.DataFrame(
                    columns=['Overproduction'],
                    data=created.sum(axis=1) - consumed.sum(axis=1) +
                    imported.sum(axis=1) - exported.sum(axis=1) +
                    stored['Retrieved'] - stored['Stored'])

                tableau = pd.concat(
                    [created, consumed, stored, imported, exported, overprod,
                     dsm, voltage_angle],
                    axis=1,
                    keys=['Created', 'Consumed', 'Storage', 'Import from',
                          'Export to', 'Balance', 'DSM', 'Voltage Angle'])
                help_ts[(stf, lv, com)] = tableau.copy()

                # timeseries sums
                help_sums = pd.concat([created.sum(), consumed.sum(),
                                       stored.sum().drop('Level'),
                                       imported.sum(), exported.sum(),
                                       overprod.sum(), dsm.sum()],
                                      axis=0,
                                      keys=['Created', 'Consumed', 'Storage',
                                            'Import', 'Export', 'Balance',
                                            'DSM'])
                try:
                    timeseries[(stf, report_sites_name[sit], com)] = \
                        timeseries[(stf, report_sites_name[sit], com)].add(
                        help_ts[(stf, lv, com)], axis=1, fill_value=0)
                    sums = sums.add(help_sums, fill_value=0)
                except BaseException:
                    timeseries[(stf, report_sites_name[sit], com)] = help_ts[
                        (stf, lv, com)]
                    sums = help_sums

            # timeseries sums
            sums = pd.concat([created.sum(), consumed.sum(),
                              stored.sum().drop('Level'),
                              imported.sum(), exported.sum(), overprod.sum(),
                              dsm.sum()],
                             axis=0,
                             keys=['Created', 'Consumed', 'Storage', 'Import',
                                   'Export', 'Balance', 'DSM'])
            energies.append(sums.to_frame("{}.{}.{}".format(stf, sit, com)))

        _all_data_to_file = pd.DataFrame()
        # write timeseries data (if any)
        if timeseries:
            # concatenate Commodity sums
            energy = pd.concat(energies, axis=1).fillna(0)
            energy.to_excel(writer, 'Commodity sums')

            _write_dataframe = pd.DataFrame()
            _unit = 'kWh'
            for _k in energy.keys():
                _string = _k.split('.')
                for _i1, _i2 in energy.index:
                    _write_dataframe = write_iamc(
                        _write_dataframe, _model, _scenario, _string[1], _i1+'|'+_i2,
                        _unit,
                        _string[0],
                        np.round(energy[_k][_i1][_i2], 3)
                    )
            _write_dataframe.to_excel(_writer, 'Commodity sums', index=False)

            # write new electricity demand profile to results file
            # write timeseries to individual sheets
            for stf, sit, com in report_tuples:
                if isinstance(sit, list):
                    sit = tuple(sit)
                # sheet names cannot be longer than 31 characters...
                sheet_name = "{}.{}.{} timeseries".format(
                    stf, report_sites_name[sit], com)[:31]
                timeseries[(stf, report_sites_name[sit], com)].to_excel(
                    writer, sheet_name)

                _write_dataframe = pd.DataFrame()
                _dataframe = timeseries[(stf, report_sites_name[sit], com)]
                for _k1, _k2 in _dataframe.keys():
                    for _i in timeseries[(stf, report_sites_name[sit], com)].index:
                        _write_dataframe = write_iamc(_write_dataframe,
                                                      _model, _scenario, report_sites_name[sit], _k1+'|'+_k2, _unit,
                                                      str(stf)+'|'+str(_i),
                                                      np.round(
                                                          timeseries[
                                                              (stf, report_sites_name[sit], com)][_k1, _k2][_i], 3))
                _write_dataframe.to_excel(_writer, sheet_name, index=False)
                _all_data_to_file = _all_data_to_file.append(_write_dataframe)

    _all_data_to_file.to_excel(_writer, 'IAMC format (all timeseries)', index=False)
    _writer.save()
