import tkinter as tk
from tkinter import messagebox

from models.admin import validate_login, register_admin
from gui.ui_theme import COLORS, apply_app_theme, entry, button


class LoginWindow(tk.Toplevel):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.on_success = on_success

        self.title("Login - HSTU Library")
        self.geometry("1040x620")
        self.minsize(1040, 620)
        self.resizable(False, False)
        self.configure(bg=COLORS["app_bg"])
        apply_app_theme(self)
        self._center(1040, 620)

        shell = tk.Frame(self, bg=COLORS["app_bg"])
        shell.pack(fill="both", expand=True, padx=24, pady=24)

        card = tk.Frame(
            shell,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
        )
        card.pack(fill="both", expand=True)

        left = tk.Frame(card, bg=COLORS["primary_dark"], width=410)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        right = tk.Frame(card, bg=COLORS["surface"])
        right.pack(side="right", fill="both", expand=True)

        self._build_hero(left)
        self._build_admin_login(right)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _center(self, width, height, win=None):
        win = win or self
        win.update_idletasks()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

    def _build_hero(self, parent):
        hero = tk.Frame(parent, bg=COLORS["primary_dark"])
        hero.pack(fill="both", expand=True, padx=32, pady=32)

        pill = tk.Label(
            hero,
            text="HSTU LIBRARY",
            bg="#1b5f96",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=6,
        )
        pill.pack(anchor="w")

        tk.Label(
            hero,
            text="Library Management\nSystem",
            bg=COLORS["primary_dark"],
            fg="white",
            font=("Segoe UI", 24, "bold"),
            justify="left",
            anchor="w",
            wraplength=300,
        ).pack(fill="x", anchor="w", pady=(18, 8))

        tk.Label(
            hero,
            text="Admin tools, student access, catalog browsing, and issue tracking — same engine, cleaner cockpit.",
            bg=COLORS["primary_dark"],
            fg=COLORS["hero_text"],
            font=("Segoe UI", 11),
            justify="left",
            wraplength=300,
        ).pack(anchor="w")

        info_box = tk.Frame(hero, bg="#113b63", padx=16, pady=16)
        info_box.pack(fill="x", pady=(26, 0))
        for title, desc in [
            ("Admin login", "Manage books, students, lending, and returns."),
            ("Student login", "Browse books and view profile details only."),
            ("Register", "Create a new admin account if needed."),
        ]:
            tk.Label(
                info_box,
                text=title,
                bg="#113b63",
                fg="white",
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w")
            tk.Label(
                info_box,
                text=desc,
                bg="#113b63",
                fg="#c8d9ea",
                font=("Segoe UI", 9),
                wraplength=280,
                justify="left",
            ).pack(anchor="w", pady=(2, 10))

        tk.Label(
            hero,
            text="Less chalkboard, more dashboard.",
            bg=COLORS["primary_dark"],
            fg="#9cc4e4",
            font=("Segoe UI", 10, "italic"),
        ).pack(anchor="w", pady=(18, 0))

    def _build_admin_login(self, parent):
        body = tk.Frame(parent, bg=COLORS["surface"])
        body.pack(fill="both", expand=True, padx=42, pady=38)

        tk.Label(
            body,
            text="Welcome back",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=("Segoe UI", 24, "bold"),
        ).pack(anchor="w")
        tk.Label(
            body,
            text="Sign in as admin to continue. Student access has its own entrance below.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            wraplength=470,
            justify="left",
        ).pack(anchor="w", pady=(6, 24))

        form = tk.Frame(body, bg=COLORS["surface"])
        form.pack(fill="x")

        tk.Label(
            form,
            text="Username",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 6))
        self.user_entry = entry(form)
        self.user_entry.pack(fill="x", ipady=9, pady=(0, 16))
        self.user_entry.focus()

        tk.Label(
            form,
            text="Password",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(0, 6))
        self.pass_entry = entry(form, show="*")
        self.pass_entry.pack(fill="x", ipady=9, pady=(0, 8))
        self.pass_entry.bind("<Return>", lambda e: self.login())

        tk.Label(
            form,
            text="Use your registered admin credentials.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(0, 20))

        button(form, "🔐 Login as Admin", self.login, "primary").pack(fill="x")
        button(form, "📝 Register Admin", self.open_register, "success").pack(fill="x", pady=(10, 0))
        button(form, "👨‍🎓 Student Login", self.open_student_login, "info").pack(fill="x", pady=(10, 0))

    def login(self):
        u = self.user_entry.get().strip()
        p = self.pass_entry.get().strip()

        if not u or not p:
            messagebox.showerror("Error", "Enter username and password")
            return

        if validate_login(u, p):
            self.master.deiconify()
            self.destroy()
            try:
                self.on_success(role="admin", username=u)
            except TypeError:
                self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
            self.pass_entry.delete(0, tk.END)
            self.user_entry.focus()

    def on_close(self):
        self.master.destroy()

    def _auth_dialog(self, title, subtitle, height=420):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry(f"560x{height}")
        win.minsize(560, height)
        win.resizable(False, False)
        win.configure(bg=COLORS["app_bg"])
        apply_app_theme(win)
        self._center(560, height, win)

        shell = tk.Frame(win, bg=COLORS["app_bg"])
        shell.pack(fill="both", expand=True, padx=18, pady=18)
        card = tk.Frame(shell, bg=COLORS["surface"], highlightbackground=COLORS["border"], highlightthickness=1)
        card.pack(fill="both", expand=True)

        body = tk.Frame(card, bg=COLORS["surface"])
        body.pack(fill="both", expand=True, padx=28, pady=26)
        tk.Label(body, text=title, bg=COLORS["surface"], fg=COLORS["text"], font=("Segoe UI", 20, "bold")).pack(anchor="w")
        tk.Label(
            body,
            text=subtitle,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            wraplength=470,
            justify="left",
        ).pack(anchor="w", pady=(6, 22))
        return win, body

    def open_student_login(self):
        sl, body = self._auth_dialog(
            "Student Login",
            "Students can browse books and view profile information from here.",
            height=380,
        )

        tk.Label(body, text="Student Email", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        username_entry = entry(body)
        username_entry.pack(fill="x", ipady=9, pady=(0, 14))

        tk.Label(body, text="Password", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        password_entry = entry(body, show="*")
        password_entry.pack(fill="x", ipady=9, pady=(0, 18))

        def do_student_login():
            u = username_entry.get().strip()
            p = password_entry.get().strip()
            if not u or not p:
                messagebox.showerror("Error", "Enter username and password", parent=sl)
                return

            from models.students import validate_student_login, get_student_by_id
            ok, student_id = validate_student_login(u, p)
            if not ok:
                messagebox.showerror("Login Failed", "Invalid username or password", parent=sl)
                return

            info = get_student_by_id(student_id)
            if not info:
                messagebox.showerror("Error", "Student record not found", parent=sl)
                return

            self.master.deiconify()
            sl.destroy()
            self.destroy()
            try:
                self.on_success(role="student", student_id=student_id, username=u)
            except TypeError:
                self.on_success()

        password_entry.bind("<Return>", lambda e: do_student_login())
        button(body, "Login", do_student_login, "success").pack(fill="x")

    def open_register(self):
        reg, body = self._auth_dialog(
            "Register Admin",
            "Create a new admin account. Password rules and validation remain the same.",
            height=470,
        )

        tk.Label(body, text="Username", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        username_entry = entry(body)
        username_entry.pack(fill="x", ipady=9, pady=(0, 14))

        tk.Label(body, text="Password", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        password_entry = entry(body, show="*")
        password_entry.pack(fill="x", ipady=9, pady=(0, 14))

        tk.Label(body, text="Confirm Password", bg=COLORS["surface"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
        confirm_entry = entry(body, show="*")
        confirm_entry.pack(fill="x", ipady=9, pady=(0, 10))

        tk.Label(
            body,
            text="Minimum password length: 8 characters.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 9),
        ).pack(anchor="w", pady=(0, 18))

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
            if len(p) < 8:
                messagebox.showerror("Error", "Password must be at least 8 characters", parent=reg)
                return

            ok, err = register_admin(u, p)
            if not ok:
                messagebox.showerror("Register Failed", err or "Unable to register", parent=reg)
                return

            messagebox.showinfo("Success", "Registration successful. You can now login.", parent=reg)
            reg.destroy()

        confirm_entry.bind("<Return>", lambda e: do_register())
        button(body, "Create Account", do_register, "primary").pack(fill="x")
