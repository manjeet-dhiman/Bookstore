# eBookstore
A database program for an ebookstore.

## Description
This program implements a bookstore clerk system using Python and SQLite. The program allows the clerk to perform CRUD (Create, Read, Update, Delete) operations on a SQLite database of ebooks.

## Programming principles

SQLite: Makes use of SQLite commands to read and write to a SQLite database file.<br />
Modularity: The program is divided into functions that each perform specific tasks, making the code more readable and easier to maintain.<br />
Error Handling: The program contains error handling features to ensure that the program does not crash when errors occur.<br />
Code Reusability: The functions were designed to be reusable, making it easier to integrate them into other programs.

## Dependencies
```
import sqlite3
```
Used to create a SQLite database to store book information.

## Code preview
```
def search_book():
    """Search for a book in the ebookstore database by id.

    Returns:
    str: A string is displayed to the user with the book's title, author, and quantity
    """

    # connect to the 'ebookstore' database
    ebookstore = connect_db()

    # create a cursor to execute SQL commands
    cursor = ebookstore.cursor()

    print(f"\n{PURPLE}{SEP * 10} [Search Book Record] {SEP * 10}{RESET}")

    # call function to generate a valid id
    id = check_id()

    # fetch the record with the corresponding id
    cursor.execute('''SELECT Title, Author, Qty FROM books WHERE id=?''', (id,))
    book = cursor.fetchone()

    # close the database connection
    ebookstore.close()

    # display record to the user
    output = f"\n{PURPLE}{SEP * 10} [ID: {id}] {SEP * 10}{RESET}\n"
    output += f"Title:\t{book[0]}\n"
    output += f"Author:\t{book[1]}\n"
    output += f"Qty:\t{book[2]}\n"

    return output
```

## Program preview
```
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ [Bookstore] ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Please choose an option:

1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
: 4

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ [Search Book Record] ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

Enter a 4-digit id for the book: 3001

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ [ID: 3001] ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Title:  A Tale of Two Cities
Author: Charles Dickens
Qty:    30

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯ [Bookstore] ⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
Please choose an option:

1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit
: 0
Closing Bookstore program.
```

## Author
Manjeet Dhiman
