import tkinter as tk
from tkinter import messagebox, ttk
from models.students import (
    add_student, register_student, update_student, delete_student,
    search_students, get_students
)

class StudentsFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="white")

        # Title
        title = tk.Label(self, text="👨‍🎓 Students Management", bg="white",
                        fg="#0b3c5d", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 15), anchor="w", padx=15)

        # Form section
        form_frame = tk.LabelFrame(self, text="Add / Update Student", bg="white",
                                   fg="#333", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        form_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Input fields
        tk.Label(form_frame, text="Name:", bg="white", font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.n_e = tk.Entry(form_frame, width=35, font=("Segoe UI", 9))
        self.n_e.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Department:", bg="white", font=("Segoe UI", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.d_e = tk.Entry(form_frame, width=35, font=("Segoe UI", 9))
        self.d_e.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Username (optional):", bg="white", font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", pady=5)
        self.u_e = tk.Entry(form_frame, width=35, font=("Segoe UI", 9))
        self.u_e.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Password (optional):", bg="white", font=("Segoe UI", 9)).grid(row=3, column=0, sticky="w", pady=5)
        self.pw_e = tk.Entry(form_frame, width=35, show='*', font=("Segoe UI", 9))
        self.pw_e.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="ID:", bg="white", font=("Segoe UI", 9)).grid(row=0, column=2, sticky="w", padx=(20, 0), pady=5)
        self.id_e = tk.Entry(form_frame, width=20, font=("Segoe UI", 9), state="readonly")
        self.id_e.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=5)

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
        list_frame = tk.LabelFrame(self, text="Students List", bg="white",
                                   fg="#333", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create treeview for better display
        columns = ("ID", "Name", "Department")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15, show="headings")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Name", width=200, anchor="w")
        self.tree.column("Department", width=150, anchor="w")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Department", text="Department")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_from_list)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for s in get_students():
            self.tree.insert("", "end", values=s)

    def fill_from_list(self, e):
        selected = self.tree.selection()
        if not selected:
            return
        data = self.tree.item(selected[0])["values"]
        self.id_e.config(state="normal")
        self.id_e.delete(0, tk.END)
        self.n_e.delete(0, tk.END)
        self.d_e.delete(0, tk.END)
        self.u_e.delete(0, tk.END)
        self.pw_e.delete(0, tk.END)

        self.id_e.insert(0, data[0])
        self.n_e.insert(0, data[1])
        self.d_e.insert(0, data[2])
        # username and password are stored in separate table; leave blank when filling
        self.id_e.config(state="readonly")

    def add(self):
        if not self.n_e.get() or not self.d_e.get():
            messagebox.showerror("Error", "Fill name and department")
            return
        try:
            # create student
            ok, student_id_or_err = register_student(self.n_e.get(), self.d_e.get())
            if not ok:
                messagebox.showerror("Error", student_id_or_err or "Failed to add student")
                return

            student_id = student_id_or_err
            # handle username/password creation
            username = self.u_e.get().strip()
            password = self.pw_e.get().strip()
            created_username = None
            created_password = None
            from models.students import create_student_user

            if username and password:
                uok, uerr = create_student_user(student_id, username, password)
                if not uok:
                    messagebox.showerror("Error", f"Student created but user not created: {uerr}")
                else:
                    created_username = username
            elif username and not password:
                messagebox.showwarning("Warning", "Username provided without password — ignoring username creation")
            elif password and not username:
                messagebox.showwarning("Warning", "Password provided without username — ignoring password")
            else:
                # auto-generate username and password
                base = ''.join(self.n_e.get().split()).lower() or f'stu{student_id}'
                gen_username = f"{base}{student_id}"
                gen_password = f"pwd{student_id}"
                uok, uerr = create_student_user(student_id, gen_username, gen_password)
                if not uok:
                    # fallback username
                    gen_username = f"stu{student_id}"
                    uok, uerr = create_student_user(student_id, gen_username, gen_password)
                if uok:
                    created_username = gen_username
                    created_password = gen_password

            self.n_e.delete(0, tk.END)
            self.d_e.delete(0, tk.END)
            self.u_e.delete(0, tk.END)
            self.pw_e.delete(0, tk.END)
            self.refresh()
            messagebox.showinfo("Success", "Student added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")

    def update(self):
        if not self.id_e.get():
            messagebox.showerror("Error", "Select a student first")
            return
        try:
            update_student(
                self.id_e.get(),
                self.n_e.get(),
                self.d_e.get()
            )
            self.refresh()
            messagebox.showinfo("Success", "Student updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")

    def delete(self):
        if not self.id_e.get():
            messagebox.showerror("Error", "Select a student first")
            return
        if not messagebox.askyesno("Confirm", "Delete this student?"):
            return
        try:
            delete_student(self.id_e.get())
            self.n_e.delete(0, tk.END)
            self.d_e.delete(0, tk.END)
            self.id_e.config(state="normal")
            self.id_e.delete(0, tk.END)
            self.id_e.config(state="readonly")
            self.refresh()
            messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")

    def search(self):
        key = self.n_e.get().strip()
        if not key:
            messagebox.showwarning("Warning", "Enter a name to search")
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        results = search_students(key)
        if not results:
            messagebox.showinfo("Search", "No students found matching your search")
        for s in results:
            self.tree.insert("", "end", values=s)

