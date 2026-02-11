import tkinter as tk
from tkinter import messagebox, ttk
from models.books import (
    add_book, update_book, delete_book,
    search_books, get_books
)

class BooksFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="white")

        # Title
        title = tk.Label(self, text="📚 Books Management", bg="white",
                        fg="#0b3c5d", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 15), anchor="w", padx=15)

        # Form section
        form_frame = tk.LabelFrame(self, text="Add / Update Book", bg="white",
                                   fg="#333", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        form_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Input fields
        tk.Label(form_frame, text="Title:", bg="white", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.t_e = tk.Entry(form_frame, width=25, font=("Segoe UI", 9))
        self.t_e.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Author:", bg="white", font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", padx=(20, 0), pady=5)
        self.a_e = tk.Entry(form_frame, width=25, font=("Segoe UI", 9))
        self.a_e.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Quantity:", bg="white", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.q_e = tk.Entry(form_frame, width=25, font=("Segoe UI", 9))
        self.q_e.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="ID:", bg="white", font=("Segoe UI", 9)).grid(row=1, column=2, sticky="w", padx=(20, 0), pady=5)
        self.id_e = tk.Entry(form_frame, width=25, font=("Segoe UI", 9), state="readonly")
        self.id_e.grid(row=1, column=3, sticky="w", padx=(10, 0), pady=5)

        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=2, column=0, columnspan=4, pady=(10, 0))

        tk.Button(button_frame, text="➕ Add", bg="#27ae60", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=15, command=self.add).pack(side="left", padx=5)
        tk.Button(button_frame, text="✏️ Update", bg="#3498db", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=15, command=self.update).pack(side="left", padx=5)
        tk.Button(button_frame, text="🗑️ Delete", bg="#e74c3c", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=15, command=self.delete).pack(side="left", padx=5)
        tk.Button(button_frame, text="🔍 Search", bg="#f39c12", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=15, command=self.search).pack(side="left", padx=5)

        # List section
        list_frame = tk.LabelFrame(self, text="Books List", bg="white",
                                   fg="#333", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create treeview for better display
        columns = ("ID", "Title", "Author", "Quantity")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15, show="headings")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Title", width=200, anchor="w")
        self.tree.column("Author", width=150, anchor="w")
        self.tree.column("Quantity", width=80, anchor="center")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Quantity", text="Quantity")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_from_list)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for b in get_books():
            self.tree.insert("", "end", values=b)

    def fill_from_list(self, e):
        selected = self.tree.selection()
        if not selected:
            return
        data = self.tree.item(selected[0])["values"]
        self.id_e.config(state="normal")
        self.id_e.delete(0, tk.END)
        self.t_e.delete(0, tk.END)
        self.a_e.delete(0, tk.END)
        self.q_e.delete(0, tk.END)

        self.id_e.insert(0, data[0])
        self.t_e.insert(0, data[1])
        self.a_e.insert(0, data[2])
        self.q_e.insert(0, data[3])
        self.id_e.config(state="readonly")

    def add(self):
        if not self.t_e.get() or not self.a_e.get() or not self.q_e.get():
            messagebox.showerror("Error", "Fill all fields except ID")
            return
        try:
            add_book(self.t_e.get(), self.a_e.get(), int(self.q_e.get()))
            self.t_e.delete(0, tk.END)
            self.a_e.delete(0, tk.END)
            self.q_e.delete(0, tk.END)
            self.refresh()
            messagebox.showinfo("Success", "Book added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add book: {str(e)}")

    def update(self):
        if not self.id_e.get():
            messagebox.showerror("Error", "Select a book first")
            return
        try:
            update_book(
                self.id_e.get(),
                self.t_e.get(),
                self.a_e.get(),
                int(self.q_e.get())
            )
            self.refresh()
            messagebox.showinfo("Success", "Book updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")

    def delete(self):
        if not self.id_e.get():
            messagebox.showerror("Error", "Select a book first")
            return
        if not messagebox.askyesno("Confirm", "Delete this book?"):
            return
        try:
            delete_book(self.id_e.get())
            self.t_e.delete(0, tk.END)
            self.a_e.delete(0, tk.END)
            self.q_e.delete(0, tk.END)
            self.id_e.config(state="normal")
            self.id_e.delete(0, tk.END)
            self.id_e.config(state="readonly")
            self.refresh()
            messagebox.showinfo("Success", "Book deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

    def search(self):
        key = self.t_e.get().strip()
        if not key:
            messagebox.showwarning("Warning", "Enter a title to search")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        results = search_books(key)
        if not results:
            messagebox.showinfo("Search", "No books found matching your search")
        for b in results:
            self.tree.insert("", "end", values=b)

