# Import necessary libraries
import pandas as pd
from chembl_webresource_client.new_client import new_client

# Target search for coronavirus
target = new_client.target
target_query = target.search('coronavirus')
targets = pd.DataFrame.from_dict(target_query)
targets

#Assign the 5th entry to variable
selected_target = targets.target_chembl_id[4]
selected_target

#retrieve bioactivity data for conronavirus 3C-like proteinase
activity = new_client.activity
res = activity.filter(target_chembl_id=selected_target).filter(standard_type="IC50")
df = pd.DataFrame.from_dict(res)
df.head(3)
df.standard_type.unique()
df.to_csv(r'/Users/sam/miniconda3/bin/ bioactivity_data_raw.csv', index=False)

#handling missing data
df2 = df[df.standard_value.notna()]
df2

#label compounds as either active, inactive or intermediate
bioactivity_class = []
for i in df2.standard_value:
    if float(i) >= 10000:
        bioactivity_class.append("inactive")
    elif float(i) <= 1000:
        bioactivity_class.append("active")
    else:
        bioactivity_class.append("intermediate")

#iterate molecule_chembl_id to a list
mol_cid = []
for i in df2.molecule_chembl_id:
    mol_cid.append(i)

#iterate canonical_smiles to a list
canonical_smiles = []
for i in df2.canonical_smiles:
    canonical_smiles.append(i)

#iterate standard_value to a list
standard_value = []
for i in df2.standard_value:
    standard_value.append(i)

#Combine 4 lists into a dataframe
data_tuples = list(zip(mol_cid, canonical_smiles, bioactivity_class, standard_value))
df3 = pd.DataFrame( data_tuples, columns=['molecule_chembl_id', 'canonical_smiles', 'bioactivity_class', 'standard_value'])
df3

#alternative method to combining into dataframe (remove the # from lines 58-60 and replace above)
#selection = ['molecule_chembl_id', 'canonical_smiles', 'standard_value']
#df3 = df2[selection]
#df3

df3.to_csv(r'/Users/sam/miniconda3/bin/ bioactivity_preprocessed_data.csv', index=False)
