"""
This program implements a bookstore clerk system using Python and SQLite. The program allows the clerk to:
1. Add new books to the database
2. Update book information
3. Delete books from the database
4. Search the database to find a specific book.

The program connects to an SQLite database called `ebookstore` and creates a table called `books` with the structure:
- id: integer, primary key
- title: text, book title
- author: text, book author
- qty: integer, quantity of the book in stock

The program presents the user with a menu of options, and performs the corresponding action based on the user's input.
The menu options include:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit

The program implements the database operations using the `sqlite3` module.
"""

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

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
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
        # close the database connection
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

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    try:
        for book in book_list:
            cursor.execute("""INSERT INTO books VALUES (?,?,?,?)""", book)
        # commit changes to books database
        ebookstore.commit()

    # catch exception when information entered is already in the table, an IntegrityError
    except sqlite3.IntegrityError:
        print("Data already exists in the table.")
        ebookstore.rollback()

    finally:
        # close the database connection
        ebookstore.close()


def check_id():
    """Function to check if a book ID exists in the database.

    This function prompts the user to enter a 4-digit id for a book, and then verifies if the id exists in the database.

    Returns:
    int: Returns the 4-digit id entered by the user, if it exists in the database.

    Raises:
    ValueError: Raised when the input is not a 4-digit integer.
    """

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    while True:
        try:
            id = int(input("Enter a 4-digit id for the book: "))
            # check if the length of the inputted ID is equal to 4
            if len(str(id)) != 4:
                # raise a ValueError if the length is not equal to 4
                raise ValueError

            # check database if id already exists
            cursor.execute("SELECT * FROM books WHERE id=?", (id,))
            result = cursor.fetchone()

            if result:
                break
            else:
                # display an error message if the ID is already present in the database
                print("This id doesn't exist. Please enter a different id.")
                continue

        except ValueError:
            # display an error message if the input is not a 4-digit integer
            print("The id must be a 4-digit integer. Please try again.")

    # close the database connection
    ebookstore.close()

    return id


def new_qty():
    """This function prompts the user to enter a quantity for a book.

    Returns:
    int: the updated quantity for the book.

    Raises:
    ValueError: if the input provided by the user is not an integer.
    """
    while True:
        try:
            # ask user for the book quantity, cast to an integer
            qty = int(input("Enter the updated quantity: "))

            # allow only a positive quantity
            if qty < 0:
                print("Please type a positive integer (minimum 0)")
                continue
            else:
                break

        except ValueError:
            # display an error message if the input is not an integer
            print("Please enter an integer for qty.")

    return qty


def new_book():
    """Add a new book to the 'books' table in the SQLite database 'ebookstore'

        This function connects to the 'ebookstore' database, creates a cursor, asks for the following input:
        id as a 4-digit integer
        title as a string
        author as a string
        qty as an integer

    If the user input for id is not a 4-digit integer, an error message will be displayed.
    If the id is already present in the database, the user will be prompted to enter a different id.

    If the user input for qty is not an integer, the user will be prompted to enter a valid integer.

    The inputted information is then inserted into the 'books' table as a new row.
    Finally, the database connection will be closed.

    Returns:
        str: A string indicating the book was successfully added displaying the title and author.
    """

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    while True:
        try:
            id = int(input("Enter a new 4-digit id for the book: "))
            # check if the length of the inputted ID is equal to 4
            if len(str(id)) != 4:
                # raise a ValueError if the length is not equal to 4
                raise ValueError

            # check database if id already exists
            cursor.execute("SELECT * FROM books WHERE id=?", (id,))
            result = cursor.fetchone()

            if result:
                # display an error message if the ID is already present in the database
                print("This id already exists. Please enter a different id.")
                continue
            else:
                break

        except ValueError:
            # display an error message if the input is not a 4-digit integer
            print("The id must be a 4-digit integer. Please try again.")

    title = input("Enter a title for the book: ")
    author = input("Enter the author of the book: ")

    qty = new_qty()

    cursor.execute("""INSERT INTO books(id, Title, Author, Qty)
                    VALUES(?,?,?,?)""", (id, title, author, qty))

    # commit changes to books database
    ebookstore.commit()

    # close the database connection
    ebookstore.close()

    return print(f"{title} by {author} successfully added!")


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

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    id = check_id()

    title = input("Enter the updated title of the book: ")
    author = input("Enter the updated author of the book: ")

    qty = new_qty()

    cursor.execute("""UPDATE books SET Title=?, Author=?, Qty=? WHERE ID=?""", (title, author, qty, id))

    # commit changes to books database
    ebookstore.commit()

    # close the database connection
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

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    id = check_id()

    cursor.execute('''DELETE FROM books WHERE id = ? ''', (id,))

    # commit changes to books database
    ebookstore.commit()

    # close the database connection
    ebookstore.close()

    return f"{id} record deleted from database."


def search_book():
    """Search for a book in the ebookstore database by id.

    Returns:
        str: A string with the book's title, author, and quantity
    """

    # connect to the 'ebookstore' database
    ebookstore = sqlite3.connect("data/ebookstore")

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    id = check_id()

    cursor.execute('''SELECT Title, Author, Qty FROM books WHERE id=?''', (id,))
    book = cursor.fetchone()

    # close the database connection
    ebookstore.close()

    return print(f"Title:\t{book[0]}\nAuthor:\t{book[1]}\nQty:\t{book[2]}")


def main():
    """Main function of the Bookstore program.

    This function performs the following operations:
    - Creates a table for storing book information.
    - Populates the table with a list of books.
    - Presents a menu to the user for performing various actions with the books.
    """
    # call function to create empty table
    create_table()

    book_list = [(3001, "A Tale of Two Cities", "Charles Dickens", 30),
                 (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
                 (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
                 (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
                 (3005, "Alice in Wonderland", "Lewis Carroll", 12),
                 ]

    # call function to fill table with information from book_list
    populate(book_list)

    while True:
        menu = input('''
    Bookstore
    Please choose an option:
    1. Enter book
    2. Update book
    3. Delete book
    4. Search books
    0. Exit
    : ''')

        if menu == '1':
            new_book()
            continue

        elif menu == '2':
            update_book()
            continue

        elif menu == '3':
            delete_book()
            continue

        elif menu == '4':
            search_book()
            continue

        elif menu == '0':
            print("Closing Bookstore program.")
            exit()

        else:
            print("You have entered an invalid choice. Please try again.")
            continue


# call the program
if __name__ == "__main__":
    main()
