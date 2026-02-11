
import tkinter as tk
from tkinter import messagebox
from models.admin import validate_login

class LoginWindow(tk.Toplevel):

    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.title("Login - HSTU Library")
        self.geometry("450x350")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 225
        y = (self.winfo_screenheight() // 2) - 175
        self.geometry(f'450x350+{x}+{y}')

        # Main frame with background
        main_frame = tk.Frame(self, bg="#0b3c5d")
        main_frame.pack(fill="both", expand=True)

        # Header
        header = tk.Label(main_frame, text="HSTU Library", 
                         bg="#0b3c5d", fg="white",
                         font=("Segoe UI", 18, "bold"))
        header.pack(pady=(20, 5))

        subtitle = tk.Label(main_frame, text="Management System", 
                           bg="#0b3c5d", fg="#ecf0f1",
                           font=("Segoe UI", 11))
        subtitle.pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(fill="x", padx=30, pady=(0, 30))

        # Username
        tk.Label(form_frame, text="Username:", bg="white", fg="#333",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 3))
        self.user_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30, bd=1)
        self.user_entry.pack(fill="x", pady=(0, 15), ipady=5)
        self.user_entry.focus()

        # Password
        tk.Label(form_frame, text="Password:", bg="white", fg="#333",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 3))
        self.pass_entry = tk.Entry(form_frame, show="*", font=("Segoe UI", 11), width=30, bd=1)
        self.pass_entry.pack(fill="x", pady=(0, 15), ipady=5)

        # Bind Enter key
        self.pass_entry.bind("<Return>", lambda e: self.login())

        # Login button
        tk.Button(form_frame, text="🔐 Login", command=self.login,
                 bg="#0b3c5d", fg="white", font=("Segoe UI", 11, "bold"),
                 padx=30, pady=8, relief="flat", cursor="hand2").pack(pady=(0, 10))

        # Close on X button closes the app
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Enter username and password")
            return

        if validate_login(u, p):
            self.master.deiconify()  # Show main window
            self.destroy()  # Close login window
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.pass_entry.delete(0, tk.END)
            self.user_entry.focus()

    def on_close(self):
        self.master.destroy()
