import requests
from bs4 import BeautifulSoup
from book import Book
import re
from urllib.parse import urljoin

class BookScraper:
    def scrape_book(self, url: str):
        try:
            response = requests.get(url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find('table', class_='table table-striped')

            def get_table_value(label):
                th = table.find('th', string=label)
                if th is None:
                    raise ValueError(f"[ERREUR] champ '{label}' introuvable dans le tableau")
                td = th.find_next_sibling('td')
                return td.text if td else "N/A"

            title = soup.find('div', class_="col-sm-6 product_main").find('h1').text
            match = re.search(r'\((\d+)\s+available\)', get_table_value('Availability'))
            number_available = int(match.group(1)) if match else "Nombre non trouvé"
            description_tag = soup.find('div', id='product_description')
            product_description = description_tag.find_next_sibling('p').text \
                if description_tag and description_tag.find_next_sibling('p') else "N/A"

            review_rating_tag = soup.find('p', class_='star-rating')
            review_rating_classes = review_rating_tag.get('class') if review_rating_tag else []
            review_rating_text = next((cls.capitalize() for cls in review_rating_classes if cls != 'star-rating'), 'Zero')
            review_rating_map = {'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            review_rating = review_rating_map.get(review_rating_text, 0)

            title = title
            product_page_url = url
            universal_product_code = get_table_value('UPC')
            price_including_tax = float(get_table_value('Price (incl. tax)').replace('£', ''))
            price_excluding_tax = float(get_table_value('Price (excl. tax)').replace('£', ''))
            number_available = number_available
            review_rating = review_rating
            product_description = product_description
            image_url = urljoin(url, soup.find('div', class_='item').find('img')['src'])
            category = soup.find('ul', class_='breadcrumb').find_all('li')[2].text.strip()

            return Book(
            title=title,
            product_page_url=product_page_url,
            universal_product_code=universal_product_code,
            price_including_tax=price_including_tax,
            price_excluding_tax=price_excluding_tax,
            number_available=number_available,
            review_rating=review_rating,
            product_description=product_description,
            image_url=image_url,
            category=category
        )

        except Exception as e:
            raise RuntimeError(f"[ERREUR] Échec de l'extraction depuis {url} : {e}")