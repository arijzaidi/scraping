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

def checkUrl(Url):
    full_url = f'https://www.automobile.tn{Url}'
    response = requests.get(full_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    Table = soup.find('table', {'class':'versions'})
    if Table :
        fiche_technique_links = soup.find_all('a', href=True, string="Fiche technique")

        # Extract the URLs into a list
        urls = [link['href'] for link in fiche_technique_links]

        # Print the result
        return urls
    
    return [Url]

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



def save_to_csv(data, headers, filename='Data/Automobiletn_Neuf_Data.csv'):
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
    headers_set = set()  # A set to store unique spec keys
    car_data = []        # List to collect all car data (to later write to CSV)

    Brands = get_brands()
    for brand in Brands:
        print(f"Scraping {brand}...")
        models = get_models(brand)

        for index, model_url in enumerate(models):
            urls = checkUrl(model_url)
            if len(urls) > 1:
                models[index:index + 1] = urls
            print(f"Scraping model: {models[index]}")

            try:
                price, specs = get_car_details(models[index])

                # Add the keys of the specs to the headers set (this ensures uniqueness)
                headers_set.update(specs.keys())

                model_parts = models[index].strip('/').split('/')
                brand_index = model_parts.index(brand)
                model_name = " ".join(model_parts[brand_index + 1:])

                # Prepare the model's data (starting with brand, model name, and price)
                model_row = {
                    'Brand': brand,
                    'Model': model_name,
                    'Price': price
                }

                # Add spec values for the model
                for key, value in specs.items():
                    model_row[key] = value

                # Add this model's data to car_data
                car_data.append(model_row)
                print(f"Data collected for {models[index]}")

            except Exception as e:
                print(f"Error occurred while scraping {models[index]}: {e}")
                continue

            time.sleep(1)

    # After collecting all data, create the final header list (sorted)
    headers = ['Brand', 'Model', 'Price'] + sorted(headers_set)

    # Now, reorder the data in car_data to match the headers order
    for row in car_data:
        # Reorder row to match header order, filling missing specs with 'None'
        reordered_row = [row.get(header, None) for header in headers]
        save_to_csv(reordered_row, headers)

    print("Data saved to CSV.")