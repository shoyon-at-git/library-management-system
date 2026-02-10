import tkinter as tk
from tkinter import messagebox
from models.books import (
    add_book, update_book, delete_book,
    search_books, get_books
)

class BooksFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="ID").grid(row=0,column=0)
        tk.Label(self, text="Title").grid(row=1,column=0)
        tk.Label(self, text="Author").grid(row=2,column=0)
        tk.Label(self, text="Quantity").grid(row=3,column=0)

        self.id_e = tk.Entry(self)
        self.t_e = tk.Entry(self)
        self.a_e = tk.Entry(self)
        self.q_e = tk.Entry(self)

        self.id_e.grid(row=0,column=1)
        self.t_e.grid(row=1,column=1)
        self.a_e.grid(row=2,column=1)
        self.q_e.grid(row=3,column=1)

        tk.Button(self, text="Add", width=10, command=self.add).grid(row=4,column=0)
        tk.Button(self, text="Update", width=10, command=self.update).grid(row=4,column=1)
        tk.Button(self, text="Delete", width=10, command=self.delete).grid(row=5,column=0)
        tk.Button(self, text="Search", width=10, command=self.search).grid(row=5,column=1)

        self.list = tk.Listbox(self, width=60)
        self.list.grid(row=0,column=2,rowspan=10,padx=10)

        self.list.bind("<<ListboxSelect>>", self.fill_from_list)

        self.refresh()


    def refresh(self):
        self.list.delete(0, tk.END)
        for b in get_books():
            self.list.insert(tk.END, b)


    def fill_from_list(self, e):
        if not self.list.curselection():
            return
        data = self.list.get(self.list.curselection())
        self.id_e.delete(0,tk.END)
        self.t_e.delete(0,tk.END)
        self.a_e.delete(0,tk.END)
        self.q_e.delete(0,tk.END)

        self.id_e.insert(0, data[0])
        self.t_e.insert(0, data[1])
        self.a_e.insert(0, data[2])
        self.q_e.insert(0, data[3])


    def add(self):
        if not self.t_e.get() or not self.a_e.get() or not self.q_e.get():
            messagebox.showerror("Error","Fill all fields except ID")
            return
        add_book(self.t_e.get(), self.a_e.get(), self.q_e.get())
        self.refresh()


    def update(self):
        if not self.id_e.get():
            messagebox.showerror("Error","Select a book first")
            return
        update_book(
            self.id_e.get(),
            self.t_e.get(),
            self.a_e.get(),
            self.q_e.get()
        )
        self.refresh()


    def delete(self):
        if not self.id_e.get():
            messagebox.showerror("Error","Select a book first")
            return
        if not messagebox.askyesno("Confirm","Delete this book?"):
            return
        delete_book(self.id_e.get())
        self.refresh()


    def search(self):
        key = self.t_e.get()
        self.list.delete(0, tk.END)
        for b in search_books(key):
            self.list.insert(tk.END, b)
