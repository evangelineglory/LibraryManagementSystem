import sqlite3

conn = sqlite3.connect("library.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER DEFAULT 1
)
""")
conn.commit()


def add_book():
    book_id = int(input("Enter Book ID: "))
    title = input("Enter Book Name: ")
    author = input("Enter Author Name: ")

    try:
        cur.execute(
            "INSERT INTO books (book_id, title, author) VALUES (?, ?, ?)",
            (book_id, title, author)
        )
        conn.commit()
        print("Book added successfully!")
    except sqlite3.IntegrityError:
        print("Book ID already exists!")


def view_books():
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()

    if not books:
        print("No books found.")
        return

    for book in books:
        status = "Available" if book[3] else "Issued"
        print(book[0], "-", book[1], "-", book[2], "-", status)


def search_book():
    title = input("Enter book name to search: ")
    cur.execute("SELECT * FROM books WHERE title LIKE ?", 
                ("%" + title + "%",))
    books = cur.fetchall()

    if books:
        for book in books:
            status = "Available" if book[3] else "Issued"
            print(book[0], "-", book[1], "-", book[2], "-", status)
    else:
        print("Book not found.")


def issue_book():
    book_id = int(input("Enter Book ID to issue: "))
    cur.execute(
        "UPDATE books SET available = 0 WHERE book_id = ? AND available = 1",
        (book_id,)
    )
    conn.commit()

    if cur.rowcount:
        print("Book issued successfully!")
    else:
        print("Book not available or invalid Book ID.")


def return_book():
    book_id = int(input("Enter Book ID to return: "))
    cur.execute(
        "UPDATE books SET available = 1 WHERE book_id = ? AND available = 0",
        (book_id,)
    )
    conn.commit()

    if cur.rowcount:
        print("Book returned successfully!")
    else:
        print("Book is not issued or invalid Book ID.")


while True:
    print("\n--- LIBRARY MANAGEMENT SYSTEM ---")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        view_books()
    elif choice == "3":
        search_book()
    elif choice == "4":
        issue_book()
    elif choice == "5":
        return_book()
    elif choice == "6":
        break
    else:
        print("Invalid choice!")

conn.close()
