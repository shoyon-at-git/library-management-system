import tkinter as tk
from tkinter import ttk
from db import init_db
from PIL import Image, ImageTk

from gui.books_frame import BooksFrame
from gui.students_frame import StudentsFrame
from gui.issue_frame import IssueFrame
from gui.login_window import LoginWindow


def build_main_ui(root):
    # ---------- Header ----------
    header = tk.Frame(root, bg="#0b3c5d", height=70)
    header.pack(fill="x")

    tk.Label(header, text="HSTU Library",
             bg="#0b3c5d", fg="white",
             font=("Segoe UI", 20, "bold")).pack(pady=(5, 0))

    tk.Label(header,
             text="Hajee Mohammad Danesh Science and Technology University, Dinajpur-5200",
             bg="#0b3c5d", fg="white",
             font=("Segoe UI", 10)).pack()

    # ---------- Main body (with background) ----------
    bg_frame = tk.Frame(root)
    bg_frame.pack(fill="both", expand=True)

    # Load the image
    img = Image.open("images/library.jpg")
    img = img.resize((1200, 673), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(img)

    # Place background
    bg_label = tk.Label(bg_frame, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Keep reference so image doesn't disappear
    bg_label.image = bg_image

    # ---------- Overlay body on top of background ----------
    body = tk.Frame(bg_frame, bg="#ffffff")
    body.place(relx=0.5, rely=0.5, anchor="center", width=1100, height=550)

    # ---------- Sidebar ----------
    sidebar = tk.Frame(body, bg="#e9eef3", width=160)
    sidebar.pack(side="left", fill="y")

    # ---------- Content area ----------
    content = tk.Frame(body, bg="white")
    content.pack(side="right", fill="both", expand=True)

    # ---------- Pages ----------
    pages = {}

    def show(page):
        for p in pages.values():
            p.pack_forget()
        pages[page].pack(fill="both", expand=True)

    pages["books"] = BooksFrame(content)
    pages["students"] = StudentsFrame(content)
    pages["issue"] = IssueFrame(content)

    # ---------- Sidebar buttons ----------
    def nav_button(text, page):
        return tk.Button(
            sidebar,
            text=text,
            anchor="w",
            relief="flat",
            padx=15,
            font=("Segoe UI", 10),
            command=lambda: show(page)
        )

    tk.Label(sidebar, text="Navigation", bg="#e9eef3",
             font=("Segoe UI", 10, "bold")).pack(pady=(10, 5))

    nav_button("📚  Books", "books").pack(fill="x", pady=2)
    nav_button("👨‍🎓  Students", "students").pack(fill="x", pady=2)
    nav_button("🔁  Issue / Return", "issue").pack(fill="x", pady=2)

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
    root.withdraw()
    root.title("HSTU Library Management System")
    root.geometry("1200x700")  # match image size for clean look

    def after_login():
        root.deiconify()
        build_main_ui(root)

    LoginWindow(root, after_login)

    root.mainloop()


if __name__ == "__main__":
    main()
