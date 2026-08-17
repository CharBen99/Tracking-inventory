import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db():
    db = sqlite3.connect("ebookstore.db")
    try:
        cursor = db.cursor() # Get a cursor to make changes to the database
        yield cursor   # give cursor to the function using it
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# Create a table called book
def book_table():
    with get_db() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS book(
            id INTEGER PRIMARY KEY,
            title TEXT,
            authorID INTEGER,
            qty INTEGER)''')
    # Insert the column values for book
    books = [
        (3001, "A Tale of Two Cities", 1290, 30),
        (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
        (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
        (3004, "The Lord of the Rings", 6380, 37),
        (3005, "Alice's Adventures in Wonderland", 5620, 12)]

    # Check if table is empty. 
    # Make sure that added rows does not vanish when program run multiple times.
    with get_db() as cursor:
        cursor.execute("SELECT COUNT(*) FROM book")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.executemany('''INSERT INTO book(id, title, authorID, qty) 
                VALUES (?, ?, ?, ?)''', books)


# Create a table called author
def author_table():
    with get_db() as cursor:
        cursor.execute('''Create TABLE IF NOT EXISTS author(
            id INTEGER PRIMARY KEY,
            name TEXT,
            country TEXT)''')

    # Insert the column values for author
    authors = [
        (1290, "Charles Dickens", "England"),
        (8937, "J.K. Rowling", "England"),
        (2356, "C.S. Lewis", "Ireland"),
        (6380, "J.R.R. Tolkien", "South Africa"),
        (5620, "Lewis Carroll", "England")]
    with get_db() as cursor:
        cursor.execute("SELECT COUNT(*) FROM author")
        counts = cursor.fetchone()[0]
        if counts == 0:
            cursor.executemany('''INSERT INTO author(id, name, country)
                VALUES(?, ?, ?)''', authors)


def enter_book():
    while True:
        try:
            new_id = input("Enter the id number of the book (4-digit number): ")
            new_book = input("What is the title of the book? ")
            new_authorID = input("Enter the author ID number of the book (4-didgit number): ")
            new_qty = int(input("Enter the quantity of the book: "))
    
            # Check if the id already exists
            with get_db() as cursor:
                cursor.execute("SELECT id FROM book WHERE id = ?", (new_id,))
                result = cursor.fetchone()
                if result:
                    print("This id already exist, please enter another id.\n")
                    continue

                cursor.execute("SELECT id FROM author WHERE id = ?", (new_authorID,))
                results = cursor.fetchone()
                if results:
                    print("Author details already exist.")
                else:
                    if new_authorID.isdigit() and len(str(new_authorID)) == 4:
                        author_name = input("Enter the author name: ")
                        country = input("Enter country: ")
                        cursor.execute('''INSERT INTO author
                            VALUES(?, ?, ?)''', (new_authorID, author_name, country))
                        print("Author details added successfully.\n")
                    else:
                        print("\nInvalid.Enter a 4-digit author ID number.\n")
                
                if not result:
                    if new_id.isdigit() and len(str(new_id)) == 4 and new_authorID.isdigit() and len(str(new_authorID)) == 4:
                        cursor.execute('''INSERT INTO book
                            VALUES(?, ?, ?, ?)''', (new_id, new_book, new_authorID, new_qty))
                        print("Book added successfully.\n")
                        break
                    else:
                        print("\nInvalid. Enter a 4-digit id number for the book.\n")
                    
        
        except ValueError:
            print("Please enter a valid number.\n")
            
          
def update_book():
    while True:
        try:
            select_id = int(input("Enter the book id number you want to update: "))
            with get_db() as cursor:
                cursor.execute("SELECT authorID FROM book WHERE id = ?", (select_id,))
                result = cursor.fetchone()

                if not result:
                    print("The book id does not exist.\n")
                    return
            
                author_id = result[0]

                cursor.execute('''SELECT name, country
                    FROM author
                    WHERE id = ?''', (author_id,))
            
                results = cursor.fetchone()

                if results:
                    print(f"""\nCurrent Author details:
Author name: {results[0]}
Country: {results[1]}\n""")

            quantity = int(input("Enter the quantity: "))
            with get_db() as cursor:
                cursor.execute("UPDATE book SET qty = ? WHERE id = ?", (quantity, select_id))
            print("Quantity has been updated successfully.\n")

            author_update = input("""Do you want to update the author details? (yes or no)""").lower()
            with get_db() as cursor:
                if author_update == "yes":
                    author_name = input("Enter the new name of the author (or press enter to skip): ")
                    author_country = input("Enter the new country (or press enter to skip): ")
                
                    if author_name:
                        cursor.execute("UPDATE author SET name = ? WHERE id = ?", (author_name, author_id))
                    if author_country:
                        cursor.execute("UPDATE author SET country = ? WHERE id = ?", (author_country, author_id))
                    print("Author details updated successfully.\n")

            while True:   
                book_update = input("""Do you want to update: 
(title or authorid or press enter to return to menu)?\n""")
                with get_db() as cursor:
                    if book_update.lower() == "title":
                        book_name = input("Enter the title of the book: ")
                        cursor.execute("UPDATE book SET title = ? WHERE id = ?", (book_name, select_id))
                        print("Title updated successfully.\n")
                        break
                    elif book_update.lower() == "authorid":
                        author_id = input("Enter the author id: ")
                        if author_id.isdigit() and len(str(author_id)) == 4:
                            cursor.execute("UPDATE book SET authorID = ? WHERE id = ?", (author_id, select_id))
                            print("Author ID updated successfully.\n")
                            break
                        else:
                            print("Invalid. Please enter a 4-digit number.\n")
                    else:
                        print("You are redirected to the menu.\n")
                        break
        except ValueError:
            print("Invalid input.\n")
        break
            

def delete_book():
    while True:
        try: 
            select_id = int(input("Enter the book id number you want to delete: "))
            with get_db() as cursor:
                cursor.execute("SELECT * FROM book WHERE id = ?", (select_id,))
                result = cursor.fetchone()
                if result:
                    cursor.execute("DELETE FROM book WHERE id = ?", (select_id,))
                    print("The book is deleted successfully.\n")
                    break
                else:
                    print("This book id does not exist.\n")
        except ValueError:
            print("Invalid number. Enter the book id number.\n")
        
       
def search_books():
    while True:
        try:
            select_id = int(input("Enter the book id number you want to view: "))
            with get_db() as cursor:
                cursor.execute("SELECT * FROM book WHERE id = ?", (select_id,))
                result = cursor.fetchone()
            if result:
                print(f"""ID: {result[0]}
Title: {result[1]}
Author ID: {result[2]}
Quantity: {result[3]}\n""")
                break
            else:
                print("The book does not exist. Please enter another book id.\n")
        except ValueError:
            print("Invalid number. Enter the id number of the book.\n")


def view_all():
    print("Details\n----------------------------------------------------------------------------------------")
    with get_db() as cursor:
        cursor.execute('''SELECT book.title, author.name, author.country
            FROM book
            INNER JOIN author
            ON book.authorID = author.id ''')
        result = cursor.fetchall()
    if result:
        for title, name, country in result:
            print(f"""Title: {title}
Author's Name: {name}
Author's Country: {country}\n----------------------------------------------------------------------------------------\n""")

book_table()
author_table()

while True:
    menu = input("""Enter a number from the list: 
1. Enter book (add new book(s))
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit
""")

    if menu == "1":
        enter_book()
    elif menu == "2":
        update_book()
    elif menu == "3":
        delete_book()
    elif menu == "4":
        search_books()
    elif menu == "5":
        view_all()
    elif menu == "0":
        print("Goodbye\n")
        break
    else:
        print("Invalid number. Please enter a number from the menu.\n")



