import csv

import requests
from bs4 import BeautifulSoup

from cities import CITIES
from timer import timed


@timed
def scrape_images(cities):
    results = []
    for city in cities:
        img = None 

        try:
            data = requests.get(f'https://en.wikipedia.org/wiki/{city}')
        except Exception as e:
            print(f'Error: {e}')
        else:
            soup = BeautifulSoup(data.text, "html.parser")
            info_boxes = soup.find_all('table', {'class': 'infobox'})
            if info_boxes:
                info_box = info_boxes[0]
                img_tags = info_box.find_all('img', {'class': 'mw-file-element'})
                if img_tags:
                    img =  f"https://{img_tags[0]['src'].strip('//')}" 
    
        results.append({'city': city, 'image': img})

    with open(f'results.csv', 'w') as csvfile:
        if results:
            writer = csv.DictWriter(csvfile, fieldnames=results[0].keys())
            writer.writeheader()
            for row in results:
                writer.writerow(row)

    

if __name__ == '__main__':
    scrape_images(CITIES)