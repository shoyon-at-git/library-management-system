import tkinter as tk
from tkinter import messagebox
from datetime import date

from db import DatabaseConfigurationError, init_db
from gui.books_frame import BooksFrame
from gui.students_frame import StudentsFrame
from gui.issue_frame import IssueFrame
from gui.login_window import LoginWindow
from gui.about_frame import AboutFrame
from gui.website_frame import WebsiteFrame
from gui.profile_frame import ProfileFrame
from gui.ui_theme import COLORS, apply_app_theme


def build_main_ui(root, on_logout, role=None, student_id=None):
    apply_app_theme(root)
    root.configure(bg=COLORS["app_bg"])

    # ---------- Header ----------
    header = tk.Frame(root, bg=COLORS["primary_dark"], height=88)
    header.pack(fill="x")
    header.pack_propagate(False)

    header_inner = tk.Frame(header, bg=COLORS["primary_dark"])
    header_inner.pack(fill="both", expand=True, padx=22, pady=14)

    left = tk.Frame(header_inner, bg=COLORS["primary_dark"])
    left.pack(side="left", fill="both", expand=True)

    tk.Label(
        left,
        text="HSTU Library Management System",
        bg=COLORS["primary_dark"],
        fg="white",
        font=("Segoe UI", 22, "bold"),
    ).pack(anchor="w")
    tk.Label(
        left,
        text="Hajee Mohammad Danesh Science and Technology University · Dinajpur-5200",
        bg=COLORS["primary_dark"],
        fg=COLORS["hero_text"],
        font=("Segoe UI", 10),
    ).pack(anchor="w", pady=(3, 0))

    role_label = "Student Portal" if role == "student" else "Admin Console"
    badge = tk.Label(
        header_inner,
        text=role_label,
        bg="#1b5f96",
        fg="white",
        font=("Segoe UI", 10, "bold"),
        padx=14,
        pady=8,
    )
    badge.pack(side="right", anchor="n")

    # ---------- Main body ----------
    body = tk.Frame(root, bg=COLORS["app_bg"])
    body.pack(fill="both", expand=True)

    # ---------- Sidebar ----------
    sidebar = tk.Frame(body, bg=COLORS["sidebar"], width=235)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    top_brand = tk.Frame(sidebar, bg=COLORS["sidebar"])
    top_brand.pack(fill="x", padx=18, pady=(18, 14))

    tk.Label(
        top_brand,
        text="Navigation",
        bg=COLORS["sidebar"],
        fg="white",
        font=("Segoe UI", 15, "bold"),
    ).pack(anchor="w")
    tk.Label(
        top_brand,
        text="Move through the system without the UI looking like it lost a fight with 2012.",
        bg=COLORS["sidebar"],
        fg="#a9c0d4",
        font=("Segoe UI", 9),
        justify="left",
        wraplength=180,
    ).pack(anchor="w", pady=(6, 0))

    tk.Frame(sidebar, bg="#24415b", height=1).pack(fill="x", padx=18, pady=(0, 12))

    # ---------- Content area ----------
    content_shell = tk.Frame(body, bg=COLORS["app_bg"])
    content_shell.pack(side="right", fill="both", expand=True, padx=16, pady=16)

    content = tk.Frame(content_shell, bg=COLORS["app_bg"])
    content.pack(fill="both", expand=True)

    pages = {}

    def show(page):
        for key, p in pages.items():
            p.pack_forget()
        pages[page].pack(fill="both", expand=True)
        for key, btn in nav_buttons.items():
            if key == page:
                btn.configure(bg=COLORS["primary"], fg="white")
            else:
                btn.configure(bg=COLORS["sidebar_soft"], fg="white")

    pages["books"] = BooksFrame(content, role=role)

    if role == "student":
        pages["profile"] = ProfileFrame(content, student_id=student_id)
        pages["about"] = AboutFrame(content)
        pages["website"] = WebsiteFrame(content)
    else:
        pages["students"] = StudentsFrame(content)
        pages["issue"] = IssueFrame(content)
        pages["about"] = AboutFrame(content)
        pages["website"] = WebsiteFrame(content)

    nav_buttons = {}

    def nav_button(text, page):
        btn = tk.Button(
            sidebar,
            text=text,
            anchor="w",
            bg=COLORS["sidebar_soft"],
            fg="white",
            activebackground=COLORS["primary"],
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=16,
            pady=12,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=lambda: show(page),
        )

        def on_enter(_):
            if btn.cget("bg") != COLORS["primary"]:
                btn.configure(bg="#1a4a73")

        def on_leave(_):
            if btn.cget("bg") != COLORS["primary"]:
                btn.configure(bg=COLORS["sidebar_soft"])

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        nav_buttons[page] = btn
        return btn

    nav_button("📚  Books", "books").pack(fill="x", pady=5, padx=14)
    if role == "student":
        nav_button("👤  Profile", "profile").pack(fill="x", pady=5, padx=14)
        nav_button("ℹ️  About", "about").pack(fill="x", pady=5, padx=14)
        nav_button("🌐  Website", "website").pack(fill="x", pady=5, padx=14)
    else:
        nav_button("👨‍🎓  Students", "students").pack(fill="x", pady=5, padx=14)
        nav_button("🔁  Issue / Return", "issue").pack(fill="x", pady=5, padx=14)
        nav_button("ℹ️  About", "about").pack(fill="x", pady=5, padx=14)
        nav_button("🌐  Website", "website").pack(fill="x", pady=5, padx=14)

    tk.Frame(sidebar, bg=COLORS["sidebar"], height=1).pack(fill="x", expand=True)

    logout_btn = tk.Button(
        sidebar,
        text="🚪  Logout",
        anchor="w",
        bg=COLORS["danger"],
        fg="white",
        activebackground=COLORS["danger_dark"],
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=16,
        pady=12,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2",
        command=on_logout,
    )
    logout_btn.pack(fill="x", pady=14, padx=14)

    show("books")

    # ---------- Status bar ----------
    status = tk.Frame(root, bg="#e2ebf5", height=34)
    status.pack(fill="x", side="bottom")
    status.pack_propagate(False)

    status_text = f"Logged in as {role_label}  ·  Date: {date.today()}"
    tk.Label(
        status,
        text=status_text,
        anchor="w",
        bg="#e2ebf5",
        fg=COLORS["text"],
        font=("Segoe UI", 9),
    ).pack(fill="x", padx=16, pady=7)



def main():
    root = tk.Tk()
    root.title("HSTU Library Management System")
    root.geometry("1280x760")
    root.minsize(1080, 680)
    root.withdraw()

    try:
        init_db()
    except DatabaseConfigurationError as exc:
        messagebox.showerror("Database Configuration Error", str(exc), parent=root)
        root.destroy()
        return
    except Exception as exc:
        messagebox.showerror("Startup Error", f"Application failed to start: {exc}", parent=root)
        root.destroy()
        return

    def show_logout():
        for widget in root.winfo_children():
            widget.destroy()
        root.withdraw()

        def after_login(role=None, student_id=None, username=None):
            build_main_ui(root, show_logout, role=role, student_id=student_id)

        LoginWindow(root, after_login)

    def after_login(role=None, student_id=None, username=None):
        build_main_ui(root, show_logout, role=role, student_id=student_id)

    LoginWindow(root, after_login)
    root.mainloop()


if __name__ == "__main__":
    main()
