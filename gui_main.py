import tkinter as tk
from gui_book import BookManagement
from gui_member import MemberManagement

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("600x400")
        self.root.resizable(False, False)

        self.button_bg = "#4a7abc"
        self.button_fg = "white"
        self.button_font = ("Arial", 12, "bold")

        tk.Label(self.root, text="Library System", font=("Arial", 14, "bold")).pack(pady=20)

        manage_books_btn = tk.Button(self.root, text="Manage Books", bg=self.button_bg, fg=self.button_fg,
                                     font=self.button_font, width=20, command=self.open_books)
        manage_books_btn.pack(pady=5)

        manage_members_btn = tk.Button(self.root, text="Manage Members", bg=self.button_bg, fg=self.button_fg,
                                       font=self.button_font, width=20, command=self.open_members)
        manage_members_btn.pack(pady=5)

        exit_btn = tk.Button(self.root, text="Exit", bg="gray", fg="white", font=self.button_font,
                             width=20, command=self.root.quit)
        exit_btn.pack(pady=5)

    def open_books(self):
        """Opens the BookManagement window."""
        self.root.withdraw()  # Hide the main window
        book_window = tk.Toplevel()
        # Pass back_to_main_window method as a callback to BookManagement
        BookManagement(book_window, self.back_to_main_window)

    def open_members(self):
        """Opens the MemberManagement window."""
        self.root.withdraw()  # Hide the main window
        member_window = tk.Toplevel()
        MemberManagement(member_window, self.back_to_main_window)
        member_window.mainloop()

    def back_to_main_window(self):
        """Brings the main window back into focus."""
        self.root.deiconify()  # Unhide the main window when "Back" is clicked
