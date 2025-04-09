import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                title TEXT,
                                author TEXT,
                                isbn TEXT PRIMARY KEY,
                                genre TEXT,
                                availability_status TEXT)''')

        # Updated members table with 'contact' instead of 'email'
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS members (
                                membershipid  INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                contact TEXT NOT NULL,
                                membershiptype TEXT NOT NULL)''')

        self.conn.commit()

    # Book-related methods
    def fetch_books(self):
        """Fetch all books from the database."""
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def insert_book(self, title, author, isbn, genre, availability_status):
        """Insert a new book into the database."""
        self.cursor.execute(
            "INSERT INTO books (title, author, isbn, genre, availability_status) VALUES (?, ?, ?, ?, ?)",
            (title, author, isbn, genre, availability_status))
        self.conn.commit()

    def update_book(self, title, author, isbn, genre, availability_status):
        """Update a book's details."""
        self.cursor.execute("UPDATE books SET title = ?, author = ?, genre = ?, availability_status = ? WHERE isbn = ?",
                            (title, author, genre, availability_status, isbn))
        self.conn.commit()

    def delete_book(self, title):
        """Delete a book by its title."""
        self.cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        self.conn.commit()

    def checkout_book(self, membership_id, book_title):
        """Check out a book if the book exists and is available."""
        self.cursor.execute("SELECT * FROM books WHERE title = ?", (book_title,))
        book = self.cursor.fetchone()

        if not book:
            return False, "Book not found."
        if book[4] == "Checked Out":
            return False, "This book is already checked out."

        # Check if member exists
        self.cursor.execute("SELECT * FROM members WHERE membershipid = ?", (membership_id,))
        member = self.cursor.fetchone()
        if not member:
            return False, "Member not found."

        # Update book status to Checked Out
        self.cursor.execute("UPDATE books SET availability_status = ? WHERE title = ?", ("Checked Out", book_title))
        self.conn.commit()

        return True, "Book checked out successfully."

    # Member-related methods
    def select_members(self):
        """Fetch all members from the database."""
        self.cursor.execute("SELECT * FROM members")
        return self.cursor.fetchall()

    def insert_member(self, name, contact, membershiptype):
        self.cursor.execute("INSERT INTO members VALUES (NULL, ?, ?, ?)", ( name, contact, membershiptype))
        self.conn.commit()

    def update_member(self, member_id, name, contact, membership_type):
        """Update an existing member's details."""
        self.cursor.execute("UPDATE members SET name = ?, contact = ?, membershiptype = ? WHERE membershipid = ?",
                            (name, contact, membership_type, member_id))
        self.conn.commit()

    def delete_member(self, member_id):
        """Delete a member by their ID."""
        self.cursor.execute("DELETE FROM members WHERE membershipid   = ?", (member_id,))
        self.conn.commit()
