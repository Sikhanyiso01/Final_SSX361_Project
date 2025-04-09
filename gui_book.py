import tkinter as tk
from tkinter import messagebox, ttk
from db import Database

db = Database("libraryDB.db")

class BookManagement:
    def __init__(self, root, back_to_main_window_callback):
        self.root = root
        self.back_to_main_window = back_to_main_window_callback
        self.root.title("Book Management")
        self.root.geometry("800x550")

        # Buttons and other UI elements
        self.button_bg = "#4a7abc"
        self.button_fg = "white"
        self.button_font = ("Arial", 12, "bold")

        # Labels for Book Details
        tk.Label(root, text="Title:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Author:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="ISBN:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.isbn_entry = tk.Entry(root)
        self.isbn_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(root, text="Genre:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(root, text="Availability Status:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.status_entry = ttk.Combobox(root, values=["Available", "Checked Out", "Reserved"])
        self.status_entry.grid(row=4, column=1, padx=10, pady=5)

        # Listbox and Scrollbar for Book List
        self.book_list = tk.Listbox(root, height=12, width=80)
        self.book_list.grid(row=6, column=0, columnspan=3, pady=10)

        scrollbar = tk.Scrollbar(root)
        scrollbar.grid(row=6, column=3, sticky='ns')

        self.book_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.book_list.yview)



        # Apply these settings to the buttons
        tk.Button(root, text="Add", width=12, command=self.add_book,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=7, column=0)

        tk.Button(root, text="Update", width=12, command=self.update_book,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=7, column=1)

        tk.Button(root, text="Delete", width=12, command=self.delete_book,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=7, column=2)

        tk.Button(root, text="Refresh", width=12, command=self.populate_books,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=8, column=1)

        tk.Button(root, text="Back", width=12, command=self.go_back,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=8, column=2)

        # Add a separator
        separator = ttk.Separator(root, orient="vertical")
        separator.grid(row=0, column=3, rowspan=8, sticky="ns", padx=20)

        # Checkout Section (to the right of the separator)
        tk.Label(root, text="Checkout Book").grid(row=0, column=4, padx=10, pady=5)

        tk.Label(root, text="Member ID:").grid(row=1, column=4, sticky="w", padx=10, pady=5)
        self.checkout_member_id_entry = tk.Entry(root)
        self.checkout_member_id_entry.grid(row=1, column=5, padx=10, pady=5)

        tk.Label(root, text="Book Title:").grid(row=2, column=4, sticky="w", padx=10, pady=5)
        self.checkout_book_title_entry = tk.Entry(root)
        self.checkout_book_title_entry.grid(row=2, column=5, padx=10, pady=5)

        tk.Button(root, text="Checkout", width=12, command=self.checkout_book,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=3, column=4, columnspan=2, pady=10)

        # Populate the book list when the window is loaded
        self.populate_books()

    def populate_books(self):
        """Populate the Listbox with books from the database."""
        self.book_list.delete(0, tk.END)
        for book in db.fetch_books():
            display = f"Title: {book[0]} |Author : {book[1]} | ISBN: {book[2]} | Genre: {book[3]} | Status: {book[4]}"
            self.book_list.insert(tk.END, display)

    def select_book(self):
        """Select a book from the Listbox and display its details."""
        try:
            index = self.book_list.curselection()[0]
            selected = db.fetch_books()[index]
            self.selected_book_id = selected[0]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(tk.END, selected[1])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(tk.END, selected[2])
            self.isbn_entry.delete(0, tk.END)
            self.isbn_entry.insert(tk.END, selected[3])
            self.genre_entry.delete(0, tk.END)
            self.genre_entry.insert(tk.END, selected[4])
            self.status_entry.set(selected[5])
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a book from the list.")

    def add_book(self):
        """Add a new book to the database with validation."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        genre = self.genre_entry.get().strip()
        status = self.status_entry.get().strip()

        # Validate that all fields are filled
        if not all([title, author, isbn, genre, status]):
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return

        # Validate ISBN is 8 digits
        if not isbn.isdigit() or len(isbn) != 8:
            messagebox.showwarning("Invalid ISBN", "ISBN must be exactly 8 digits.")
            return

        # Check if ISBN already exists
        if db.isbn_exists(isbn):
            messagebox.showerror("Duplicate ISBN", "A book with this ISBN already exists.")
            return

        # If everything is valid, insert book
        db.insert_book(title, author, isbn, genre, status)
        self.populate_books()
        messagebox.showinfo("Success", "Book added successfully.")

    def update_book(self):
        """Update the selected book's details."""
        try:
            db.update_book(
                self.title_entry.get(),
                self.author_entry.get(),
                self.isbn_entry.get(),
                self.genre_entry.get(),
                self.status_entry.get()
            )
            self.populate_books()
        except AttributeError:
            messagebox.showwarning("Selection Error", "Please select a book to update")

    def delete_book(self):
        """Delete a book by title if it exists."""
        title = self.title_entry.get().strip()

        if not title:
            messagebox.showwarning("Input Error", "Please enter the book title to delete.")
            return

        # Check if book exists
        book = db.get_book_by_title(title)
        if not book:
            messagebox.showerror("Not Found", "Book with this title does not exist.")
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{title}'?")
        if confirm:
            db.delete_book(book[0])  # book[0] is the book ID
            self.populate_books()
            messagebox.showinfo("Success", f"'{title}' has been deleted.")

    def checkout_book(self):
        """Checkout the book based on the member ID and book title."""
        member_id_input = self.checkout_member_id_entry.get().strip()
        book_title_input = self.checkout_book_title_entry.get().strip()

        if not member_id_input or not book_title_input:
            messagebox.showwarning("Input Error", "Please fill both fields.")
            return

        try:
            membership_id = int(member_id_input)
        except ValueError:
            messagebox.showwarning("Input Error", "Member ID must be a number.")
            return

        success, message = db.checkout_book(membership_id, book_title_input)

        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)

    def go_back(self):
        """Go back to the main window."""
        self.root.destroy()
        import gui_main
        main = tk.Tk()
        gui_main.MainApp(main)
        main.mainloop()
