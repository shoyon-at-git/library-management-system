import tkinter as tk
from tkinter import messagebox, ttk
from models.students import (
    register_student, update_student, delete_student,
    search_students, get_students
)


class StudentsFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master, bg="white")
        self.selected_record_id = None

        # Title
        title = tk.Label(
            self,
            text="👨‍🎓 Students Management",
            bg="white",
            fg="#0b3c5d",
            font=("Segoe UI", 16, "bold"),
        )
        title.pack(pady=(0, 15), anchor="w", padx=15)

        # Form section
        form_frame = tk.LabelFrame(
            self,
            text="Add / Update Student",
            bg="white",
            fg="#333",
            font=("Segoe UI", 10, "bold"),
            padx=15,
            pady=10,
        )
        form_frame.pack(fill="x", padx=15, pady=(0, 15))

        # Input fields
        tk.Label(form_frame, text="ID:", bg="white", font=("Segoe UI", 9)).grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.db_id_e = tk.Entry(form_frame, width=12, font=("Segoe UI", 9), state="readonly")
        self.db_id_e.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Student ID:", bg="white", font=("Segoe UI", 9)).grid(
            row=0, column=2, sticky="w", padx=(20, 0), pady=5
        )
        self.id_e = tk.Entry(form_frame, width=22, font=("Segoe UI", 9))
        self.id_e.grid(row=0, column=3, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Name:", bg="white", font=("Segoe UI", 9)).grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.n_e = tk.Entry(form_frame, width=35, font=("Segoe UI", 9))
        self.n_e.grid(row=1, column=1, columnspan=2, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Session:", bg="white", font=("Segoe UI", 9)).grid(
            row=1, column=3, sticky="w", padx=(20, 0), pady=5
        )
        self.session_e = tk.Entry(form_frame, width=20, font=("Segoe UI", 9))
        self.session_e.grid(row=1, column=4, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Department:", bg="white", font=("Segoe UI", 9)).grid(
            row=2, column=0, sticky="w", pady=5
        )
        self.d_e = tk.Entry(form_frame, width=35, font=("Segoe UI", 9))
        self.d_e.grid(row=2, column=1, columnspan=2, sticky="w", padx=(10, 0), pady=5)

        tk.Label(form_frame, text="Birth Date (YYYY-MM-DD):", bg="white", font=("Segoe UI", 9)).grid(
            row=2, column=3, sticky="w", padx=(20, 0), pady=5
        )
        self.birth_e = tk.Entry(form_frame, width=20, font=("Segoe UI", 9))
        self.birth_e.grid(row=2, column=4, sticky="w", padx=(10, 0), pady=5)

        # Buttons
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.grid(row=3, column=0, columnspan=5, pady=(10, 0))

        tk.Button(
            button_frame,
            text="➕ Add",
            bg="#27ae60",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            command=self.add,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="✏️ Update",
            bg="#3498db",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            command=self.update,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="🗑️ Delete",
            bg="#e74c3c",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            command=self.delete,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="🔍 Search",
            bg="#f39c12",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            command=self.search,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="🔄 Clear",
            bg="#7f8c8d",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            padx=15,
            command=self.clear_form,
        ).pack(side="left", padx=5)

        # List section
        list_frame = tk.LabelFrame(
            self,
            text="Students List",
            bg="white",
            fg="#333",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
        )
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("ID", "Student ID", "Name", "Department", "Email", "Session", "Birth Date")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15, show="headings")

        self.tree.column("ID", width=60, anchor="center")
        self.tree.column("Student ID", width=110, anchor="center")
        self.tree.column("Name", width=160, anchor="w")
        self.tree.column("Department", width=150, anchor="w")
        self.tree.column("Email", width=220, anchor="w")
        self.tree.column("Session", width=100, anchor="center")
        self.tree.column("Birth Date", width=110, anchor="center")

        for col in columns:
            self.tree.heading(col, text=col)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.fill_from_list)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for student in get_students():
            self.tree.insert("", "end", values=student)

    def _set_readonly_entry(self, entry, value):
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, value)
        entry.config(state="readonly")

    def clear_form(self):
        self.selected_record_id = None
        self._set_readonly_entry(self.db_id_e, "")
        self.id_e.delete(0, tk.END)
        self.n_e.delete(0, tk.END)
        self.d_e.delete(0, tk.END)
        self.session_e.delete(0, tk.END)
        self.birth_e.delete(0, tk.END)
        self.id_e.focus_set()
        for item in self.tree.selection():
            self.tree.selection_remove(item)

    def fill_from_list(self, _event):
        selected = self.tree.selection()
        if not selected:
            return

        data = self.tree.item(selected[0])["values"]
        if len(data) < 7:
            return

        self.selected_record_id = data[0]
        self._set_readonly_entry(self.db_id_e, str(data[0]))

        self.id_e.delete(0, tk.END)
        self.id_e.insert(0, data[1] or "")

        self.n_e.delete(0, tk.END)
        self.n_e.insert(0, data[2] or "")

        self.d_e.delete(0, tk.END)
        self.d_e.insert(0, data[3] or "")

        self.session_e.delete(0, tk.END)
        self.session_e.insert(0, data[5] or "")

        self.birth_e.delete(0, tk.END)
        self.birth_e.insert(0, data[6] or "")

        self.id_e.focus_set()

    def _validated_birth_date(self):
        birth_val = self.birth_e.get().strip() or None
        if birth_val:
            try:
                from datetime import datetime

                datetime.strptime(birth_val, "%Y-%m-%d")
            except Exception:
                messagebox.showerror("Error", "Birth date must be in YYYY-MM-DD format")
                return None, False
        return birth_val, True

    def add(self):
        if not self.id_e.get().strip() or not self.n_e.get().strip() or not self.d_e.get().strip():
            messagebox.showerror("Error", "Fill Student ID, name, and department")
            return

        birth_val, ok_birth = self._validated_birth_date()
        if not ok_birth:
            return

        try:
            sid = self.id_e.get().strip()
            session_val = self.session_e.get().strip() or None

            ok, result = register_student(sid, self.n_e.get(), self.d_e.get(), session_val, birth_val)
            if not ok:
                messagebox.showerror("Error", result or "Failed to add student")
                return

            _student_id, email, pwd = result
            self.refresh()
            self.clear_form()
            messagebox.showinfo("Success", f"Student added successfully!\n\nEmail: {email}\nPassword: {pwd}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add student: {str(e)}")

    def update(self):
        if not self.selected_record_id:
            messagebox.showerror("Error", "Select a student first")
            return

        birth_val, ok_birth = self._validated_birth_date()
        if not ok_birth:
            return

        try:
            session_val = self.session_e.get().strip() or None
            update_student(
                self.selected_record_id,
                self.id_e.get(),
                self.n_e.get(),
                self.d_e.get(),
                session_val,
                birth_val,
            )
            self.refresh()
            messagebox.showinfo("Success", "Student updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update student: {str(e)}")

    def delete(self):
        if not self.selected_record_id:
            messagebox.showerror("Error", "Select a student first")
            return
        if not messagebox.askyesno("Confirm", "Delete this student?"):
            return

        try:
            delete_student(self.selected_record_id)
            self.refresh()
            self.clear_form()
            messagebox.showinfo("Success", "Student deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete student: {str(e)}")

    def search(self):
        key = (
            self.db_id_e.get().strip()
            or self.id_e.get().strip()
            or self.n_e.get().strip()
            or self.d_e.get().strip()
        )
        if not key:
            messagebox.showwarning("Warning", "Enter ID, Student ID, name, or department to search")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        results = search_students(key)
        if not results:
            messagebox.showinfo("Search", "No students found matching your search")
            return

        for student in results:
            self.tree.insert("", "end", values=student)
