import tkinter as tk
from tkinter import messagebox, ttk
from db import Database

db = Database("libraryDB.db")

class MemberManagement:
    def __init__(self, root, back_to_main_window_callback):
        self.root = root
        self.back_to_main_window = back_to_main_window_callback
        self.root.title("Member Management")
        self.root.geometry("700x450")

        # Buttons and other UI elements
        self.button_bg = "#4a7abc"
        self.button_fg = "white"
        self.button_font = ("Arial", 12, "bold")

        # Labels
        tk.Label(root, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Contact:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.contact_entry = tk.Entry(root)
        self.contact_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Membership Type:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.membership_type = ttk.Combobox(root, values=["Standard", "Premium", "Student"])
        self.membership_type.grid(row=2, column=1, padx=10, pady=5)

        # Listbox and Scrollbar
        self.member_list = tk.Listbox(root, height=12, width=80)
        self.member_list.grid(row=4, column=0, columnspan=3, pady=10)

        scrollbar = tk.Scrollbar(root)
        scrollbar.grid(row=4, column=3, sticky='ns')

        self.member_list.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.member_list.yview)

        self.member_list.bind('<<ListboxSelect>>', self.select_member)

        # Apply these settings to the buttons
        tk.Button(root, text="Add", width=12, command=self.add_member,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=5, column=0)

        tk.Button(root, text="Update", width=12, command=self.update_member,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=5, column=1)

        tk.Button(root, text="Delete", width=12, command=self.delete_member,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=5, column=2)

        tk.Button(root, text="Refresh", width=12, command=self.populate_members,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=6, column=0)

        tk.Button(root, text="Back", width=12, command=self.go_back,
                  bg=self.button_bg, fg=self.button_fg, font=self.button_font).grid(row=6, column=2)

        # Populate the member list when the window is loaded
        self.populate_members()

    def populate_members(self):
        """Populate the Listbox with members from the database."""
        self.member_list.delete(0, tk.END)
        for member in db.select_members():
            display = f"ID: {member[0]} | Name: {member[1]} | Contact: {member[2]} | Type: {member[3]}"
            self.member_list.insert(tk.END, display)

    def select_member(self, event):
        """Select a member from the Listbox and display their details."""
        try:
            index = self.member_list.curselection()[0]
            selected = db.select_members()[index]
            self.selected_member_id = selected[0]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(tk.END, selected[1])
            self.contact_entry.delete(0, tk.END)
            self.contact_entry.insert(tk.END, selected[2])
            self.membership_type.set(selected[3])
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a member from the list.")

    def add_member(self):
        """Add a new member to the database."""
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        membership_type = self.membership_type.get()

        # Check if all fields are filled
        if name and contact and membership_type:
            db.insert_member(name, contact, membership_type)
            self.populate_members()
        else:
            messagebox.showwarning("Input error", "Please fill all fields")

    def update_member(self):
        """Update the selected member's details."""
        try:
            db.update_member(
                self.selected_member_id,
                self.name_entry.get(),
                self.contact_entry.get(),
                self.membership_type.get()
            )
            self.populate_members()
        except AttributeError:
            messagebox.showwarning("Selection Error", "Please select a member to update")

    def delete_member(self):
        """Delete the selected member."""
        try:
            db.delete_member(self.selected_member_id)
            self.populate_members()
        except AttributeError:
            messagebox.showwarning("Selection Error", "Please select a member to delete")

    def go_back(self):
        """Go back to the main window."""
        self.root.destroy()
        import gui_main  # import only when needed to avoid circular import
        main = tk.Tk()
        gui_main.MainApp(main)
        main.mainloop()
