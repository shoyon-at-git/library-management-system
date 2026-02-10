import tkinter as tk
from tkinter import messagebox
from models.students import (
    add_student, update_student, delete_student,
    search_students, get_students
)

class StudentsFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="ID").grid(row=0,column=0)
        tk.Label(self, text="Name").grid(row=1,column=0)
        tk.Label(self, text="Department").grid(row=2,column=0)

        self.id_e = tk.Entry(self)
        self.n_e = tk.Entry(self)
        self.d_e = tk.Entry(self)

        self.id_e.grid(row=0,column=1)
        self.n_e.grid(row=1,column=1)
        self.d_e.grid(row=2,column=1)

        tk.Button(self, text="Add", width=10, command=self.add).grid(row=3,column=0)
        tk.Button(self, text="Update", width=10, command=self.update).grid(row=3,column=1)
        tk.Button(self, text="Delete", width=10, command=self.delete).grid(row=4,column=0)
        tk.Button(self, text="Search", width=10, command=self.search).grid(row=4,column=1)

        self.list = tk.Listbox(self, width=60)
        self.list.grid(row=0,column=2,rowspan=10,padx=10)

        self.list.bind("<<ListboxSelect>>", self.fill_from_list)

        self.refresh()


    def refresh(self):
        self.list.delete(0, tk.END)
        for s in get_students():
            self.list.insert(tk.END, s)


    def fill_from_list(self, e):
        if not self.list.curselection():
            return
        data = self.list.get(self.list.curselection())
        self.id_e.delete(0,tk.END)
        self.n_e.delete(0,tk.END)
        self.d_e.delete(0,tk.END)

        self.id_e.insert(0, data[0])
        self.n_e.insert(0, data[1])
        self.d_e.insert(0, data[2])


    def add(self):
        if not self.n_e.get() or not self.d_e.get():
            messagebox.showerror("Error","Fill name and department")
            return
        add_student(self.n_e.get(), self.d_e.get())
        self.refresh()


    def update(self):
        if not self.id_e.get():
            messagebox.showerror("Error","Select a student first")
            return
        update_student(
            self.id_e.get(),
            self.n_e.get(),
            self.d_e.get()
        )
        self.refresh()


    def delete(self):
        if not self.id_e.get():
            messagebox.showerror("Error","Select a student first")
            return
        if not messagebox.askyesno("Confirm","Delete this student?"):
            return
        delete_student(self.id_e.get())
        self.refresh()


    def search(self):
        key = self.n_e.get()
        self.list.delete(0, tk.END)
        for s in search_students(key):
            self.list.insert(tk.END, s)
