import sqlite3

# -----------------------------
# CONNECT TO DATABASE
# -----------------------------
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# -----------------------------
# CREATE TABLE IF NOT EXISTS
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    isbn TEXT UNIQUE
)
""")

conn.commit()


# -----------------------------
# FUNCTIONS
# -----------------------------

def add_book():
    title = input("Enter Book Title: ")
    author = input("Enter Author Name: ")
    year = input("Enter Published Year: ")
    isbn = input("Enter ISBN Number: ")

    cursor.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                   (title, author, year, isbn))
    conn.commit()
    print("Book added successfully!")


def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    print("\n--- Library Books ---")
    for book in books:
        print(book)
    print("---------------------")


def search_book():
    keyword = input("Enter title/author/ISBN to search: ")
    cursor.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
    """, ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

    results = cursor.fetchall()

    print("\n--- Search Results ---")
    for book in results:
        print(book)
    if not results:
        print("No book found!")
    print("----------------------")


def update_book():
    book_id = input("Enter Book ID to update: ")

    print("Enter new details (leave blank if no change):")
    title = input("New Title: ")
    author = input("New Author: ")
    year = input("New Year: ")
    isbn = input("New ISBN: ")

    # Existing data fetch
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    old = cursor.fetchone()

    if not old:
        print("Book ID not found!")
        return

    # Keep old values if blank input
    new_title = title if title else old[1]
    new_author = author if author else old[2]
    new_year = year if year else old[3]
    new_isbn = isbn if isbn else old[4]

    cursor.execute("""
        UPDATE books 
        SET title=?, author=?, year=?, isbn=? 
        WHERE id=?
    """, (new_title, new_author, new_year, new_isbn, book_id))

    conn.commit()
    print("Book updated successfully!")


def delete_book():
    book_id = input("Enter Book ID to delete: ")

    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Book deleted successfully!")
    else:
        print("Book ID not found!")


# -----------------------------
# MAIN MENU
# -----------------------------

while True:
    print("\n========= LIBRARY MANAGEMENT SYSTEM =========")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Exit")
    print("============================================")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()

    elif choice == "2":
        view_books()

    elif choice == "3":
        search_book()

    elif choice == "4":
        update_book()

    elif choice == "5":
        delete_book()

    elif choice == "6":
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid choice! Please try again.")

# Close database
conn.close()
