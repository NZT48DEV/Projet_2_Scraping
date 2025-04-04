import os
import sys
import csv
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

if __name__ == "__main__" and __package__ is None:
    # Ajoute le dossier parent (racine du projet) à sys.path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    projet_root = os.path.abspath(os.path.join(script_dir, '..'))
    sys.path.insert(0, projet_root)

from phase1.scraper import fetch_page, extract_book_data, DATE_TODAY


URL = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"


def fetch_category_urls(category_url, session):
    """
    Récupère tous les liens des livres d'une catégorie donnée sur Books to Scrape.

    La fonction explore toutes les pages de la catégorie via pagination automatique.

    Args:
        category_url (str): L'URL de la catégorie à scraper.
        session (requests.Session): Session HTTP réutilisable pour optimiser les requêtes réseau.

    Raises:
        RuntimeError: En cas d'échec HTTP (connexion, statut non 200) 
                      ou d'erreur lors du parsing HTML (articles introuvables).

    Returns:
        list[str]: Liste des URLs complètes des livres présents dans la catégorie.
    """
    urls = []
    current_url = category_url
    page_number = 1

    while True:
        try:
            response = session.get(current_url, timeout=10)
            response.encoding = 'utf-8'
            response.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"[ERREUR HTTP] Impossible de récupérer la page {current_url} : {e}")
        
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('article', class_='product_pod')
        if not articles:
            raise RuntimeError(f"[ERREUR PARSING] Aucun article trouvé sur la page : {current_url}")

        for article in articles:
            try:
                relative_url = article.find('h3').find('a')['href'].replace('../', '')
                full_url = "https://books.toscrape.com/catalogue/" + relative_url
                urls.append(full_url)
            except Exception as e:
                print(f"[AVERTISSEMENT] Problème d'extraction d'un lien sur la page : {current_url} -> {e}")

        print(f"Page {page_number} traitée, {len(articles)} livres trouvés.")

        next_li = soup.find('li', class_='next')
        if next_li:
            next_page = next_li.find('a')['href']
            current_url = urljoin(current_url, next_page)
            page_number += 1
        else:
            break

    return urls


def save_category_to_csv(data_list, category_name):
    """
    Crée un dossier 'CSV' dans le dossier phase2 (s'il n'existe pas), 
    puis enregistre les données d'une catégorie de livres dans un fichier CSV.

    Args:
        data_list (list[dict[[str, any]]): Liste des dictionnaires contenant les données extraites des pages produit.
        category_name (str): Nom de la catégorie à utiliser pour nommer le fichier CSV.

    Raises:
        Exception: En cas d'erreur lors de la création du dossier ou de l'écriture du fichier CSV.
    """
    if not data_list:
        print("[INFO] Aucun livre à enregistrer.")
        return

    try:
        phase2_dir = os.path.dirname(os.path.abspath(__file__))

        csv_path = os.path.join(phase2_dir, "CSV")
        os.makedirs(csv_path, exist_ok=True) 

        csv_fieldname = f"products_category_{category_name}_{DATE_TODAY}.csv"
        csv_path = os.path.join(csv_path, csv_fieldname)

        with open(csv_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data_list[0].keys(), delimiter=';')
            writer.writeheader()
            writer.writerows(data_list)

        print(f"[SAUVEGARDE] {len(data_list)} livres enregistrés dans : CSV/{csv_fieldname}")
    except Exception as e:
        print(f"[ERREUR] Échec lors de l'écriture du fichier CSV : {e}")


def extract_category_name(url):
    """
    Extrait le nom de la catégorie depuis une URL de Books to Scrape à l’aide d’une expression régulière.
    Exemple d'URL attendue : '.../category/books/mystery_3/index.html'

    Args:
        url (str): L'URL complète de la page de catégorie.

    Returns:
        str: Le nom de la catégorie avec la première lettre en majuscule. 
             Retourne 'Inconnue' si le nom ne peut pas être extrait.
    """
    match = re.search(r'/books/([^_]+)_\d+/', url)
    return match.group(1).capitalize() if match else "Inconnue"


def main():
    try:
        with requests.Session() as session:
            category_name = extract_category_name(URL)
            print(f"\nDébut du scraping de la catégorie {category_name}.\n")

            urls = fetch_category_urls(URL, session)
            print(f"\nTotal des liens récupérés : {len(urls)}.\n")

            all_products = []
            for index, url in enumerate(urls, start=1):
                try:
                    print(f"Scraping du livre {index}/{len(urls)} (Catégorie {category_name}) : {url}\n")
                    soup = fetch_page(url)
                    product_data = extract_book_data(soup, url)
                    all_products.append(product_data)
                except Exception as e:
                    print(f"Erreur lors du scraping du livre {url} : {e}\n")
            
            save_category_to_csv(all_products, category_name)

    except Exception as e:
        print(f"[ERREUR] : {e}")


if __name__ == "__main__":
    main()