import tkinter as tk
import webbrowser

from gui.ui_theme import COLORS, page_header, card, button, metric_chip, apply_app_theme


class WebsiteFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS["app_bg"])
        apply_app_theme(self)

        page_header(
            self,
            "🌐 Our Website",
            "A simple launch page for the official HSTU Library website, dressed up a little so it earns its pixels.",
            "External link",
        )

        wrap, body = card(
            self,
            "Visit the Official Library Website",
            "Open the site in your default browser for more information, announcements, and resources.",
        )
        wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        link_url = "https://hstu.ac.bd/library"

        chips = tk.Frame(body, bg=COLORS["surface"])
        chips.pack(fill="x", pady=(0, 16))
        metric_chip(chips, "Destination", "HSTU Library").pack(side="left", padx=(0, 10))
        metric_chip(chips, "Type", "Official website").pack(side="left")

        hero = tk.Frame(
            body,
            bg=COLORS["surface_alt"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            padx=18,
            pady=18,
        )
        hero.pack(fill="x")

        tk.Label(
            hero,
            text="Need more library information?",
            bg=COLORS["surface_alt"],
            fg=COLORS["text"],
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            hero,
            text="Click the official address below or use the button to open the website in your browser.",
            bg=COLORS["surface_alt"],
            fg=COLORS["muted"],
            font=("Segoe UI", 10),
            wraplength=760,
            justify="left",
        ).pack(anchor="w", pady=(6, 16))

        link = tk.Label(
            hero,
            text=link_url,
            bg=COLORS["surface_alt"],
            fg=COLORS["primary"],
            cursor="hand2",
            font=("Segoe UI", 12, "underline"),
        )
        link.pack(anchor="w")

        def open_link(event=None):
            try:
                webbrowser.open(link_url)
            except Exception:
                pass

        link.bind("<Button-1>", open_link)
        button(body, "Open in browser", open_link, "primary").pack(anchor="w", pady=(18, 0))
