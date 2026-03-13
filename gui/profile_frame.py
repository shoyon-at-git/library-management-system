import tkinter as tk

from models.students import get_student_by_id
from gui.ui_theme import COLORS, page_header, metric_chip, apply_app_theme


class ProfileFrame(tk.Frame):
    def __init__(self, master, student_id=None):
        super().__init__(master, bg=COLORS["app_bg"])
        apply_app_theme(self)
        self.student_id = student_id
        self.info_cards = []
        self.details_grid = None

        self._build_ui()
        self.bind("<Configure>", self._on_resize)

    def _build_ui(self):
        page_header(
            self,
            "👤 Student Profile",
            "Your library identity card, rebuilt as a cleaner dashboard while keeping the same data source.",
            "Student view",
        )

        container = tk.Frame(self, bg=COLORS["app_bg"])
        container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.profile_card = tk.Frame(
            container,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0,
        )
        self.profile_card.pack(fill="both", expand=True)

        if self.student_id is None:
            self._build_empty_state("No student selected.")
            return

        info = get_student_by_id(self.student_id)
        if not info:
            self._build_empty_state("Student record not found.")
            return

        self._build_profile_card(info)

    def _build_empty_state(self, text):
        empty = tk.Frame(self.profile_card, bg=COLORS["surface"])
        empty.pack(expand=True)

        circle = tk.Canvas(empty, width=82, height=82, bg=COLORS["surface"], highlightthickness=0)
        circle.pack(pady=(60, 12))
        circle.create_oval(6, 6, 76, 76, fill=COLORS["primary_soft"], outline="")
        circle.create_text(41, 41, text="!", fill=COLORS["primary_dark"], font=("Segoe UI", 24, "bold"))

        tk.Label(empty, text=text, bg=COLORS["surface"], fg=COLORS["text"], font=("Segoe UI", 14, "bold")).pack()
        tk.Label(
            empty,
            text="Please log in again or check whether the student record exists in the database.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            wraplength=520,
            justify="center",
        ).pack(pady=(8, 50))

    def _build_profile_card(self, info):
        student_id, name, dept, email, session, birth_date = info
        initials = self._make_initials(name)

        hero = tk.Frame(self.profile_card, bg=COLORS["primary_dark"], height=170)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        hero_inner = tk.Frame(hero, bg=COLORS["primary_dark"])
        hero_inner.pack(fill="both", expand=True, padx=28, pady=22)

        left = tk.Frame(hero_inner, bg=COLORS["primary_dark"])
        left.pack(side="left", fill="y")

        avatar = tk.Canvas(left, width=96, height=96, bg=COLORS["primary_dark"], highlightthickness=0)
        avatar.pack(side="left", padx=(0, 18))
        avatar.create_oval(6, 6, 90, 90, fill="#f0f6ff", outline="")
        avatar.create_text(48, 48, text=initials, fill=COLORS["primary_dark"], font=("Segoe UI", 24, "bold"))

        identity = tk.Frame(left, bg=COLORS["primary_dark"])
        identity.pack(side="left", fill="y")
        tk.Label(identity, text=name, bg=COLORS["primary_dark"], fg="white", font=("Segoe UI", 23, "bold")).pack(anchor="w")
        tk.Label(identity, text=f"Department of {dept}", bg=COLORS["primary_dark"], fg=COLORS["hero_text"], font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 0))
        tk.Label(identity, text="Library Member", bg=COLORS["primary_dark"], fg="#9cc4e4", font=("Segoe UI", 10, "italic")).pack(anchor="w", pady=(8, 0))

        right = tk.Frame(hero_inner, bg=COLORS["primary_dark"])
        right.pack(side="right", anchor="n")
        self._hero_chip(right, "Student ID", str(student_id)).pack(anchor="e", pady=(0, 10))
        self._hero_chip(right, "Session", str(session)).pack(anchor="e")

        body = tk.Frame(self.profile_card, bg=COLORS["surface"])
        body.pack(fill="both", expand=True, padx=24, pady=24)

        top_metrics = tk.Frame(body, bg=COLORS["surface"])
        top_metrics.pack(fill="x", pady=(0, 18))
        metric_chip(top_metrics, "Email", email).pack(side="left", fill="x", expand=True, padx=(0, 10))
        metric_chip(top_metrics, "Birth Date", str(birth_date)).pack(side="left", fill="x", expand=True)

        intro = tk.Frame(body, bg=COLORS["surface"])
        intro.pack(fill="x", pady=(0, 14))
        tk.Label(intro, text="Personal Information", bg=COLORS["surface"], fg=COLORS["text"], font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(
            intro,
            text="Everything here comes from the student record already stored in the system.",
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(4, 0))

        self.details_grid = tk.Frame(body, bg=COLORS["surface"])
        self.details_grid.pack(fill="both", expand=True)

        items = [
            ("Student ID", str(student_id), "🆔"),
            ("Full Name", name, "👤"),
            ("Department", dept, "🏫"),
            ("Email", email, "✉️"),
            ("Session", str(session), "📘"),
            ("Birth Date", str(birth_date), "🎂"),
        ]

        self.info_cards = [self._detail_card(self.details_grid, label, value, icon) for label, value, icon in items]
        self.after(50, self._arrange_cards)

    def _hero_chip(self, parent, label, value):
        chip = tk.Frame(parent, bg="#174a75", padx=14, pady=10)
        tk.Label(chip, text=label, bg="#174a75", fg=COLORS["hero_text"], font=("Segoe UI", 8, "bold")).pack(anchor="e")
        tk.Label(chip, text=value, bg="#174a75", fg="white", font=("Segoe UI", 13, "bold")).pack(anchor="e")
        return chip

    def _detail_card(self, parent, label, value, icon):
        card = tk.Frame(parent, bg=COLORS["surface_alt"], highlightbackground=COLORS["border"], highlightthickness=1, padx=16, pady=14)
        top = tk.Frame(card, bg=COLORS["surface_alt"])
        top.pack(fill="x")
        tk.Label(top, text=icon, bg=COLORS["surface_alt"], fg=COLORS["primary"], font=("Segoe UI", 14)).pack(side="left")
        tk.Label(top, text=label, bg=COLORS["surface_alt"], fg=COLORS["muted"], font=("Segoe UI", 10, "bold")).pack(side="left", padx=(8, 0))
        tk.Label(card, text=value, bg=COLORS["surface_alt"], fg=COLORS["text"], font=("Segoe UI", 13, "bold"), wraplength=420, justify="left").pack(anchor="w", pady=(10, 0))
        return card

    def _make_initials(self, name):
        parts = [p for p in str(name).split() if p.strip()]
        if not parts:
            return "?"
        if len(parts) == 1:
            return parts[0][:2].upper()
        return (parts[0][0] + parts[-1][0]).upper()

    def _on_resize(self, _event=None):
        self._arrange_cards()

    def _arrange_cards(self):
        if not self.details_grid or not self.info_cards:
            return

        width = self.winfo_width() or self.master.winfo_width()
        cols = 1 if width < 980 else 2

        for child in self.info_cards:
            child.grid_forget()

        for c in range(cols):
            self.details_grid.grid_columnconfigure(c, weight=1, uniform="profile")
        for c in range(cols, 2):
            self.details_grid.grid_columnconfigure(c, weight=0, uniform="")

        for index, card in enumerate(self.info_cards):
            row = index // cols
            col = index % cols
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
