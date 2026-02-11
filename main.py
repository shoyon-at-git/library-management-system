import tkinter as tk
from tkinter import ttk
from db import init_db
from PIL import Image, ImageTk

from gui.books_frame import BooksFrame
from gui.students_frame import StudentsFrame
from gui.issue_frame import IssueFrame
from gui.login_window import LoginWindow
from gui.about_frame import AboutFrame


def build_main_ui(root, on_logout):
    # ---------- Header ----------
    header = tk.Frame(root, bg="#0b3c5d", height=70)
    header.pack(fill="x")

    tk.Label(header, text="HSTU Library Management System",
             bg="#0b3c5d", fg="white",
             font=("Segoe UI", 20, "bold")).pack(pady=(5, 0))

    tk.Label(header,
             text="Hajee Mohammad Danesh Science and Technology University, Dinajpur-5200",
             bg="#0b3c5d", fg="white",
             font=("Segoe UI", 10)).pack()

    # ---------- Main body ----------
    body = tk.Frame(root, bg="#f5f5f5")
    body.pack(fill="both", expand=True)

    # ---------- Sidebar ----------
    sidebar = tk.Frame(body, bg="#2c3e50", width=180)
    sidebar.pack(side="left", fill="y", padx=0)
    sidebar.pack_propagate(False)

    # ---------- Content area ----------
    content = tk.Frame(body, bg="white")
    content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ---------- Pages ----------
    pages = {}
    page_titles = {}

    def show(page):
        for p in pages.values():
            p.pack_forget()
        pages[page].pack(fill="both", expand=True)

    pages["books"] = BooksFrame(content)
    pages["students"] = StudentsFrame(content)
    pages["issue"] = IssueFrame(content)
    pages["about"] = AboutFrame(content)

    page_titles["books"] = "Books Management"
    page_titles["students"] = "Students Management"
    page_titles["issue"] = "Issue / Return Books"

    # ---------- Sidebar buttons ----------
    tk.Label(sidebar, text="MENU", bg="#2c3e50",
             fg="white", font=("Segoe UI", 12, "bold")).pack(pady=(20, 20), fill="x")

    def nav_button(text, page):
        btn = tk.Button(
            sidebar,
            text=text,
            anchor="w",
            bg="#34495e",
            fg="white",
            activebackground="#0b3c5d",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=12,
            font=("Segoe UI", 11),
            command=lambda: show(page)
        )
        return btn

    nav_button("📚  Books", "books").pack(fill="x", pady=5, padx=10)
    nav_button("👨‍🎓  Students", "students").pack(fill="x", pady=5, padx=10)
    nav_button("🔁  Issue / Return", "issue").pack(fill="x", pady=5, padx=10)
    nav_button("ℹ️  About", "about").pack(fill="x", pady=5, padx=10)

    # Add logout button at bottom
    tk.Frame(sidebar, bg="#2c3e50", height=1).pack(fill="x", expand=True)
    tk.Button(
        sidebar,
        text="🚪  Logout",
        anchor="w",
        bg="#c0392b",
        fg="white",
        activebackground="#a93226",
        relief="flat",
        padx=15,
        pady=12,
        font=("Segoe UI", 11),
        command=on_logout
    ).pack(fill="x", pady=5, padx=10)

    show("books")

    # ---------- Status bar ----------
    from datetime import date
    status = tk.Label(
        root,
        text=f"Logged in | HSTU Library System     Date: {date.today()}",
        anchor="w",
        bg="#f0f0f0",
        font=("Segoe UI", 9)
    )
    status.pack(fill="x", side="bottom")


def main():
    init_db()

    root = tk.Tk()
    root.title("HSTU Library Management System")
    root.geometry("1200x700")
    root.minsize(1000, 600)
    root.withdraw()

    def show_logout():
        # Clear all widgets from root
        for widget in root.winfo_children():
            widget.destroy()
        
        root.withdraw()
        
        # Show login window again
        def after_login():
            build_main_ui(root, show_logout)
        
        LoginWindow(root, after_login)

    # Create initial login window
    def after_login():
        build_main_ui(root, show_logout)
    
    LoginWindow(root, after_login)

    root.mainloop()


if __name__ == "__main__":
    main()
