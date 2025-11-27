class Book:
    def __init__(self, key, title, author, year, category, stock, location):
        self.key = key
        self.title = title
        self.author = author
        self.year = year
        self.category = category
        self.stock =  int(stock)
        self.location = location
    def __str__(self):
        return (f"[{self.key}] {self.title} | {self.author} | "
        f"{self.year} | {self.category} | Stok: {self.stock} | Rak: {self.location}")