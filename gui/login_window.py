
import tkinter as tk
from tkinter import messagebox
from models.admin import validate_login

class LoginWindow(tk.Toplevel):

    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.title("Login - HSTU Library")
        self.geometry("300x180")
        self.resizable(False, False)

        tk.Label(self, text="Username").pack(pady=5)
        self.user_entry = tk.Entry(self)
        self.user_entry.pack()

        tk.Label(self, text="Password").pack(pady=5)
        self.pass_entry = tk.Entry(self, show="*")
        self.pass_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.master.destroy)

    def login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Enter username and password")
            return

        if validate_login(u, p):
            self.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login failed", "Invalid username or password")
