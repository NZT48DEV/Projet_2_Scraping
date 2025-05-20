from scraper import BookScraper

def main():
    url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    scraper = BookScraper()
    book = scraper.scrape_book(url)
    print(book)



if __name__ == "__main__":
    main()