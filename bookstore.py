import sqlite3


def create_table():
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()
    try:
        # creates a file called ebookstore with a SQLite3 DB

        cursor.execute("""CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)
        """)

        ebookstore.commit()

    # catch any exception
    except Exception as e:
        # Roll back any change if something goes wrong
        ebookstore.rollback()
        raise e

    finally:
        # close the db connection
        ebookstore.close()


def populate(book_list):
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    try:
        for book in book_list:
            cursor.execute("""INSERT INTO books VALUES (?,?,?,?)""", book)

        ebookstore.commit()

    # catch exception when information entered is already in the table, an IntegrityError
    except sqlite3.IntegrityError:
        print("Data already exists in the table.")
        ebookstore.rollback()

    finally:
        ebookstore.close()


def new_book():
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    id = int(input("Enter a new id for the book: "))
    title = input("Enter a title for the book: ")
    author = input("Enter the author of the book: ")
    qty = int(input("Enter a quantity for the book: "))

    cursor.execute("""INSERT INTO books(id, Title, Author, Qty)
                    VALUES(?,?,?,?)""", (id, title, author, qty))

    ebookstore.commit()

    ebookstore.close()


def update_book():
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    id = int(input("Enter the id for the book you wish to edit: "))
    title = input("Enter the updated title of the book: ")
    author = input("Enter the updated author of the book: ")
    qty = int(input("Enter the updated quantity: "))

    cursor.execute("""UPDATE books SET Title=?, Author=?, Qty=? WHERE ID=?""", (id, title, author, qty))

    ebookstore.commit()

    ebookstore.close()

    return "Book updated successfully!"


def delete_book():
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    id = int(input("Enter the id for the book you wish to delete: "))

    cursor.execute('''DELETE FROM books WHERE id = ? ''', (id,))

    ebookstore.commit()

    ebookstore.close()

    return f"{id} deleted from database."


def search_book():
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    id = int(input("Enter the id for the book you wish to search: "))

    cursor.execute('''SELECT Title, Author, Qty FROM books WHERE id=?''', (id,))
    book = cursor.fetchone()

    print(f"""
    Title: {book[0]}
    Author: {book[1]}
    Qty: {book[2]}
    """)

    ebookstore.commit()

    ebookstore.close()


def main():
    create_table()

    book_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                 (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                 (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
                 (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                 (3005, "Alice in Wonderland", "Lewis Carroll", 12),
                 ]

    populate(book_list)

    while True:
        try:
            menu = int(input('''
Bookstore
Please choose an option:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
: '''))

            if menu == 1:
                new_book()
                continue

            elif menu == 2:
                update_book()
                continue

            elif menu == 3:
                delete_book()
                continue

            elif menu == 4:
                search_book()
                continue

            elif menu == 0:
                print("Closing Bookstore program.")
                exit()

            else:
                print("You have entered an invalid choice. Please try again.")
                continue

        except ValueError:
            print("You have entered an invalid choice. Please try again.")


# call the program
if __name__ == "__main__":
    main()
