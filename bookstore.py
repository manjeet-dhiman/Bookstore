import sqlite3


def create_table():
    """Create a table named 'books' in the SQLite database 'ebookstore'

    The table has four columns:
        'id' as INTEGER with PRIMARY KEY constraint,
        'Title' as TEXT,
        'Author' as TEXT,
        'Qty' as INTEGER.

    The function connects to the 'ebookstore' database and creates the 'books' table if it does not already exist.
    In case of any exceptions, the changes will be rolled back and the exception will be raised.
    Finally, the database connection will be closed.
    """

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
    """Populate the 'books' table in the SQLite database 'ebookstore' with data from 'book_list'

    Args:
        book_list ([int, str, str, int],): A list of book tuples where each tuple contains:
            'id' as INTEGER,
            'Title' as TEXT,
            'Author' as TEXT,
            'Qty' as INTEGER.

    The function connects to the 'ebookstore' database and inserts the data from 'book_list' into the 'books' table.
    In case of an IntegrityError, which is raised when the data is already in the table,
    the error message "Data already exists in the table." will be printed.
    Finally, the database connection will be closed.
    """

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
    """Add a new book to the 'books' table in the SQLite database 'ebookstore'

    Connects to the 'ebookstore' database and prompts the user to input the following information for a new book:
        'id' as INTEGER,
        'Title' as TEXT,
        'Author' as TEXT,
        'Qty' as INTEGER.

    The inputted information is then inserted into the 'books' table as a new row.
    Finally, the database connection will be closed.
    """

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

    return f"{title} by {author} successfully added!"


def update_book():
    """Update an existing book in the 'books' table in the SQLite database 'ebookstore'

    This function connects to the 'ebookstore' database, asks for id and input information for the book to be updated:
        'Title' as TEXT,
        'Author' as TEXT,
        'Qty' as INTEGER.

    The inputted information is then used to update the corresponding row in the 'books' table.
    Finally, the database connection will be closed.

    Returns:
        str: A string indicating the id of the book was successfully updated.
    """

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
    """Deletes a book from the ebookstore SQLite3 database.

    Connects to the "data/ebookstore" SQLite3 database and creates a cursor.
    The user is prompted to enter the id of the book they wish to delete.
    The book with the specified id is then deleted from the "books" table.
    The changes are committed and the connection to the database is closed.

    Returns:
        str: A string indicating the id of the book that was deleted from the database.
    """

    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    id = int(input("Enter the id for the book you wish to delete: "))

    cursor.execute('''DELETE FROM books WHERE id = ? ''', (id,))

    ebookstore.commit()

    ebookstore.close()

    return f"{id} deleted from database."


def search_book():
    """Search for a book in the ebookstore database by id.

    Returns:
        str: A string with the book's title, author, and quantity
    """
    ebookstore = sqlite3.connect("data/ebookstore")

    cursor = ebookstore.cursor()

    id = int(input("Enter the id for the book you wish to search: "))

    cursor.execute('''SELECT Title, Author, Qty FROM books WHERE id=?''', (id,))
    book = cursor.fetchone()

    ebookstore.close()

    return print(f"Title:\t{book[0]}\nAuthor:\t{book[1]}\nQty:\t{book[2]}")


def main():
    """Main function of the Bookstore program.

    This function performs the following operations:
    - Creates a table for storing book information.
    - Populates the table with a list of books.
    - Presents a menu to the user for performing various actions with the books.
    """
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
