#!/usr/bin/env python3

import time
import json
import argparse
import requests
import pandas as pd


def gene_symbols_api_call(protein_ids):
    url = 'https://rest.uniprot.org/idmapping/run'

    params = {
        'from': 'UniProtKB_AC-ID',
        'to': 'Gene_Name',
        'ids': ','.join(protein_ids),
    }

    response = requests.post(url, params=params)
    if response.ok:
        return json.loads(response.text)['jobId']
    else:
        return 'Error: ' + response.text


def check_job_status(job_id):
    status_url = f'https://rest.uniprot.org/idmapping/status/{job_id}'
    print(job_id)
    while True:
        response = requests.get(status_url)
        if response.ok:
            results = json.loads(response.text)
            print(results)
            if results['jobStatus'] == 'RUNNING':
                time.sleep(5)
            else:
                return results
        else:
            return 'Error: ' + str(response.status_code)


def main():
    parser = argparse.ArgumentParser(description='Convert CSV to TSV')
    
    parser.add_argument('input', type=str, help='The input CSV fila path')
    
    args = parser.parse_args()
    input = args.input

    df = pd.read_csv(input, sep='\t')
    protein_ids = df['Parent Accession'].tolist()
    protein_ids = [str(x) for x in protein_ids]
    protein_ids = [x for x in protein_ids if len(x) == 6]

    job_id = gene_symbols_api_call(protein_ids)
    print(check_job_status(job_id))

if __name__ == "__main__":
    main()
