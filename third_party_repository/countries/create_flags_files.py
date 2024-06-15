import os

import pandas as pd

df = pd.read_csv('country_data.csv')
df = df[df['isIndependent'] == 'Yes'][['Name', 'OfficialName', 'Capital', 'Language', 'Region',
                                       'RegionCode', 'CallingCode', 'NationalNumberLength', 'Flag', 'Currency', 'IsoAlpha2', 'IsoAlpha3']]
df.loc[df['Name'] == 'Namibia', 'IsoAlpha2'] = 'NA'

flags_dir = "flags"
if not os.path.exists(flags_dir):
    os.makedirs(flags_dir)

for index, row in df.iterrows():
    isocode = row['IsoAlpha2']
    flag_content = row['Flag']
    file_path = os.path.join(flags_dir, f"{isocode}.svg")
    with open(file_path, "w") as f:
        f.write(flag_content)
