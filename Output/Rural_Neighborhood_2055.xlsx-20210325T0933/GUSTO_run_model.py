# import required packages
import os
import shutil
import pandas as pd
import urbs

import GUSTO_compare_results as cr

# change terminal display
pd.set_option('display.max_columns', None)  
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

# set up directory file
input_files = 'Rural_Neighborhood_2055.xlsx'
input_dir = 'Input'
input_path = os.path.join(input_dir, input_files)

# set output folder name individually
result_name = input_files
result_dir = urbs.prepare_result_directory(result_name)  # name + time stamp

# copy input file to result directory
try:
    shutil.copytree(input_path, os.path.join(result_dir, input_dir))
except NotADirectoryError:
    shutil.copyfile(input_path, os.path.join(result_dir, input_files))
# copy run file to result directory
shutil.copy(__file__, result_dir)

# choose Solver (cplex, glpk, gurobi, ...)
# solver needs to be installed to environment previously
solver = 'gurobi'


# simulation timesteps
(offset, length) = (-1, 24)  # time step selection
timesteps = range(offset, length)

dt = 1  # length of each time step (unit: hours)

# detailed reporting commodity/sites
report_tuples = [
    (2025, 'LMAB1', 'Elec'),
    (2025, 'LMAB2', 'Elec'),
    (2025, 'LMAB3', 'Elec'),
    (2025, 'LMAB4', 'Elec'),
    (2025, 'LMAB5', 'Elec'),
    (2025, 'LMAB6', 'Elec'),
    (2025, 'LMAB7', 'Elec'),
    (2025, 'LMAB8', 'Elec'),
    (2025, 'LMAB9', 'Elec'),
    (2025, 'LMAB10', 'Elec'),
    (2025, 'LMAB1', 'Heat'),
    (2025, 'LMAB2', 'Heat'),
    (2025, 'LMAB3', 'Heat'),
    (2025, 'LMAB4', 'Heat'),
    (2025, 'LMAB5', 'Heat'),
    (2025, 'LMAB6', 'Heat'),
    (2025, 'LMAB7', 'Heat'),
    (2025, 'LMAB8', 'Heat'),
    (2025, 'LMAB9', 'Heat'),
    (2025, 'LMAB10', 'Heat')
    ]

# optional: define names for sites in report_tuples
report_sites_name = {'LMAB1': 'SFH1'}

# plotting commodities/sites
plot_tuples = []

# optional: define names for sites in plot_tuples
plot_sites_name = None

# plotting timesteps
plot_periods = {
    'all': timesteps[1:]
}

# add or change plot colors
my_colors = {
    'LMAB1': (176, 202, 199),
    'LMAB2': (255, 87, 34),
    'LMAB3': (240, 154, 233),
    'LMAB4': (75, 93, 103)
}
for country, color in my_colors.items():
    urbs.COLORS[country] = color

# B) run only maximum points of pareto front (three dimensions)
scenarios = [
    [urbs.scenario_HighxElectrification, 'cost'],
]

for scenario, objective in scenarios:

    # tba: stop criteria if 'upper_bound' < Cost minimal solution (A)
    # then calculate solution with (A) and stop algorithm

    print('Running scenario:', scenario.__name__[9:])
    print('Selected objective function:', objective)
    prob = urbs.run_scenario(input_path, solver, timesteps, scenario,
                             result_dir, dt, objective,
                             plot_tuples=plot_tuples,
                             plot_sites_name=plot_sites_name,
                             plot_periods=plot_periods,
                             report_tuples=report_tuples,
                             report_sites_name=report_sites_name,
                             input_file_name=input_files)


cr.generate_comparison_figure()

