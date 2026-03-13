import os
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk

from gui.ui_theme import COLORS, page_header, card, text_widget, apply_app_theme


class AboutFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=COLORS["app_bg"])
        apply_app_theme(self)
        self.photos = []

        page_header(
            self,
            "ℹ️ About HSTU Library",
            "A cleaner information page with image cards and a readable article layout.",
            "University info",
        )

        media_wrap, media_body = card(
            self,
            "Library Glimpses",
            "A few visuals from the library so the page feels alive instead of looking like a wall of text with trust issues.",
        )
        media_wrap.pack(fill="x", padx=20, pady=(0, 14))

        gallery = tk.Frame(media_body, bg=COLORS["surface"])
        gallery.pack(fill="x")

        bases = ["library1", "library-1", "library_1", "library 1"]
        img_names = [bases, [b.replace("1", "2") for b in bases], [b.replace("1", "3") for b in bases]]
        exts = [".jpg", ".jpeg", ".png"]

        def find_image_for_variants(variants):
            images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
            for variant in variants:
                for ext in exts:
                    path = os.path.join(images_dir, variant + ext)
                    if os.path.exists(path):
                        return path
            return None

        for variants in img_names:
            path = find_image_for_variants(variants)
            holder = tk.Frame(
                gallery,
                bg=COLORS["surface_alt"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                padx=8,
                pady=8,
            )
            holder.pack(side="left", fill="both", expand=True, padx=6, pady=4)

            if path:
                try:
                    img = Image.open(path)
                    img.thumbnail((280, 180))
                    ph = ImageTk.PhotoImage(img)
                    lbl = tk.Label(holder, image=ph, bg=COLORS["surface_alt"])
                    lbl.image = ph
                    lbl.pack(fill="both", expand=True)
                    self.photos.append(ph)
                except Exception:
                    tk.Label(
                        holder,
                        text=os.path.basename(path),
                        bg=COLORS["surface_alt"],
                        fg=COLORS["muted"],
                        width=30,
                        height=8,
                    ).pack(fill="both", expand=True)
            else:
                tk.Label(
                    holder,
                    text=f"{variants[0]}\nnot found",
                    bg=COLORS["surface_alt"],
                    fg=COLORS["muted"],
                    width=30,
                    height=8,
                ).pack(fill="both", expand=True)

        text_wrap, text_body = card(
            self,
            "Library Overview",
            "Detailed institutional information with better spacing and readable typography.",
            padx=14,
            pady=14,
        )
        text_wrap.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        text_frame = tk.Frame(text_body, bg=COLORS["surface"])
        text_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", style="App.Vertical.TScrollbar")
        scrollbar.pack(side="right", fill="y")

        text = text_widget(text_frame, yscrollcommand=scrollbar.set)
        text.pack(fill="both", expand=True, side="left")
        scrollbar.config(command=text.yview)

        long_text = (
            "Hajee Mohammad Danesh Science and Technology University is the only Science and Technology University for the northern region of the country. "
            "The library is called the heart of an institution. The university creates knowledge through research, and the library preserves research output and academic resources. "
            "So the library plays an enormous role in research, lesson preparation, and learning.\n\n"
            "Activities and Facilities:\n\n"
            "HSTU Library is a well-furnished multistoried building. It operates through several sections including Acquisition, Circulation, Processing, and Reference. "
            "The Administrative section manages administrative activities. Acquisition works to collect required documents for users. Recently, it collected many books for different faculties. "
            "The Circulation section is on the ground floor. Researchers, students, and teachers may borrow required books as per the rules for home or outside reading. Only books with more than two copies are available for loan. "
            "The Processing section prepares catalogues and classification using AACR-2 code and D.D.C. scheme. The Reference section is on the first and second floors, where teachers, researchers, and students may read rare documents. "
            "It also provides photocopy service for a nominal fee and regularly sends lists of newly received documents to faculties. Thesis works, journals, and daily newspapers are preserved on the second floor. "
            "There is also a cyber center in the library that users may use for a nominal fee.\n\n"
            "Mission:\n\n"
            "The Library's mission is to provide comprehensive resources and services in support of the research, teaching, and learning needs of the University community.\n\n"
            "Vision:\n\n"
            "Build a world-class Knowledge Resource Centre and provide innovative services and collections to the research, teaching, and learning communities using the latest technology.\n\n"
            "Library Resources:\n\n"
            "1. Printed Books: 23,105\n"
            "2. Thesis: 800\n"
            "3. Audio-Visual Materials: 300\n"
            "4. Periodicals:\n"
            "   a) Printed Journals: 89 (National and International)\n"
            "   b) E-Journals: Access to more than 40 thousand e-journals through consortium and digital library programs.\n"
            "   c) E-books: Access to 7,053 e-books of different subjects through digital library support.\n\n"
            "Library Hour:\n\n"
            "The Library is open from 8:00 am to 7:00 pm and is closed on university holidays.\n\n"
            "Library User Policy:\n\n"
            "1. A teacher may borrow up to 5 books for 30 days, and a student or researcher may borrow up to 3 books for 20 days.\n"
            "2. Personal bags, coats, jackets, umbrellas, and similar items must be kept near the security desk.\n"
            "3. Group study, gossiping, eating, drinking, and smoking are prohibited inside the library.\n"
            "4. Users must handle all library property carefully and leave materials neat and tidy after use.\n"
            "5. Mobile phones cannot be used inside the library.\n"
            "6. No book shall be issued within the last half hour before daily closing.\n"
        )

        bold_font = tkfont.Font(font=text.cget("font"))
        bold_font.configure(weight="bold")
        text.tag_configure("heading", font=bold_font, foreground=COLORS["primary_dark"])

        for line in long_text.splitlines(True):
            start = text.index(tk.INSERT)
            text.insert(tk.INSERT, line)
            end = text.index(tk.INSERT)
            if line.strip().endswith(":"):
                text.tag_add("heading", start, end)

        text.config(state="disabled")
