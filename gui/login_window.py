
import tkinter as tk
from tkinter import messagebox
from models.admin import validate_login, register_admin

class LoginWindow(tk.Toplevel):

    def __init__(self, master, on_success):
        super().__init__(master)

        self.on_success = on_success

        self.title("Login - HSTU Library")
        self.geometry("450x480")
        self.resizable(False, False)
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 225
        y = (self.winfo_screenheight() // 2) - 240
        self.geometry(f'450x480+{x}+{y}')

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
        form_frame.pack(fill="x", padx=30, pady=(0, 20))

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

        # Buttons container to ensure consistent layout
        button_frame = tk.Frame(form_frame, bg="white")
        button_frame.pack(fill="x", pady=(0, 10))

        tk.Button(button_frame, text="🔐 Login", command=self.login,
             bg="#0b3c5d", fg="white", font=("Segoe UI", 11, "bold"),
             padx=30, pady=8, relief="flat", cursor="hand2").pack(fill="x", pady=(0, 6))

        tk.Button(button_frame, text="📝 Register", command=self.open_register,
             bg="#16a085", fg="white", font=("Segoe UI", 11, "bold"),
             padx=30, pady=8, relief="flat", cursor="hand2").pack(fill="x")

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

    def open_register(self):
        reg = tk.Toplevel(self)
        reg.title("Register - HSTU Library")
        reg.geometry("400x320")
        reg.resizable(False, False)

        # center
        reg.update_idletasks()
        x = (reg.winfo_screenwidth() // 2) - 200
        y = (reg.winfo_screenheight() // 2) - 160
        reg.geometry(f'400x320+{x}+{y}')

        main_frame = tk.Frame(reg, bg="#0b3c5d")
        main_frame.pack(fill="both", expand=True)

        header = tk.Label(main_frame, text="Register Admin",
                         bg="#0b3c5d", fg="white",
                         font=("Segoe UI", 16, "bold"))
        header.pack(pady=(20, 5))

        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(fill="x", padx=30, pady=(10, 20))

        tk.Label(form_frame, text="Username:", bg="white", fg="#333",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 3))
        username_entry = tk.Entry(form_frame, font=("Segoe UI", 11), width=30, bd=1)
        username_entry.pack(fill="x", pady=(0, 15), ipady=5)

        tk.Label(form_frame, text="Password:", bg="white", fg="#333",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 3))
        password_entry = tk.Entry(form_frame, show="*", font=("Segoe UI", 11), width=30, bd=1)
        password_entry.pack(fill="x", pady=(0, 15), ipady=5)

        tk.Label(form_frame, text="Confirm Password:", bg="white", fg="#333",
                font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 3))
        confirm_entry = tk.Entry(form_frame, show="*", font=("Segoe UI", 11), width=30, bd=1)
        confirm_entry.pack(fill="x", pady=(0, 15), ipady=5)

        def do_register():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            c = confirm_entry.get().strip()

            if not u or not p or not c:
                messagebox.showerror("Error", "All fields are required", parent=reg)
                return
            if p != c:
                messagebox.showerror("Error", "Passwords do not match", parent=reg)
                return
            if len(p) < 4:
                messagebox.showerror("Error", "Password must be at least 4 characters", parent=reg)
                return

            ok, err = register_admin(u, p)
            if not ok:
                messagebox.showerror("Register Failed", err or "Unable to register", parent=reg)
                return

            messagebox.showinfo("Success", "Registration successful. You can now login.", parent=reg)
            reg.destroy()

        tk.Button(form_frame, text="Create Account", command=do_register,
                 bg="#0b3c5d", fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, relief="flat", cursor="hand2").pack(pady=(5, 5))

        # bind enter to register
        confirm_entry.bind("<Return>", lambda e: do_register())
