import re
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup


url_g="https://baniola.tn/voitures"

# nbre_page=39
nbre_page=2
n=0

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
prices=[]
negotiables = []
total_df = pd.DataFrame()

for n in range(nbre_page):

    url=url_g+"?page="+str(n*50)

    code_page=requests.get(url)

    soup=BeautifulSoup(code_page.text,'html.parser')

    print('the url now is :',url)
    
    #extraire les liens des voitures pour plus de details:
    links_container=soup.findAll('div',class_='card-body')
    # print(links_container[0])


    links = []
    for item in links_container:
        link_tag = item.find('a', class_='card-title text-capitalize', href=True)
        if link_tag:
            link = link_tag['href']
            links.append(link)
    

    # extraire les features des voitures à partir de la page details de chaque voiture + les prix:
 
    for link in links:
        print('-------------------')
        page_voiture=requests.get(link)
        soup_voiture=BeautifulSoup(page_voiture.text,'html.parser')

        prices_container=soup_voiture.findAll('div',class_='price')
        for price in prices_container:
            price_text = price.text.strip()
            # Utiliser une expression régulière pour extraire le nombre
            price_number = re.search(r'\d+', price_text.replace('TND', '').replace(' ', ''))
            if price_number:
                prices.append(price_number.group())
            else:
                prices.append(np.nan)  

            # Vérifier la présence de l'état de négociation
            if 'Négociable' in price_text:
                negotiables.append('Négociable')
            elif 'Non Négociable' in price_text:
                negotiables.append('Non Négociable')
            else:
                negotiables.append(np.nan)

        # print(prices)
        # print(negotiables)

        liste_features=soup_voiture.findAll('div',class_='value')
        # print(liste_features.__len__())
        for i in range(len(liste_features)):

            feature=liste_features[i].text.strip()
            # print(feature)

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
            # print(len(cylindres))
        if len(nbre_portes) < len(prices):
            nbre_portes.append(np.nan)
            # print(len(nbre_portes))
                
    if len(prices) == len(marques) == len(modeles) == len(kilometrages) == len(years) == len(boites) == len(puissances_fiscales) == len(fuels) == len(negotiables) == len(cylindres) == len(nbre_portes):
            data = {
                'Marque': marques,
                'Modèle': modeles,
                'year': years,
                'puissances_fiscales': puissances_fiscales,
                'road': kilometrages,
                'boite': boites,
                'fuel': fuels,
                'cylindres': cylindres,
                'nbre_portes': nbre_portes,
                'negociable': negotiables,
                'Prix': prices
            }
            df = pd.DataFrame(data)
            print(df)
            
    total_df = pd.concat([total_df, df], ignore_index=True)

    total_df.to_csv('../data/baniola.csv', index=False)
    print(df)
