import tkinter as tk
from tkinter import messagebox

from models.books import add_book, update_book, delete_book, search_books, get_books
from gui.ui_theme import COLORS, page_header, card, form_label, entry, button, treeview, apply_app_theme


class BooksFrame(tk.Frame):
    def __init__(self, master, role=None):
        super().__init__(master, bg=COLORS["app_bg"])
        apply_app_theme(self)
        self.role = role
        self.student_view = role == "student"

        page_title = "📚 Browse Books" if self.student_view else "📚 Books Management"
        subtitle = (
            "Search the catalog and browse availability. Students only get discovery tools here, exactly as intended."
            if self.student_view
            else "Manage the catalog, keep stock updated, and search records without changing any underlying workflow."
        )
        badge = "Student view" if self.student_view else "Admin tools"
        page_header(self, page_title, subtitle, badge)

        if self.student_view:
            self._build_student_view()
        else:
            self._build_admin_view()

        self._build_list_section()
        self.refresh()

    def _build_student_view(self):
        wrap, body = card(
            self,
            "Search Books",
            "Search by Book ID, title, or author. Show All resets the catalog view.",
        )
        wrap.pack(fill="x", padx=20, pady=(0, 14))

        grid = tk.Frame(body, bg=COLORS["surface"])
        grid.pack(fill="x")
        grid.grid_columnconfigure(0, weight=0)
        grid.grid_columnconfigure(1, weight=1)

        form_label(grid, "Search term").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 6))
        self.search_e = entry(grid)
        self.search_e.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 8), ipady=8)

        tk.Label(
            grid,
            text="Examples: 101, database systems, tanenbaum",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).grid(row=2, column=0, columnspan=2, sticky="w")

        actions = tk.Frame(body, bg=COLORS["surface"])
        actions.pack(fill="x", pady=(14, 0))
        button(actions, "🔍 Search Book", self.search, "warning").pack(side="left", padx=(0, 10))
        button(actions, "🔄 Show All", self.refresh, "neutral").pack(side="left")

        self.t_e = None
        self.a_e = None
        self.q_e = None
        self.id_e = None

    def _build_admin_view(self):
        wrap, body = card(
            self,
            "Catalog Editor",
            "Create, update, delete, or search books from one clean control panel.",
        )
        wrap.pack(fill="x", padx=20, pady=(0, 14))

        grid = tk.Frame(body, bg=COLORS["surface"])
        grid.pack(fill="x")
        for col in range(4):
            grid.grid_columnconfigure(col, weight=1)

        form_label(grid, "Title").grid(row=0, column=0, sticky="w", pady=(0, 6))
        form_label(grid, "Author").grid(row=0, column=1, sticky="w", padx=(12, 0), pady=(0, 6))
        form_label(grid, "Quantity").grid(row=0, column=2, sticky="w", padx=(12, 0), pady=(0, 6))
        form_label(grid, "Book ID").grid(row=0, column=3, sticky="w", padx=(12, 0), pady=(0, 6))

        self.t_e = entry(grid)
        self.t_e.grid(row=1, column=0, sticky="ew", ipady=8)
        self.a_e = entry(grid)
        self.a_e.grid(row=1, column=1, sticky="ew", padx=(12, 0), ipady=8)
        self.q_e = entry(grid)
        self.q_e.grid(row=1, column=2, sticky="ew", padx=(12, 0), ipady=8)
        self.id_e = entry(grid, state="readonly")
        self.id_e.grid(row=1, column=3, sticky="ew", padx=(12, 0), ipady=8)

        actions = tk.Frame(body, bg=COLORS["surface"])
        actions.pack(fill="x", pady=(16, 0))
        button(actions, "➕ Add", self.add, "success").pack(side="left", padx=(0, 10))
        button(actions, "✏️ Update", self.update, "info").pack(side="left", padx=(0, 10))
        button(actions, "🗑️ Delete", self.delete, "danger").pack(side="left", padx=(0, 10))
        button(actions, "🔍 Search Book", self.search, "warning").pack(side="left", padx=(0, 10))
        button(actions, "🔄 Show All", self.refresh, "neutral").pack(side="left")

        self.search_e = None

    def _build_list_section(self):
        title = "Available Books" if self.student_view else "Catalog Records"
        subtitle = "Live data from the database. Click a row to load it into the form in admin view."
        wrap, body = card(self, title, subtitle, padx=14, pady=14)
        wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "Title", "Author", "Quantity")
        table_wrap = tk.Frame(body, bg=COLORS["surface"])
        table_wrap.pack(fill="both", expand=True)

        self.tree = treeview(table_wrap, columns=columns, height=16)
        self.tree.column("ID", width=70, anchor="center")
        self.tree.column("Title", width=320, anchor="w")
        self.tree.column("Author", width=240, anchor="w")
        self.tree.column("Quantity", width=110, anchor="center")

        for col in columns:
            self.tree.heading(col, text=col)

        scroll = tk.Scrollbar(table_wrap, orient="vertical", command=self.tree.yview, bg=COLORS["surface_alt"])
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.fill_from_list)

    def clear_inputs(self):
        if self.student_view:
            self.search_e.delete(0, tk.END)
            return

        self.t_e.delete(0, tk.END)
        self.a_e.delete(0, tk.END)
        self.q_e.delete(0, tk.END)
        self.id_e.config(state="normal")
        self.id_e.delete(0, tk.END)
        self.id_e.config(state="readonly")

    def refresh(self):
        if self.student_view and self.search_e is not None:
            self.search_e.delete(0, tk.END)

        for item in self.tree.get_children():
            self.tree.delete(item)
        for index, b in enumerate(get_books()):
            tags = ("alt",) if index % 2 else ()
            self.tree.insert("", "end", values=b, tags=tags)
        self.tree.tag_configure("alt", background=COLORS["row_alt"])

    def fill_from_list(self, _event):
        if self.student_view:
            return

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
        if self.student_view:
            return
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
        if self.student_view:
            return
        if not self.id_e.get():
            messagebox.showerror("Error", "Select a book first")
            return
        try:
            update_book(self.id_e.get(), self.t_e.get(), self.a_e.get(), int(self.q_e.get()))
            self.refresh()
            messagebox.showinfo("Success", "Book updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update book: {str(e)}")

    def delete(self):
        if self.student_view:
            return
        if not self.id_e.get():
            messagebox.showerror("Error", "Select a book first")
            return
        if not messagebox.askyesno("Confirm", "Delete this book?"):
            return
        try:
            delete_book(self.id_e.get())
            self.clear_inputs()
            self.refresh()
            messagebox.showinfo("Success", "Book deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete book: {str(e)}")

    def search(self):
        if self.student_view:
            search_key = self.search_e.get().strip()
            if not search_key:
                messagebox.showwarning("Warning", "Enter a Book ID, Title, or Author to search")
                return
        else:
            title_key = self.t_e.get().strip()
            author_key = self.a_e.get().strip()
            id_key = self.id_e.get().strip()
            search_key = title_key or author_key or id_key
            if not search_key:
                messagebox.showwarning("Warning", "Enter a Book ID, Title, or Author to search")
                return

        for item in self.tree.get_children():
            self.tree.delete(item)
        results = search_books(search_key)
        if not results:
            messagebox.showinfo("Search", "No books found matching your search")
        for index, b in enumerate(results):
            tags = ("alt",) if index % 2 else ()
            self.tree.insert("", "end", values=b, tags=tags)
        self.tree.tag_configure("alt", background=COLORS["row_alt"])
