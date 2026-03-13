import tkinter as tk
from tkinter import ttk

COLORS = {
    "app_bg": "#eef3f8",
    "surface": "#ffffff",
    "surface_alt": "#f7fbff",
    "primary": "#0f4c81",
    "primary_dark": "#0a3558",
    "primary_soft": "#dceaf8",
    "sidebar": "#0b1f33",
    "sidebar_soft": "#13314d",
    "text": "#102a43",
    "muted": "#6b7c93",
    "border": "#d7e3f0",
    "success": "#1f8f63",
    "success_dark": "#18714f",
    "danger": "#d1495b",
    "danger_dark": "#b83c4d",
    "warning": "#f29f05",
    "warning_dark": "#d78a00",
    "info": "#3e7cb1",
    "info_dark": "#315f88",
    "neutral": "#7b8fa1",
    "neutral_dark": "#627384",
    "row_alt": "#f8fbff",
    "hero_text": "#dbeafe",
}

FONTS = {
    "hero": ("Segoe UI", 24, "bold"),
    "page_title": ("Segoe UI", 20, "bold"),
    "section_title": ("Segoe UI", 13, "bold"),
    "body": ("Segoe UI", 10),
    "body_bold": ("Segoe UI", 10, "bold"),
    "small": ("Segoe UI", 9),
    "small_bold": ("Segoe UI", 9, "bold"),
    "button": ("Segoe UI", 10, "bold"),
}


def apply_app_theme(widget):
    """Apply shared ttk styling once per toplevel/root."""
    style = ttk.Style(widget)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(
        "App.Treeview",
        background=COLORS["surface"],
        fieldbackground=COLORS["surface"],
        foreground=COLORS["text"],
        bordercolor=COLORS["border"],
        borderwidth=0,
        relief="flat",
        rowheight=34,
        font=("Segoe UI", 10),
    )
    style.map(
        "App.Treeview",
        background=[("selected", COLORS["primary_soft"])],
        foreground=[("selected", COLORS["text"])],
    )
    style.configure(
        "App.Treeview.Heading",
        background=COLORS["surface_alt"],
        foreground=COLORS["text"],
        relief="flat",
        borderwidth=0,
        font=("Segoe UI", 10, "bold"),
        padding=(10, 10),
    )
    style.map(
        "App.Treeview.Heading",
        background=[("active", COLORS["surface_alt"])],
        foreground=[("active", COLORS["text"])],
    )

    style.configure(
        "App.Vertical.TScrollbar",
        troughcolor=COLORS["app_bg"],
        background=COLORS["neutral"],
        borderwidth=0,
        arrowcolor=COLORS["surface"],
        relief="flat",
    )


def page_frame(master):
    return tk.Frame(master, bg=COLORS["app_bg"])


def page_header(parent, title, subtitle=None, action_text=None):
    wrap = tk.Frame(parent, bg=COLORS["app_bg"])
    wrap.pack(fill="x", padx=20, pady=(18, 14))

    tk.Label(
        wrap,
        text=title,
        bg=COLORS["app_bg"],
        fg=COLORS["text"],
        font=FONTS["page_title"],
    ).pack(anchor="w")

    if subtitle:
        tk.Label(
            wrap,
            text=subtitle,
            bg=COLORS["app_bg"],
            fg=COLORS["muted"],
            font=FONTS["body"],
            wraplength=950,
            justify="left",
        ).pack(anchor="w", pady=(4, 0))

    if action_text:
        pill = tk.Label(
            wrap,
            text=action_text,
            bg=COLORS["primary_soft"],
            fg=COLORS["primary_dark"],
            font=FONTS["small_bold"],
            padx=10,
            pady=5,
        )
        pill.pack(anchor="e", pady=(8, 0))
    return wrap


def card(parent, title=None, subtitle=None, padx=18, pady=16):
    outer = tk.Frame(
        parent,
        bg=COLORS["surface"],
        highlightbackground=COLORS["border"],
        highlightthickness=1,
        bd=0,
    )
    inner = tk.Frame(outer, bg=COLORS["surface"])
    inner.pack(fill="both", expand=True, padx=padx, pady=pady)

    if title:
        tk.Label(
            inner,
            text=title,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["section_title"],
        ).pack(anchor="w")
    if subtitle:
        tk.Label(
            inner,
            text=subtitle,
            bg=COLORS["surface"],
            fg=COLORS["muted"],
            font=FONTS["small"],
            wraplength=920,
            justify="left",
        ).pack(anchor="w", pady=(4, 12))
    elif title:
        tk.Frame(inner, bg=COLORS["surface"], height=10).pack()
    return outer, inner


def section_divider(parent, pady=(10, 10)):
    tk.Frame(parent, bg=COLORS["border"], height=1).pack(fill="x", pady=pady)


def form_label(parent, text):
    return tk.Label(parent, text=text, bg=COLORS["surface"], fg=COLORS["muted"], font=FONTS["small_bold"])


def entry(parent, textvariable=None, show=None, width=None, state="normal"):
    e = tk.Entry(
        parent,
        textvariable=textvariable,
        show=show,
        width=width,
        state=state,
        font=("Segoe UI", 10),
        bg=COLORS["surface_alt"],
        fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["primary"],
        bd=0,
    )
    return e


def button(parent, text, command, variant="primary", width=None):
    bg_map = {
        "primary": (COLORS["primary"], COLORS["primary_dark"]),
        "success": (COLORS["success"], COLORS["success_dark"]),
        "danger": (COLORS["danger"], COLORS["danger_dark"]),
        "warning": (COLORS["warning"], COLORS["warning_dark"]),
        "info": (COLORS["info"], COLORS["info_dark"]),
        "neutral": (COLORS["neutral"], COLORS["neutral_dark"]),
        "sidebar": (COLORS["sidebar_soft"], COLORS["primary"]),
    }
    bg, hover = bg_map.get(variant, bg_map["primary"])
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        bg=bg,
        fg="white",
        activebackground=hover,
        activeforeground="white",
        font=FONTS["button"],
        relief="flat",
        bd=0,
        cursor="hand2",
        padx=16,
        pady=10,
    )

    def on_enter(_):
        btn.configure(bg=hover)

    def on_leave(_):
        btn.configure(bg=bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def metric_chip(parent, label, value):
    chip = tk.Frame(parent, bg=COLORS["surface_alt"], padx=12, pady=10, highlightbackground=COLORS["border"], highlightthickness=1)
    tk.Label(chip, text=label, bg=COLORS["surface_alt"], fg=COLORS["muted"], font=FONTS["small_bold"]).pack(anchor="w")
    tk.Label(chip, text=value, bg=COLORS["surface_alt"], fg=COLORS["text"], font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(4, 0))
    return chip


def treeview(parent, columns, height=12):
    tv = ttk.Treeview(parent, columns=columns, show="headings", height=height, style="App.Treeview")
    return tv


def text_widget(parent, **kwargs):
    base = dict(
        wrap="word",
        bg=COLORS["surface_alt"],
        fg=COLORS["text"],
        relief="flat",
        bd=0,
        font=("Segoe UI", 10),
        insertbackground=COLORS["text"],
        highlightthickness=1,
        highlightbackground=COLORS["border"],
        highlightcolor=COLORS["primary"],
        padx=14,
        pady=12,
    )
    base.update(kwargs)
    return tk.Text(parent, **base)
