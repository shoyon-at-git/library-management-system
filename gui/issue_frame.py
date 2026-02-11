import tkinter as tk
from tkinter import messagebox, ttk
from models.issued import issue_book, return_book, get_issued

class IssueFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        # Title
        title = tk.Label(self, text="🔁 Issue / Return Books", bg="white",
                        fg="#0b3c5d", font=("Segoe UI", 16, "bold"))
        title.pack(pady=(0, 15), anchor="w", padx=15)

        # Issue section
        issue_frame = tk.LabelFrame(self, text="Issue Book to Student", bg="white",
                                   fg="#333", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        issue_frame.pack(fill="x", padx=15, pady=(0, 15))

        tk.Label(issue_frame, text="Book ID:", bg="white", font=("Segoe UI", 9)).pack(side="left", anchor="w")
        self.b = tk.Entry(issue_frame, width=15, font=("Segoe UI", 9))
        self.b.pack(side="left", padx=(5, 20))

        tk.Label(issue_frame, text="Student ID:", bg="white", font=("Segoe UI", 9)).pack(side="left", anchor="w")
        self.s = tk.Entry(issue_frame, width=15, font=("Segoe UI", 9))
        self.s.pack(side="left", padx=(5, 20))

        tk.Button(issue_frame, text="📤 Issue Book", bg="#27ae60", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=15, command=self.issue).pack(side="left", padx=5)

        # Return section
        return_frame = tk.LabelFrame(self, text="Return Book", bg="white",
                                    fg="#333", font=("Segoe UI", 10, "bold"), padx=15, pady=10)
        return_frame.pack(fill="x", padx=15, pady=(0, 15))

        tk.Label(return_frame, text="Issue Record ID:", bg="white", font=("Segoe UI", 9)).pack(side="left", anchor="w")
        self.r = tk.Entry(return_frame, width=20, font=("Segoe UI", 9))
        self.r.pack(side="left", padx=(5, 20))

        tk.Button(return_frame, text="📥 Return Book", bg="#e74c3c", fg="white",
                 font=("Segoe UI", 9, "bold"), padx=15, command=self.ret).pack(side="left", padx=5)

        # List section
        list_frame = tk.LabelFrame(self, text="Issued Books Records", bg="white",
                                   fg="#333", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Create treeview for better display
        columns = ("ID", "Book ID", "Student ID", "Issue Date", "Return Date")
        self.tree = ttk.Treeview(list_frame, columns=columns, height=15, show="headings")
        
        self.tree.column("ID", width=40, anchor="center")
        self.tree.column("Book ID", width=60, anchor="center")
        self.tree.column("Student ID", width=80, anchor="center")
        self.tree.column("Issue Date", width=100, anchor="center")
        self.tree.column("Return Date", width=100, anchor="center")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Book ID", text="Book ID")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Issue Date", text="Issue Date")
        self.tree.heading("Return Date", text="Return Date")

        self.tree.pack(fill="both", expand=True)

        self.refresh()

    def issue(self):
        try:
            b_id = int(self.b.get().strip())
            s_id = int(self.s.get().strip())
            
            if b_id <= 0 or s_id <= 0:
                messagebox.showerror("Error", "Book ID and Student ID must be positive numbers")
                return
            
            issue_book(b_id, s_id)
            self.b.delete(0, tk.END)
            self.s.delete(0, tk.END)
            self.refresh()
            messagebox.showinfo("Success", "Book issued successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric IDs")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to issue book: {str(e)}")

    def ret(self):
        try:
            issue_id = int(self.r.get().strip())
            
            if issue_id <= 0:
                messagebox.showerror("Error", "Issue ID must be a positive number")
                return
            
            return_book(issue_id)
            self.r.delete(0, tk.END)
            self.refresh()
            messagebox.showinfo("Success", "Book returned successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Issue ID")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i in get_issued():
            self.tree.insert("", "end", values=i)

