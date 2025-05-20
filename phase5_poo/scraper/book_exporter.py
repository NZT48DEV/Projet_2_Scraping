import os
import re
import csv
from datetime import datetime
from book import Book


class BookExporter:
    def __init__(self, book_folder: str = "Livre") -> None:
        self.book_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", book_folder))
        os.makedirs(self.book_folder, exist_ok=True)

    def clean_filename(self, title, max_length=50):
        title = re.sub(r'[^\w\s-]', '', title)
        title = title.strip().replace(' ', '_')
        return title[:max_length]
    
    def export_to_csv(self, book: Book):
        try:
            clean_title = self.clean_filename(book.title)
            date_str = datetime.today().strftime('%Y-%m-%d')
            filename = f"{clean_title}_{date_str}.csv"
            filepath = os.path.join(self.book_folder, filename)
            print(f"Chemin du fichier : {filepath}")

            with open(filepath, mode='w', newline='', encoding='utf-8-sig') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=vars(book).keys(), delimiter=';') 
                writer.writeheader()
                writer.writerow(vars(book))

        except Exception as e:
            raise RuntimeError(f"[ERREUR] Impossible de préparer le fichier : {e}")
        

if __name__ == "__main__":
    book = Book(
        title="Harry Potter & la pierre philosophale",
        product_page_url="http://example.com/hp1",
        universal_product_code="HP123",
        price_including_tax=10.99,
        price_excluding_tax=9.99,
        number_available=12,
        review_rating=5,
        product_description="Un jeune sorcier découvre qu’il est célèbre...",
        image_url="http://example.com/image.jpg",
        category="Fantasy"
    )

    exporter = BookExporter()
    exporter.export_to_csv(book)