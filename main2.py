import csv

import requests
from bs4 import BeautifulSoup
import re
from timer import timed


@timed
def scrape_countries():

    res = requests.get('https://www.cia.gov/the-world-factbook/page-data/sq/d/1627106492.json')
    countries = [
        country['name'] for country in res.json()['data']['countries']['nodes']
    ]
    results = []
    for country in countries:
        country_name = re.sub(r'[^a-zA-Z0-9\s\-]', '', country.lower().replace(',', '')).replace(' ', '-')
        if country_name == 'baker-island':
            country_name = 'united-states-pacific-island-wildlife-refuges'
        try:
            res = requests.get(f'https://www.cia.gov/the-world-factbook/countries/{country_name}')
            soup = BeautifulSoup(res.text, "html.parser")
            geography_div = soup.find(id="geography")
            geography_info = geography_div.get_text(separator='\n')
        except Exception as e:
            results.append({'name': country, 'geography': f'Error: {e}'})
        else:
            results.append({'name': country, 'geography': geography_info})

    with open(f'results.csv', 'w') as csvfile:
        if results:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            for row in results:
                writer.writerow(row)

    

if __name__ == '__main__':
    scrape_countries()