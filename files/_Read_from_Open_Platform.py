import pyam

# read from the open platform (scenario explorer)
_dataframe = pyam.read_iiasa(
    'openentrance',
    model='GUSTO v1.0',
    scenario='CS3_2030oE_Storyline',
    region='Norway|Finmark',
    variable='LoadFactor|Electricity|Solar|Profile')

_dataframe.as_pandas().to_excel('Solar.xlsx')