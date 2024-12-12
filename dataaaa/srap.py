from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
import requests
import pandas as pd
import numpy as np
import re

# URL de base
BASE_URL = 'https://www.automobile.tn/fr/occasion'

# Données collectées
total_df = pd.DataFrame()

# Fonction pour nettoyer le texte
def clean_text(text, regex_pattern=r'\d+'):
    if not text:
        return np.nan
    match = re.search(regex_pattern, text.replace('DT', '').replace('\xa0', '').strip())
    return match.group() if match else np.nan

# Fonction pour extraire les détails des annonces
def scrape_details(link):
    try:
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')
        container = soup.findAll('span', class_='spec-name')

        porte, cylindre = np.nan, np.nan
        for item in container:
            if item.text.strip() == 'Nombre de portes':
                porte = item.findNext('span').text.strip() if item.findNext('span') else np.nan
            elif item.text.strip() == 'Cylindrée':
                cylindre = clean_text(item.findNext('span').text if item.findNext('span') else np.nan)

        return porte, cylindre
    except Exception as e:
        print(f"Erreur lors du scraping des détails : {e}")
        return np.nan, np.nan

# Fonction principale pour une page
def scrape_page(page_number):
    url = f"{BASE_URL}/{page_number}"
    code_page = requests.get(url)
    soup = BeautifulSoup(code_page.text, 'html.parser')
    print(f"Scraping URL: {url}")

    marques, modeles, years, roads, boites, transmissions, horsepowers, fuels, prices, links = ([] for _ in range(10))

    container = soup.findAll(class_='occasion-item-v2')

    for item in container:
        road = item.find('li', class_='road')
        roads.append(road.text.strip() if road else np.nan)

        year = item.find('li', class_='year')
        years.append(year.text.strip() if year else np.nan)

        boite = item.find('li', class_='boite')
        boites.append(boite.text.strip() if boite else np.nan)

        transmission = item.find('li', class_='transmission')
        transmissions.append(transmission.text.strip() if transmission else np.nan)

        horsepower = item.find('li', class_='horsepower')
        horsepowers.append(horsepower.text.strip() if horsepower else np.nan)

        fuel = item.find('li', class_='fuel')
        fuels.append(fuel.text.strip() if fuel else np.nan)

        noms = item.findAll('h2')
        for nom in noms:
            nom_car = nom.text.strip() if nom else np.nan
            if nom_car:
                marques.append(nom_car.split()[0])
                parts = nom_car.split()
                modeles.append(' '.join(parts[1:]))
            else:
                marques.append(np.nan)
                modeles.append(np.nan)

        price_tag = item.find('div', class_='price')
        prices.append(clean_text(price_tag.text if price_tag else np.nan))

        link_tag = item.find('a', class_='occasion-link-overlay', href=True)
        if link_tag:
            correct_link = f'https://www.automobile.tn/{link_tag["href"]}'
            links.append(correct_link)

    return marques, modeles, years, roads, boites, transmissions, horsepowers, fuels, prices, links

# Scraping principal
nbre_page = 100  # Modifier pour plus de pages
all_data = []

for page_number in range(1, nbre_page + 1):
    marques, modeles, years, roads, boites, transmissions, horsepowers, fuels, prices, links = scrape_page(page_number)

    # Scraper les détails des liens
    with ThreadPoolExecutor() as executor:
        details = list(executor.map(scrape_details, links))

    portes, cylindres = zip(*details) if details else ([], [])
    all_data.append(pd.DataFrame({
        'Marque': marques,
        'Modèle': modeles,
        'year': years,
        'road': roads,
        'boite': boites,
        'horsepower': horsepowers,
        'fuel': fuels,
        'nbre_portes': portes,
        'cylindrée': cylindres,
        'transmission': transmissions,
        'Prix': prices
    }))

# Combiner les résultats
total_df = pd.concat(all_data, ignore_index=True)
total_df.to_csv('automobile_data.csv', index=False)
print(total_df)
