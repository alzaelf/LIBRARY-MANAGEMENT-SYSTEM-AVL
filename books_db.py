import csv
from book import Book

FILENAME = "books.csv"

def load_books():
    books = []
    with open(FILENAME, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            books.append(Book(
                row['id'],
                row['title'],
                row['author'],
                row['year'],
                row['category'],
                row['stock'],
                row['location']
            ))
    return books

def save_books(book_list):
    with open(FILENAME, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["id", "title", "author", "year", "category", "stock", "location"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for b in book_list:
            writer.writerow({
                "id": b.key,
                "title": b.title,
                "author": b.author,
                "year": b.year,
                "category": b.category,
                "stock": b.stock,
                "location": b.location
            })
