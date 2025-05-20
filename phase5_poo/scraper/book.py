class Book:
    def __init__(self, title, product_page_url, universal_product_code,
                price_including_tax, price_excluding_tax, number_available,
                review_rating, product_description, image_url, category):
        self.title = title
        self.product_page_url = product_page_url
        self.universal_product_code = universal_product_code
        self.price_including_tax = price_including_tax
        self.price_excluding_tax = price_excluding_tax
        self.number_available = number_available
        self.review_rating = review_rating
        self.product_description = product_description
        self.image_url = image_url
        self.category = category

    def __str__(self):
        return (
            f"Titre : {self.title}\n"
            f"Catégorie : {self.category}\n"
            f"Prix (TTC) : {self.price_including_tax}\n"
            f"Prix (HT) : {self.price_excluding_tax}\n"
            f"Stock : {self.number_available}\n"
            f"Note : {self.review_rating}\n"
            f"Description : {self.product_description}\n"
            f"URL de l'image : {self.image_url}\n"
            f"URL du livre : {self.product_page_url}\n"
            f"Category du livre : {self.category}\n"
        )

