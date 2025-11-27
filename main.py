from avl_tree import AVLTree
from books_db import load_books, save_books
from book import Book
from user_db import authenticate, register_user

avl = AVLTree()
root = None
book_list = []


def print_menu(title, options):
    items = [f"{i}. {opt}" for i, opt in enumerate(options, 1)]
    width = max(len(title), *(len(it) for it in items)) + 4
    line = "+" + "-" * width + "+"
    print("\n" + line)
    print(f"| {title.center(width - 2)} |")
    print(line)
    for it in items:
        print(f"| {it.ljust(width - 2)} |")
    print(line)


def login():
    print("\n======== LOGIN SISTEM ========")
    username = input("Username : ")
    password = input("Password : ")

    user = authenticate(username, password)

    if user is None:
        print("Login gagal! Username atau password salah.\n")
        return

    if user.role == "admin":
        print(f"\nSelamat datang Admin, {user.username}!\n")
        admin_menu()
    else:
        print(f"\nSelamat datang {user.username} (Pengunjung)!\n")
        user_menu()


def register():
    print("\n======== REGISTER ========")
    username = input("Buat username : ")
    password = input("Buat password : ")

    if not username or not password:
        print("Username dan password tidak boleh kosong.\n")
        return

    created = register_user(username, password)
    if created:
        print("Registrasi berhasil! Silakan login.\n")
    else:
        print("Registrasi gagal: username sudah digunakan.\n")

def admin_add():
    global root, book_list

    print("\n=== Tambah Buku ===")
    key = input("ID Buku: ")
    title = input("Judul: ")
    author = input("Penulis: ")
    year = input("Tahun Terbit: ")
    category = input("Kategori: ")
    stock = input("Stok: ")
    location = input("Lokasi Rak: ")

    book = Book(key, title, author, year, category, stock, location)

    book_list.append(book)
    save_books(book_list)

    root = avl.insert(root, book)
    print("Buku berhasil ditambahkan!\n")


def admin_delete():
    global root, book_list

    print("\n=== Hapus Buku ===")
    key = input("Masukkan ID Buku: ")

    book_list = [b for b in book_list if b.key != key]
    save_books(book_list)

    root = avl.delete(root, key)

    print("Buku berhasil dihapus!\n")


def admin_show_all():
    print("\n=== Daftar Semua Buku ===")
    avl.inorder(root)
    print()


def admin_menu():
    while True:
        print_menu("MENU ADMIN", [
            "Tambah Buku",
            "Hapus Buku",
            "Cari Buku (ID)",
            "Cari Buku (Awal Judul)",
            "Cari Buku (Rentang ID)",
            "Lihat Semua Buku",
            "Logout",
        ])
        pilih = input("Pilih: ")

        if pilih == "1":
            admin_add()
        elif pilih == "2":
            admin_delete()
        elif pilih == "3":
            search()
        elif pilih == "4":
            search_by_prefix()
        elif pilih == "5":
            get_books_in_range()
        elif pilih == "6":
            admin_show_all()
        elif pilih == "7":
            break
        else:
            print("Pilihan tidak valid!")

def print_books_table(books):
    headers = ["ID", "Judul", "Penulis", "Tahun", "Kategori", "Stok", "Lokasi"]
    widths = [6, 25, 18, 6, 14, 6, 10]

    def line():
        return "+" + "+".join("-" * (w + 2) for w in widths) + "+"

    def row(values):
        return "| " + " | ".join(f"{val:<{w}}" for val, w in zip(values, widths)) + " |"

    print(line())
    print(row(headers))
    print(line())
    for b in books:
        print(row([b.key, b.title, b.author, b.year, b.category, b.stock, b.location]))
    print(line())


def search():
    print("\n=== Cari Buku ===")
    key = input("Masukkan ID Buku: ")

    result = avl.search(root, key)
    if result:
        print("\nBuku ditemukan:")
        print_books_table([result])
    else:
        print("Buku tidak ditemukan.\n")


def search_by_prefix():
    print("\n=== Cari Buku Berdasarkan Huruf Awal Judul ===")
    prefix = input("Masukkan huruf awal (contoh: A, Str, Ma): ").strip()
    if not prefix:
        print("Prefix tidak boleh kosong.\n")
        return

    prefix_low = prefix.lower()
    hasil = []

    def traverse(node):
        if not node:
            return
        traverse(node.left)
        if node.book.title.lower().startswith(prefix_low):
            hasil.append(node.book)
        traverse(node.right)

    traverse(root)

    if hasil:
        print_books_table(hasil)
    else:
        print("Tidak ada buku dengan judul yang diawali prefix tersebut.\n")


def get_books_in_range():
    print("\n=== Cari Buku Berdasarkan Rentang ID ===")
    min_id = input("Masukkan ID minimum: ").strip()
    max_id = input("Masukkan ID maksimum: ").strip()

    try:
        min_val = int(min_id)
        max_val = int(max_id)
    except ValueError:
        print("ID harus berupa angka.\n")
        return

    if min_val > max_val:
        min_val, max_val = max_val, min_val

    hasil = []

    def traverse(node):
        if not node:
            return
        traverse(node.left)
        try:
            key_val = int(node.book.key)
        except ValueError:
            pass
        else:
            if min_val <= key_val <= max_val:
                hasil.append(node.book)
        traverse(node.right)

    traverse(root)

    if hasil:
        print_books_table(hasil)
    else:
        print("Tidak ada buku dalam rentang ID tersebut.\n")

def borrow_book():
    global book_list

    print("\n=== Pinjam Buku ===")
    key = input("Masukkan ID Buku: ")

    book = avl.search(root, key)
    if book is None:
        print("Buku tidak ditemukan.\n")
        return

    if book.stock <= 0:
        print("Stok buku habis.\n")
        return

    book.stock -= 1
    save_books(book_list)
    print(f"Buku '{book.title}' berhasil dipinjam. Sisa stok: {book.stock}\n")

def user_menu():
    while True:
        print_menu("MENU PENGUNJUNG", [
            "Pinjam Buku",
            "Cari Buku (ID)",
            "Cari Buku (Awal Judul)",
            "Cari Buku (Rentang ID)",
            "Lihat Semua Buku",
            "Keluar",
        ])
        pilih = input("Pilih: ")

        if pilih == "1":
            borrow_book()
        elif pilih == "2":
            search()
        elif pilih == "3":
            search_by_prefix()
        elif pilih == "4":
            get_books_in_range()
        elif pilih == "5":
            admin_show_all()
        elif pilih == "6":
            break
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    book_list = load_books()

    for b in book_list:
        root = avl.insert(root, b)

    while True:
        print_menu("SELAMAT DATANG", [
            "Login",
            "Register",
            "Keluar",
        ])
        pilihan = input("Pilih: ")
        if pilihan == "1":
            login()
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            break
        else:
            print("Pilihan tidak valid!")
