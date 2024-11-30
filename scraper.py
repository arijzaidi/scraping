from bs4 import BeautifulSoup
import pandas as pd
import requests

url = 'https://www.automobile.tn/fr'
code_page=requests.get(url)

html=code_page.text

soup= BeautifulSoup(html, 'html.parser')

class_price=soup.findAll(class_='price')
labels=[]
for price in class_price:
    price_final=price.find('span').text
    #print(price_final)
    price_final=price_final.replace('DT','')
    labels.append(price_final)
#print(labels) # les prix des voitures sont les labels de notre dataset*

class_marque = soup.findAll('select', class_='model-selector brand form-select')
marques = []
for select in class_marque:
    options = select.findAll('option')
    for option in options:
        marque = option.text.strip()
        if marque:
            marques.append(marque)
#print(marques) # les marques des voitures sont un feature de notre dataset*


class_modele = soup.findAll('select', class_='model-selector model form-select')    


item_div = soup.findAll('div', class_='versions-item')
#print(item[0])
'''print(item[0].find('h2').text)
for i in item:
    modeles = i.findAll('h2')
    for modele in modeles:
        print(modele.text)

'''
######### 1 ere page du site contenant les prix des derniers modeles de voitures #########
items = []
marques = []
modeles = []
prices = []

for i in item_div:  # pour chaque voiture à vendre dans le site automobile.tn
    #extraire la marque et le modele(sous h2)
    noms = i.findAll('h2')
    for nom in noms:
        item = nom.text.strip()
        if item:
            items.append(item)
            marques.append(item.split()[0])
            parts = item.split()
            modeles.append(' '.join(parts[1:]))
    # extraire le prix
    price_div = i.find('div', class_='price')
    if price_div:
        price_span = price_div.find('span')
        if price_span:
            price_final = price_span.text.replace('DT', '').replace('\xa0', '').strip()
            prices.append(price_final)
            
#print(items) 
#print(marques) # les marques des voitures sont un feature de notre dataset*
#print(modeles) # les modeles des voitures sont un feature de notre dataset*
print(prices) # les prix des voitures sont les labels de notre dataset*

if len(prices) == len(marques) == len(modeles):
        data = {'Marque': marques, 'Modèle': modeles, 'Prix': prices}
        df = pd.DataFrame(data)
        print(df)
else:
        print("Le nombre de marques, de modèles et de prix ne correspond pas.")
