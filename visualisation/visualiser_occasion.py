import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger les données
df = pd.read_csv('../dataaaa/final_data.csv')

# Convertir les colonnes numériques
df['road'] = pd.to_numeric(df['road'].str.replace(' ', ''), errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['horsepower'] = pd.to_numeric(df['horsepower'], errors='coerce')
df['Prix'] = pd.to_numeric(df['Prix'].str.replace(' ', ''), errors='coerce')

# 1. Distribution des prix
def plot_price_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Prix'], kde=True)
    plt.title('Distribution des Prix des Voitures')
    plt.xlabel('Prix (DT)')
    plt.ylabel('Nombre de Voitures')
    plt.show()

# 2. Boxplot des prix par marque
def plot_price_by_brand(df):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Marque', y='Prix', data=df)
    plt.title('Prix des Voitures par Marque')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# 3. Scatter plot : Kilométrage vs Prix
def plot_mileage_vs_price(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='road', y='Prix', hue='Marque', data=df)
    plt.title('Relation entre Kilométrage et Prix')
    plt.xlabel('Kilométrage')
    plt.ylabel('Prix (DT)')
    plt.tight_layout()
    plt.show()

# 4. Distribution des années
def plot_year_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['year'], bins=20, kde=True)
    plt.title('Distribution des Années des Voitures')
    plt.xlabel('Année')
    plt.ylabel('Nombre de Voitures')
    plt.show()

# 5. Heatmap de corrélation
def plot_correlation_heatmap(df):
    # Sélectionner les colonnes numériques
    numeric_columns = ['road', 'year', 'horsepower', 'Prix']
    corr = df[numeric_columns].corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
    plt.title('Matrice de Corrélation')
    plt.tight_layout()
    plt.show()

# 6. Répartition des carburants
def plot_fuel_distribution(df):
    plt.figure(figsize=(10, 6))
    df['fuel'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title('Répartition des Types de Carburant')
    plt.ylabel('')
    plt.show()

# 7. Boîtes de vitesses
def plot_transmission_distribution(df):
    plt.figure(figsize=(10, 6))
    df['boite'].value_counts().plot(kind='bar')
    plt.title('Répartition des Types de Boîtes de Vitesses')
    plt.xlabel('Type de Boîte')
    plt.ylabel('Nombre de Voitures')
    plt.tight_layout()
    plt.show()

# 8. Prix moyen par année
def plot_average_price_by_year(df):
    plt.figure(figsize=(12, 6))
    df.groupby('year')['Prix'].mean().plot(kind='bar')
    plt.title('Prix Moyen des Voitures par Année')
    plt.xlabel('Année')
    plt.ylabel('Prix Moyen (DT)')
    plt.tight_layout()
    plt.show()

# Fonction pour générer toutes les visualisations
def visualize_all_data(df):
    plot_price_distribution(df)
    plot_price_by_brand(df)
    plot_mileage_vs_price(df)
    plot_year_distribution(df)
    plot_correlation_heatmap(df)
    plot_fuel_distribution(df)
    plot_transmission_distribution(df)
    plot_average_price_by_year(df)


visualize_all_data(df)