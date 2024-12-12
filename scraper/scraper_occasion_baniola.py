import re
import os  # Import os to handle directories
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

url_g = "https://baniola.tn/voitures"

# Number of pages to scrape
nbre_page = 25

marques = []
modeles = []
years = []
puissances_fiscales = []
prices = []
kilometrages = []
boites = []
fuels = []  
cylindres = []
nbre_portes = []
negotiables = []
total_df = pd.DataFrame()

# Directory to save the CSV
output_directory = '../data'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for n in range(nbre_page):
    url = url_g + "?page=" + str(n * 50)
    code_page = requests.get(url)
    soup = BeautifulSoup(code_page.text, 'html.parser')

    print('The URL now is:', url)

    # Extract car links for details
    links_container = soup.findAll('div', class_='card-body')

    links = []
    for item in links_container:
        link_tag = item.find('a', class_='card-title text-capitalize', href=True)
        if link_tag:
            link = link_tag['href']
            links.append(link)

    # Extract car features and prices
    for link in links:
        print('-------------------')
        page_voiture = requests.get(link)
        soup_voiture = BeautifulSoup(page_voiture.text, 'html.parser')

        prices_container = soup_voiture.findAll('div', class_='price')
        for price in prices_container:
            price_text = price.text.strip()
            price_number = re.search(r'\d+', price_text.replace('TND', '').replace(' ', ''))
            if price_number:
                prices.append(price_number.group())
            else:
                prices.append(np.nan)

            if 'Négociable' in price_text:
                negotiables.append('Négociable')
            elif 'Non Négociable' in price_text:
                negotiables.append('Non Négociable')
            else:
                negotiables.append(np.nan)

        liste_features = soup_voiture.findAll('div', class_='value')
        for i in range(len(liste_features)):
            feature = liste_features[i].text.strip()
            if feature:
                if i == 0:
                    marques.append(feature)
                elif i == 1:
                    modeles.append(feature)
                elif i == 2:
                    years.append(feature)
                elif i == 3:
                    puissances_fiscales.append(feature)
                elif i == 4:
                    kilometrages.append(feature)
                elif i == 5:
                    boites.append(feature)
                elif i == 6:
                    fuels.append(feature)
                elif i == 7:
                    cylindres.append(feature)
                elif i == 8:
                    nbre_portes.append(feature)
            else:
                if i == 0:
                    marques.append(np.nan)
                elif i == 1:
                    modeles.append(np.nan)
                elif i == 2:
                    years.append(np.nan)
                elif i == 3:
                    puissances_fiscales.append(np.nan)
                elif i == 4:
                    kilometrages.append(np.nan)
                elif i == 5:
                    boites.append(np.nan)
                elif i == 6:
                    fuels.append(np.nan)
                elif i == 7:
                    cylindres.append(np.nan)
                elif i == 8:
                    nbre_portes.append(np.nan)

        if len(cylindres) < len(prices):
            cylindres.append(np.nan)
        if len(nbre_portes) < len(prices):
            nbre_portes.append(np.nan)

    # Create and append the DataFrame
    if len(prices) == len(marques) == len(modeles) == len(kilometrages) == len(years) == len(boites) == len(puissances_fiscales) == len(fuels) == len(negotiables) == len(cylindres) == len(nbre_portes):
        data = {
            'Marque': marques,
            'Modèle': modeles,
            'year': years,
            'horsepower': puissances_fiscales,
            'road': kilometrages,
            'boite': boites,
            'fuel': fuels,
            'cylindrée': cylindres,
            'nbre_portes': nbre_portes,
            'Negociable': negotiables,
            'Prix': prices
            
            
        }
        df = pd.DataFrame(data)
        print(df)

    total_df = pd.concat([total_df, df], ignore_index=True)

# Save the DataFrame to CSV
total_df.to_csv(os.path.join(output_directory, 'baniola1.csv'), index=False)
print('Data saved to:', os.path.join(output_directory, 'baniola1.csv'))
