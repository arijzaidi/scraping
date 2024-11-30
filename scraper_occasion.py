from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.automobile.tn/fr/occasion'
nbre_page=175
n=1 #page 1
total_df = pd.DataFrame()

for n in range(nbre_page):

    url = 'https://www.automobile.tn/fr/occasion/'+str(n)
    code_page=requests.get(url)

    print(url)
    html=code_page.text

    soup= BeautifulSoup(html, 'html.parser')

    container=soup.findAll(class_='occasion-item-v2')

    print(len(container))
    roads=[]
    years=[]
    boites=[]
    transmissions=[]
    horsepowers=[]
    fuels=[]


    items = []
    marques = []
    modeles = []
    prices = []

    for item in container:
        road=item.find('li',class_='road').text.strip()
        roads.append(road)
        print(road)

        year=item.find('li',class_='year').text.strip()
        years.append(year)
        print(year)

        boite=item.find('li',class_='boite').text.strip()
        boites.append(boite)
        print(boite)

        transmission=item.find('li',class_='transmission').text.strip()
        transmissions.append(transmission)
        print(transmission)

        horsepower=item.find('li',class_='horsepower').text.strip()
        horsepowers.append(horsepower)
        print(horsepower)

        fuel=item.find('li',class_='fuel').text.strip()
        fuels.append(fuel)
        print(fuel)



        #extraire la marque et le modele(sous h2)
        noms = item.findAll('h2')
        for nom in noms:
            nom_car = nom.text.strip()
            if nom_car:
                items.append(nom_car)
                marques.append(nom_car.split()[0])
                parts = nom_car.split()
                modeles.append(' '.join(parts[1:]))
        prices_dirty=item.findAll('div',class_='price')
        for p in prices_dirty:
            if p:
                price_final = p.text.replace('DT', '').replace('\xa0', '').strip()
                prices.append(price_final)
        
    print(prices)

    
    if len(prices) == len(marques) == len(modeles) == len(roads) == len(years) == len(boites) == len(transmissions) == len(horsepowers) == len(fuels):
        data = {'Marque': marques, 'Modèle': modeles, 'road': roads, 'year': years, 'boite': boites, 'transmission': transmissions, 'horsepower': horsepowers, 'fuel': fuels, 'Prix': prices}
        df = pd.DataFrame(data)
        #print(df)
    
    total_df = pd.concat([total_df, df], ignore_index=True)


#la dataframe totale contenant les données scrapées de toutes les pages:
total_df.to_csv('cars.csv', index=False)
print(df)



