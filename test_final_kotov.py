#  This script aims to complete the task in supplement materials
#  https://docs.google.com/document/d/158xCyqyGMJ52C88aAgzFle0eZ98NUmHmMnD1ABk80Tw/edit?pli=1&tab=t.0

import pandas as pd

#  -- functions

def fdata_clean(series):
    
    cleaned_series = series.str.strip()
    cleaned_series = cleaned_series.str.replace(r'\?+', '', regex=True)
    cleaned_series = cleaned_series.str.title()
    cleaned_series = cleaned_series.str.replace(r'[^\w\s\/&-]', '', regex=True)
    cleaned_series = cleaned_series.str.replace(r'\s*-\s*', '-', regex=True)
    cleaned_series = cleaned_series.str.replace(r'\s+', ' ', regex=True)
    cleaned_series = cleaned_series.str.replace(r'\-$', ' ', regex=True)
    cleaned_series = cleaned_series.str.strip()
    
    return cleaned_series

def faddress_normalize(series):
    
    normalized_series = series.str.replace(r'\bAve\.?\b', 'Avenue', regex=True)
    normalized_series = normalized_series.str.replace(r'\bBlvd\.?\b', 'Boulevard', regex=True)
    normalized_series = normalized_series.str.replace(r'\bBoul\.?\b', 'Boulevard', regex=True)
    normalized_series = normalized_series.str.replace(r'\bRd\.?\b', 'Road', regex=True)
    normalized_series = normalized_series.str.replace(r'\bSt\.?\b', 'Street', regex=True)
    normalized_series = normalized_series.str.replace(r'\bStreet\.?\b', 'Street', regex=True)
    normalized_series = normalized_series.str.replace(r'\bCres\.?\b', 'Crescent', regex=True)
    normalized_series = normalized_series.str.replace(r'\bDr\.?\b', 'Drive', regex=True)
    normalized_series = normalized_series.str.replace(r'\bLn\.?\b', 'Lane', regex=True)
    normalized_series = normalized_series.str.replace(r'\bPkwy\.?\b', 'Parkway', regex=True)
    normalized_series = normalized_series.str.replace(r'\bCt\.?\b', 'Court', regex=True)
    normalized_series = normalized_series.str.replace(r'\bPl\.?\b', 'Place', regex=True)
    normalized_series = normalized_series.str.replace(r'\bTerr\.?\b', 'Terrace', regex=True)
    normalized_series = normalized_series.str.replace(r'\bHwy\.?\b', 'Highway', regex=True)
    normalized_series = normalized_series.str.replace(r'\bCir\.?\b', 'Circle', regex=True)
    normalized_series = normalized_series.str.replace(r'[^\w\s-]', '', regex=True)
    normalized_series = normalized_series.str.replace(r'\s+', ' ', regex=True)
    
    return normalized_series

def fcompany_name_normalize(series):
    
    normalized_series = series.str.replace('Inc', '', regex=True)
    normalized_series = normalized_series.str.replace('Ltd', '', regex=True)
    normalized_series = normalized_series.str.replace('&', 'and', regex=False)
    normalized_series = normalized_series.str.replace('Limited', '', regex=True)
    normalized_series = normalized_series.str.replace('Lp', '', regex=True)
    normalized_series = normalized_series.str.replace(r'\s+', ' ', regex=True)
    
    return normalized_series
    
def fcountry_normalize(series):
    
    
    
    if series is None:
        return
    
    usa_indices = series[series['postal_zip'].str.match(r'^\d{5,}$', na=False)].index
    series.loc[usa_indices, 'country'] = 'USA'
    
    can_indices = series[series['postal_zip'].str.match(r'^[A-Z]\d[A-Z]\d[A-Z]\d$', na=False)].index
    series.loc[can_indices, 'country'] = 'Canada'
    
    return series

def fstate_normalize(series):
    
    states_to_map = {
        # Canada
        'On': 'ON',
        'Ontario': 'ON',
        'Ontraio': 'ON',
        'Qc': 'QC',
        'Québec': 'QC',
        'Quebec': 'QC',
        'Qubec': 'QC',
        'Bc': 'BC',
        'Sk': 'SK',
        'Saskatchewan': 'SK',
        'Manitoba': 'MB',
        'Mb': 'MB',
        'New Brunswick': 'NB',
        'Nova Scotia': 'NS',
        'Ns': 'NS',
        'Nl': 'NL',
        'Nb': 'NB',
        'Pe': 'PE',
        'Pei': 'PE',
        'Ab': 'AB',
        'Alberta': 'AB',
        'Toronto On': 'ON',
        'Toronto': 'ON',
        'Kronau': 'SK',
        'Montréal': 'QC',
        'British Columbia': 'BC',
        
        # USA
        'Wi': 'WI',
        'Mn': 'MN',
        'Ma': 'MA',
        'Nc': 'NC',
        'Sc': 'SC',
        'Pa': 'PA',
        'Fl': 'FL',
        'Il': 'IL',
        'In': 'IN',
        'Texas': 'TX',
        'Tx': 'TX',
        'Or': 'OR',
        'Mo': 'MO',
        'Ok': 'OK',
        'Minnesota': 'MN',
        
        
        # Not defined
        'M5V 2H2': None
        
    }

    series = series.map(states_to_map) 
    
    return series
    
def fpostalzip_normalize(series):
    
    series = series.str.strip()
    series = series.str.replace(r'\s+', '', regex=True)
    series = series.str.replace(r'-', '', regex=True)
    
    return series
 
#  initialization
   
#  loading data to previous data cleaning/normalization

dataset1 = pd.read_csv('/Users/bazilio97/Documents/DataEngineer_Task/company_dataset_1.csv')
dataset2 = pd.read_csv('/Users/bazilio97/Documents/DataEngineer_Task/company_dataset_2.csv')


dataset1.rename({
    'custnmbr': 'customer_number',
    'addrcode': 'address_code',
    'custname': 'company_name',
    'sStreet1': 'address_1',
    'sStreet2': 'address_2',
    'sCity': 'city',
    'sProvState': 'state',
    'sCountry': 'country',
    'sPostalZip': 'postal_zip'
    }, axis=1, inplace=True)

dataset2.rename({
    'custnmbr': 'customer_number',
    'addrcode': 'address_code',
    'custname': 'company_name',
    'address1': 'address_1',
    'address2': 'address_2',
    'address3': 'address_3',
    'ccode': 'country_code',
    'state': 'state',
    'zip': 'postal_zip'
    }, axis=1, inplace=True)

#  data cleaning/normalization

dataset1_cleaned = dataset1.apply(fdata_clean)
dataset1_cleaned = fcountry_normalize(dataset1_cleaned)
dataset1_cleaned['state'] = fstate_normalize(dataset1_cleaned['state'])
dataset1_cleaned['company_name'] = fcompany_name_normalize(dataset1_cleaned['company_name'])
for col in ['address_1', 'address_2']:
    dataset1_cleaned[col] = faddress_normalize(dataset1_cleaned[col])
   

dataset2_cleaned = dataset2.apply(fdata_clean)
dataset2_cleaned['postal_zip'] = fpostalzip_normalize(dataset2_cleaned['postal_zip'])
dataset2_cleaned = fcountry_normalize(dataset2_cleaned)
dataset2_cleaned['state'] = fstate_normalize(dataset2_cleaned['state'])
dataset2_cleaned['company_name'] = fcompany_name_normalize(dataset2_cleaned['company_name'])
for col in ['address_1', 'address_2', 'address_3']:
    dataset2_cleaned[col] = faddress_normalize(dataset2_cleaned[col])


cols = ['company_name', 'address_1', 'address_code', 'country', 'state', 'postal_zip', 'city']
dataset1_cleaned = dataset1_cleaned.drop_duplicates(subset=cols)
dataset2_cleaned = dataset2_cleaned.drop_duplicates(subset=cols)

#  matching companies between dataset1_cleaned and dataset2_cleaned based on
#  company name and location

company_matches = pd.merge(
    dataset1_cleaned,
    dataset2_cleaned,
    on=['company_name', 'country', 'state', 'postal_zip'],
    how='left',
    indicator=True 
)


#  creating a merged dataset that contains: 
#  - all unique companies from dataset1_cleaned
#  - including corresponding company matches from dataset2_cleaned where they exist
#  - containing column with list of locations for company from dataset1_cleaned
#  - containing column with list of locations for company from dataset2_cleaned
#  - containing column with overlapping locations between two companies
#  if no locations overlap – keep company name match, and leave overlapping locations column empty 


locations_dataset1 = dataset1_cleaned.groupby('company_name').apply(
    lambda x: list(zip(x['state'], x['postal_zip'], x['country'], x['city']))
).reset_index(name='locations_dataset1')

locations_dataset2 = dataset2_cleaned.groupby('company_name').apply(
    lambda x: list(zip(x['state'], x['postal_zip'], x['country'], x['city']))
).reset_index(name='locations_dataset2')

merged = pd.merge(
    locations_dataset1,
    locations_dataset2,
    on='company_name',
    how='left'
)

merged['overlapping_locations'] = merged.apply(
    lambda row: list(set(row['locations_dataset1']).intersection(row['locations_dataset2']))
                if isinstance(row['locations_dataset2'], list) else [], axis=1 )


# calculating the match rate %

total_companies = len(merged)
matched_companies = merged['locations_dataset2'].notna().sum()

match_rate = round( matched_companies / total_companies * 100, 2 )

# calculating the unmatch rate %

all_companies = set(dataset1_cleaned['company_name']).union(dataset2_cleaned['company_name'])
matched_companies = set(dataset1_cleaned['company_name']).intersection(dataset2_cleaned['company_name'])
unmatched_companies = all_companies - matched_companies
unmatched_rate = round(len(unmatched_companies) / len(all_companies) * 100, 2)

#  calculating one-to-many match rate %

one_to_many_count = merged['locations_dataset2'].apply(lambda x: isinstance(x, list) and len(x) > 1).sum()
total_companies = len(merged)
one_to_many_rate = round(one_to_many_count / total_companies * 100, 2)

merged.to_csv('/Users/bazilio97/Documents/DataEngineer_Task/final_test_kotov.csv', index=False)

print('match rate: {}, unmatched rate: {}, one to many rate: {}'.format(match_rate, unmatched_rate, one_to_many_rate))





