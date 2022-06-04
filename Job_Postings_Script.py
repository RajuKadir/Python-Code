import requests, json, csv, pandas as pd, os, glob
from datetime import datetime

##Intialize API access

ClientID = "#####"
SecretID = "#####"
Scope = "#####"

##Grab current month and year 

current_month = datetime.now().strftime('%m')
current_year_full = datetime.now().strftime('%Y')
EndDate = '{}-{}'.format(current_year_full , current_month)

##Grab Token Key from EMSI API

url = "https://auth.emsicloud.com/connect/token"

payload = f"client_id={ClientID}&client_secret={SecretID}&grant_type=client_credentials&scope={Scope}"

headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers)
token_json = response.json()

token_name = token_json['access_token']

##Grab Job Postings data by LAU1_Name

regions = ['North East Lincolnshire','North Lincolnshire','Lincoln','North Kesteven','South Kesteven','East Lindsey','West Lindsey','Boston','South Holland','Rutland']

for element in regions:

    url = "https://emsiservices.com/uk-jpa/timeseries"

    payload = f'{{ "filter": {{ "when": {{ "start": "2016-01", "end": "{EndDate}" }}, "lau1_name":  ["{element}" ] }}, "metrics":  ["unique_postings"]  }}'
    

    headers = {
        'Authorization': f"Bearer {token_name}",
        'Content-Type': "application/json"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    lau_json = response.json()
    
    df = pd.DataFrame(response.json()["data"]["timeseries"])
    df['region'] = f"{element}"
    df.head()

    df.to_csv(f"{element}.csv", index=False)
    
##Combine CSVs into one

os.chdir(os.path.dirname(__file__))

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

os.chdir(os.path.dirname(__file__))

combined_csv.to_csv( "EMSI_Job_Postings.csv", index=False, encoding='utf-8-sig')