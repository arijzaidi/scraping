import requests
from bs4 import BeautifulSoup
import time
import csv

BASE_URL = 'https://www.automobile.tn/fr/neuf'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

# Function to get the list of available brands
def get_brands():
    response = requests.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all brand selection options
    brand_select = soup.find('select', class_='model-selector')
    brands = [option['value'] for option in brand_select.find_all('option') if option['value']]
    
    return brands

# Function to get the models of a specific brand
def get_models(brand):
    brand_url = f'{BASE_URL}/{brand}'
    response = requests.get(brand_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all model links
    model_links = []
    article = soup.find('div', class_='articles')
    links = article.find_all('a', href=True)
    for link in links:
        if link:
            model_links.append(link['href'])
    return model_links

def get_car_details(car_url):
    full_url = f'https://www.automobile.tn{car_url}'
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract car price
    price = soup.find('div', {'class': 'buttons'}).find('span').get_text(strip=True)

    # Extract technical details (fiche technique)
    specs = {}
    specs_section = soup.find('div', {'id': 'specs'})
    if specs_section:
        tables = specs_section.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                try:
                    key = row.find('th').get_text(strip=True)
                    value = row.find('td').get_text(strip=True)
                    specs[key] = value
                except AttributeError:
                    continue

    return price, specs



def save_to_csv(data, headers, filename='Data/cars_data.csv'):
    """ Write data to CSV, dynamically handling the headers """
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write headers if the file is empty
        if file.tell() == 0:
            writer.writerow(headers)
        # Write the data row
        writer.writerow(data)

# Start scraping
if __name__ == '__main__':
    all_specs = set()  # A set to keep track of all unique spec keys
    car_data = []      # List to collect all car data (to later write to CSV)

    Brands = get_brands()
    for brand in Brands:
        print(f"Scraping {brand}...")
        models = get_models(brand)

        for model_url in models:
            print(f"Scraping model: {model_url}")
            try:
                price, specs = get_car_details(model_url)
                # Add all specs keys to the set of unique specs
                all_specs.update(specs.keys())

                model_parts=model_url.strip('/').split('/')
                brand_index = model_parts.index(brand)
                model_name = " ".join(model_parts[brand_index + 1:])

                # Prepare the data row, starting with the brand, model URL, and price
                row = [brand, model_url, price]

                # Add spec values in the correct order of the columns
                for key in all_specs:
                    # Get the spec value, or leave it empty if it doesn't exist for this model
                    row.append(specs.get(key, ''))

                car_data.append(row)
                print(f"Data collected for {model_url}")

            except Exception as e:
                print(f"Error occurred while scraping {model_url}: {e}")
                continue

            time.sleep(1)

    # After collecting all data, write to CSV
    if car_data:
        headers = ['Brand', 'Model', 'Price'] + list(all_specs)
        for row in car_data:
            save_to_csv(row, headers,filename='cars_neuf.csv')
        print("Data saved to CSV.")